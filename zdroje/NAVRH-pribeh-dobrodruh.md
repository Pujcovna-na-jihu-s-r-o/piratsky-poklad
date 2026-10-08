# Návrh nového příběhu: hledač pokladů místo námořníka

Stav: návrh k diskusi (2026-10-08), nic ve hře zatím nezměněno.

## Proč měnit

Dnešní rámec dělá z dítěte námořníka (Plavčík → Námořník → Lodník → Kormidelník →
Kapitán → Admirál). To koliduje s tím, co hra učí: čtení **mapy terénu** (les, louka,
balvany, cesty), ne námořních map. Lov pokladu, cesta podle mapy i přesun po moři mezi
ostrovy jsou v pořádku, ale hrdina má být **dobrodruh, hledač pokladů**.

## Doporučený koncept: „Hledač pokladů proti pirátovi"

**Logline:** Piráti kdysi zakopali poklad a nakreslili k němu mapu stejnými značkami,
jaké dnes používá orientační běh. Kapitán Mlha mapu ukradl a roztrhal. Jenže Mlha umí
jen plout po moři. V lese se ztratí za první borovicí, a proto poklad nikdy nenašel,
i když mapu držel v ruce. Ty jsi hledač pokladů. Hledači nesedí na lodi, chodí po lese,
přes kopce a louky, a mapu čtou jako knížku. Přesně to se naučíš, a proto poklad najdeš
ty, ne on.

**Proč to funguje:**
- Motivace je přímo dovednost, kterou hra učí: číst mapu terénu je superschopnost,
  kterou pirát nemá. Dítě ho poráží tím, co se právě učí.
- Moře zůstává jen jako doprava mezi ostrovy (loďka je jako autobus). Práce začíná na
  břehu. Nic „námořního" se neučí ani nehraje.
- Pirátský poklad, Zlatý kompas, kapitán Mlha i papoušek Pepík zůstávají. Název hry
  „Pirátský poklad" platí dál: je to poklad pirátů, ne hra o tom, že jsi pirát.
- Pepíkovo „Arr!" dává smysl: je to bývalý pirátský papoušek, který se přidal
  k hledačům pokladů. (Volitelně: seděl na rameni pirátovi, který mapu kreslil,
  proto zná každou značku.)

## Hrdina a oslovení

- Dítě = **hledač pokladů** od první minuty. Univerzální oslovení ve všech Pepíkových
  i úkolových větách: **„dobrodruhu"** (nahrazuje „plavčíku" i „námořníku").
- Mlha dítě oslovuje posměšně: **„suchozemská kryso"** (pirátské „landlubber").
  Podtrhuje kontrast moře × souš a dětem to přijde vtipné. Alternativa: „hledači".
- Vrcholná pochvala: „Jsi opravdový hledač pokladů!" / „Jsi mistr mapy!"
  (místo „opravdový kapitán" a „jako opravdový pirát").

## Hodnosti (Klub hledačů pokladů)

| XP  | dnes        | nově               | emoji |
|-----|-------------|--------------------|-------|
| 0   | Plavčík     | Nováček            | 🧒    |
| 20  | Námořník    | Stopař             | 👣    |
| 50  | Lodník      | Průzkumník         | 🔭    |
| 90  | Kormidelník | Hledač pokladů     | 🗺️    |
| 150 | Kapitán     | Mistr mapy         | 🏅    |
| 240 | Admirál     | Legenda            | 👑    |

Hodnosti jsou stupně v Klubu hledačů pokladů. „Mistr mapy" sedí přesně na cíl hry.

## Nové a změněné texty příběhu

Úvodní příběh `story_0`, `story_1`, `mlha_story`, `story_2`, `story_3` zůstávají
beze změny (nemluví o námořnících). Přibývá jedna věta mezi `story_2` a `story_3`:

- `story_2b` (Pepík): „Kapitán Mlha umí plout po moři, ale v lese se ztratí hned za
  první borovicí. Proto poklad nikdy nenašel, i když měl mapu v ruce. Ty jsi hledač
  pokladů. Hledači nesedí na lodi, chodí po lese, přes kopce a louky, a mapu čtou
  jako knížku."

Volitelně do `story_3`: „Já jsem papoušek Pepík. Kdysi jsem seděl na rameni pirátovi,
který tu mapu kreslil, a tak znám každou značku. Budu ti pomáhat. …" (přegenerování
1 klipu navíc).

## Mapování stávajících prvků

