# Návrh rozšíření hry „Pirátský poklad“

Stav: návrh k diskusi (bez zásahu do kódu). Podklady: `ISOM-2017-2-cz-CSOS.pdf`, `mapovy-klic-ISOM2017-2-ISCD2018-tabulka.pdf`, `gen_symbols.py`, `tts/make_manifest.py`, `app/www/index.html` a tři soubory ISCD (původ viz sekce 8): **`ISCD-2024-cz-CSOS.pdf`**, `ISCD-2024-IOF.pdf`, `ISCD-2018-IOF.pdf`. **Návrh stojí na aktuálně platné verzi ISCD 2024** (máme k ní oficiální český překlad); rozdíly proti 2018, ověřené proti oběma anglickým originálům, jsou v sekci 10.

## 1. Shrnutí

- Hra se z 24 ostrovů ve 4 mořích prodlouží na **48 ostrovů v 8 mořích** (~2× delší, +192 úkolů, 8 na ostrov).
- **Moře 5–6 učí popis kontrol** (hlavička, sloupce A–H, zvláštní řádky): **69 nových piktogramů** (21 sloupce D, 5 sloupce C, 11 E, 7 F, 14 G, 1 H, 10 řádků mimo sloupce), všechny ověřené proti ISCD. Značka 704 (číslo kontroly) se zavádí přímo v moři 5 u sloupce A.
- **Moře 7 „Dvojčata“:** +18 mapových značek ISOM (86 → 104), vždy jako dvojčata už známých značek; 5 značek se vynechá (704 je v moři 5).
- **Moře 8 je „kapitánská zkouška“** přes všechno + vysvědčení. Navíc po každém moři **zkouška moře** a opakovací zastavení.
- 7 nových typů úkolů, jeden z nich výslovně učí „jeden piktogram – víc mapových značek“.
- Dabing: zhruba **+380 klipů** (421 → ~800), při denních limitech 2–3 dny čistého generování, rozložené do etap.
- Postup stávajících hráčů zůstane zachován: nové ostrovy se jen **připojují na konec** a `G.unlocked` (index) se tak nemění.

## 2. Nový scénář

### 2a) Stávající moře 1–4 (24 ostrovů, beze změny pořadí)

| Moře | Co se mění |
|---|---|
| 1 Papouščí, 2 Mlžné, 3 Bouřlivé, 4 Ledové | Obsah ostrovů zůstává (kvůli uloženému postupu). Přibývá **zkouška moře** (sekce 3), gradace obtížnosti (sekce 4) a u 21 značek bez otázky „na rozum“ jen volitelné doplnění. Pexeso/desc jsou dnes pro 15 značek bez piktogramu vynechány; ověřeno podle ISCD: **7 z nich piktogram v ISCD má** (viz sekce 6), 8 ne (v ISCD jsou piktogramy jen pro objekty kontroly, ne pro start, cíl, spojnici apod.). |

Pozn.: finále „Zlatý kompas“ (`G.won`) zůstává tam, kde je. Nová moře se nabídnou jako **„Druhá plavba“** po `G.won`, aby se dětem nezměnil konec hry.

### 2b) Nová moře (využívají už existující `SEAS[4..7]`: Sluneční, Korálové, Půlnoční, Perlové)

Pořadí (rozhodl Martin): popisy kontrol jako moře 5 a 6, doplnění mapových značek („Dvojčata“) až moře 7, kapitánská zkouška moře 8.

| Moře | Ostrovy (5 + souboj s Mlhou) | Zavádí se |
|---|---|---|
| 5 Sluneční – **„Jak mluví popis“ I** | Ostrov šifer (hlavička, řádek, A s **704 číslo kontroly**, B) · Ostrov hádanek (D voda, vegetace) · Ostrov skrýší (D skály) · Ostrov kopců (D terén) · Ostrov staveb (D umělé objekty) · Mlha | hlavička, sloupce A, B, D (+21 nových piktogramů D) |
| 6 Korálové – **„Jak mluví popis“ II** | Ostrov dvojčat C · Ostrov podob E · Ostrov rozměrů F · Ostrov poloh G · Ostrov zpráv H a zvláštních řádků · Mlha | sloupce C, E, F, G, H, zvláštní řádky (48 nových piktogramů) |
| 7 Půlnoční – **„Dvojčata“** (doplnění ISOM) | Ostrov dvojčat vody a zeleně · Ostrov rozpadlých věcí · Ostrov strání a hranic · Ostrov drsných povrchů · Ostrov mapového okraje · Mlha | 18 značek (níže) |
| 8 Perlové – **„Kapitánská zkouška“** | Ostrov první trati (čtení řádků + mini mapa) · Ostrov rychlé plavby (na čas) · Ostrov záměn (jen záměnné dvojice) · Ostrov celé trati (mapa + popis dohromady) · Ostrov velké zkoušky (vše) · Kapitán Mlha, poslední souboj | nic nového, jen souhrn |

**Značky pro moře 7 (18 z 23 chybějících; čísla ISOM ověřena proti PDF, názvy z textu PDF).** Značka 704 se v tomto pořadí zavádí už v moři 5 (u sloupce A), proto zde chybí.

