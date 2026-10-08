# Návrh: denní smyčka, větší pexeso, nákupy, se kterými se dá hrát

Stav: návrh k diskusi (2026-10-08). Navazuje na `NAVRH-pribeh-dobrodruh.md`
(hrdina = hledač pokladů, domov = Tábor hledačů).

## Co dnes chybí

- Denní poklad je jedno klepnutí za 4 až 8 zlaťáků. Není co dělat, není na co se těšit,
  nic nehrozí. Zlaťáků je navíc hodně (každá správná odpověď + padající mince), takže
  samy o sobě nemotivují.
- Pexeso má 3 až 4 dvojice (6 až 8 karet), jen značka ↔ jméno, jen z aktuálního ostrova.
- Krám prodává klobouk, vlajku a „poklady", které jsou jen řádek emoji na domovské
  obrazovce. Nejde si je prohlédnout ani s nimi nic dělat.

## Princip: tři háčky, které u dětí 7–8 let fungují

1. **Něco, co roste** – Tábor hledačů se plní věcmi a zvířaty, každý den je vidět změna.
2. **Sbírka s prázdnými místy** – album nálezů se siluetami toho, co ještě chybí.
3. **Těšení na zítřek** – truhla dne se otevře jen po splnění denní výpravy, večer
   Pepík ukáže siluetu zítřejšího nálezu.

Zlaťáky zůstávají měnou na věci z krámu. Nálezy do sbírky za zlaťáky koupit NEJDOU,
jen z truhly dne a z řetězu výprav. To dává dennímu hraní smysl, který krám nenahradí.

## 1. Denní výprava (místo Denního pokladu)

Na domovské obrazovce místo tlačítka „Denní poklad" je **„📓 Deník hledače"**.
Po otevření Pepík přečte stránku dne: datum, řetěz výprav a **tři úkoly dne**.
Každý trvá 1 až 2 minuty, celkem do 5 minut.

| úkol dne | co to je | odkud bere obsah | výuka |
|----------|----------|------------------|-------|
| 🔎 **Značka dne** | jedna značka: Pepík řekne výklad (`say_<id>`), pak 2 rychlé otázky (najdi na mapě, co to je) | nejslabší naučená značka z `prog` (box nejnižší), po dohrání i obrázky z popisu kontrol | opakování podle zapomínání |
| ⚡ **Rychlá výprava** | 6 otázek v řadě, střídá typy úkolů (find, what, map, desc) | naučené značky, výběr vážený slabostí | spaced repetition |
| 🃏 **Pexeso dne** | velké pexeso (viz 2) | naučené značky, od 6 do 8 dvojic podle postupu | paměť + značka ↔ jméno/piktogram |

Po splnění všech tří se otevře **🎁 Truhla dne**: zlaťáky (5 + řetěz, strop 12) a
**jeden nález do sbírky** (viz 3c). Nálezy se losují z těch, které dítě ještě nemá.

**Řetěz výprav:** proužek 7 dnů s otisky bot 👣 (dnes zvýrazněný). Každý 7. den v řadě
= **Týdenní truhla** (vzácný nález + 20 zlaťáků). Přerušení: Pepík jen řekne „Včera jsme
na výpravě nebyli, řetěz začíná znovu", nic se neodebírá. Jeden „volný den" týdně
(řetěz přežije jednodenní pauzu) – doporučuji, děti nehrají o víkendu u babičky.

