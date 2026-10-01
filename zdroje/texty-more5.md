# 5. moře „Jak mluví popis I“: texty a data ke schválení

Podklad pro majitele. Je to druhá etapa rozšíření hry (výuka popisů kontrol, sloupce A, B, D). Moře 5 = `SEAS[4]` Sluneční moře, 5 ostrovů a souboj s kapitánem Mlhou, za stávajícími 24 ostrovy. Vše je zatím jen data a texty, herní logiku doplní další krok. Soubor vzniká podle `gen_symbols.py` a `tts/manifest.json`.

## Počty nových klipů k namluvení

| Hlas | Nových klipů |
|---|---|
| Pepík | 47 |
| Úkolový hlas | 58 |
| Mlha | 0 |
| **Celkem** | **105** |

Pepík: 6 úvodů ostrovů, 6 jmen ostrovů, 6 vět posádky, 7 kroků výkladu, 19 výkladů nových piktogramů, výklad značky 704 a texty `ui_newpds`, `ui_boss_rules5`. Úkolový hlas: 37 jmen piktogramů, jméno značky 704 a zadání a zpětná vazba nových úkolů. Mlha nemá nové věty (souboj používá stávající `mlha_*` klipy).

### Znovupoužité klipy (36 jmen piktogramů)

Mluvený název piktogramu je shodný s textem už namluveného klipu jména mapové značky, proto se použije ten a nenamlouvá se znovu.

| Piktogram | Mluvený název | Klip |
|---|---|---|
| 1.6 | Zemní val | `n_val` |
| 1.7 | Rýha | `n_ryha` |
| 1.10 | Kupka | `n_kupka` |
| 1.12 | Prohlubeň | `n_prohluben` |
| 1.14 | Jáma | `n_jama` |
| 1.15 | Rozbitý povrch | `n_rozbity` |
| 2.1 | Skalní sráz | `n_sraz` |
| 2.4 | Balvan | `n_balvan` |
| 2.5 | Balvanové pole | `n_balvanove_pole` |
| 2.6 | Shluk balvanů | `n_shluk` |
| 2.7 | Kamenitý povrch | `n_kamenity` |
| 2.8 | Holá skála | `n_skala` |
| 3.3 | Jáma s vodou | `n_jama_s_vodou` |
| 3.4 | Potok | `n_potok` |
| 3.6 | Úzká bažina | `n_uzka_bazina` |
| 3.7 | Bažina | `n_bazina` |
| 3.9 | Studna | `n_studna` |
| 3.10 | Pramen | `n_pramen` |
| 4.5 | Hustník | `n_housti` |
| 4.10 | Vývrat | `n_veg_x` |
| 5.1 | Silnice | `n_silnice` |
| 5.3 | Průsek | `n_prusek` |
| 5.4 | Most | `n_most` |
| 5.5 | Elektrické vedení | `n_vedeni` |
| 5.8 | Zeď | `n_zed` |
| 5.9 | Plot | `n_plot` |
| 5.10 | Průchod | `n_pruchod` |
| 5.11 | Budova | `n_budova` |
| 5.13 | Zřícenina | `n_zricenina` |
| 5.14 | Potrubí | `n_potrubi` |
| 5.16 | Posed | `n_posed` |
| 5.17 | Hraniční kámen | `n_mohyla` |
| 5.18 | Krmelec | `n_krmelec` |
| 5.24 | Železnice | `n_zeleznice` |
| 6.1 | Zvláštní objekt – křížek | `n_krizek` |
| 6.2 | Zvláštní objekt – kroužek | `n_krouzek` |

## Ostrovy 5. moře