| Ostrov | Značky | Didaktický důvod |
|---|---|---|
| Vody a zeleně | 305 malý překonatelný tok, 307 nepřekonatelná bažina, 404 divoký prostor s rozptýlenými stromy, 409 vegetace s dobrou viditelností | každá se učí vedle známé předlohy (potok, bažina, divoký prostor, podrost); „co je jinak?“ Piktogramy už děti znají z moře 5 (3.4, 3.7, 4.2) |
| Rozpadlých věcí | 106 rozpadlý zemní val, 514 rozpadlá zeď, 517 rozpadlý plot, 507 nezřetelná pěšina, 511 hlavní elektrické vedení | společný princip „rozpadlé / nezřetelné = přerušená čára“; v popisu je „rozpadlý“ výslovně sloupec E (8.11 zbořený) – krásná vazba na moře 6; vedení je rozšíření známého `vedeni` |
| Strání a hranic | 102 zdůrazněná vrstevnice, 108 malá erozní rýha, 415 zřetelná hranice obdělávané půdy | 102 je nutné pro čtení kopce („každá pátá silnější“); 108 má v ISCD vlastní piktogram 1.8 Malá rýha |
| Drsných povrchů | 114 velmi rozbitý povrch, 209 husté balvanové pole, 211 kamenitý povrch (chůze) | stupňování „víc teček = hůř se běží“; v popisu sdílí piktogramy 1.15, 2.5, 2.7 |
| Mapového okraje | 601 magnetický poledník, 702 místo výdeje map, 708 nepřekonatelná hranice | okraj mapy a pomocné značky |

**Vynecháno (5):** 212 (v textu PDF jen duplicitní nadpis; podle ISOM 2017-2 jde o kamenitý povrch – obtížný pohyb, tedy třetí stupeň k 210/211, český název ověřit v PDF), 215 (v extrahovaném textu PDF nejasný název; podle ISOM 2017-2 příkop/zákop, český název ověřit), 602 registrační značka a 603 výšková kóta (dítě je v mapě pro 2. třídu nepotřebuje, nemají piktogram ani úkolový smysl). **704 není vynechána, jen se přesouvá do moře 5.**

**Moře 5–6 – popis kontrol, ověřený obsah (zdroj: ISCD 2024, česky ČSOS a anglicky IOF, viz sekce 8 a 9).** Úplné seznamy piktogramů jsou v sekci 9.

| Sloupec | Co říká (podle ISCD) | Piktogramy ISCD | Nové ve hře |
|---|---|---|---|
| Hlavička | název závodu, kategorie (nepovinná), název tratě, délka v km (na 0,1 km) a převýšení v m (na 5 m); volitelný řádek 14.1 „vzdálenost z měřeného startu k mapovému startu“ | 0 (text), řádek 14.1 | 14.1 v „zvláštních řádcích“ |
| A | číslo kontroly v pořadí běhu (u score-O prázdné nebo bodová hodnota) | 0, číslo | 0 – **tady se zavádí 704** |
| B | kód kontroly, přirozené číslo > 30; nepoužívají se kódy zaměnitelné vzhůru nohama (66, 68, 86, 89, 98, 99); u startu může být S1, S2… | 0, číslo | 0 |
| C | který z několika podobných objektů | **5** (0.1–0.5) | 5 |
| D | objekt kontroly | **73** (1.1–6.2) + národní 7.n | 21 (ve hře už 52) |
| E | vzhled objektu; někdy druhý objekt (křížení, větvení, mezi) | **11** (8.1–8.11) | 11 |
| F | rozměry (9.1–9.4), kombinace dvou objektů (10.1, 10.2), ohyb (11.1) | **7** | 7 |
| G | poloha lampionu vůči objektu | **14** (12.1–12.14) | 14 |
| H | další informace | **3** (13.1–13.3) | 1 (13.1, 13.2 ve hře jsou) |
| zvláštní řádky | 14.1 vzdálenost ke startu; 15.1–15.6 značený úsek, povinný průběh, výměna a otočka mapy; 16.1–16.3 cesta z poslední kontroly do cíle | **10** řádků | 10 |

Celkem ISCD 2024 čísluje **123 symbolů** (73 + 5 + 11 + 7 + 14 + 3 + 10). Hra jich zná 54 (52 sloupce D + 13.1 a 13.2), **nových je 69**. Proti verzi 2018 jsou v 2024 dva symboly navíc (5.24 železnice, 15.6 otočka mapy); jinak číslování zůstalo stejné (podrobně sekce 10). Hra a komentář v `gen_symbols.py` dnes uvádějí „ISCD 2018“, v uživatelském rozhraní hry je jen „ISCD“.

Tabulka mapových ↔ popisových symbolů, kterou uvádí ISCD (2018 i 2024), potvrzuje poznámku o 212 a 215: **212 → 2.7 Kamenitý povrch (anglicky Stony ground), 215 → 2.10 Příkop (Trench)**; obě mají piktogram v obou verzích.

### 2c) Sdílené piktogramy – výslovně naučený jev

V datech ověřeno: 6 skupin, 15 značek, které mají identický piktogram:

| Piktogram | Mapové značky |
|---|---|
| zelená mřížka „porost“ | hustník, světlá zelená, střední zelená, podrost (4) |
| tečkovaná šikmá čára | úzká bažina, hranice vegetace, průsek (3) |
| „V“ | jáma, kamenná jáma (2) |
| plná šikmá čára | silnice, široká silnice (2) |
| přerušovaná šikmá čára | vozovka, cesta (2) |
| „×“ | vodní objekt, křížek (2) |

ISCD tento jev potvrzuje a je ještě širší: jeden piktogram 5.2 „Cesta, pěšina“ patří ISOM 504–507 (vozovka, cesta, pěšina i nezřetelná pěšina), 4.1 „Otevřený prostor“ patří 401, 403, 412–414 (louka, pole, sad, vinice), 6.1 patří 115, 313, 419, 531 a 3.7 „Bažina“ patří 307, 308, 310. Hra dnes některé tyto dvojice kreslí **různě** (viz tabulka odchylek v sekci 6).

Lekce „Jeden obrázek – víc map“ (Ostrov hádanek, moře 5): Pepík vysvětlí: *popis říká CO to je (objekt), mapa říká JAK je to znázorněné.* Úkol „sdílený piktogram“ (sekce 5). Zkouška moře 5 pak tyto skupiny vždy obsahuje.

## 3. Postupné testy