| prvek                      | dnes                              | nově                                   | klipy |
|----------------------------|-----------------------------------|----------------------------------------|-------|
| oslovení hráče             | plavčíku / námořníku              | dobrodruhu                             | 9     |
| hodnosti                   | námořnické                        | Klub hledačů pokladů (viz výše)        | 5     |
| hráč = kapitán / pirát     | „jsi opravdový kapitán/pirát"     | „opravdový hledač pokladů", „mistr mapy" | 5   |
| domov                      | loď s vlajkou                     | **Tábor hledačů**: stan, ohýnek, stožár s vlajkou, truhla, parta zvířat u ohně, loďka u břehu v pozadí | 0 |
| tlačítko „⛵ Vyplout na mapu" | vyplout                         | „🗺️ Na výpravu!"                        | 0     |
| „Až budeš připravený, vypluj!" | vypluj                        | „…vyraz na výpravu!"                   | 2     |
| Volné moře (nekonečný režim) | Volné moře                      | **Divočina** 🌲 („Kolik značek přečteš v řadě…") | 3 |
| Druhá plavba (moře 5)      | plavba                            | Druhá výprava                          | 1     |
| Kapitánův rozkaz (pořadí)  | rozkaz                            | „Stopa za stopou! Klepni značky v tomhle pořadí." | 1 (+2 nepoužité fr_) |
| Zkouška moře               | moře = oblast ostrovů             | zůstává (oslovení uvnitř → dobrodruhu) | 2     |
| krám                       | Pirátský krám, „vlajku dáš na loď" | **Krám U Papouška**, „vlajku vyvěsíš nad tábor" | 2 |
| kategorie v krámu          | Vlajky na loď                     | Vlajky nad tábor (klobouky a poklady zůstávají) | 0 |
| posádka zvířat             | „se přidává k posádce"            | zůstává „posádka" (posádka výpravy je běžné), jen 6 vět s lodním slovníkem přepsat | 6 |
| moře 1–8, ostrovy, Mlhova zátoka/útes/pevnost/šifrovna | –    | zůstává (oblasti světa, doprava po moři je povolená) | 0 |
| kapitán Mlha, Zlatý kompas, Pepík, zlaťáky, truhla, hvězdy, medaile | – | zůstává | 0 |

Věty posádky k přepsání (jen lodní slovník):
- Opička Kiki: „Umí šplhat na **stromy** a hlídat zlaťáky." (2 klipy, crew0 a crew20)
- Chobotnice Ola: „Osmi rukama **prohrabe každou skrýš**."
- Delfín Dan: „**Převeze tě přes každou řeku.**"
- Tučňák Pája: „Chodí v obleku **i v lese**."
- Koala Kuba: „Prospí celou **výpravu**."

## Co se nemění

Značky, ostrovy, úkoly, zkoušky, souboje se svíčkou, finále na mini mapě, sbírání
kousků mapy, posádka zvířat (jen 6 vět), krám (jen názvy), 5. moře a popisy kontrol.
Název hry, bundle id, server, OTA.

## Náklady

- **Dabing: 34 klipů přepsat a přegenerovat** (26 Pepík na 2.5-flash, 7 úkol na
  3.1-flash, 1 Mlha na 2.5-pro) + 1 nový `story_2b`. Vejde se do jednoho dne kvót.
  Kontrola mužského hlasu přes `tts/gender.py` jako při minulé opravě.
- Texty: `tts/make_manifest.py` (UI, RANKS), `gen_symbols.py` (CREW, PRAISE),
  `hra-piratsky-poklad.html` (RANKS, SHOP, tlačítka, nadpisy, popis v `<meta>`).
- Domovská scéna: nové SVG tábora místo lodi (Sonnet subagent, jen CSS/markup).
- Appka: bump cache `pp-audio-v1` → `v2` v `app/wrapper/tail.html`, `build_app.py`,
  commit, OTA build. Nahrání nových mp3 FTP (Martin).

## Alternativy (nedoporučuji, pro úplnost)

**B. Poklad dávné civilizace.** Značky vymysleli „Lidé z Mlžných ostrovů", poklad je
v jejich ztraceném chrámu, Mlha je pirát, který ho chce taky. Plus: víc „legendy".
Minus: přepis `story_0/1`, finále („pirátská mapa", „Pirátská cesta" v hlavičce
popisu), název hry → o ~10 klipů víc, bez pedagogického zisku.

**C. Dědečkova mapa.** Mapu nakreslil dědeček orienťák a schoval vnoučeti poklad;
nejpoctivější vysvětlení, proč mapa používá značky ISOM. Minus: piráti a Mlha pak
nedávají smysl, znamenalo by to nového záporáka, nové názvy ostrovů Mlhy a nový název
hry. Zdaleka nejdražší varianta.

## Rozhodnuto (Martin 2026-10-08)

1. Mlha oslovuje hráče „suchozemská kryso". ANO.
2. Nekonečný režim se jmenuje „Divočina". ANO.
3. „Posádka" zůstává (přepsat jen 6 vět s lodním slovníkem).
4. Pepík je bývalý pirátský papoušek, přidat do `story_3`. ANO.

Navazující požadavky (denní motivace, větší pexeso, užitečné nákupy) jsou
v `NAVRH-denni-motivace.md`. Tábor hledačů z tohoto návrhu je tam rozpracovaný
jako hratelná scéna, proto ho stavět rovnou se sloty pro věci z krámu.