| # | Ostrov (id) | Co se učí | Piktogramů | Z toho nových |
|---|---|---|---|---|
| 25 | 📜 Ostrov šifer (`sifry`) | Co je popis kontrol (lístek, řádek = kontrola), hlavička, sloupec A (pořadí = číslo u kolečka, nová mapová značka 704 Číslo kontroly), sloupec B (kód na lampionu, větší než 30), sloupec D (co je objekt); rozdíl značka z mapy × obrázek z popisu | 0 | 0 |
| 26 | 🧩 Ostrov hádanek (`hadanky`) | Sloupec D: voda a vegetace, zopakování známých a nové 3.8, 3.11, 4.4, 4.6, 4.8 | 21 | 5 |
| 27 | 🗝️ Ostrov skrýší (`skryse`) | Sloupec D: skály a balvany, známé a nové 2.3, 2.9, 2.10 | 10 | 3 |
| 28 | ⛰️ Ostrov kopců (`kopce`) | Sloupec D: terénní tvary, známé a nové 1.1, 1.2, 1.3, 1.5, 1.8, 1.11, 1.12, 1.16 | 16 | 8 |
| 29 | 🏗️ Ostrov pirátských staveb (`pstavby`) | Sloupec D: umělé objekty a zvláštní objekty 6.1, 6.2, známé a nové 5.6, 5.7, 5.20 | 26 | 3 |
| 30 | 🌫️ Mlhova šifrovna (`mlha5`) (souboj) | Souboj: rychlé „najdi piktogram podle jména“ ze všech piktogramů, které dítě zná | 0 | 0 |

Každý z 73 piktogramů sloupce D je právě na jednom ostrově. Ostrov šifer a souboj nemají vlastní seznam piktogramů. Ostrov staveb se jmenuje „Ostrov pirátských staveb“, protože „Ostrov staveb“ už je ve 3. moři.

### Texty ostrovů

| Id klipu | Hlas | Text |
|---|---|---|
| `intro_sifry` | Pepík | Na Ostrově šifer leží pirátský lístek plný řádků a čísel. Říká se mu popis kontrol. Pojď, naučím tě ho číst! |
| `iname_sifry` | Pepík | Ostrov šifer |
| `crew_crew24` | Pepík | Mýval Mates se přidává k posádce! Luští šifry jako oříšky. |
| `intro_hadanky` | Pepík | Na Ostrově hádanek jsou obrázky z popisu kontrol. Hádej, co znamenají: voda, bažina, strom nebo světlina uprostřed lesa. |
| `iname_hadanky` | Pepík | Ostrov hádanek |
| `crew_crew25` | Pepík | Vydra Vanda se přidává k posádce! Zná každou řeku i každý rybník. |
| `intro_skryse` | Pepík | Mezi skalami jsou skrýše pirátů: jeskyně, úzký průchod i příkop. Poznáš jejich obrázky v popisu kontrol? |
| `iname_skryse` | Pepík | Ostrov skrýší |
| `crew_crew26` | Pepík | Krokodýl Karel se přidává k posádce! Najde každou skrýš mezi skalami. |
| `intro_kopce` | Pepík | Na Ostrově kopců je samý kopec, hřbítek a údolíčko. Najdeš tu i sedlo, lom a mraveniště. Ukážu ti jejich obrázky z popisu! |
| `iname_kopce` | Pepík | Ostrov kopců |
| `crew_crew27` | Pepík | Medvěd Macek se přidává k posádce! Vyleze na každý hřbítek. |
| `intro_pstavby` | Pepík | Na tomhle ostrově stojí stavby: sloup, tunel i pomník. Poznáš jejich obrázky v popisu kontrol? |
| `iname_pstavby` | Pepík | Ostrov pirátských staveb |
| `crew_crew28` | Pepík | Bobr Bořek se přidává k posádce! Postaví most i hráz. |
| `intro_mlha5` | Pepík | Kapitán Mlha se ukrývá v šifrovně! Řekne ti jméno a ty rychle najdeš jeho obrázek v popisu kontrol. Kdo jich najde víc, než dohoří svíčka? |
| `iname_mlha5` | Pepík | Mlhova šifrovna |
| `crew_crew29` | Pepík | Labuť Lída se přidává k posádce! Proplave každou mlhou. |

### Výklad lístku popisu kontrol (Ostrov šifer)