**Zkouška moře** (po 5. běžném ostrově, před soubojem s Mlhou, ~22 značek):
- Každá značka moře **přesně 1×**, směr se losuje (`find`: jméno → značka / `what`: značka → jméno). Chybně zodpovězené se po zkoušce zeptají **ještě 1× v opačném směru** (ověření, že to není náhoda).
- Výsledek po značkách: mřížka karet 🟢/🟡/🔴 (🟢 správně napoprvé, 🟡 správně až v opačném směru, 🔴 chyba), hlasem „Zvládl jsi 19 z 22, tyhle tři zkus znovu“.
- Neúspěch (chyba nebo 🔴): značce se sníží krabička o 1 (stejná logika jako `progBad`), přidá se **opravný ostrůvek** (3 úkoly jen s těmito značkami, bez dalších nároků). Zkoušku lze opakovat jen s neúspěšnými. Postup se **nepodmiňuje** (zachová se filosofie hry); medaile (bronz ≥ 60 %, stříbro ≥ 80 %, zlato ≥ 95 %) je odměna a vypíše se na mapě moře.
- Na krabičky navazuje: zlatý výsledek dá značce `box=4` (naučeno) i bez dalších pokusů; 🔴 vrátí na `box=1`.

**Průběžná opakovací zastavení:** po 3. ostrově každého moře 1 krátký úkol „Z minulých ostrovů“ (6 otázek z nejnižších krabiček napříč dosud odemčenými značkami, ne jen z moře).

**Kapitánská zkouška (moře 8):** přes všech 104 značek a 73 piktogramů D (+ piktogramy sloupců A–H); vybírá po ~2 otázky z každého moře a vždy nejnižší krabičky (max. 30 otázek), z toho 6 úkolů s popisem kontroly a 3 dvojité úkoly (řádek → mini mapa). Výsledek: **vysvědčení / diplom** (uložená stránka s jménem hráče, medailemi za 8 moří, počtem naučených značek a piktogramů, tisk přes stávající tisk karet).

## 4. Gradace obtížnosti

| Moře | Možností | Distraktory | Čas | Nápověda |
|---|---|---|---|---|
| 1 | 3 | jako dnes (80 % stejná barva) | ne | opakovat hlas, text vidět |
| 2 | 3 | 1 z 2 vždy z tabulky záměn (`CONF`) | ne | text vidět |
| 3 | 4 | 1 záměna povinně | měkký: bonus mince za rychlost, žádný trest | text vidět |
| 4 | 4 | 2 záměny | měkký | úkoly `what`/`order` bez zobrazeného textu jména (jen hlas) |
| 5–6 (popisy) | 3 → 4 | piktogramy ze stejné skupiny (sdílené nejsou nikdy mezi distraktory jako „špatně“) | ne | text jména skrytý, jen hlas |
| 7 (dvojčata) | 4 | vždy dvojče vedle předlohy | ne | bez textu jména, jen hlas |
| 8 | 5 | pouze záměny a dvojčata | měkký + souboje na čas | bez textu |

`CONF` = tabulka ~12 záměnných skupin v `gen_symbols.py` (kdo se mate: bažina / nezřetelná / úzká; balvan / velký / obrovský / shluk; zeď / nepřekonatelná zeď; plot / nepřekonatelný plot; sráz / nepřekonatelný sráz; louka / roztroušené / divoký; kupka / protáhlá; jáma / kamenná jáma; zelené odstíny; silnice / široká; vozovka / cesta; krouzek / krizek).

## 5. Nové typy úkolů

Dítě čte málo: vše se čte hlasem, skládá se z fragmentů `fr_*` + jmen `n_<id>` (pro piktogramy `pd_<id>`).

| Typ | Vidí a slyší | Ťuká | Vyhodnocení |
|---|---|---|---|
| **radek** – řádek → mapa | řádek popisu (A–G) a mini mapa 6–8 objektů; hlas „Řádek tři: …, kontrola na … straně objektu …“ | místo na mini mapě | trefa místa; chyba → zvýrazní řádek a řekne jen chybějící sloupec |
| **slozradek** – slož řádek | obrázek mapy s kontrolou, prázdný řádek s poli D, G | piktogram do pole D, pak G (výběr z 3–4) | oba správně = ok; bod za každé pole |
| **sloupec** – který sloupec? | zvýrazněný sloupec/ikona; hlas „Který sloupec říká, kde u objektu leží kontrola?“ | písmeno A–H (osm velkých kartiček) | trefa; využívá se i pro hlavičku |
| **pd_jmeno** – piktogram → název | piktogram; hlas „Co to je?“ | 3–5 jmen (jména jako ikony značek) | trefa; rozšíření stávajícího `desc` |
| **pd_obrazek** – název → piktogram | hlas „Najdi v popisu: sedlo“ | 3–5 piktogramů | trefa; sdílené piktogramy neberou se jako distraktor |
| **mapa_popis** – mapa, nebo popis? | karta se značkou nebo piktogramem | dvě velká tlačítka MAPA / POPIS | trefa; rozcvička pro moře 5 |
| **sdilene** – jeden obraz, víc map | piktogram; hlas „Kterým značkám patří tenhle obrázek?“ | všechny správné značky (2–4 z 6) | přesná množina; chybějící jmenuje hlasem |

## 6. Dopad na data a kód

**Piktogramy sloupce D – ověřeno proti ISCD.** `DESC` v `gen_symbols.py` má 71 položek. Z toho 67 jsou piktogramy sloupce D (pokrývají **52 z 73** čísel ISCD, protože některé sdílí číslo), 2 patří do sloupce H (`prvni_pomoc` = 13.1 kříž, `obcerstveni` = 13.2 kelímek; obě kresby souhlasí s originálem 2024, s. 16) a 2 nejsou ze sloupce D:
- `pisek` je ve skutečnosti symbol **sloupce E 8.8 „Sandy“ (písčitý)**, tečkovaná plocha (originál 2024, s. 13). ISCD pro písčitý povrch (ISOM 213) nemá vlastní piktogram D, ale kombinaci 4.1 Otevřený prostor + 8.8 (v 2018 ještě bez této věty, viz sekce 10). Kresba ve hře (mřížka teček ve čtverci) odpovídá; je to ale piktogram sloupce E.
- `pruchod` (ISOM 710) je **řádek 15.3 „Mandatory crossing point(s)“** (povinný bod přechodu), s. 17 originálu 2024. Tvar ve hře (dvě oblouky, horní prohnutý dolů, dolní nahoru, takže se uprostřed přibližují) odpovídá střední části symbolu 15.3. Pozor: v ISCD je celý řádek se symboly startu a cíle po stranách (kroužek, šipka) a patří mezi zvláštní pokyny, ne do pole D.