**Těšení:** po zavření truhly Pepík ukáže siluetu zítřejšího nálezu („Zítra v truhle
najdeš… něco s dírou!"). Silueta je tajemství, text je obecný, stačí 1 klip + pár variant.

**Když je hra dohraná:** úkoly dne čerpají z celé naučené sady (86 značek + 73 piktogramů),
takže denní výprava funguje i po Zlatém kompasu. To je dnes hlavní díra: po dohrání
zbývá jen Volné moře.

**Volitelně (fáze 3):** iOS připomínka přes `@capacitor/local-notifications` v 17:00
„Pepík: Dnešní výprava čeká!" – vyžaduje plugin, nový build a souhlas v iOS, zapnout
jen po Martinově schválení.

**Volitelně, ale silné:** jednou týdně **🌲 Výprava ven**: Pepík zadá, co najít venku
s rodičem („Najdi dnes opravdový balvan a klepni, až ho uvidíš"), rodič potvrdí
klepnutím, odměna = vzácný nález. Most mezi hrou a skutečným lesem, 6 až 8 klipů.

## 2. Větší pexeso

- **Na ostrově:** 6 dvojic (12 karet, 3×4 na výšku). Dvojice: značky ostrova + doplněk
  z dřívějších ostrovů (opakování). První dva ostrovy 4 dvojice.
- **Pexeso dne:** 6 až 8 dvojic (až 16 karet, 4×4). Velikost roste s počtem naučených
  značek a s řetězem výprav.
- **Tři druhy dvojic** podle postupu: značka ↔ značka (nejlehčí, první moře), značka ↔
  jméno (dnes), **značka ↔ piktogram popisu kontrol** (od 5. moře; přesně rozdíl mapa ×
  popis, který hra učí).
- Odměna roste s velikostí: 1 zlaťák za dvojici + bonus 2/3/4 za 4/6/8 dvojic bez chyby,
  u 8 dvojic navíc 2 XP. Chyby se dál nepočítají (bonusová hra).
- Karty 4×4 na telefonu: ~80 px, SVG značky čitelné, u jmen jen emoji + krátký název
  (font 12 px), piktogram jako SVG.

## 3. Nákupy, se kterými se dá hrát

### 3a. Tábor hledačů = hratelná scéna (domov)

Domovská obrazovka je tábor na pláži s pevnými **sloty**: stan, ohniště, stožár s vlajkou,
truhla, lavička pro posádku, strom, břeh s loďkou, obloha. Věci z krámu se do slotů
usazují a **reagují na klepnutí** (zvuk + animace, bez TTS, u posádky stávající klipy):

| věc (krám, kategorie 🏕️ Do tábora) | cena | co dělá po klepnutí |
|----|----|----|
| ⛺ Větší stan (3 stupně) | 20 / 45 / 80 | stan se nafoukne, zevnitř vykoukne člen posádky |
| 🔥 Ohniště → 🍲 Kotlík | 15 / 30 | praská, jiskry; kotlík bublá, posádka se nahrne blíž, Pepík „Mňam!" |
| 🪵 Lavička → 🪑 Houpací síť | 18 / 35 | zvíře se posadí / houpe se |
| 🥁 Bubínek | 25 | hraje rytmus, zvířata poskakují do taktu |
| 🪔 Lampion | 22 | tábor se setmí, rozsvítí se, svítí světlušky (noční režim scény) |
| 🔭 Pozorovatelna | 60 | ukáže siluetu příštího ostrova a jeho 2 značky dopředu |
| 🐟 Rybníček | 40 | ryba vyskočí, mince z vody (1 denně) |
| 🗿 Totem | 50 | zazpívá tři tóny podle hodnosti |
| 🎪 Vlajkový stožár s vlajkou (vlajky z krámu) | dnes | vlajka zavlaje, zní fanfára |

Posádka v táboře: klepnutí na zvíře = jeho věta (klipy `crew_*` už existují) + poskok.
Čím víc věcí, tím živější tábor: to je „něco, co roste".

### 3b. Vybavení hledače (má herní účinek)

| věc | cena | účinek |
|----|----|----|
| 🧭 Kompas | 30 | 1× za ostrov nápověda: Pepík znovu řekne výklad hledané značky (`say_<id>`, pedagogicky čisté) |
| 🪔 Lucerna | 35 | svíčka v souboji s Mlhou hoří o 20 % déle (pomůže slabším dětem přes bosse) |
| 🥾 Boty hledače | 40 | v Divočině 1 chyba odpuštěna (druhý život) |
| 🔭 Dalekohled (dnes „poklad") | 38 | na mapě ostrovů ukáže značky příštího ostrova |
| 🎒 Batoh | 45 | truhla dne dá 2 nálezy místo 1 (jednou týdně) |

Nasazené vybavení je vidět na avatarovi v táboře (vedle klobouku).

### 3c. Sbírka nálezů (album) – jen z truhly dne

Truhla v táboře se po klepnutí otevře na celou obrazovku: police s nálezy, chybějící jako
siluety s otazníkem. Každý nález má **jednu Pepíkovu větu** (klip) a drobnou reakci na
klepnutí (diamant se zatřpytí, mušle zašumí, bota zasmrdí = zvířata uskočí).

Čtyři sady po 6 (24 nálezů, 24 klipů Pepíka):
- **Mlhovy ztráty:** Mlhova bota 🥾, Mlhova ponožka 🧦, Mlhův kartáček 🪥, Mlhova lžíce 🥄,
  Mlhův deník s dírou 📓, Mlhův kompas bez střelky 🧭 („Proto se v lese ztratí!")
- **Z moře:** mušle 🐚, žraločí zub 🦷, perla 🦪, hvězdice ⭐, láhev se vzkazem 🍾
  (vzkaz = nápověda k dalšímu ostrovu), stará kotva ⚓
- **Z lesa:** šiška 🌰, paroh 🦌, pírko 🪶, kámen s dírou 🪨, muchomůrka 🍄, sovička z kůry 🦉
- **Pirátské:** zlatý dublon 🪙, prsten s lebkou 💍, mapa s dírou 🗺️, stará lampa 🪔,
  papouščí pírko (Pepíkovo!) 🦜, kousek Mlhovy vlajky 🏴‍☠️

Hotová sada = odznak do deníku + věc do tábora zdarma. Všech 24 = „Mistr sběratel"
(hodnost Legenda má smysl i sběratelsky). Vzácné nálezy (1 na sadu) jen z Týdenní truhly.

### 3d. Co s dnešním krámem

- Klobouky zůstávají (přidat 🤠 klobouk hledače a 🪖 helmu nechat).
- Vlajky: kategorie „Vlajky nad tábor", stejné položky.
- „Poklady do truhly" (diamant, prsten, pohár, socha, klíč): přesunout do sbírky jako
  pátá sada „Z krámu" (jediná, která jde koupit), ať nejsou dvě truhly. Dalekohled
  se stane vybavením.

## Ekonomika (hrubě)

Ostrov vynese ~15 až 25 zlaťáků, denní výprava ~10 až 15. Nový krám má ~20 položek za
~700 zlaťáků, takže malá věc do tábora každé 2 až 3 dny, velká týdně. Ceny doladit
po prvním týdnu hraní podle skutečného stavu truhly.

## Náklady

- **Dabing (Pepík, 2.5-flash):** deník a úkoly dne ~12 klipů, truhla dne a řetěz ~8,
  nálezy 24 (+6 za sadu „Z krámu"), tábor ~6, vybavení ~5. Celkem ~60 Pepíkových
  klipů = jeden den kvóty; úkolové prompty se recyklují (ask_/askpd_ existují).
  Reakce věcí v táboře jsou zvukové efekty (WebAudio), bez TTS.
- **Kód:** nová obrazovka Deník, generátor úkolů dne nad `prog`, pexeso s velikostí
  a druhem dvojic, scéna tábora se sloty (SVG + CSS animace), album, vybavení (5 háčků
  v herní logice), nový `G.daily` (řetěz, volný den, nálezy, vybavení, tábor).
- **Uložení:** vše v `G` (localStorage + Preferences v appce), žádný server.

## Pořadí prací (návrh)

1. **Fáze 1 – příběh + tábor + pexeso:** texty podle `NAVRH-pribeh-dobrodruh.md`,
   hodnosti, tábor jako scéna se sloty (zatím stan, ohniště, stožár, truhla, posádka),
   větší pexeso na ostrovech. ~35 klipů.
2. **Fáze 2 – denní výprava + sbírka:** Deník, tři úkoly dne, truhla dne, řetěz,
   silueta zítřka, album nálezů, krám přeskládaný. ~45 klipů.
3. **Fáze 3 – věci do tábora + vybavení + Výprava ven + připomínka:** interaktivní
   věci, 5 účinků vybavení, týdenní úkol venku, iOS notifikace. ~15 klipů.

Každá fáze = commit, build appky, nové klipy FTP, bump audio cache.
Texty všech klipů Martinovi ukázat před generováním (soubor `zdroje/texty-faze<N>.md`).
