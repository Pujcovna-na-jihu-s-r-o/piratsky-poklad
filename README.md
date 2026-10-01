# Orientační běh – čtení mapy a značky (výukové materiály)

Sada výukových materiálů o čtení map a mapových značkách pro orientační běh,
ve dvou verzích: **pro děti (2. třída ZŠ)** a **pro dospělé** (norma ISOM/ISSprOM).

Poslední aktualizace: 2026-09-30 (hra v2.1: příběh, finále čtení mapy, 86 značek ISOM 2017-2 + popisy kontrol ISCD 2018).

## Struktura složek

```
orientacni beh/
├─ deti-2trida/        … výstupy z NotebookLM (dětská verze) + tiskové kartičky
├─ dospeli/            … výstupy z NotebookLM (dospělá verze)
├─ zdroje/             … zdroj hry, generátor značek, podklady ISOM/ISCD, tiskové kartičky
└─ README.md
```

## NotebookLM notebooky

Zdroje a artefakty (prezentace/kartičky/kvíz/podcast) jsou i online v NotebookLM:

- **Děti (2. třída):** základní/školní sada značek, 10 zdrojů
  https://notebooklm.google.com/notebook/82214b68-d9e7-42b0-ab8b-67a564f199bf
- **Dospělí:** kompletní norma ISOM 2017-2 + ISSprOM 2019-2 + ČSOS, 12 zdrojů
  https://notebooklm.google.com/notebook/13ad2daa-8d41-45cc-bf6b-d68aee11ff5c

Globální jazyk generování v NotebookLM byl nastaven na **češtinu** (`notebooklm language set cs`).

### deti-2trida/
- `PREZENTACE-orientacni-beh.pdf` – prezentace „Jak číst orientační mapu"
- `kARTICKY-orientacni-beh.md` – textové kartičky (NotebookLM)
- `KVIZ-orientacni-beh.md` – kvíz (NotebookLM)
- `PODCAST-orientacni-beh.mp3` – původní krátký podcast
- `podcast-dil1-barvy.mp3` – série: 1. díl Barvy na mapě
- `podcast-dil2-kudy-se-da-behat.mp3` – 2. díl Kudy se dá běžet
- `podcast-dil3-kopecky-voda.mp3` – 3. díl Kopečky, vrstevnice a voda
- `podcast-dil4-znacky-trati.mp3` – 4. díl Značky trati
- `karticky-obrazkove-tisk.pdf` – **obrázkové kartičky k vytisknutí** (12 značek, 2× A4)

### dospeli/
- `prezentace.pdf` – prezentace „Dekódování krajiny"
- `karticky.md` – kartičky se značkami a čísly symbolů ISOM
- `kviz.md` – kvíz (těžší)
- `podcast.mp3` – podrobný podcast

## Interaktivní hra „Pirátský poklad" (dětská)

Mluvící pirátská hra se scénářem **„Cesta za Zlatým kompasem"**: kapitán Mlha
roztrhal mapu na 24 kousků a schoval je na 24 ostrovech ve čtyřech mořích.
Dítě (plavčík) s papouškem Pepíkem pluje od ostrova k ostrovu, na každém se
naučí 3–6 nových značek, získá kousek mapy a člena posádky; poslední ostrov
každého moře je souboj s Mlhou na čas.

- **Úvodní příběh (4 stránky s obrázky a hlasem):** piráti nakreslili mapu
  pokladu stejnými značkami, jaké se používají v orientačním běhu; Mlha ji
  roztrhal; kdo chce poklad, musí umět značky číst a vymyslet cestu. Nový
  hráč začíná tlačítkem „Začít příběh“, příběh jde pustit znovu.
- **Finále „Cesta k pokladu“:** kousky mapy jsou výřezy skutečné mini mapy
  nakreslené značkami ISOM (les, louka, rybník, bažina, vrstevnice, pěší
  cesta, balvan, strom, trať start → 1 → 2 → cíl s ✖). Po složení dítě podle
  Pepíkových pokynů klepe trasu (start → balvan → kopec → strom → poklad);
  chybný klik (bažina, voda, hustník) hra vysvětlí. Až pak dostane Zlatý kompas.

- **Online (živá hra):** https://claude.ai/artifact/AShD2kGa4BBoFiS8nSxD7i
- **Zdroj:** `zdroje/hra-piratsky-poklad.html` (předchozí jednoduchá verze
  s 12 značkami: `zdroje/hra-piratsky-poklad-v1.html`)
- Úprava: edituj HTML a přepublikuj na stejnou adresu (v Claude Code:
  Artifact publish s `url` = výše, `file_path` = tento HTML).

### Značky – přesně podle mapového klíče
- **86 značek ISOM 2017-2** (ze 109; chybí jen varianty a technické značky, viz níže) (terénní tvary, skály a kameny, voda a bažiny,
  vegetace, komunikace, umělé objekty, značky tratě) s oficiálními čísly
  a českými názvy podle překladu ČSOS; barvy podle PMS (hnědá 471, modrá 299,
  žlutá 136, zelená 361, fialová) včetně rastrů 30/50/60 %.