**Chybějících 21 piktogramů D** (sekce 9 uvádí názvy z ISCD): 1.1 terasa, 1.2 hřbítek, 1.3 údolíčko, 1.5 lom, 1.8 malá rýha, 1.11 sedlo, 1.12 prohlubeň (vrstevnicí), 1.16 mraveniště; 2.3 jeskyně, 2.9 úzký průchod, 2.10 příkop; 3.8 pevná půda v bažině, 3.11 vodní nádrž/žlab; 4.6 úzký hustník/živý plot, 4.8 skupina stromů; 5.6 sloup el. vedení, 5.7 tunel, 5.19 milíř/plošinka, 5.20 pomník/socha, 5.23 oblast se zákazem vstupu, 5.24 železnice.

**Pět značek, kterým původní návrh chtěl doplnit piktogram:**

| Značka (id, ISOM) | Existuje piktogram? | Závěr |
|---|---|---|
| nezřetelná bažina (`nezretelna_bazina`, 310) | ano, 3.7 Bažina (307, 308, 310). **Jen v ISCD 2024**: v 2018 je u 3.7 jen 307, 308 | použít existující piktogram `bazina`, žádné nové SVG |
| sad (`sad`, 413) | ano, 4.1 Otevřený prostor (412, 413, 414). **Jen v ISCD 2024**: v 2018 je u 4.1 jen 401, 403 | použít existující `louka`; stejně lze doplnit `pole` 412 a `vinice` 414 |
| plošinka / terénní objekt (`teren_objekt`, 115) | ano, 5.19 Milíř, plošinka (115) a 6.1 Výrazný objekt (115), stejně v 2018 i 2024 | 6.1 už ve hře je (×); 5.19 je nové SVG, pokud chceme „plošinku“ doslova |
| oblast zákazu (`zakaz`, 520) | ano, 5.23 Oblast se zákazem vstupu (stejně v 2018 i 2024) | nové SVG (v seznamu 21) |
| hřbítek (`doplnkova`, 103) | **ne ve smyslu 1:1**: 103 doplňková vrstevnice nemá vlastní piktogram; v ISCD 2024 patří k šesti tvarům (v 2018 měly tyto tvary jen 101; 102 a 103 přibyly) (1.1 terasa, 1.2 hřbítek, 1.3 údolíčko, 1.9 kupa, 1.11 sedlo, 1.12 prohlubeň) | původní předpoklad neplatí; značku bez piktogramu ponechat, tvary se učí jako 1.x |

Dále: `zeleznice` (509) má 5.24 Železnice – jen v ISCD 2024, v 2018 ne (originál 2018 symbol nemá). Ze 15 značek bez `desc` tedy piktogram v ISCD mají: nezřetelná bažina, pole, sad, vinice, plošinka, zákaz, železnice (7); nemají: pomocná vrstevnice, start, kontrola, cíl, spojnice, značený úsek, nepřístupná oblast, nepřístupná trasa (8; v ISCD je pro nepřístupnou oblast a značený úsek řádek 15.1–15.4, ne pole D).

**Odchylky hry od ISCD – porovnání kresby `DESC` s originálem 2024 (s. 7–11):**

| Skupina ve hře | ISCD (originál 2024) | Hra | Závěr |
|---|---|---|---|
| kupka × protáhlá kupka | 1.10 Knoll: jeden symbol, plný kroužek, pro 109 i 110 (s. 7) | `kupka` plný kroužek r 9 (v souladu); `protahla_kupka` plná elipsa 15 × 7 | `kupka` souhlasí; `protahla_kupka` je odchylka (ISCD kreslí i 110 kroužkem) |
| balvan × velký balvan | 2.4 Boulder: jeden plný trojúhelník pro 204 i 205 (s. 8) | oba plné trojúhelníky, jen větší (`velkybalvan`) | tvar souhlasí, rozlišení velikostí je navíc |
| (`obrovsky`) | 2.2 Rock pillar: úzký vysoký plný trojúhelník (206) | úzký vysoký trojúhelník | souhlasí |
| sráz × nepřekonatelný sráz | 2.1 Cliff, Crag: jeden symbol, vodorovná čára se třemi zuby dolů (201, 202) | `sraz`: čára s 5 zuby (v souladu v principu); `nepr_sraz`: silnější čára + 5 zubů | liší se počtem zubů; silná čára u `nepr_sraz` je odchylka |
| zeď × vysoká zeď | 5.8 Wall: jeden symbol, šikmá čára s tečkami (513, 514, 515) | `zed` čára + 3 tečky (v souladu); `nepr_zed` silnější čára + větší tečky | `zed` souhlasí, `nepr_zed` je odchylka |
| plot × vysoký plot | 5.9 Fence: jeden symbol, šikmá čára s krátkými příčkami (516, 517, 518) | `plot` čára + 3 příčky (v souladu); `nepr_plot` čára + dvojité příčky | `plot` souhlasí, `nepr_plot` je odchylka |
| potrubí × vysoké potrubí | 5.14 Prominent man-made line feature: jeden symbol, čára s šipkami (528, 529) | `potrubi` čára + 3 šipky (v souladu); `nepr_potrubi` silnější čára + 4 šipky | `potrubi` souhlasí, `nepr_potrubi` je odchylka |
| vozovka / cesta × pěšina | 5.2 Track / Path: jeden symbol, čárkovaná čára (504–507) (s. 10) | `vozovka` a `cesta` stejná čárkovaná čára (v souladu); `pesina` tenčí a s kratšími čárkami | `vozovka`, `cesta` souhlasí; `pesina` je jemná odchylka |