| Id klipu | Hlas | Text |
|---|---|---|
| `les_1` | Pepík | Piráti si trasu píšou na lístek. Říká se mu popis kontrol. Je to tabulka a každý řádek v ní patří jedné kontrole. |
| `les_2` | Pepík | Nahoře je hlavička. Je v ní název trati, její délka v kilometrech a převýšení. To je, kolik metrů celkem vystoupáš do kopce. |
| `les_3` | Pepík | Pod hlavičkou jsou řádky. Jeden řádek, jedna kontrola. Čtou se shora dolů, tak jak poběžíš. |
| `les_4` | Pepík | Ve sloupci A je pořadí kontroly. Stejné číslo najdeš na mapě vedle fialového kolečka. První řádek je první kolečko. |
| `les_5` | Pepík | Ve sloupci B je kód kontroly. To je číslo napsané na lampionu. Podle něj poznáš, že jsi doběhl ke správné kontrole. Kód je vždycky větší než třicet. |
| `les_6` | Pepík | Ve sloupci D je obrázek, který říká, co na kontrole najdeš. Třeba balvan, studnu nebo kopec. |
| `les_7` | Pepík | Pozor! Značka na mapě a obrázek v popisu kontrol nejsou totéž. Mapa ti ukáže, kde to je. Obrázek v popisu ti řekne, co to je. Proto vypadají jinak. |

### Mapová značka 704 Číslo kontroly

ISOM 2017-2, s. 34: fialová číslice (Arial 4,0 mm, ne tučně, ne kurzívou, orientovaná k severu) u kolečka kontroly. Zatím mimo seznam značek hry (v datech `SYM704`).

| Id klipu | Hlas | Text |
|---|---|---|
| `n_cislo_kontroly` | úkolový | Číslo kontroly |
| `say_cislo_kontroly` | Pepík | Fialová číslice vedle kolečka je číslo kontroly. Říká, kolikátá v pořadí to je. Pomůcka: kolečko má číslo, aby ses v pořadí nepletl! |

## Zadání a zpětná vazba nových úkolů

Id jsou závazná, herní logika je použije přesně takto. Čísla se nenamlouvají. Za fragmenty `ui_pd_pic`, `fr_vpopisu` se přehraje jméno piktogramu.

| Id klipu | Hlas | Text |
|---|---|---|
| `ui_mp` | úkolový | Je tohle značka z mapy, nebo obrázek z popisu kontrol? |
| `fr_zmapy` | úkolový | To je značka z mapy. |
| `fr_zpopisu` | úkolový | To je obrázek z popisu kontrol. |
| `ui_pd_name` | úkolový | Co znamená tenhle obrázek v popisu kontrol? |
| `ui_pd_pic` | úkolový | Najdi v popisu kontrol: |
| `fr_vpopisu` | úkolový | V popisu kontrol je to |
| `ui_row_a` | úkolový | Ťukni na pořadí kontroly. |
| `ui_row_b` | úkolový | Ťukni na kód kontroly. |
| `ui_row_d` | úkolový | Ťukni na obrázek, který říká, co na kontrole najdeš. |
| `ui_row_len` | úkolový | Ťukni na délku tratě. |
| `ui_row_climb` | úkolový | Ťukni na převýšení. |
| `ui_row_name` | úkolový | Ťukni na název tratě. |
| `fr_row_a` | úkolový | To je pořadí kontroly. Stejné číslo najdeš na mapě u kolečka. |
| `fr_row_b` | úkolový | To je kód kontroly. Stejné číslo najdeš na lampionu. |
| `fr_row_d` | úkolový | To je obrázek, který říká, co na kontrole najdeš. |
| `fr_row_len` | úkolový | To je délka tratě. Říká, kolik kilometrů poběžíš. |
| `fr_row_climb` | úkolový | To je převýšení. Říká, kolik metrů celkem vystoupáš do kopce. |
| `fr_row_name` | úkolový | To je název tratě. |
| `ui_newpds` | Pepík | Tohle jsou nové obrázky z popisu kontrol. Klepni na ně a poslechni si je. Až budeš připravený, vypluj! |
| `ui_boss_rules5` | Pepík | Já ti řeknu jméno a ty rychle klepni na jeho obrázek v popisu kontrol. Vyhraje ten, kdo jich najde víc, než dohoří svíčka. |
| `ui_duel_pd` | úkolový | Souboj! Najdi v popisu kontrol správný obrázek dřív než Mlha, než dohoří svíčka. |
| `exam5_intro` | úkolový | Zkouška moře! Na každý obrázek z popisu kontrol se zeptám jen jednou a nápovědu nedám. Ukaž, co umíš, námořníku! |

