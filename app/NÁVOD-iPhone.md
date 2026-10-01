# Pirátský poklad – appka na iPhone (bez Macu)

Hra zabalená do nativního obalu (Capacitor + WKWebView). **Appka je minimalistická**:
v balíčku je jen hra a fonty (~1,3 MB). **Zvuky (421 klipů) se při prvním spuštění
stáhnou z hostingu** (GitHub Pages) do úložiště a pak fungují offline. Postup se ukládá
trvale (nativní Preferences + localStorage), takže se o nic nepřijde.

Protože nemáš Mac, **appka se kompiluje na GitHubu** (GitHub Actions, macOS runner) a
podepíše se až potom na Windows přes Sideloadly nebo AltStore. Veřejné repo = minuty
na build zdarma.

## Jak vznikne .ipa (na GitHubu)
1. Push do repa spustí workflow `.github/workflows/ios.yml` (jde spustit i ručně:
   GitHub → záložka **Actions** → *Build iOS (unsigned IPA)* → **Run workflow**).
2. Workflow na macOS runneru sestaví **nepodepsané `.ipa`** a nahraje ho jako
   **artifact** (dole u běhu workflow, `PiratskyPoklad-unsigned-ipa`).
3. Artifact (zip s `.ipa`) si stáhneš na Windows.

## Jak dostat .ipa do iPhonu (Windows, Apple ID zdarma)
Použij **Sideloadly** (sideloadly.io) nebo **AltStore**:
1. Nainstaluj Sideloadly, připoj iPhone kabelem, nainstaluj iTunes + iCloud (kvůli
   ovladačům), pokud to Sideloadly vyžaduje.
2. V Sideloadly přetáhni `.ipa`, zadej svoje **Apple ID** (zdarma), klikni **Start**.
   Sideloadly appku podepíše tvým účtem a nahraje do telefonu.
3. V iPhonu: **Nastavení → Obecné → Správa VPN a zařízení** → tvůj účet → **Důvěřovat**.
4. Při prvním spuštění appka stáhne hlasy (ukazatel průběhu), pak už jede offline.

Apple ID zdarma: podpis vydrží **7 dní**, pak appku znovu nahraj přes Sideloadly
(postup ve hře zůstane). S placeným Apple Developer Programem vydrží rok.

## Hosting zvuků (GitHub Pages)
- Zvuky se berou z `https://<tvůj-účet>.github.io/piratsky-poklad/zdroje/tts/audio/`.
- Pages se zapne v **Settings → Pages → Source: Deploy from a branch → main / (root)**.
- Soubor `.nojekyll` v kořeni zajistí, že se složky servírují tak, jak jsou.
- Když změníš účet/název repa, uprav `AUDIO_BASE` v `app/www/index.html`.

## Když se hra později změní
Přepiš `app/www/index.html` (nebo znovu vygeneruj z `zdroje/`), pushni – workflow
sám sestaví nové `.ipa`. Když přibudou nové zvuky, nahraj je do `zdroje/tts/audio/`
(Pages je bude hostovat) a v appce se dostáhnou (smaž `pp_audio_dl` v úložišti nebo
to dožene postupně při hraní).

## Co je uvnitř
- `app/www/` – minimalistická hra: `index.html` + `fonts/` (offline), zvuky se stahují.
- `app/capacitor.config.json`, `app/package.json` – Capacitor.
- `app/assets/` – podklady pro ikonu a splash.
- `.github/workflows/ios.yml` – build .ipa na GitHubu.

Pozn.: tohle je obal webové hry pro vlastní iPhone / rodinu. Do App Store by Apple
u čistého webview mohl chtít víc; pro sideload to řeší bez problému.