Shrnutí: **ISCD žádné rozlišení „vysoký/nepřekonatelný“ nemá**, všechna párová rozlišení ve hře (silnější čára, dvojité příčky, protáhlá elipsa) jsou didaktická, ne z ISCD. Základní varianty (`kupka`, `balvan`, `sraz`, `zed`, `plot`, `potrubi`, `vozovka`, `cesta`) jsou s ISCD v souladu. Kresbu jsem porovnával vizuálně z vykreslených stran originálu a ze zdrojového kódu `DESC`, ne pixelově. Pro přesnost vůči ISCD by popisové varianty měly být shodné s základním symbolem (a pak patří do skupiny sdílených piktogramů, sekce 2c).

**Otáčení symbolů ve sloupcích C a G (originál 2024):** sloupec C má symboly **0.1 šipka k severu a 0.2 šikmá šipka k jihovýchodu** (s. 6); ostatní světové strany se kreslí **otočením téže šipky** (v příkladu na s. 19, řádek 9 „Eastern re-entrant“, je šipka vodorovně doprava). **0.3 Horní, 0.4 Dolní, 0.5 Prostřední** jsou pevné symboly bez otáčení (čárky s tečkou nad/pod, svislé čárky s tečkou uprostřed). Ve sloupci G: výslovné pravidlo je jen u rohů: *„The orientation of the symbol indicates the direction in which the corner points“* (12.4 vnitřní a 12.5 vnější roh, s. 15). Symboly 12.1 strana a 12.2 okraj (s. 14), 12.6 cíp, 12.7 konec a 12.12 pata se směrem (s. 15–16) jsou ukázány v jedné orientaci a podle příkladů (s. 19: řádek 12 „east edge“ má kroužek s ouškem vpravo, řádky 14 a 16 „end“) se **otáčejí na světovou stranu**; 12.8–12.11, 12.13, 12.14 jsou pevné. U 12.3 „část“ (kroužek s tečkou, s. 15) jsem ze stran 15 a 19 nepoznal, zda se otáčí; **neověřeno**. Českému překladu (s. 15) odpovídá věta „Orientace symbolu určuje směr, kterým roh míří“. Pro hru z toho plyne: stačí **5 základních SVG pro C** (0.1, 0.2 + 3 pevné) a **7 základních SVG pro G se směrem** (12.1, 12.2, 12.4, 12.5, 12.6, 12.7, 12.12) s rotací v kódu; počet nových SVG se tím sníží.

**`gen_symbols.py`:** +18 SVG značek (`add(...)`, přesná kartografie dle ISOM: tloušťky čar, rozteče teček; skupiny „rozpadlá“ a „zdůrazněná“ čerpají z existujících vzorů, např. 102 = 101 s tloušťkou 2×, 209 = 208 s hustším rastrem); **+21 piktogramů D**; nový slovník `PD` (piktogramy sloupců A–H a řádků, **48**) a `CONF` (záměny); +24 položek `ISL`; `CON` pro 18 nových (a nepovinně pro 21 chybějících) otázek „na rozum“; doplnění `desc` pro 7 stávajících značek bez nového SVG (kromě 5.23 a případně 5.19). **Celkem ~87 nových SVG** (18 + 21 + 48), všechny piktogramy ověřené.

**`make_manifest.py` – odhad klipů (421 → ~800):**

| Hlas | Nové klipy | Obsah | Dní při limitu |
|---|---|---|---|
| Orus (úkoly a jména, 100/den) | ~185 | 18 + 69 `n_`/`pd_` jmen, ~40 fragmentů `fr_*`, ~18 q + 18 hint, pochvaly | 2 |
| Pepík (Achird, 100/den) | ~183 | `say_` (18) a výklady sloupců (~30), 24 × (intro + iname + crew), seadone, ui, vysvědčení | 2 |
| Mlha (Charon, 50/den) | ~12 | zkouška a poslední souboj | 1 |

Hlasy běží paralelně (limit je na model), proto celkem **~2 dny** čistého dabingu; po etapách (sekce 7) vychází 1 den na etapu. Pokud kolega znovu generuje, `pp_audio_dl` (flag stažení zvuku v appce) se musí zvednout, aby se nové klipy stáhly do Cache.

**Herní logika (`index.html`):**
- Nové typy úkolů `MODES.radek`, `slozradek`, `sloupec`, `pd_jmeno`, `pd_obrazek`, `mapa_popis`, `sdilene` + mini mapa (znovupoužití dílků `tile` ze značek).
- `planTasks` pro nová moře; `finishIsland` a stav „zkouška“ (`R.exam`) pro zkoušku moře; kapitánská zkouška; vysvědčení.
- `distractors()` rozšířit o `CONF`; nový `descDistractors` pro piktogramy sdílených skupin.
- **Zpětná kompatibilita:**
  - `orient_prog` se nemění (nové značky se inicializují automaticky přes `SY.forEach`).
  - Piktogramy mají vlastní klíč `orient_progd` (krabičky `pd_*`), takže `masteredCount` a existující postup nejsou dotčeny.
  - `G.unlocked` je index → nové ostrovy **jen na konec**, žádné vkládání doprostřed; `G.islands` je podle `id`, takže bezpečné.
  - `G.exams` a `G.won2` (nové klíče) se doplní přes `defG()` (`Object.assign` už dnes dosadí chybějící klíče).
  - Díky `G.won` se nová moře odemknou až po stávajícím finále.
  - Po OTA aktualizaci si hráč s uloženým postupem „Druhou plavbu“ prostě otevře.

## 7. Etapy realizace