Navíc oproti zadání (stávající texty říkají „značka“, tady jde o obrázky z popisu): `ui_newpds`, `ui_boss_rules5`, `ui_duel_pd`, `exam5_intro`.

## Piktogramy sloupce D (73)

Český název podle překladu ČSOS (`ISCD-2024-cz-CSOS.pdf`), strana originálu IOF 2024 (`ISCD-2024-IOF.pdf`). „Nový“ = hra pro něj nemá mapovou značku; jen u nových je výklad Pepíka (ostatní mají výklad u mapové značky). Klip „znovu“ = použije se existující klip jména značky, „nový“ = nový klip `pdn_`.

### Terénní tvary (1.x, Ostrov kopců)

| ISCD | Strana IOF | Oficiální název (ČSOS) | Mluvený název | Alt | Klip | Mapové značky hry | Výklad (jen nové) |
|---|---|---|---|---|---|---|---|
| 1.1 | 6 | Terasa | Terasa | – | `pdn_1_1` (nový) | – | **nový** 📏 Terasa je rovná plošinka na svahu, takový obří schod. Na mapě poznáš, že tu jsou vrstevnice daleko od sebe. |
| 1.2 | 6 | Hřbítek | Hřbítek | – | `pdn_1_2` (nový) | – | **nový** 👃 Hřbítek je výběžek kopce, jako nos vystrčený do údolí. Vrstevnice na mapě z kopce vybíhají ven. |
| 1.3 | 6 | Údolíčko | Údolíčko | – | `pdn_1_3` (nový) | – | **nový** 🏞️ Údolíčko je zářez do kopce, malé údolí, opak hřbítku. Vrstevnice na mapě v něm vybíhají do kopce. |
| 1.4 | 7 | Zemní sráz | Zemní sráz | – | `pdn_1_4` (nový) | zemni_sraz |  |
| 1.5 | 7 | Lom | Lom | – | `pdn_1_5` (nový) | – | **nový** ⛏️ Lom je místo, kde lidé vytěžili kámen, písek nebo štěrk. Má strmé stěny, jako by někdo ukousl kus kopce. |
| 1.6 | 7 | Zemní val | Zemní val | – | `n_val` (znovu) | val |  |
| 1.7 | 7 | Rýha | Rýha | – | `n_ryha` (znovu) | ryha |  |
| 1.8 | 7 | Malá rýha | Malá rýha | – | `pdn_1_8` (nový) | – | **nový** 🌧️ Malá rýha je úzká brázda vymletá vodou, většinou suchá. Je menší a mělčí než rýha. |
| 1.9 | 7 | Kupa | Kupa | – | `pdn_1_9` (nový) | kopec, doplnkova |  |
| 1.10 | 7 | Kupka | Kupka | – | `n_kupka` (znovu) | kupka, protahla_kupka |  |
| 1.11 | 7 | Sedlo | Sedlo | – | `pdn_1_11` (nový) | – | **nový** 🐴 Sedlo je nižší místo mezi dvěma kopci, jako sedlo mezi dvěma hrby. Na mapě stojí dvě kupy vrstevnic proti sobě. |
| 1.12 | 7 | Prohlubeň | Prohlubeň | – | `n_prohluben` (znovu) | – | **nový** 🥣 Prohlubeň je dolík, ze kterého jde terén odevšad jen nahoru. Na mapě ji kreslí uzavřená vrstevnice s čárkami dovnitř, malá prohlubeň má jen hnědou misku. |
| 1.13 | 7 | Malá prohlubeň | Malá prohlubeň | – | `pdn_1_13` (nový) | prohluben |  |
| 1.14 | 7 | Jáma | Jáma | – | `n_jama` (znovu) | jama, kamenna_jama |  |
| 1.15 | 7 | Rozbitý povrch | Rozbitý povrch | – | `n_rozbity` (znovu) | rozbity |  |
| 1.16 | 7 | Mraveniště (termitiště) | Mraveniště | termitiště | `pdn_1_16` (nový) | – | **nový** 🐜 Mraveniště je velký kopeček z jehličí a větviček, který postavili mravenci. Na mapě bývá jako hnědá tečka nebo trojúhelníček. |

