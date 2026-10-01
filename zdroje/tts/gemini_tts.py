# -*- coding: utf-8 -*-
"""
Gemini TTS pro hru Pirátský poklad.

Klíč: proměnná prostředí GEMINI_API_KEY nebo soubor `.env` v této složce
(řádek GEMINI_API_KEY=...). Klíč se nikam neloguje ani nevypisuje.

Použití:
  python gemini_tts.py test                      – hlasová zkouška (Pepík, Mlha, dialog) do ./test/
  python gemini_tts.py say --voice Puck --role pepik --text "Ahoj!" --out ahoj.mp3
  python gemini_tts.py build manifest.json out/  – vygeneruje všechny klipy z manifestu
                                                    (manifest: [{"id":..., "role":..., "text":...}, ...])
Volby: --model gemini-2.5-flash-preview-tts | gemini-2.5-pro-preview-tts, --sleep 2, --wav (bez převodu na mp3)
"""
import argparse, base64, io, json, os, struct, subprocess, sys, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

class NoAudioError(Exception):
    pass

# Role = kdo mluví. Styl je anglicky (instrukce pro model), text je česky.
ROLES = {
    "pepik": dict(voice="Achird", style=(
        "MLUV ČESKY. Řekni následující text plynulou, spisovnou češtinou s přirozeným rodilým českým přízvukem a správnou výslovností (ř, ě, č, ž, š, ů). "
        "Nepřepínej do jiného jazyka, nečti to s cizím přízvukem. "
        "Jsi kamarádský průvodce pro sedmileté dítě ve hře o hledání pokladu. Mluv normálním, vlídným a veselým hlasem, srozumitelně a klidným tempem, ne přehnaně, ne pisklavě.")),
    "mlha": dict(voice="Charon", style=(
        "MLUV ČESKY. Řekni následující text plynulou, spisovnou češtinou s přirozeným rodilým českým přízvukem a správnou výslovností. Nepřepínej do jiného jazyka. "
        "Jsi kapitán Mlha, protivný, teatrální pirátský padouch v dětské hře. Mluv hlubším, důrazným, trochu chraplavým hlasem, komicky a hravě, nikdy ne doopravdy strašidelně. Klidné tempo.")),
    "ukol": dict(voice="Orus", style=(
        "MLUV ČESKY. Řekni následující text plynulou, spisovnou češtinou s přirozeným rodilým českým přízvukem a správnou výslovností (ř, ě, č, ž, š, ů, rybník ne řibník). "
        "Nepřepínej do jiného jazyka, nečti to s cizím přízvukem. "
        "Jsi hlas, který dětem ve hře zadává úkoly a čte jména mapových značek. Mluv jasně, srozumitelně, vlídně a klidným tempem, ne přehnaně.")),
    "vypravec": dict(voice="Charon", style=(
        "Speak in Czech with natural, native Czech pronunciation. You are a warm storyteller reading a pirate adventure to young children. "
        "Calm, clear, slightly mysterious, with gentle excitement.")),
}

def load_key():
    k = os.environ.get("GEMINI_API_KEY", "").strip()
    if not k:
        env = os.path.join(HERE, ".env")
        if os.path.exists(env):
            for line in io.open(env, encoding="utf-8-sig"):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    name, val = line.split("=", 1)
                    if name.strip() == "GEMINI_API_KEY":
                        k = val.strip().strip('"').strip("'")
                else:
                    k = line.strip('"').strip("'")   # v souboru je jen samotný klíč
    if not k:
        sys.exit("Chybí GEMINI_API_KEY (env nebo zdroje/tts/.env).")
    return k

def tts_request(key, model, text, voice=None, speakers=None, retries=4):
    """Vrátí (pcm_bytes, sample_rate). speakers = [(jmeno, voice), ...] pro vícehlasý dialog."""
    if speakers:
        speech = {"multiSpeakerVoiceConfig": {"speakerVoiceConfigs": [
            {"speaker": n, "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": v}}} for n, v in speakers]}}
    else:
        speech = {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}
    body = {"contents": [{"parts": [{"text": text}]}],
            "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": speech}}
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(API.format(model=model), data=data, method="POST",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": key})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                resp = json.loads(r.read().decode("utf-8"))
            part = resp["candidates"][0]["content"]["parts"][0]["inlineData"]
            mime = part.get("mimeType", "audio/L16;codec=pcm;rate=24000")
            rate = 24000
            for kv in mime.split(";"):
                if kv.strip().startswith("rate="):
                    rate = int(kv.strip()[5:])
            return base64.b64decode(part["data"]), rate
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:400]
            if e.code in (400, 429, 500, 503) and attempt < retries - 1:
                wait = 8 * (attempt + 1)
                print(f"  HTTP {e.code}, čekám {wait}s a zkusím znovu…", file=sys.stderr)
                time.sleep(wait); continue
            raise SystemExit(f"HTTP {e.code}: {msg}")
        except (KeyError, IndexError):
            raise NoAudioError("Odpověď neobsahuje audio: " + json.dumps(resp)[:200])

def write_wav(path, pcm, rate):
    with open(path, "wb") as f:
        f.write(b"RIFF" + struct.pack("<I", 36 + len(pcm)) + b"WAVE")
        f.write(b"fmt " + struct.pack("<IHHIIHH", 16, 1, 1, rate, rate * 2, 2, 16))
        f.write(b"data" + struct.pack("<I", len(pcm)) + pcm)

# Ořez ticha na začátku i konci (aby skládané věty na sebe plynule navazovaly), ponechá ~40 ms.
TRIM_AF = ("silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.04:detection=peak,"
           "areverse,"
           "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.04:detection=peak,"
           "areverse")