| Etapa | Obsah | Nový dabing | Pracnost |
|---|---|---|---|
| **1 – Zkoušky a opakování** (schváleno) | zkouška moře 1–4, opravný ostrůvek, opakovací zastavení, medaile, gradace (`CONF`, 4–5 možností), doplnění `desc` pro stávající značky (nezřetelná bažina, sad, pole, vinice, plošinka, zákaz; nové SVG jen 5.23), lekce „sdílené piktogramy“ jako ustálený úkol | min. (~10–15 klipů pro Pepíka, 1 den; zkoušky využívají `n_*` a `fr_*`) | 5–6 dní |
| **2 – Popisy kontrol I (moře 5)** | hlavička, A (**704 číslo kontroly**), B, D (+21 piktogramů), úkoly `pd_jmeno`, `pd_obrazek`, `mapa_popis`, `sdilene`, mini mapa, zkouška moře 5 | ~120 klipů (1–2 dny) | 7–9 dní |
| **3 – Popisy kontrol II (moře 6)** | sloupce C, E, F, G, H, zvláštní řádky (48 piktogramů), úkoly `radek`, `slozradek`, `sloupec`, zkouška moře 6 | ~110 klipů (1–2 dny) | 8–10 dní |
| **4 – Dvojčata (moře 7)** | 18 SVG značek, 5 ostrovů + Mlha, intro, crew, zkouška moře 7 | ~120 klipů (1–2 dny) | 5–7 dní |
| **5 – Moře 8 a vysvědčení** | kapitánská zkouška, finální souboj, diplom, tisk | ~25 klipů (1 den) | 4–5 dní |

Každá etapa se dá vydat samostatně: 1 neruší nic, 2–5 jen přidávají ostrovy na konec.

## 8. Otázky pro Martina

**Rozhodnuto**

1. ~~Zdroj ISCD.~~ **Vyřešeno.** V `zdroje/` jsou tři oficiální soubory: (a) `ISCD-2024-cz-CSOS.pdf` (6 536 492 B, 33 stran; český překlad ISCD 2024, přeložili J. Fátor a R. Hošek, ČSOS), stažen z `https://www.ceskyorientak.cz/wp-content/uploads/sites/2/2025/04/ob-mezinarodni-popisy-kontrol-2024.pdf` (odkaz ze `https://metodika.ceskyorientak.cz/materialy/125-popisy-kontrol`, web nástupce `orientacnisporty.cz`); (b) `ISCD-2024-IOF.pdf` (5 119 899 B, anglický originál „IOF Control Descriptions 2024“) a (c) `ISCD-2018-IOF.pdf` (4 746 707 B, „control description-updated-A4-2019.pdf“, revize 6. 3. 2019); obě anglické verze stáhl orchestrátor přes Martinův prohlížeč s jeho souhlasem z odkazů na `https://orienteering.sport/iof/rules/control-descriptions/`. Český překlad verze 2018 jsem nenašel (na webu ČSOS je aktuální jen 2024).
2. ~~Pořadí nových moří.~~ **Rozhodnuto:** popisy kontrol jsou moře 5 a 6, „Dvojčata“ moře 7, kapitánská zkouška moře 8 (704 se zavádí v moři 5).
3. ~~Etapa 1.~~ **Schváleno k realizaci** (zkoušky, opravný ostrůvek, opakování, gradace).

**Otevřené**

4. **Přejít ve hře z ISCD 2018 na ISCD 2024?** Hra a komentář v `gen_symbols.py` dnes uvádějí „ISCD 2018“. Doporučení: **ano** – 2024 je platná verze, máme k ní oficiální český překlad a rozdíly jsou malé (sekce 10): 2 nové symboly (5.24 železnice, 15.6 otočka mapy), větší seznam ISOM čísel u šesti piktogramů D a upřesněné použití. Dopad: u hry **žádné přečíslování ani změna kresby** (čísla 0.1–16.3 jsou v obou verzích stejná); změní se jen komentář a popisky „ISCD 2018“ → „ISCD 2024“, název podkladové tabulky `mapovy-klic-ISOM2017-2-ISCD2018-tabulka.pdf` (tabulka je z ISCD 2018, zůstává) a možnost doplnit 7 značek (nezřetelná bažina, pole, sad, vinice, zdůrazněná a doplňková vrstevnice, železnice), které mají piktogram až v 2024. Nové ostrovy popisů (moře 5–6) se píší rovnou podle 2024.
5. **Pořadí: finále a nová moře.** Doporučení: ponechat dnešní finále a nová moře nabídnout jako „Druhou plavbu“ po `G.won`, ne měnit konec.
6. **Podmiňovat postup zkouškou?** Doporučení: ne (jen medaile a opravný ostrůvek), ať se děti nezablokují; při zlatém výsledku zrychlit `box`.
7. **Které z vynechaných značek chceš?** Doporučení: nezavádět 212/215/602/603; podle ISCD jsou 212 (2.7) a 215 (2.10) piktogramově pokryté, názvy v ISOM ještě ověřit.
8. **Nejasnost 4 vs. 5 možností.** Pro osmileté dítě na dotykové obrazovce 5 karet znamená malé cíle. Doporučení: max. 4 v mořích 1–7, 5 jen v moři 8 a v „Volném moři“.
9. **Piktogramy sdílené s více značkami: počítat odpověď jako správnou pro všechny?** Doporučení: ano (u `pd_obrazek` a `desc` je správně každá z nich), a výslovně to vysvětlit jednou hlasem v etapě 2.
10. **Odchylky hry od ISCD** (sekce 6, např. zeď × vysoká zeď): sjednotit s ISCD, nebo nechat didaktické rozlišení?

## 9. Ověřený seznam piktogramů (ISCD 2024: česky ČSOS, anglicky IOF)

Počty: C 5 · D 73 · E 11 · F 7 · G 14 · H 3 · zvláštní řádky 10. České názvy jsou z překladu ČSOS, anglické v závorce z originálu IOF 2024 (`ISCD-2024-IOF.pdf`). „Ve hře“: ano = ve hře existuje piktogram, **ne** = chybí. Dvojice čísel v závorce jsou ISOM značky, které piktogram zastupuje.