### Skály a balvany (2.x, Ostrov skrýší)

| ISCD | Strana IOF | Oficiální název (ČSOS) | Mluvený název | Alt | Klip | Mapové značky hry | Výklad (jen nové) |
|---|---|---|---|---|---|---|---|
| 2.1 | 7 | (Skalní) sráz | Skalní sráz | sráz | `n_sraz` (znovu) | sraz, nepr_sraz |  |
| 2.2 | 8 | Skalní věž {obrovský balvan} | Skalní věž | obrovský balvan | `pdn_2_2` (nový) | obrovsky |  |
| 2.3 | 8 | Jeskyně | Jeskyně | – | `pdn_2_3` (nový) | – | **nový** 🦇 Jeskyně je díra ve skále nebo v úbočí kopce, může vést pod zem. Na mapě ji kreslí černé véčko, stejně jako kamennou jámu. |
| 2.4 | 8 | Balvan | Balvan | – | `n_balvan` (znovu) | balvan, velkybalvan |  |
| 2.5 | 8 | Balvanové pole | Balvanové pole | – | `n_balvanove_pole` (znovu) | balvanove_pole |  |
| 2.6 | 8 | Shluk balvanů | Shluk balvanů | – | `n_shluk` (znovu) | shluk |  |
| 2.7 | 8 | Kamenitý povrch | Kamenitý povrch | – | `n_kamenity` (znovu) | kamenity |  |
| 2.8 | 8 | Holá skála | Holá skála | – | `n_skala` (znovu) | skala |  |
| 2.9 | 8 | Úzký {skalní} průchod | Úzký průchod | úzký skalní průchod | `pdn_2_9` (nový) | – | **nový** 🚶 Úzký průchod je štěrbina mezi dvěma skalami, které stojí proti sobě. Na mapě ho poznáš podle dvou černých srázů vedle sebe. |
| 2.10 | 8 | Příkop | Příkop | – | `pdn_2_10` (nový) | – | **nový** 🕳️ Příkop je úzký zářez ve skále nebo v zemi, často ho vykopali lidé. Je hluboký aspoň metr, takže ho nepřehlédneš. |

### Voda a bažiny (3.x, Ostrov hádanek)

| ISCD | Strana IOF | Oficiální název (ČSOS) | Mluvený název | Alt | Klip | Mapové značky hry | Výklad (jen nové) |
|---|---|---|---|---|---|---|---|
| 3.1 | 8 | Jezero | Jezero | – | `pdn_3_1` (nový) | voda |  |
| 3.2 | 8 | Rybníček | Rybníček | – | `pdn_3_2` (nový) | melka_voda |  |
| 3.3 | 8 | Jáma s vodou | Jáma s vodou | – | `n_jama_s_vodou` (znovu) | jama_s_vodou |  |
| 3.4 | 8 | Řeka, potok | Potok | řeka | `n_potok` (znovu) | potok |  |
| 3.5 | 8 | Malý vodní příkop {meliorační rýha} | Malý vodní příkop | meliorační rýha | `pdn_3_5` (nový) | prikop |  |
| 3.6 | 8 | Úzká bažina | Úzká bažina | – | `n_uzka_bazina` (znovu) | uzka_bazina |  |
| 3.7 | 9 | Bažina | Bažina | – | `n_bazina` (znovu) | bazina, nezretelna_bazina |  |
| 3.8 | 9 | Pevná půda v bažině | Pevná půda v bažině | – | `pdn_3_8` (nový) | – | **nový** 🏝️ Pevná půda v bažině je suchý ostrůvek uprostřed mokřiny, nebo pevný pás mezi dvěma bažinami. Tudy se dá bažinou projít a nezapadneš. |
| 3.9 | 9 | Studna | Studna | – | `n_studna` (znovu) | studna |  |
| 3.10 | 9 | Pramen | Pramen | – | `n_pramen` (znovu) | pramen |  |
| 3.11 | 9 | Vodní nádrž, vodní žlab | Vodní nádrž | vodní žlab | `pdn_3_11` (nový) | – | **nový** 🚰 Vodní nádrž je kamenná nebo betonová nádoba na vodu, kterou postavili lidé. Může to být i žlab, ze kterého pijí zvířata. |