- Každá značka má **tři podoby**: kartu, dílek mapy (pro režim „Mapa ostrova")
  a **piktogram z popisů kontrol (ISCD 2018)** – 71 značek ho má, u zbylých
  (značky tratě, barvy porostu, pole/sad…) hra řekne, že se v popisech
  kontrol nepoužívají a jsou jen v mapě.
- Opraveno oproti v1: **balvan je černá tečka (204)**, černý trojúhelník je
  **shluk balvanů (207)**; „kopec" jsou **vrstevnice (101)**; cesty rozlišeny
  na silnici (503), vozovou cestu (504), pěší cestu (505) a pěšinu (506).
- „Mez“ v lese (výškový schod) je značka **104 Zemní sráz** (český překlad
  ISOM u ní meze výslovně uvádí), ve hře pojmenovaná „Mez (zemní sráz)“;
  „hráz“ vlastní značku nemá, kreslí se jako zemní sráz (104) nebo val (105).
- Zatím nezařazeno (23): varianty už zařazených značek (102, 106, 108, 114,
  209, 211, 212, 215, 305, 307, 404, 409, 415, 507, 511, 514, 517) a technické
  značky či značky tratě bez smyslu pro děti (601, 602, 603, 702, 704, 708).
- Podklady (staženo 2026-09-30): `zdroje/ISOM-2017-2-cz-CSOS.pdf`
  (https://www.ceskyorientak.cz/wp-content/uploads/2025/04/csos-isom2017-2i22cz.pdf),
  `zdroje/mapovy-klic-ISOM2017-2-ISCD2018-tabulka.pdf`
  (https://zacitorientak.cz/assets/files/Mapovy_klic_ISOM2017-2.pdf).
- Přehled všech značek, jak je hra kreslí: `zdroje/galerie-znacek.png`.
- Říkankové pomůcky a věty „povzbuzení" po správné odpovědi u základních
  12 značek jsou z NotebookLM (`zdroje/znacky-podklady-z-notebooklm.md`),
  s opravou balvanu (tečka) a vrstevnic.
- Katalog generuje `zdroje/gen_symbols.py` (Python) – definice značek,
  ostrovů a otázek „na rozum" na jednom místě; skript je vloží do HTML.
  Nové značky přidávej tam (`add(...)`), spusť skript a přepublikuj.

### Co ve hře je
- **Mapa ostrovů** po „mořích" (Papouščí, Mlžné, Bouřlivé, Ledové; 6 ostrovů
  na moře, stránkuje se ◀ ▶), ostrovy se odemykají postupně, každý má 1–3
  hvězdy podle počtu chyb (motivace hrát znovu). Cesta mezi ostrovy je
  zakreslená jako trať podle ISOM: fialový start (701, trojúhelník otočený
  k první kontrole), kroužky kontrol (703) s čísly (704), rovné spojnice od
  okraje ke kraji (705), cíl jako dva kroužky (706); mezi mořemi spojnice
  odbíhá z mapy. Úvod ostrova říká „Start trati“ / „Kontrola n z 22“ / „Cíl“.
- **Sedm typů úkolů** (8 na ostrov, střídají se): *Najdi na mapě* (slyší
  jméno → klepne značku), *Co je to?* (vidí značku → vybere jméno), *Na rozum*
  („Kde si namočíš nohy?", „Co nesmíš přelézt?" – 22 otázek o tom, co značka
  znamená pro běžce), *Mapa ostrova* (mapka z dílků 4×4 s podkladem les/louka),
  *Kapitánův rozkaz* (klepni 2–3 značky popořadě), *Popisy kontrol* (piktogram
  ISCD → najdi na mapě, nebo mapová značka → vyber piktogram), *Pexeso*
  (dvojice značka + jméno, bonus). Boss: *Souboj s Mlhou* – 50 s, kdo přečte
  víc značek; po prohře je Mlha „unavený" a pomalejší.
- Nabídky k rozlišení obsahují přednostně **značku stejné barvy** (tečka vs.
  trojúhelník, plot vs. nepřekonatelný plot…), po chybě hlas řekne „to není X,
  ale Y" a ukáže správnou.
- **Odměny:** zlaťáky (+ bonus za sérii a za hvězdy), kousky mapy (skládá se
  obrázek pokladové mapy), posádka na palubě lodi (fond 20 zvířátek + Mlhův
  kocour), hodnosti Plavčík → Admirál, **denní poklad** (streak po dnech),
  **Pirátský krám** (klobouky, vlajky, poklady do truhly), po dohrání koruna,
  **Volné moře** (nekonečný režim s nejlepší sérií).
- **Učení:** karta ukazuje vedle sebe „Na mapě" a „V popisech kontrol",
  číslo ISOM a ostrov; nové značky se představí před ostrovem (karta + hlas +
  mini piktogram); adaptivní opakování (Leitner, `orient_prog`). Vše mluví
  (české TTS), číst není třeba.
- Pokrok uložen v prohlížeči (`orient_prog`, `orient_coins`, `orient_game`),
  tlačítko „Začít úplně znovu" vše smaže.

### Jak přidat další značky / ostrovy
1. V `zdroje/gen_symbols.py` přidej `add(id=…, name=…, isom=…, emoji=…, col=…,
   say=…, svg=…)`; plošné značky navíc `fill` (+ `deco`), liniové `tile`
   (kresba přes celý dílek mapy), piktogram do slovníku `DESC`.
2. Přidej ostrov do `ISL` (`id`, `name`, `emoji`, `syms`, `intro`; `boss=True`
   = souboj); skript hlídá, že každá značka je právě na jednom ostrově.
3. Volitelně otázku do `CON`. Spusť `python zdroje/gen_symbols.py`
   (přepíše datový blok v HTML) a přepublikuj.
Ostrovy se samy rozdělí po šesti do moří, kousků mapy je tolik jako ostrovů,
známé značky se na dalších ostrovech sčítají. Sprintový klíč ISSprOM 2019-2
(školní/parkové mapy) zatím není zvlášť – dá se přidat jako další moře.

## Tisknutelné obrázkové kartičky

- Hotové PDF: `deti-2trida/karticky-obrazkove-tisk.pdf`
- Zdroj: `zdroje/karticky-tisk.html`
- Přegenerování PDF: `python zdroje/render_pdf.py`
  (potřebuje Playwright s Chromium; renderuje HTML → A4 PDF)