**Sloupec C (5):** 0.1 Severní (Northern) · 0.2 Jihovýchodní (South Eastern) · 0.3 Horní (Upper) · 0.4 Dolní (Lower) · 0.5 Prostřední (Middle). Všechny **ne**. Ostatní světové strany se kreslí otočením 0.1 a 0.2 (sekce 6, s. 6 a 19 originálu).

**Sloupec D (73), terénní tvary (16):** 1.1 Terasa (Terrace) **ne** · 1.2 Hřbítek (Spur) **ne** · 1.3 Údolíčko (Re-entrant) **ne** · 1.4 Zemní sráz (Earth bank) ano · 1.5 Lom (Quarry) **ne** · 1.6 Zemní val (Earth wall) ano · 1.7 Rýha (Erosion gully) ano · 1.8 Malá rýha (Small erosion gully) **ne** · 1.9 Kupa (Hill) ano · 1.10 Kupka (Knoll) ano · 1.11 Sedlo (Saddle) **ne** · 1.12 Prohlubeň (Depression) **ne** · 1.13 Malá prohlubeň (Small depression) ano · 1.14 Jáma (Pit) ano · 1.15 Rozbitý povrch (Broken ground) ano · 1.16 Mraveniště, termitiště (Ant hill, termite mound) **ne**.

**Skály a balvany (10):** 2.1 (Skalní) sráz (Cliff, Crag) ano · 2.2 Skalní věž, obrovský balvan (Rock pillar) ano · 2.3 Jeskyně (Cave) **ne** · 2.4 Balvan (Boulder) ano · 2.5 Balvanové pole (Boulder field) ano · 2.6 Shluk balvanů (Boulder cluster) ano · 2.7 Kamenitý povrch (Stony ground) ano · 2.8 Holá skála (Bare rock) ano · 2.9 Úzký (skalní) průchod (Narrow passage) **ne** · 2.10 Příkop (Trench) **ne**.

**Voda a bažiny (11):** 3.1 Jezero (Lake) ano · 3.2 Rybníček (Pond) ano · 3.3 Jáma s vodou (Waterhole) ano · 3.4 Řeka, potok (River, Stream, Watercourse) ano · 3.5 Malý vodní příkop (Minor water channel, Ditch) ano · 3.6 Úzká bažina (Narrow marsh) ano · 3.7 Bažina (Marsh) ano · 3.8 Pevná půda v bažině (Firm ground in marsh) **ne** · 3.9 Studna (Well) ano · 3.10 Pramen (Spring) ano · 3.11 Vodní nádrž, vodní žlab (Water tank, Water trough) **ne**.

**Vegetace (10):** 4.1 Otevřený prostor (Open land) ano · 4.2 Polootevřený prostor (Semi-open land) ano · 4.3 Roh lesa (Forest corner) ano · 4.4 Světlina (Clearing) ano · 4.5 Hustník (Thicket) ano · 4.6 Úzký hustník, živý plot (Linear thicket) **ne** · 4.7 Hranice vegetace (Vegetation boundary) ano · 4.8 Skupina stromů (Copse) **ne** · 4.9 Výrazný strom (Prominent tree) ano · 4.10 Vývrat, pařez (Prominent vegetation feature, e.g. root stock, tree stump) ano.

**Umělé objekty (24):** 5.1 Silnice (Road) ano · 5.2 Cesta, pěšina (Track / Path) ano · 5.3 Průsek (Ride) ano · 5.4 Most (Bridge) ano · 5.5 Elektrické vedení (Power line) ano · 5.6 Sloup elektrického vedení (Pylon) **ne** · 5.7 Tunel (Tunnel) **ne** · 5.8 Zeď (Wall) ano · 5.9 Plot (Fence) ano · 5.10 Průchod (Crossing point) ano · 5.11 Budova (Building) ano · 5.12 Zpevněná plocha (Paved area) ano · 5.13 Zřícenina (Ruin) ano · 5.14 Potrubí, bobová dráha (Prominent man-made line feature, e.g. pipeline; bobsleigh/skeleton track) ano · 5.15 Věž, stožár (Tower / Pylon) ano · 5.16 Posed (Shooting platform) ano · 5.17 Hraniční kámen, mohyla (Boundary stone, Cairn) ano · 5.18 Krmelec (Fodder rack) ano · 5.19 Milíř, plošinka (Charcoal burning ground, Platform) **ne** · 5.20 Pomník, socha (Monument or Statue) **ne** · 5.21 Zastřešení (Canopy) ano · 5.22 Schodiště (Stairway) ano · 5.23 Oblast se zákazem vstupu (Out of Bounds area) **ne** · 5.24 Železnice (Railway) **ne** (jen ISCD 2024).

**Zvláštní výrazné objekty (2):** 6.1 a 6.2 Výrazný objekt / Zvláštní objekt (Prominent feature / Special item): 6.1 pro ISOM 115, 313, 419, 531 ano; 6.2 pro 530 ano. Národní symboly 7.n se neřadí do počtu.

**Sloupec E (11):** 8.1 Nízký, plochý (Low) · 8.2 Mělký (Shallow) · 8.3 Hluboký (Deep) · 8.4 Zarostlý (Overgrown) · 8.5 Otevřený (Open) · 8.6 Skalnatý, kamenitý (Rocky, Stony) · 8.7 Bažinatý (Marshy) · 8.8 Písčitý (Sandy) **ano (ve hře jako `pisek`)** · 8.9 Jehličnatý (Needle leaved) · 8.10 Listnatý (Broad leaved) · 8.11 Zbořený (Ruined). Ostatní **ne**. (8.6 s 1.14 značí kamennou jámu, 8.8 s 4.1 písčitý povrch.)