### Vegetace (4.x, Ostrov hádanek)

| ISCD | Strana IOF | Oficiální název (ČSOS) | Mluvený název | Alt | Klip | Mapové značky hry | Výklad (jen nové) |
|---|---|---|---|---|---|---|---|
| 4.1 | 9 | Otevřený prostor | Otevřený prostor | – | `pdn_4_1` (nový) | louka, pole, sad, vinice |  |
| 4.2 | 9 | Polootevřený prostor | Polootevřený prostor | – | `pdn_4_2` (nový) | roztrousene, divoky |  |
| 4.3 | 9 | Roh lesa | Roh lesa | – | `pdn_4_3` (nový) | les |  |
| 4.4 | 9 | Světlina | Světlina | – | `pdn_4_4` (nový) | – | **nový** ☀️ Světlina je malá louka uprostřed lesa, kde nerostou stromy. Poznáš ji tak, že je tam světlo a dobře se tam vidí. |
| 4.5 | 9 | Hustník | Hustník | – | `n_housti` (znovu) | housti, zelena_svetla, zelena_stredni, podrost |  |
| 4.6 | 9 | Úzký hustník, živý plot | Úzký hustník | živý plot | `pdn_4_6` (nový) | – | **nový** 🌿 Úzký hustník je řada keřů nebo stromů, kterou někdo vysázel a nejde přes ni snadno projít. Často je to živý plot. |
| 4.7 | 9 | Hranice vegetace | Hranice vegetace | – | `pdn_4_7` (nový) | hranice_veg |  |
| 4.8 | 10 | Skupina stromů | Skupina stromů | – | `pdn_4_8` (nový) | – | **nový** 🌳 Skupina stromů je malá skupinka stromů uprostřed otevřeného místa, třeba na louce. Může to být i průchodnější kousek lesa mezi hustším porostem. |
| 4.9 | 10 | Výrazný strom | Výrazný strom | – | `pdn_4_9` (nový) | strom, ker |  |
| 4.10 | 10 | Vývrat, pařez | Vývrat | pařez | `n_veg_x` (znovu) | veg_x |  |

### Umělé objekty (5.x, Ostrov pirátských staveb)

| ISCD | Strana IOF | Oficiální název (ČSOS) | Mluvený název | Alt | Klip | Mapové značky hry | Výklad (jen nové) |
|---|---|---|---|---|---|---|---|
| 5.1 | 10 | Silnice | Silnice | – | `n_silnice` (znovu) | silnice, sirokasilnice |  |
| 5.2 | 10 | Cesta, pěšina | Cesta | pěšina | `pdn_5_2` (nový) | vozovka, cesta, pesina |  |
| 5.3 | 10 | Průsek | Průsek | – | `n_prusek` (znovu) | prusek |  |
| 5.4 | 10 | Most | Most | – | `n_most` (znovu) | most |  |
| 5.5 | 10 | Elektrické vedení | Elektrické vedení | – | `n_vedeni` (znovu) | vedeni |  |
| 5.6 | 10 | Sloup elektrického vedení | Sloup elektrického vedení | – | `pdn_5_6` (nový) | – | **nový** ⚡ Sloup drží dráty elektrického nebo telefonního vedení, někdy i lanovku. Dráty už znáš a kontrola může být na jednom ze sloupů. |
| 5.7 | 10 | Tunel | Tunel | – | `pdn_5_7` (nový) | – | **nový** 🚇 Tunel je podchod pod silnicí nebo pod železnicí. Dá se jím projít na druhou stranu. |
| 5.8 | 10 | Zeď | Zeď | – | `n_zed` (znovu) | zed, nepr_zed |  |
| 5.9 | 10 | Plot | Plot | – | `n_plot` (znovu) | plot, nepr_plot |  |
| 5.10 | 11 | Průchod | Průchod | – | `n_pruchod` (znovu) | pruchod_plot |  |
| 5.11 | 11 | Budova | Budova | – | `n_budova` (znovu) | budova |  |
| 5.12 | 11 | Zpevněná plocha | Zpevněná plocha | – | `pdn_5_12` (nový) | zpevnena |  |
| 5.13 | 11 | Zřícenina | Zřícenina | – | `n_zricenina` (znovu) | zricenina |  |
| 5.14 | 11 | Potrubí, bobová dráha | Potrubí | bobová dráha | `n_potrubi` (znovu) | potrubi, nepr_potrubi |  |
| 5.15 | 11 | Věž, stožár | Věž | stožár | `pdn_5_15` (nový) | veza |  |
| 5.16 | 11 | Posed | Posed | – | `n_posed` (znovu) | posed |  |
| 5.17 | 11 | Hraniční kámen, mohyla | Hraniční kámen | mohyla | `n_mohyla` (znovu) | mohyla |  |
| 5.18 | 11 | Krmelec | Krmelec | – | `n_krmelec` (znovu) | krmelec |  |
| 5.19 | 11 | Milíř, plošinka | Milíř | plošinka | `pdn_5_19` (nový) | teren_objekt |  |
| 5.20 | 11 | Pomník, socha | Pomník | socha | `pdn_5_20` (nový) | – | **nový** 🗽 Pomník je památník nebo socha, kterou lidé postavili na památku. Mívá kamenný podstavec. |
| 5.21 | 11 | Zastřešení | Zastřešení | – | `pdn_5_21` (nový) | zastreseni |  |
| 5.22 | 11 | Schodiště | Schodiště | – | `pdn_5_22` (nový) | schody |  |
| 5.23 | 11 | Oblast se zákazem vstupu | Oblast se zákazem vstupu | – | `pdn_5_23` (nový) | zakaz |  |
| 5.24 | 11 | Železnice | Železnice | – | `n_zeleznice` (znovu) | zeleznice |  |