def to_mp3(wav, mp3):
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", TRIM_AF, "-ac", "1", "-b:a", "64k", mp3])
    if r.returncode == 0:
        os.remove(wav); return mp3
    return wav

def synth(key, model, text, role=None, voice=None, style=None, speakers=None, out="out.mp3", mp3=True, sleep=2.0):
    if role:
        style = style or ROLES[role]["style"]; voice = voice or ROLES[role]["voice"]
    prompt = (style + "\n\n" + text) if style else text
    try:
        pcm, rate = tts_request(key, model, prompt, voice=voice, speakers=speakers)
    except NoAudioError:
        pcm, rate = tts_request(key, model, prompt.rstrip(". ") + " .", voice=voice, speakers=speakers)
    base, ext = os.path.splitext(out)
    wav = base + ".wav"
    write_wav(wav, pcm, rate)
    result = to_mp3(wav, base + ".mp3") if mp3 and ext.lower() != ".wav" else wav
    secs = len(pcm) / 2 / rate
    print(f"  {os.path.basename(result)}  ({secs:.1f} s)")
    time.sleep(sleep)
    return result

TEST_PEPIK = ("Ahoj, plavčíku! Já jsem papoušek Pepík. Před dávnými časy schovali piráti na ostrově poklad "
              "a nakreslili mapu úplně stejnými značkami, jaké se dnes používají v orientačním běhu. "
              "Kdo chce poklad najít, musí umět mapu číst! Modrá je voda, žlutá louka a černá tečka je balvan.")
TEST_MLHA = ("Arr! Já jsem kapitán Mlha! Mapu jsem roztrhal na čtyřiadvacet kousků a poklad bude můj. "
             "Chceš kousek mapy, plavčíku? Tak mě poraz v souboji! Kdo přečte víc značek, než dohoří svíčka?")
TEST_DIALOG = ("Pepík: Kapitáne Mlho, vraťte nám mapu!\n"
               "Mlha: Cha chá! Nikdy! Nejdřív mě musíte porazit.\n"
               "Pepík: Neboj, plavčíku, ten mrzout čte mapu pomaleji než želva. Do souboje!")

def cmd_test(key, model, mp3, sleep):
    out = os.path.join(HERE, "test"); os.makedirs(out, exist_ok=True)
    print("Pepík (papoušek) – 4 hlasy:")
    for v in ("Puck", "Zephyr", "Leda", "Aoede"):
        synth(key, model, TEST_PEPIK, role="pepik", voice=v, out=os.path.join(out, f"pepik-{v}.mp3"), mp3=mp3, sleep=sleep)
    print("Kapitán Mlha – 3 hlasy:")
    for v in ("Algenib", "Charon", "Orus"):
        synth(key, model, TEST_MLHA, role="mlha", voice=v, out=os.path.join(out, f"mlha-{v}.mp3"), mp3=mp3, sleep=sleep)
    print("Dialog (Pepík = Puck, Mlha = Charon):")
    style = ("Speak in Czech with natural native pronunciation. Pepík is a cheerful pirate parrot talking to a child; "
             "Mlha is a grumpy, theatrical, comical pirate villain. Read this dialogue:")
    synth(key, model, style + "\n\n" + TEST_DIALOG, speakers=[("Pepík", "Puck"), ("Mlha", "Charon")],
          out=os.path.join(out, "dialog-Puck-Charon.mp3"), mp3=mp3, sleep=sleep)
    print("Hotovo ->", out)

def cmd_build(key, model, manifest, outdir, mp3, sleep):
    items = json.load(io.open(manifest, encoding="utf-8"))
    os.makedirs(outdir, exist_ok=True)
    done = 0; failed = []
    todo = [it for it in items if not os.path.exists(os.path.join(outdir, it["id"] + (".mp3" if mp3 else ".wav")))]
    for n, it in enumerate(todo, 1):
        target = os.path.join(outdir, it["id"] + (".mp3" if mp3 else ".wav"))
        print(f"[{n}/{len(todo)}] {it['id']}")
        try:
            synth(key, model, it["text"], role=it.get("role", "pepik"), voice=it.get("voice"), style=it.get("style"), out=target, mp3=mp3, sleep=sleep)
            done += 1
        except NoAudioError:
            print("  PRESKOCENO (bez audia):", it["id"], file=sys.stderr); failed.append(it["id"]); time.sleep(sleep)
    print("Hotovo, novych klipu:", done, "| preskoceno:", len(failed), (",".join(failed) if failed else ""))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["test", "say", "build"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--model", default="gemini-2.5-flash-preview-tts")
    ap.add_argument("--role", default="pepik"); ap.add_argument("--voice"); ap.add_argument("--style")
    ap.add_argument("--text"); ap.add_argument("--out", default="out.mp3")
    ap.add_argument("--wav", action="store_true", help="nechat WAV (nepřevádět přes ffmpeg na mp3)")
    ap.add_argument("--sleep", type=float, default=2.0, help="pauza mezi požadavky (s)")
    a = ap.parse_args()
    key = load_key(); mp3 = not a.wav
    if a.cmd == "test":
        cmd_test(key, a.model, mp3, a.sleep)
    elif a.cmd == "say":
        synth(key, a.model, a.text, role=a.role, voice=a.voice, style=a.style, out=a.out, mp3=mp3, sleep=0)
    else:
        if len(a.args) < 2: sys.exit("build manifest.json outdir")
        cmd_build(key, a.model, a.args[0], a.args[1], mp3, a.sleep)

if __name__ == "__main__":
    main()