**Sloupec F (7):** 9.1 Výška nebo hloubka (Height or Depth) · 9.2 Velikost (Size) · 9.3 Výška objektu ve svahu (Height on slope) · 9.4 Výšky dvou objektů (Heights of two features) · 10.1 Křížení (Crossing) · 10.2 Větvení (Junction) · 11.1 Ohyb (Bend). Všechny **ne**.

**Sloupec G (14):** 12.1 strana (North east Side) · 12.2 okraj (South east Edge) · 12.3 část (West Part) · 12.4 roh vnitřní (East Corner, inside) · 12.5 roh vnější (South Corner, outside) · 12.6 cíp (South west Tip) · 12.7 konec (North west End) · 12.8 Horní část (Upper Part) · 12.9 Dolní část (Lower Part) · 12.10 Nahoře (Top) · 12.11 Pata bez udání směru (Foot, no direction) · 12.12 pata se směrem (North east Foot) · 12.13 Pod (Beneath) · 12.14 Mezi (Between). Všechny **ne**; směr se u 12.1, 12.2, 12.4–12.7 a 12.12 kreslí otočením.

**Sloupec H (3):** 13.1 Stanoviště první pomoci (First Aid post) ano · 13.2 Občerstvovací stanice (Refreshment point) ano · 13.3 Lidská posádka (Manned control) **ne**.

**Zvláštní řádky (10):** 14.1 vzdálenost z měřeného startu k mapovému startu (Distance to the start triangle from the point of the timed start) · 15.1 značený úsek od kontroly (Follow Taped Route 60 m away from control) · 15.2 značený úsek mezi kontrolami (Follow Taped Route 300 m between controls) · 15.3 povinný bod přechodu (Mandatory crossing point or points; ve hře střed řádku jako `pruchod`) · 15.4 povinný průběh skrz zakázanou oblast (Mandatory passage through out of bounds area) · 15.5 značený úsek k výměně map (Follow Taped Route 50 m to Map Exchange) · 15.6 otočka mapy (Map flip, turn the map over; jen 2024) · 16.1 do cíle po značeném úseku (400 m from last control to Finish, follow taped route) · 16.2 trychtýřové značení a značený úsek (150 m, navigate to finish funnel, then follow taped route) · 16.3 cesta do cíle není značena (380 m, navigate to finish, no tapes). Všechny řádky kromě střední části 15.3 **ne**.

## 10. Rozdíly ISCD 2018 → 2024 (ověřeno porovnáním obou anglických originálů)

Porovnány všechny číslované položky (0.1–16.3: čísla, názvy, seznamy ISOM čísel, popisy), nejen úvod. Oficiální seznam změn v originálu 2024 má 8 bodů; český překlad přidává devátý v {závorce} jako poznámku překladatele (průsek kreslený žlutým rastrem), v angličtině není.

| Oblast | Změna 2018 → 2024 |
|---|---|
| Číslování | **Beze změny.** Všech 0.1–16.3 je v obou verzích stejných, nic se nepřečíslovalo ani nezaniklo. |
| Nové symboly | **5.24 Železnice (Railway; ISOM 509)**, **15.6 Otočka mapy (Map flip)**. |
| Změněné názvy | 4.10 „Root stock, Tree stump“ → „Prominent vegetation feature, e.g. root stock, tree stump“; 5.6 „Power line pylon“ → „Pylon“; 5.14 „Pipeline; bobsleigh/skeleton track“ → „Prominent man-made line feature, e.g. pipeline; bobsleigh/skeleton track“. Kosmetické: 0.2 „South Eastern“, 15.x bez čárky. |
| Rozšířené seznamy ISOM čísel | 1.1, 1.2, 1.3, 1.9, 1.11, 1.12: nově také 102, 103 (dříve jen 101); 3.2 +301; 3.7 a 3.8 +310; 4.1 nově 213, 412, 413, 414 (dříve 401, 403); 4.5 +406, 418; 4.7 +415; 4.8 +408, 410; 5.3 +401/416, 403/416; 5.6 +524; 5.11 +522.1; 6.2 jen 530 (dříve 115, 313, 530). |
| Upřesněné použití | 4.8 Copse i „průběžnější plocha stromů obklopená hustším porostem“; 5.11 Building i sloup podpírající střechu; 12.10 Nahoře a 12.13 Pod i pro horní a dolní ze dvou úrovní; 4.1 + 8.8 = písčitý povrch (213); 8.6 + 1.14 = kamenná jáma (203); sloupec C: pokud symbol nestačí k jednoznačnému určení místa lampionu, objekt není vhodný pro kontrolu; 12.1 zjednodušen (odpadla varianta b); odstraněny zmínky o sprintu u 4.5 a 4.6. |
| Dokument | pokrývá ISOM i ISSprOM; popis tisknout černě nebo fialově (2018 jen „čtvercová pole 5–7 mm“); kód startu (S1, S2) ve sloupci B. Změny 2018 oproti 2004 (např. ohyb ve sloupci F, nový příkop a zakázaná oblast, zrušený symbol rádiové/TV kontroly) už platí v obou verzích. |

**Co se týká piktogramů, které hra už má:** žádný piktogram ve hře se nemění ani nepřečísluje; čísla 0.1–16.3 jsou v obou verzích stejná a vzhled symbolů jsem u položek, které hra má, v obou verzích neporovnával pixelově (rozdíly v popisu textu žádné vizuální změny nenaznačují). Dotčené jsou jen **ISOM čísla** (mapování mapových značek na piktogram): značky, kterým hra dnes piktogram nedává, ho v 2018 nemají, ale v 2024 ano: nezřetelná bažina 310 (3.7), pole 412, sad 413, vinice 414 (4.1), zdůrazněná vrstevnice 102 a doplňková 103 (1.1–1.12) a železnice 509 (5.24). Značky `zakaz` (520) a `teren_objekt` (115) mají piktogram v obou verzích. `veg_x` (4.10), `veza` (5.15) a `potrubi` (5.14) mají jen změněný anglický název.