### Zvláštní objekty (6.x, Ostrov pirátských staveb)

| ISCD | Strana IOF | Oficiální název (ČSOS) | Mluvený název | Alt | Klip | Mapové značky hry | Výklad (jen nové) |
|---|---|---|---|---|---|---|---|
| 6.1 | 12 | Výrazný objekt / Zvláštní objekt | Zvláštní objekt – křížek | výrazný objekt | `n_krizek` (znovu) | vodni_objekt, krizek |  |
| 6.2 | 12 | Výrazný objekt / Zvláštní objekt | Zvláštní objekt – kroužek | výrazný objekt | `n_krouzek` (znovu) | krouzek |  |

## K rozhodnutí a ověření

- Dvojité názvy: mluví se první tvar (např. „Potok“, „Věž“, „Pomník“), druhý je v `alt` a lze ho přidat do výkladu. Piktogramy 6.1 a 6.2 mají v ČSOS stejný název „Výrazný objekt / Zvláštní objekt“. Aby se daly rozlišit, mluví se „Zvláštní objekt – křížek“ a „– kroužek“ (stejně jako mapové značky 531 a 530).
- Piktogram 1.12 se jmenuje „Prohlubeň“, tedy stejně jako mapová značka 111 (ISOM „Malá prohlubeň“, piktogram 1.13) ve hře. Znovupoužije se proto klip `n_prohluben`. Doporučuji přejmenovat mapovou značku ve hře na „Malá prohlubeň“ (název podle ISOM i ISCD), je to ale změna stávajícího klipu.
- Mapová značka „Mez (zemní sráz)“ se mluví „Mez“, piktogram 1.4 se mluví „Zemní sráz“ (název z ČSOS), proto má nový klip.
- Piktogram 4.4 Světlina nebyl v zadání, hra ho ale nemá, patří k vegetaci a je na Ostrově hádanek (nových je tedy 19, ne 18).
- Věcně nejméně jisté výklady: 1.8 Malá rýha, 2.10 Příkop, 1.16 Mraveniště, 5.6 Sloup (opírám se o text ISOM a ISCD; „aspoň metr hluboký“ u příkopu je z ISOM 215).
- Kresby „jak to vypadá na mapě“ (`ill`) jsou schematické, ne měřítkové. Hřbítek a údolíčko jsou záměrně zrcadlové (U špičkou dolů a nahoru).
