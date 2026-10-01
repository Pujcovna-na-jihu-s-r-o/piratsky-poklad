#!/usr/bin/env python3
"""Generuje app/www/index.html (iPhone appka, Capacitor) ze zdrojového jádra hry.

Výstup = app/wrapper/head.html + zdroje/hra-piratsky-poklad.html (s náhradou
řádku s fonty za lokální fonts.css a AUDIO_BASE za absolutní URL) + app/wrapper/tail.html.

app/www/index.html se už RUČNĚ NEEDITUJE: jádro hry se mění ve zdroji
(zdroje/hra-piratsky-poklad.html), obal appky v app/wrapper/.

Použití:
  python zdroje/build_app.py           # vygeneruje app/www/index.html (UTF-8, LF)
  python zdroje/build_app.py --check   # nic nezapisuje; kód 1, když se soubor liší
                                       # od toho, co by se vygenerovalo (bez ohledu na CR)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "zdroje" / "hra-piratsky-poklad.html"
HEAD = ROOT / "app" / "wrapper" / "head.html"
TAIL = ROOT / "app" / "wrapper" / "tail.html"
OUT = ROOT / "app" / "www" / "index.html"

FONTS_OLD = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Pirata+One'
             '&family=Baloo+2:wght@600;700;800&family=Nunito:wght@600;700;800&display=swap">')
FONTS_NEW = '<link rel="stylesheet" href="fonts.css">'
AUDIO_OLD = 'const AUDIO_BASE="audio/";'
AUDIO_NEW = 'const AUDIO_BASE="https://www.kukackovi.cz/piratsky-poklad/audio/";'


def read(p: Path) -> str:
    # univerzální konce řádků: CRLF i CR se převedou na LF
    with open(p, encoding="utf-8", newline=None) as f:
        return f.read()


def replace_once(text: str, old: str, new: str, what: str) -> str:
    n = text.count(old)
    if n != 1:
        sys.exit(f"CHYBA: náhrada „{what}“ musí sednout právě jednou, nalezeno {n}x "
                 f"(hledáno v {SRC.name}): {old[:90]}")
    return text.replace(old, new)


def build() -> str:
    core = read(SRC)
    core = replace_once(core, FONTS_OLD, FONTS_NEW, "řádek s fonty")
    core = replace_once(core, AUDIO_OLD, AUDIO_NEW, "AUDIO_BASE")
    return read(HEAD) + core + read(TAIL)


def main() -> int:
    out = build()
    if "--check" in sys.argv[1:]:
        cur = read(OUT) if OUT.exists() else None
        if cur != out:
            print(f"NESOUHLASÍ: {OUT.relative_to(ROOT)} neodpovídá zdroji + obalu. "
                  f"Spusť: python zdroje/build_app.py")
            return 1
        print("OK: app/www/index.html odpovídá zdroji.")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print(f"Zapsáno {OUT.relative_to(ROOT)} ({len(out)} znaků)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
