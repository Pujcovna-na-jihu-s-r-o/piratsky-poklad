# -*- coding: utf-8 -*-
"""Generuje datový blok hry (SY, ISLANDS, CONCEPTS) podle ISOM 2017-2 a vloží ho do HTML."""
import io, json, re

import os
HTML = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hra-piratsky-poklad.html")

# Barvy ISOM 2017-2 (PMS → sRGB, procenta = rastr na bílé)
C = dict(
    bk="#000000", br="#D15C00", br50="#E8AE80", bl="#00A3E0", bl50="#80D1F0",
    ye="#FFBA37", ye50="#FFDD9B", gr="#1A9E3B", gr30="#BAE2C4", gr60="#76C589",
    gy="#B4B4B4", ol="#9DA02E", pu="#BB29BB", wh="#FFFFFF", wstroke="#CFD8DC",
)

def area(fill, stroke=None, sw=3):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="12" y="22" width="76" height="56" rx="14" fill="{fill}"{s}/>'

def dots(color, pts, r):
    return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>' for x, y in pts)

def grid(x0, y0, x1, y1, sx, sy, off=0):
    out = []; row = 0
    y = y0
    while y <= y1:
        x = x0 + (sx / 2 if (row % 2 and off) else 0)
        while x <= x1:
            out.append((x, y)); x += sx
        y += sy; row += 1
    return out

def tags(color, y, x0, x1, step, length, w, double=False, up=False):
    out = []
    x = x0
    while x <= x1:
        y2 = y - length if up else y + length
        out.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y2}" stroke="{color}" stroke-width="{w}"/>')
        if double:
            out.append(f'<line x1="{x+4}" y1="{y}" x2="{x+4}" y2="{y2}" stroke="{color}" stroke-width="{w}"/>')
        x += step
    return "".join(out)

bk, br, bl, ye, gr, pu, gy, ol, wh = C["bk"], C["br"], C["bl"], C["ye"], C["gr"], C["pu"], C["gy"], C["ol"], C["wh"]

# ---------- ZNAČKY ----------
# Každá: id (stálý), name (dětské/krátké), isom (číslo + oficiální název), emoji, col (barevná rodina), say,
#        svg (karta 100×100); plošné: fill (+deco přes výplň); liniové: tile (přes celý dílek mapy); base=True = podklad mapy
S = []
def add(**k): S.append(k)

# --- VODA A BAŽINY (modrá) ---
add(id="voda", name="Voda", isom="301 Nepřekonatelné vodní těleso", emoji="💧", col="blue", fill=bl, base=False,
    say="Modrá plocha s černým okrajem je voda, rybník nebo jezero. Vodu nepřeběhneš, musíš ji oběhnout. Pomůcka: modrá jako vodička, osvěží tě trošička!", cheer="Vodu snadno oběhneš a vesele běžíš dál k další kontrole!",
    svg=area(bl, bk, 3), deco=f'<rect x="1.5" y="1.5" width="97" height="97" fill="none" stroke="{bk}" stroke-width="3"/>')
add(id="melka_voda", name="Mělká voda", isom="302 Mělké vodní těleso", emoji="🏖️", col="blue", fill=C["bl50"],
    say="Světle modrá plocha je mělká voda, třeba brod nebo mělká tůň. Dá se přebrodit, ale namočíš se. Pomůcka: světlejší modrá, mělčí voda!",
    svg=area(C["bl50"], bl, 3), deco=f'<rect x="1.5" y="1.5" width="97" height="97" fill="none" stroke="{bl}" stroke-width="3"/>')
add(id="potok", name="Potok", isom="304 Překonatelný vodní tok", emoji="🏞️", col="blue",
    say="Modrá čára je potok nebo říčka. Dá se přeskočit nebo přebrodit. Pomůcka: modrá čára teče jako potok!",
    svg=f'<path d="M14 30 C 34 66, 60 34, 86 70" stroke="{bl}" stroke-width="4.5" fill="none" stroke-linecap="round"/>',
    tile=f'<path d="M0 30 C 30 75, 65 25, 100 70" stroke="{bl}" stroke-width="4.5" fill="none"/>')
add(id="prikop", name="Vodní příkop", isom="306 Malý / občasný vodní příkop", emoji="💦", col="blue",
    say="Modrá přerušovaná čára je malý vodní příkop, někdy i vyschlý. Pomůcka: přerušovaná modrá, voda jen někdy!",
    svg=f'<path d="M14 40 C 34 70, 60 30, 86 64" stroke="{bl}" stroke-width="3.5" fill="none" stroke-dasharray="10 6" stroke-linecap="round"/>',
    tile=f'<path d="M0 40 C 30 75, 65 25, 100 64" stroke="{bl}" stroke-width="3.5" fill="none" stroke-dasharray="10 6"/>')
add(id="bazina", name="Bažina", isom="308 Bažina", emoji="🐸", col="blue",
    say="Modré vodorovné čárky jsou mokrá bažina, plná vody a bláta. Pomůcka: modré čárky vedle sebe, bláto v botě studí, zebe!", cheer="Opatrně bažinku oběhni a botky zůstanou suché!",
    svg="".join(f'<line x1="22" y1="{y}" x2="78" y2="{y}" stroke="{bl}" stroke-width="3.5" stroke-linecap="round"/>' for y in (34, 42, 50, 58, 66)),
    tile="".join(f'<line x1="0" y1="{y}" x2="100" y2="{y}" stroke="{bl}" stroke-width="3"/>' for y in range(6, 100, 10)))
add(id="nezretelna_bazina", name="Nezřetelná bažina", isom="310 Nezřetelná bažina", emoji="🌫️", col="blue",
    say="Modré přerušované čárky jsou nezřetelná bažina. Někdy je mokrá, někdy suchá. Pomůcka: přerušované čárky, bažina jen občas!",
    svg="".join(f'<line x1="22" y1="{y}" x2="78" y2="{y}" stroke="{bl}" stroke-width="3.5" stroke-dasharray="9 6" stroke-linecap="round"/>' for y in (34, 42, 50, 58, 66)),
    tile="".join(f'<line x1="{2 if i%2 else 8}" y1="{y}" x2="100" y2="{y}" stroke="{bl}" stroke-width="3" stroke-dasharray="9 6"/>' for i, y in enumerate(range(6, 100, 10))))
add(id="uzka_bazina", name="Úzká bažina", isom="309 Úzká bažina", emoji="〰️", col="blue",
    say="Modrá tečkovaná čára je úzká bažina, mokrý pruh v lese. Pomůcka: modré tečky v řadě, mokrá cestička!",
    svg=f'<path d="M14 50 C 40 28, 60 72, 86 50" stroke="{bl}" stroke-width="4.5" fill="none" stroke-dasharray="0.5 8" stroke-linecap="round"/>',
    tile=f'<path d="M0 50 C 35 20, 65 80, 100 50" stroke="{bl}" stroke-width="4.5" fill="none" stroke-dasharray="0.5 8" stroke-linecap="round"/>')
add(id="jama_s_vodou", name="Jáma s vodou", isom="303 Jáma s vodou", emoji="🕳️", col="blue",
    say="Modré véčko je malá jáma plná vody. Pomůcka: modré V jako vana!",
    svg=f'<path d="M36 34 L50 66 L64 34" stroke="{bl}" stroke-width="5" fill="none" stroke-linejoin="round" stroke-linecap="round"/>')
add(id="studna", name="Studna", isom="311 Studna, fontána nebo vodní nádrž", emoji="🪣", col="blue",
    say="Modrý čtvereček je studna, fontána nebo nádrž na vodu. Pomůcka: modrý čtvereček, studánka v kamenném rámečku!",
    svg=f'<rect x="37" y="37" width="26" height="26" fill="none" stroke="{bl}" stroke-width="4.5"/>')
add(id="pramen", name="Pramen", isom="312 Pramen", emoji="⛲", col="blue",
    say="Modrý háček je pramen, tam voda vytéká ze země. Pomůcka: háček ukazuje, kudy voda odtéká!",
    svg=f'<path d="M40 38 a11 11 0 1 1 11 11 v20" stroke="{bl}" stroke-width="5" fill="none" stroke-linecap="round"/>')
add(id="vodni_objekt", name="Zvláštní vodní objekt", isom="313 Výrazný vodní objekt", emoji="✳️", col="blue",
    say="Modrá hvězdička je zvláštní vodní věc, kterou mapa vysvětlí v legendě, třeba napajedlo. Pomůcka: modrá hvězdička, něco s vodou!",
    svg=f'<g stroke="{bl}" stroke-width="4.5" stroke-linecap="round"><line x1="50" y1="30" x2="50" y2="70"/><line x1="33" y1="40" x2="67" y2="60"/><line x1="33" y1="60" x2="67" y2="40"/></g>')

# --- VEGETACE (žlutá, zelená, bílá) ---
add(id="louka", name="Louka", isom="401 Otevřený prostor", emoji="🌼", col="yellow", fill=ye, base=True,
    say="Žlutá je otevřená louka nebo pole bez stromů, kde se běží lehce a daleko vidíš. Pomůcka: žlutá jako sluníčko, usmívej se maličko!", cheer="Na louce natáhni nožky a leť rychle jako vítr!",
    svg=area(ye))
add(id="roztrousene", name="Louka se stromy", isom="402 Otevřený prostor s rozptýlenými stromy", emoji="🌳", col="yellow", fill=ye,
    say="Žlutá s bílými puntíky je louka, kde tu a tam roste strom. Pomůcka: bílé puntíky jsou stromy na louce!",
    svg=area(ye) + dots(wh, grid(28, 34, 74, 68, 15, 16, 1), 4.5),
    deco=dots(wh, grid(10, 10, 92, 92, 22, 22, 1), 5.5))
add(id="divoky", name="Paseka", isom="403 Divoký otevřený prostor", emoji="🌾", col="yellow", fill=C["ye50"],
    say="Světle žlutá je paseka nebo zarostlá louka s vysokou trávou. Běží se pomaleji než po louce. Pomůcka: bledší žlutá, vyšší tráva!",
    svg=area(C["ye50"]))
add(id="pole", name="Pole", isom="412 Obdělávaná půda", emoji="🚜", col="yellow", fill=ye,
    say="Žlutá s černými tečkami je oraná půda, pole. Na pole se často nesmí, hlídej pokyny. Pomůcka: černé tečky jsou zrníčka na poli!",
    svg=area(ye) + dots(bk, grid(24, 32, 78, 70, 9, 9, 1), 1.8),
    deco=dots(bk, grid(5, 5, 97, 97, 12, 12, 1), 2))
add(id="sad", name="Sad", isom="413 Sad", emoji="🍎", col="yellow", fill=ye,
    say="Žlutá se zelenými tečkami v řádcích je ovocný sad. Stromy tu rostou pěkně v řadách. Pomůcka: zelené tečky v řadě, jabloně v sadě!",
    svg=area(ye) + dots(gr, grid(26, 33, 76, 68, 12.5, 11.5), 3.2),
    deco=dots(gr, grid(8, 8, 94, 94, 17, 17), 3.6))
add(id="vinice", name="Vinice", isom="414 Vinice", emoji="🍇", col="yellow", fill=ye,
    say="Žlutá se zelenými čárkami v řádcích je vinice. Pomůcka: zelené čárky jsou řady vína!",
    svg=area(ye) + "".join(f'<line x1="{x}" y1="{y-5}" x2="{x}" y2="{y+5}" stroke="{gr}" stroke-width="3"/>' for x, y in grid(26, 34, 76, 68, 12.5, 15)),
    deco="".join(f'<line x1="{x}" y1="{y-6}" x2="{x}" y2="{y+6}" stroke="{gr}" stroke-width="3"/>' for x, y in grid(8, 10, 94, 92, 17, 20)))
add(id="les", name="Běhací les", isom="405 Les", emoji="🌲", col="white", fill=wh, base=True,
    say="Bílá je přehledný les, kterým se dá volně a rychle běhat. Na orienťácké mapě je les bílý, ne zelený! Pomůcka: bílá barva v lese svítí, žádné větve tě nechytí!", cheer="Lesem bez překážek se ti poběží úplně lehce!",
    svg=area(wh, C["wstroke"], 3))
add(id="zelena_svetla", name="Řídké křoví", isom="406 Vegetace, pomalý běh", emoji="🌿", col="green", fill=C["gr30"],
    say="Světle zelená je řidší porost, kde se běží pomaleji. Pomůcka: světle zelená trochu brzdí!",
    svg=area(C["gr30"]))
add(id="zelena_stredni", name="Hustší křoví", isom="408 Vegetace, chůze", emoji="🌳", col="green", fill=C["gr60"],
    say="Středně zelená je hustý porost, kde už jen jdeš. Pomůcka: čím tmavší zelená, tím hůř se běží!",
    svg=area(C["gr60"]))
add(id="housti", name="Hustník", isom="410 Vegetace, prodírání", emoji="🌲", col="green", fill=gr,
    say="Tmavě zelená je hustník, husté křoví, kterým se musíš prodírat. Radši ho oběhni. Pomůcka: zelená jako stromeček, zpomalí tvůj krokáček!", cheer="Nevadí, když tě houští zbrzdí, chytře ho oběhni po cestičce!",
    svg=area(gr))
add(id="podrost", name="Podrost", isom="407 Vegetace, pomalý běh, dobrá viditelnost", emoji="🌱", col="green",
    say="Zelené svislé pruhy jsou podrost, třeba ostružiní nebo vysoké kapradí. Vidíš daleko, ale běží se pomalu. Pomůcka: zelené pruhy jako stébla!",
    svg="".join(f'<line x1="{x}" y1="30" x2="{x}" y2="70" stroke="{gr}" stroke-width="3.5"/>' for x in range(28, 76, 11)),
    tile="".join(f'<line x1="{x}" y1="0" x2="{x}" y2="100" stroke="{gr}" stroke-width="3.5"/>' for x in range(6, 100, 12)))
add(id="strom", name="Velký strom", isom="417 Výrazný velký strom", emoji="🌳", col="green",
    say="Zelený kroužek je jeden výrazný velký strom. Pomůcka: kroužek jako koruna stromu!",
    svg=f'<circle cx="50" cy="50" r="13" fill="none" stroke="{gr}" stroke-width="5"/>')
add(id="ker", name="Keř", isom="418 Výrazný keř nebo strom", emoji="🌵", col="green",
    say="Malá zelená tečka s bílým středem je výrazný keř nebo menší strom. Pomůcka: tečka je keřík, kroužek velký strom!",
    svg=f'<circle cx="50" cy="50" r="8" fill="{gr}"/><circle cx="50" cy="50" r="2.8" fill="{wh}"/>')
add(id="veg_x", name="Vývrat", isom="419 Výrazný vegetační objekt", emoji="🪵", col="green",
    say="Zelený křížek je zvláštní věc z rostlin, nejčastěji vyvrácený strom, vývrat. Pomůcka: zelený křížek, strom leží!",
    svg=f'<g stroke="{gr}" stroke-width="5.5" stroke-linecap="round"><line x1="35" y1="35" x2="65" y2="65"/><line x1="65" y1="35" x2="35" y2="65"/></g>')
add(id="hranice_veg", name="Hranice porostu", isom="416 Zřetelná hranice vegetace", emoji="🧵", col="black",
    say="Černá tečkovaná čára je hranice porostu, třeba kde končí vysoký les a začíná mladý. Pomůcka: tečky jako šev mezi lesy!",
    svg=f'<path d="M14 66 C 34 30, 66 70, 86 34" stroke="{bk}" stroke-width="3.5" fill="none" stroke-dasharray="0.5 7" stroke-linecap="round"/>',
    tile=f'<path d="M0 66 C 35 30, 65 70, 100 34" stroke="{bk}" stroke-width="3.5" fill="none" stroke-dasharray="0.5 7" stroke-linecap="round"/>')

# --- TERÉNNÍ TVARY (hnědá) ---
add(id="kopec", name="Vrstevnice", isom="101 Základní vrstevnice", emoji="⛰️", col="brown",
    say="Hnědé čáry jsou vrstevnice, ukazují kopečky a jak je svah strmý. Čím blíž jsou u sebe, tím víc se zadýcháš. Pomůcka: hnědá jako čokoláda, kopečky má každý rád!", cheer="Každý kopec hravě vyšlápneš a nahoře budeš mít přehled!",
    svg=f'<g fill="none" stroke="{br}" stroke-width="3.5"><ellipse cx="50" cy="56" rx="34" ry="19"/><ellipse cx="50" cy="52" rx="22" ry="12"/><ellipse cx="50" cy="48" rx="10" ry="5.5"/></g>',
    tile=f'<g fill="none" stroke="{br}" stroke-width="3.2"><path d="M0 28 C 30 10, 70 46, 100 24"/><path d="M0 58 C 30 40, 70 76, 100 54"/><path d="M0 88 C 30 70, 70 100, 100 84"/></g>')
add(id="doplnkova", name="Pomocná vrstevnice", isom="103 Doplňková vrstevnice", emoji="〽️", col="brown",
    say="Hnědá přerušovaná čára je pomocná vrstevnice. Ukazuje malý kopeček nebo dolík mezi velkými vrstevnicemi. Pomůcka: přerušovaná hnědá, jen maličký hrbolek!",
    svg=f'<path d="M14 62 C 34 30, 66 70, 86 38" stroke="{br}" stroke-width="3.2" fill="none" stroke-dasharray="10 6" stroke-linecap="round"/>',
    tile=f'<path d="M0 62 C 35 30, 65 70, 100 38" stroke="{br}" stroke-width="3.2" fill="none" stroke-dasharray="10 6"/>')
add(id="kupka", name="Kupka", isom="109 Malá kupka", emoji="🐜", col="brown",
    say="Hnědá tečka je malá kupka, kopeček tak vysoký jako ty. Pomůcka: hnědá tečka, mraveniště nebo hromádka!",
    svg=f'<circle cx="50" cy="50" r="8" fill="{br}"/>')
add(id="protahla_kupka", name="Protáhlá kupka", isom="110 Malá protáhlá kupka", emoji="🥖", col="brown",
    say="Hnědá protáhlá tečka je podlouhlá kupka, jako veka ležící na zemi. Pomůcka: protáhlá tečka, protáhlý kopeček!",
    svg=f'<ellipse cx="50" cy="50" rx="14" ry="6.5" fill="{br}"/>')
add(id="prohluben", name="Prohlubeň", isom="111 Malá prohlubeň", emoji="🥣", col="brown",
    say="Hnědá miska, půlkroužek otevřený nahoru, je malá prohlubeň, mělký dolík. Pomůcka: hnědá miska, dolík jako mistička!",
    svg=f'<path d="M34 42 a16 16 0 0 0 32 0" stroke="{br}" stroke-width="5" fill="none" stroke-linecap="round"/>')
add(id="jama", name="Jáma", isom="112 Jáma", emoji="🕳️", col="brown",
    say="Hnědé véčko je jáma se strmými stěnami. Pomůcka: hnědé V jako hluboká díra!",
    svg=f'<path d="M36 34 L50 66 L64 34" stroke="{br}" stroke-width="5" fill="none" stroke-linejoin="round" stroke-linecap="round"/>')
add(id="teren_objekt", name="Zvláštní terénní objekt", isom="115 Výrazný terénní objekt", emoji="🔺", col="brown",
    say="Malý hnědý trojúhelníček je zvláštní terénní tvar, mapa ho vysvětlí v legendě. Pomůcka: hnědý trojúhelníček, něco z hlíny!",
    svg=f'<path d="M50 34 L64 62 L36 62 Z" fill="{br}"/>')
add(id="rozbity", name="Rozbitý povrch", isom="113 Rozbitý povrch", emoji="🟤", col="brown",
    say="Rozházené hnědé tečky jsou rozbitý povrch, samé hrboly a dolíky. Pomůcka: hnědé tečky, hrbolatá zem!",
    svg=dots(br, [(28, 36), (44, 30), (60, 38), (76, 32), (34, 52), (52, 50), (70, 56), (26, 66), (44, 68), (62, 64), (78, 70)], 2.6),
    tile=dots(br, [(10, 12), (28, 6), (48, 14), (70, 8), (90, 16), (18, 30), (40, 34), (62, 28), (84, 36), (8, 52), (30, 56), (52, 50), (74, 58), (94, 52), (14, 74), (36, 78), (58, 72), (80, 80), (24, 94), (48, 92), (70, 96), (92, 94)], 2.8))
add(id="zemni_sraz", name="Mez (zemní sráz)", isom="104 Zemní sráz", emoji="🪜", col="brown",
    say="Hnědá čára s čárkami dolů je mez, zemní sráz: strmý schod z hlíny v lese, násep u silnice nebo strmá strana hráze. Čárky ukazují, kam to padá dolů. Pomůcka: hnědý hřeben, hlína padá dolů!",
    svg=f'<line x1="18" y1="42" x2="82" y2="42" stroke="{br}" stroke-width="3.5"/>' + tags(br, 42, 24, 78, 12, 13, 2.5),
    tile=f'<line x1="0" y1="40" x2="100" y2="40" stroke="{br}" stroke-width="3.5"/>' + tags(br, 40, 6, 98, 12, 14, 2.5))
add(id="ryha", name="Rýha", isom="107 Erozní rýha", emoji="🪓", col="brown",
    say="Tlustá hnědá čára je erozní rýha, hluboký zářez vymletý vodou. Pomůcka: tlustá hnědá, voda vyryla rýhu!",
    svg=f'<path d="M18 70 C 40 40, 60 60, 82 30" stroke="{br}" stroke-width="6" fill="none" stroke-linecap="round"/>',
    tile=f'<path d="M0 74 C 35 40, 65 60, 100 26" stroke="{br}" stroke-width="6" fill="none"/>')
add(id="val", name="Zemní val", isom="105 Zemní val", emoji="🧱", col="brown",
    say="Hnědá čára s tečkami je zemní val, dlouhý násep z hlíny, třeba hráz rybníka. Hráz nemá vlastní značku, kreslí se jako val nebo zemní sráz. Pomůcka: hnědá čára s korálky, val jako náhrdelník!",
    svg=f'<line x1="18" y1="50" x2="82" y2="50" stroke="{br}" stroke-width="3"/>' + dots(br, [(30, 50), (50, 50), (70, 50)], 4),
    tile=f'<line x1="0" y1="50" x2="100" y2="50" stroke="{br}" stroke-width="3"/>' + dots(br, [(12, 50), (36, 50), (62, 50), (88, 50)], 4))

# --- SKÁLY A KAMENY (černá, šedá) ---
add(id="balvan", name="Balvan", isom="204 Balvan", emoji="🪨", col="black",
    say="Černá tečka je balvan, velký kámen vyšší než ty. Pozor, trojúhelník je až celá hromada kamenů. Pomůcka: černá tečka v lese stojí, velký kámen nohám neublíží!", cheer="Balvan nepřehlédneš, je to báječný bod pro orientaci!",
    svg=f'<circle cx="50" cy="50" r="9" fill="{bk}"/>')
add(id="velkybalvan", name="Velký balvan", isom="205 Velký balvan", emoji="🗿", col="black",
    say="Větší černá tečka je velký balvan, vyšší než dospělý člověk. Pomůcka: větší tečka, větší kámen!",
    svg=f'<circle cx="50" cy="50" r="14" fill="{bk}"/>')
add(id="shluk", name="Shluk balvanů", isom="207 Shluk balvanů", emoji="🧱", col="black",
    say="Černý trojúhelník je shluk balvanů, hromada kamenů těsně u sebe. Pomůcka: trojúhelník jako hromada kamení!",
    svg=f'<path d="M50 28 L72 66 L28 66 Z" fill="{bk}"/>')
add(id="obrovsky", name="Obrovský balvan", isom="206 Obrovský balvan nebo skalní věž", emoji="🏔️", col="black",
    say="Černá plocha nakreslená podle skutečného tvaru je obrovský balvan nebo skalní věž. Pomůcka: černá skvrna, skála velká jako dům!",
    svg=f'<path d="M34 40 C 40 26, 62 28, 68 40 C 76 50, 70 66, 58 68 C 44 72, 30 62, 34 40 Z" fill="{bk}"/>')
add(id="balvanove_pole", name="Balvanové pole", isom="208 Balvanové pole", emoji="🧗", col="black",
    say="Rozházené malé černé trojúhelníčky jsou balvanové pole, spousta kamenů, po kterých se špatně běží. Pomůcka: malé trojúhelníčky, samé kameny!",
    svg="".join(f'<path d="M{x} {y-5} L{x+5} {y+4} L{x-5} {y+4} Z" fill="{bk}"/>' for x, y in [(30, 36), (52, 32), (72, 40), (40, 54), (62, 58), (28, 68), (50, 70), (74, 66)]),
    tile="".join(f'<path d="M{x} {y-5} L{x+5} {y+4} L{x-5} {y+4} Z" fill="{bk}"/>' for x, y in [(12, 12), (36, 8), (60, 16), (86, 10), (22, 34), (48, 38), (74, 32), (10, 56), (36, 60), (62, 54), (90, 58), (20, 82), (46, 86), (72, 80), (94, 88)]))
add(id="kamenity", name="Kamenitý povrch", isom="210 Kamenitý povrch, pomalý běh", emoji="🪨", col="black",
    say="Malé černé tečky rozházené po ploše jsou kamenitý povrch, samé menší kameny. Pomůcka: černé tečky, kamínky pod nohama!",
    svg=dots(bk, [(28, 34), (44, 30), (60, 36), (76, 32), (34, 48), (52, 46), (70, 52), (26, 62), (44, 66), (62, 62), (78, 68), (36, 76)], 2.2),
    tile=dots(bk, grid(8, 8, 94, 94, 14, 14, 1), 2.2))
add(id="skala", name="Holá skála", isom="214 Holá skála", emoji="🪨", col="grey", fill=gy,
    say="Šedá plocha je holá skála bez hlíny a stromů, skalní plotna. Pomůcka: šedá jako kámen!",
    svg=area(gy))
add(id="sraz", name="Skalní sráz", isom="202 Sráz", emoji="⛰️", col="black",
    say="Černá čára s čárkami je skalní sráz, který se dá slézt. Čárky ukazují dolů ze skály. Pomůcka: černý hřeben, skála se svažuje!",
    svg=f'<line x1="18" y1="42" x2="82" y2="42" stroke="{bk}" stroke-width="3"/>' + tags(bk, 42, 24, 78, 12, 12, 2.2),
    tile=f'<line x1="0" y1="40" x2="100" y2="40" stroke="{bk}" stroke-width="3"/>' + tags(bk, 40, 6, 98, 12, 13, 2.2))
add(id="nepr_sraz", name="Nepřekonatelný sráz", isom="201 Nepřekonatelný sráz", emoji="🧗", col="black",
    say="Tlustá černá čára s dlouhými čárkami je nepřekonatelný sráz, vysoká skalní stěna. Tam nelez, je to nebezpečné! Pomůcka: tlustá černá, skála stop!",
    svg=f'<line x1="18" y1="40" x2="82" y2="40" stroke="{bk}" stroke-width="6"/>' + tags(bk, 40, 24, 78, 12, 17, 2.8),
    tile=f'<line x1="0" y1="38" x2="100" y2="38" stroke="{bk}" stroke-width="6"/>' + tags(bk, 38, 6, 98, 12, 18, 2.8))
add(id="kamenna_jama", name="Kamenná jáma", isom="203 Kamenná jáma nebo jeskyně", emoji="🕳️", col="black",
    say="Černé véčko je kamenná jáma nebo jeskyně. Pomůcka: černé V, díra ve skále!",
    svg=f'<path d="M36 34 L50 66 L64 34" stroke="{bk}" stroke-width="5" fill="none" stroke-linejoin="round" stroke-linecap="round"/>')

add(id="pisek", name="Písek", isom="213 Písčitý povrch", emoji="🏖️", col="yellow", fill=C["ye50"],
    say="Světle žlutá s černými tečkami je písčitý povrch. V písku se běží ztěžka, nohy se boří. Pomůcka: tečky jako zrnka písku!",
    svg=area(C["ye50"]) + dots(bk, grid(24, 32, 78, 70, 9, 9, 1), 1.6),
    deco=dots(bk, grid(5, 5, 97, 97, 12, 12, 1), 1.8))

# --- KOMUNIKACE (černá, hnědá) ---
add(id="zpevnena", name="Asfalt", isom="501 Zpevněná plocha", emoji="🅿️", col="tan", fill=C["br50"],
    say="Světle hnědá plocha s černým okrajem je asfalt, beton nebo dlažba, třeba parkoviště nebo hřiště. Pomůcka: světle hnědá, tvrdá zem!",
    svg=area(C["br50"], bk, 2), deco=f'<rect x="1" y="1" width="98" height="98" fill="none" stroke="{bk}" stroke-width="2"/>')
add(id="sirokasilnice", name="Široká silnice", isom="502 Široká silnice", emoji="🛣️", col="black",
    say="Dvě černé čáry se světle hnědou uprostřed jsou široká silnice. Pozor na auta! Pomůcka: dvě čáry, mezi nimi jede auto!",
    svg=f'<path d="M14 62 C 34 40, 66 60, 86 38" stroke="{bk}" stroke-width="13" fill="none"/><path d="M14 62 C 34 40, 66 60, 86 38" stroke="{C["br50"]}" stroke-width="9" fill="none"/>',
    tile=f'<path d="M0 64 C 35 40, 65 60, 100 36" stroke="{bk}" stroke-width="14" fill="none"/><path d="M0 64 C 35 40, 65 60, 100 36" stroke="{C["br50"]}" stroke-width="10" fill="none"/>')
add(id="silnice", name="Silnice", isom="503 Silnice", emoji="🚗", col="black",
    say="Plná černá čára je silnice, po které jezdí auta. Pomůcka: plná černá čára, tvrdá cesta pro auta!",
    svg=f'<path d="M14 62 C 34 40, 66 60, 86 38" stroke="{bk}" stroke-width="6" fill="none" stroke-linecap="round"/>',
    tile=f'<path d="M0 64 C 35 40, 65 60, 100 36" stroke="{bk}" stroke-width="6" fill="none"/>')
add(id="vozovka", name="Vozová cesta", isom="504 Vozová cesta", emoji="🚜", col="black",
    say="Černá čára z dlouhých čárek je vozová cesta, širší lesní cesta pro traktor. Pomůcka: dlouhé čárky, traktor tudy projede!",
    svg=f'<path d="M14 66 C 34 34, 66 66, 86 32" stroke="{bk}" stroke-width="4.5" fill="none" stroke-dasharray="18 5"/>',
    tile=f'<path d="M0 68 C 35 32, 65 68, 100 30" stroke="{bk}" stroke-width="4.5" fill="none" stroke-dasharray="18 5"/>')
add(id="cesta", name="Pěší cesta", isom="505 Pěší cesta", emoji="🛤️", col="black",
    say="Černá přerušovaná čára je pěší cesta, po které se běží rychle a nezabloudíš. Pomůcka: po černé čáře jako po chodníčku, doběhneš tam za chviličku!", cheer="Držíš se cesty a bezpečně dorazíš až do cíle!",
    svg=f'<path d="M14 68 C 34 30, 66 70, 86 32" stroke="{bk}" stroke-width="4" fill="none" stroke-dasharray="12 6"/>',
    tile=f'<path d="M0 70 C 35 30, 65 70, 100 30" stroke="{bk}" stroke-width="4" fill="none" stroke-dasharray="12 6"/>')
add(id="pesina", name="Pěšina", isom="506 Pěšina", emoji="🥾", col="black",
    say="Tenká černá přerušovaná čára je pěšina, úzká stezka pro jednoho. Pomůcka: tenké čárky, úzká stezička!",
    svg=f'<path d="M14 68 C 34 30, 66 70, 86 32" stroke="{bk}" stroke-width="2.4" fill="none" stroke-dasharray="8 5"/>',
    tile=f'<path d="M0 70 C 35 30, 65 70, 100 30" stroke="{bk}" stroke-width="2.4" fill="none" stroke-dasharray="8 5"/>')
add(id="prusek", name="Průsek", isom="508 Průsek nebo liniová trasa terénem", emoji="🪚", col="black",
    say="Tenká černá čára z dlouhých čárek je průsek, rovný pruh vysekaný lesem, třeba pod dráty. Pomůcka: dlouhé tenké čárky, jako by někdo lesem prořízl pruh!",
    svg=f'<path d="M14 66 C 34 34, 66 66, 86 32" stroke="{bk}" stroke-width="2.2" fill="none" stroke-dasharray="16 5"/>',
    tile=f'<path d="M0 68 C 35 32, 65 68, 100 30" stroke="{bk}" stroke-width="2.2" fill="none" stroke-dasharray="16 5"/>')
add(id="zeleznice", name="Železnice", isom="509 Železnice", emoji="🚂", col="black",
    say="Tlustá černá čára s mezerami je železnice. Na koleje se nesmí! Pomůcka: tlustá čára s mezírkami, jedou po ní vagónky!",
    svg=f'<line x1="14" y1="50" x2="86" y2="50" stroke="{bk}" stroke-width="1.6"/><line x1="14" y1="50" x2="86" y2="50" stroke="{bk}" stroke-width="6" stroke-dasharray="14 5"/>',
    tile=f'<line x1="0" y1="50" x2="100" y2="50" stroke="{bk}" stroke-width="1.6"/><line x1="0" y1="50" x2="100" y2="50" stroke="{bk}" stroke-width="6" stroke-dasharray="14 5"/>')
add(id="vedeni", name="Elektrické vedení", isom="510 Elektrické vedení", emoji="⚡", col="black",
    say="Tenká černá čára s příčnými čárkami je elektrické vedení nebo lanovka. Dráty vedou vysoko nad hlavou. Pomůcka: čárky jako sloupy, drát mezi nimi!",
    svg=f'<line x1="14" y1="50" x2="86" y2="50" stroke="{bk}" stroke-width="2"/>' + "".join(f'<line x1="{x}" y1="40" x2="{x}" y2="60" stroke="{bk}" stroke-width="2.2"/>' for x in (28, 50, 72)),
    tile=f'<line x1="0" y1="50" x2="100" y2="50" stroke="{bk}" stroke-width="2"/>' + "".join(f'<line x1="{x}" y1="40" x2="{x}" y2="60" stroke="{bk}" stroke-width="2.2"/>' for x in (12, 37, 62, 87)))
add(id="most", name="Most", isom="512 Most / tunel", emoji="🌉", col="black",
    say="Cesta se dvěma závorkami je most, po kterém přejdeš potok nebo silnici. Pomůcka: závorky drží most!",
    svg=f'<line x1="18" y1="50" x2="82" y2="50" stroke="{bk}" stroke-width="4" stroke-dasharray="10 5"/><path d="M34 36 h-8 v28 h8 M66 36 h8 v28 h-8" stroke="{bk}" stroke-width="3" fill="none"/>',
    tile=f'<line x1="0" y1="50" x2="100" y2="50" stroke="{bk}" stroke-width="4" stroke-dasharray="10 5"/><path d="M36 36 h-8 v28 h8 M64 36 h8 v28 h-8" stroke="{bk}" stroke-width="3" fill="none"/>')
add(id="zed", name="Zeď", isom="513 Zeď", emoji="🧱", col="black",
    say="Černá čára s tečkami je kamenná zeď, přes kterou se dá přelézt. Pomůcka: tečky jsou kameny ve zdi!",
    svg=f'<line x1="18" y1="50" x2="82" y2="50" stroke="{bk}" stroke-width="2.5"/>' + dots(bk, [(30, 50), (50, 50), (70, 50)], 3.8),
    tile=f'<line x1="0" y1="50" x2="100" y2="50" stroke="{bk}" stroke-width="2.5"/>' + dots(bk, [(12, 50), (37, 50), (62, 50), (87, 50)], 3.8))
add(id="nepr_zed", name="Vysoká zeď", isom="515 Nepřekonatelná zeď", emoji="🏯", col="black",
    say="Tlustá černá čára s velkými tečkami je nepřekonatelná zeď. Přes ni nesmíš, hledej průchod. Pomůcka: tlustá zeď s velkými kameny, stop!",
    svg=f'<line x1="18" y1="50" x2="82" y2="50" stroke="{bk}" stroke-width="5"/>' + dots(bk, [(30, 50), (50, 50), (70, 50)], 5),
    tile=f'<line x1="0" y1="50" x2="100" y2="50" stroke="{bk}" stroke-width="5"/>' + dots(bk, [(12, 50), (37, 50), (62, 50), (87, 50)], 5))
add(id="plot", name="Plot", isom="516 Plot", emoji="🚧", col="black",
    say="Černá čára s krátkými čárkami na jedné straně je plot, který se dá přelézt. Pomůcka: čárky jako kolíky v plotě!",
    svg=f'<line x1="16" y1="52" x2="84" y2="52" stroke="{bk}" stroke-width="2.5"/>' + tags(bk, 52, 24, 78, 13.5, 10, 2.5, up=True),
    tile=f'<line x1="0" y1="52" x2="100" y2="52" stroke="{bk}" stroke-width="2.5"/>' + tags(bk, 52, 8, 96, 14.5, 11, 2.5, up=True))
add(id="nepr_plot", name="Vysoký plot", isom="518 Nepřekonatelný plot", emoji="⛔", col="black",
    say="Černá čára s dvojitými čárkami je nepřekonatelný plot. Přes něj se nesmí, musíš najít branku. Pomůcka: dvojité čárky, dvakrát stop!",
    svg=f'<line x1="16" y1="52" x2="84" y2="52" stroke="{bk}" stroke-width="3"/>' + tags(bk, 52, 22, 76, 16, 11, 2.5, double=True, up=True),
    tile=f'<line x1="0" y1="52" x2="100" y2="52" stroke="{bk}" stroke-width="3"/>' + tags(bk, 52, 8, 92, 17, 12, 2.5, double=True, up=True))

add(id="pruchod_plot", name="Průchod v plotu", isom="519 Průchod", emoji="🚪", col="black",
    say="Plot s mezerou a dvěma čárkami je průchod, branka nebo schůdky, kudy se přes plot nebo zeď smí. Pomůcka: mezera v plotě, tudy projdeš!",
    svg=f'<line x1="16" y1="52" x2="42" y2="52" stroke="{bk}" stroke-width="2.5"/><line x1="58" y1="52" x2="84" y2="52" stroke="{bk}" stroke-width="2.5"/>'
        + tags(bk, 52, 22, 36, 9, 10, 2.5, up=True) + tags(bk, 52, 64, 80, 9, 10, 2.5, up=True)
        + f'<line x1="42" y1="43" x2="42" y2="61" stroke="{bk}" stroke-width="3"/><line x1="58" y1="43" x2="58" y2="61" stroke="{bk}" stroke-width="3"/>',
    tile=f'<line x1="0" y1="52" x2="40" y2="52" stroke="{bk}" stroke-width="2.5"/><line x1="60" y1="52" x2="100" y2="52" stroke="{bk}" stroke-width="2.5"/>'
        + tags(bk, 52, 6, 34, 9.5, 11, 2.5, up=True) + tags(bk, 52, 66, 96, 9.5, 11, 2.5, up=True)
        + f'<line x1="40" y1="42" x2="40" y2="62" stroke="{bk}" stroke-width="3"/><line x1="60" y1="42" x2="60" y2="62" stroke="{bk}" stroke-width="3"/>')

# --- UMĚLÉ OBJEKTY (černá, olivová, šedá) ---
add(id="budova", name="Budova", isom="521 Budova", emoji="🏠", col="black",
    say="Černá plocha ve tvaru domu je budova, dům, chata nebo stavba. Pomůcka: černá kostka v mapě stojí, domeček se deště nebojí!", cheer="Podle budovy hned poznáš, kde přesně na mapě jsi!",
    svg=f'<path d="M28 34 h44 v18 h-18 v14 h-26 z" fill="{bk}"/>')
add(id="zakaz", name="Zakázaný prostor", isom="520 Oblast se zákazem vstupu", emoji="🚫", col="olive", fill=ol,
    say="Olivově zelená plocha je soukromý pozemek nebo zahrada, kam se nesmí. Pomůcka: olivová jako zavřená vrátka, tam nechoď!",
    svg=area(ol))
add(id="zricenina", name="Zřícenina", isom="523 Zřícenina", emoji="🏚️", col="black",
    say="Černý přerušovaný obrys je zřícenina, zbytky starého domu nebo hradu. Pomůcka: přerušované zdi, dům se rozpadl!",
    svg=f'<rect x="30" y="34" width="40" height="32" fill="none" stroke="{bk}" stroke-width="3.5" stroke-dasharray="7 5"/>')
add(id="zastreseni", name="Přístřešek", isom="522 Zastřešení", emoji="⛺", col="grey", fill="#D9D9D9",
    say="Světle šedá plocha s černým okrajem je přístřešek nebo zastřešení, střecha bez zdí, pod kterou proběhneš. Pomůcka: šedá střecha, pod ní sucho!",
    svg=area("#D9D9D9", bk, 2.5), deco=f'<rect x="1.5" y="1.5" width="97" height="97" fill="none" stroke="{bk}" stroke-width="2.5"/>')
add(id="veza", name="Vysoká věž", isom="524 Vysoká věž", emoji="🗼", col="black",
    say="Černá čtyřcípá hvězda je vysoká věž nebo velký sloup, který kouká nad les. Pomůcka: hvězda ční do výšky jako věž!",
    svg=f'<path d="M50 22 L56 44 L78 50 L56 56 L50 78 L44 56 L22 50 L44 44 Z" fill="{bk}"/>')
add(id="posed", name="Posed", isom="525 Malá věž (posed)", emoji="🪑", col="black",
    say="Černé T je posed, malá věž pro myslivce. Pomůcka: T jako trůn pro myslivce!",
    svg=f'<rect x="28" y="30" width="44" height="6.5" fill="{bk}"/><rect x="46.5" y="30" width="7" height="42" fill="{bk}"/>')
add(id="schody", name="Schody", isom="532 Schodiště", emoji="🪜", col="black",
    say="Černý žebříček je schodiště venku v terénu. Pomůcka: příčky jako schody!",
    svg=f'<g stroke="{bk}" stroke-width="3"><line x1="40" y1="24" x2="40" y2="76"/><line x1="60" y1="24" x2="60" y2="76"/>' + "".join(f'<line x1="40" y1="{y}" x2="60" y2="{y}"/>' for y in range(28, 76, 8)) + '</g>')
add(id="mohyla", name="Hraniční kámen", isom="526 Mohyla (hraniční kámen)", emoji="🪦", col="black",
    say="Černý kroužek s tečkou uprostřed je hraniční kámen, pomníček nebo mohyla. Pomůcka: tečka v kroužku, kámen s nápisem!",
    svg=f'<circle cx="50" cy="50" r="10" fill="none" stroke="{bk}" stroke-width="3"/><circle cx="50" cy="50" r="3.2" fill="{bk}"/>')
add(id="krmelec", name="Krmelec", isom="527 Krmelec", emoji="🦌", col="black",
    say="Černá šipka nahoru je krmelec, kam myslivci nosí zvířatům jídlo. Pomůcka: šipka ukazuje na střechu krmelce!",
    svg=f'<g stroke="{bk}" stroke-width="4.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="50" y1="72" x2="50" y2="30"/><path d="M37 43 L50 30 L63 43"/></g>')
add(id="krouzek", name="Zvláštní objekt – kroužek", isom="530 Výrazný umělý objekt – kroužek", emoji="⭕", col="black",
    say="Černý kroužek je zvláštní věc, kterou postavili lidé. Co to je, říká legenda mapy, třeba lavička. Pomůcka: kroužek, koukni do legendy!",
    svg=f'<circle cx="50" cy="50" r="11" fill="none" stroke="{bk}" stroke-width="3.5"/>')
add(id="krizek", name="Zvláštní objekt – křížek", isom="531 Výrazný umělý objekt – křížek", emoji="❌", col="black",
    say="Černý křížek je jiná zvláštní věc od lidí, třeba pomníček nebo tabule. Pomůcka: křížek, koukni do legendy!",
    svg=f'<g stroke="{bk}" stroke-width="5" stroke-linecap="round"><line x1="36" y1="36" x2="64" y2="64"/><line x1="64" y1="36" x2="36" y2="64"/></g>')

def chevrons(color, y, xs, w, double=False):
    out = []
    for x in xs:
        out.append(f'<path d="M{x-4} {y-6} L{x+2} {y} L{x-4} {y+6}" stroke="{color}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        if double:
            out.append(f'<path d="M{x+2} {y-6} L{x+8} {y} L{x+2} {y+6}" stroke="{color}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    return "".join(out)
add(id="potrubi", name="Potrubí", isom="528 Výrazný liniový objekt", emoji="🔩", col="black",
    say="Černá čára se šipkami je potrubí nebo jiná dlouhá věc od lidí, kterou překročíš. Co to přesně je, řekne legenda mapy. Pomůcka: šipky ukazují, kudy trubka vede!",
    svg=f'<line x1="14" y1="50" x2="86" y2="50" stroke="{bk}" stroke-width="2.5"/>' + chevrons(bk, 50, (30, 50, 70), 2.5),
    tile=f'<line x1="0" y1="50" x2="100" y2="50" stroke="{bk}" stroke-width="2.5"/>' + chevrons(bk, 50, (14, 38, 62, 86), 2.5))
add(id="nepr_potrubi", name="Vysoké potrubí", isom="529 Výrazný nepřekonatelný liniový objekt", emoji="🏗️", col="black",
    say="Tlustá černá čára s dvojitými šipkami je vysoké potrubí nebo jiná dlouhá překážka, přes kterou se nedostaneš. Pomůcka: dvojité šipky, dvakrát stop!",
    svg=f'<line x1="14" y1="50" x2="86" y2="50" stroke="{bk}" stroke-width="4.5"/>' + chevrons(bk, 50, (26, 50, 74), 2.8, double=True),
    tile=f'<line x1="0" y1="50" x2="100" y2="50" stroke="{bk}" stroke-width="4.5"/>' + chevrons(bk, 50, (12, 42, 72), 2.8, double=True))

# --- ZNAČKY TRATĚ (fialová) ---
add(id="start", name="Start", isom="701 Start", emoji="🚩", col="purple",
    say="Fialový trojúhelník je start, odtud tvá trať začíná. Pomůcka: trojúhelník ukazuje špičkou vpřed, vyraz jako raketa na výzvěd!", cheer="Zorientuj mapu, nadechni se a vyraz za dobrodružstvím!",
    svg=f'<path d="M50 26 L73 68 L27 68 Z" fill="none" stroke="{pu}" stroke-width="6.5" stroke-linejoin="round"/>')
add(id="kontrola", name="Kontrola", isom="703 Kontrola", emoji="🎯", col="purple",
    say="Fialové kolečko je kontrola, je tam oranžovo-bílý lampionek a čip. Pomůcka: kolečko je jako lampionek, oraž si ho za okamžik!", cheer="Skvělá práce, další kontrolu máš v kapse!",
    svg=f'<circle cx="50" cy="50" r="24" fill="none" stroke="{pu}" stroke-width="6.5"/>')
add(id="cil", name="Cíl", isom="706 Cíl", emoji="💎", col="purple",
    say="Dvě fialová kolečka jsou cíl, konec trati a schovaný poklad. Pomůcka: dvě kolečka jako medaile, v cíli tě každý pochválí!", cheer="Zvládl jsi to úžasně, užij si zasloužený potlesk!",
    svg=f'<circle cx="50" cy="50" r="25" fill="none" stroke="{pu}" stroke-width="6"/><circle cx="50" cy="50" r="15" fill="none" stroke="{pu}" stroke-width="6"/>')
add(id="spojnice", name="Spojnice", isom="705 Spojnice", emoji="➖", col="purple",
    say="Fialová rovná čára spojuje kontroly a ukazuje, v jakém pořadí je máš hledat. Pomůcka: čára vede od kolečka ke kolečku!",
    svg=f'<line x1="18" y1="72" x2="82" y2="28" stroke="{pu}" stroke-width="5" stroke-linecap="round"/>',
    tile=f'<line x1="0" y1="80" x2="100" y2="20" stroke="{pu}" stroke-width="5"/>')
add(id="znaceny", name="Značený úsek", isom="707 Značený úsek", emoji="🎗️", col="purple",
    say="Fialová přerušovaná čára je značený úsek. Tudy musíš běžet po fáborkách. Pomůcka: čárky jako fáborky na stromech!",
    svg=f'<line x1="18" y1="72" x2="82" y2="28" stroke="{pu}" stroke-width="5" stroke-dasharray="11 7" stroke-linecap="round"/>',
    tile=f'<line x1="0" y1="80" x2="100" y2="20" stroke="{pu}" stroke-width="5" stroke-dasharray="11 7"/>')
add(id="nepristupna", name="Zakázaná oblast", isom="709 Nepřístupná oblast", emoji="⛔", col="purple",
    say="Fialové šrafování je oblast, kam se při závodě nesmí. Pomůcka: fialová mřížka, zamčeno!",
    svg=f'<rect x="20" y="28" width="60" height="44" fill="none" stroke="{pu}" stroke-width="3"/>' + "".join(f'<line x1="{x}" y1="28" x2="{x-22}" y2="72" stroke="{pu}" stroke-width="2.6"/>' for x in range(30, 104, 11)) + f'<rect x="12" y="20" width="76" height="60" fill="{wh}" fill-opacity="0" stroke="none"/>',
    tile="".join(f'<line x1="{x}" y1="0" x2="{x-50}" y2="100" stroke="{pu}" stroke-width="2.8"/>' for x in range(0, 152, 12)))
add(id="pruchod", name="Průchod", isom="710 Průchod", emoji="🚪", col="purple",
    say="Dvě fialové obloučky proti sobě jsou průchod, jediné místo, kudy smíš přes plot nebo zeď. Pomůcka: obloučky jako otevřená vrátka!",
    svg=f'<g stroke="{pu}" stroke-width="5" fill="none" stroke-linecap="round"><path d="M28 34 q22 16 44 0"/><path d="M28 66 q22 -16 44 0"/></g>')
add(id="prvni_pomoc", name="První pomoc", isom="712 Stanoviště první pomoci", emoji="🩹", col="purple",
    say="Fialový kříž je stanoviště první pomoci. Když se zraníš, běž sem. Pomůcka: kříž jako na lékárničce!",
    svg=f'<rect x="42" y="26" width="16" height="48" fill="{pu}"/><rect x="26" y="42" width="48" height="16" fill="{pu}"/>')
add(id="obcerstveni", name="Občerstvení", isom="713 Občerstvovací stanice", emoji="🥤", col="purple",
    say="Fialový kelímek je občerstvovací stanice. Tady se při závodě napiješ. Pomůcka: kelímek s pitím!",
    svg=f'<path d="M32 30 h36 l-5 40 h-26 z" fill="none" stroke="{pu}" stroke-width="5" stroke-linejoin="round"/><line x1="36" y1="42" x2="64" y2="42" stroke="{pu}" stroke-width="4"/>')

add(id="nepristupna_trasa", name="Zakázaná trasa", isom="711 Nepřístupná trasa", emoji="🚷", col="purple",
    say="Fialové křížky na cestě jsou zakázaná trasa. Cestu smíš přeběhnout napříč, ale nesmíš po ní běžet. Pomůcka: křížky přeškrtly cestu!",
    svg=f'<path d="M12 50 H88" stroke="{bk}" stroke-width="2.2" stroke-dasharray="10 5" opacity=".55"/>'
        + "".join(f'<g stroke="{pu}" stroke-width="4.5" stroke-linecap="round"><path d="M{x-7} 43 L{x+7} 57"/><path d="M{x+7} 43 L{x-7} 57"/></g>' for x in (26, 50, 74)),
    tile=f'<path d="M0 50 H100" stroke="{bk}" stroke-width="2.2" stroke-dasharray="10 5" opacity=".55"/>'
        + "".join(f'<g stroke="{pu}" stroke-width="4.5" stroke-linecap="round"><path d="M{x-7} 43 L{x+7} 57"/><path d="M{x+7} 43 L{x-7} 57"/></g>' for x in (14, 50, 86)))

ids = [s["id"] for s in S]
assert len(ids) == len(set(ids)), "duplicitní id"

# ---------- POPISY KONTROL (ISCD 2024, IOF) – černé piktogramy ze sloupce D ----------
# Závazným zdrojem je ISCD 2024 (originál IOF + český překlad ČSOS). Kresby piktogramů se NEKRESLÍ ručně:
# vektorizuje je nástroj trace_iscd.py přímo z originálu do iscd_piktogramy.json (číslo piktogramu → SVG cesta).
# Značka dostane piktogram podle čísel ISOM, která u piktogramů uvádí ISCD (s. 6–12 originálu 2024). Když ISCD
# dvě značky nerozlišuje (např. 109 a 110 → 1.10), mají stejné číslo, tedy shodný piktogram – hra s tím počítá
# („sdílené piktogramy“, úkol sdilene).
#
# Přepínač ISCD_2024: piktogramy, které značce přiřazuje teprve verze 2024 (ISCD_ONLY_2024), se při False vynechají,
# takže hra se pak chová podle verze 2018. Schválený stav je True (přechod na ISCD 2024).
# Další rozdíly 2018 → 2024 u značek hry přepínač neřeší (v 2018 je ISOM 406 → 4.8 a 405 → 4.8 místo 4.5 a 4.3,
# viz kontrola-piktogramu.html), protože hra už sleduje tabulku v repu a verzi 2024.
ISCD_2024 = True
with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "iscd_piktogramy.json"), encoding="utf-8") as _f:
    PICTO = json.load(_f)      # "1.14" -> {"d": "M…Z", "pageIOF": 7, "pageCZ": 7}

ISCD_REF = {
    # voda a bažiny (ISOM 3.3)
    "voda": "3.1", "melka_voda": "3.2", "potok": "3.4", "prikop": "3.5", "bazina": "3.7", "nezretelna_bazina": "3.7",
    "uzka_bazina": "3.6", "jama_s_vodou": "3.3", "studna": "3.9", "pramen": "3.10", "vodni_objekt": "6.1",
    # vegetace (ISOM 3.4)
    "louka": "4.1", "pole": "4.1", "sad": "4.1", "vinice": "4.1", "roztrousene": "4.2", "divoky": "4.2", "les": "4.3",
    "housti": "4.5", "zelena_svetla": "4.5", "zelena_stredni": "4.5", "podrost": "4.5", "hranice_veg": "4.7",
    "strom": "4.9", "ker": "4.9", "veg_x": "4.10",
    # terén (ISOM 3.1)
    "kopec": "1.9", "doplnkova": "1.9", "kupka": "1.10", "protahla_kupka": "1.10", "prohluben": "1.13", "jama": "1.14",
    "teren_objekt": "5.19", "rozbity": "1.15", "zemni_sraz": "1.4", "ryha": "1.7", "val": "1.6",
    # skály a balvany (ISOM 3.2)
    "balvan": "2.4", "velkybalvan": "2.4", "obrovsky": "2.2", "shluk": "2.6", "balvanove_pole": "2.5", "kamenity": "2.7",
    "skala": "2.8", "sraz": "2.1", "nepr_sraz": "2.1", "kamenna_jama": "1.14", "pisek": "8.8",
    # umělé objekty (ISOM 3.5)
    "zpevnena": "5.12", "silnice": "5.1", "sirokasilnice": "5.1", "vozovka": "5.2", "cesta": "5.2", "pesina": "5.2",
    "prusek": "5.3", "zeleznice": "5.24", "vedeni": "5.5", "most": "5.4", "zed": "5.8", "nepr_zed": "5.8", "plot": "5.9",
    "nepr_plot": "5.9", "pruchod_plot": "5.10", "budova": "5.11", "zakaz": "5.23", "zricenina": "5.13", "zastreseni": "5.21",
    "veza": "5.15", "posed": "5.16", "schody": "5.22", "mohyla": "5.17", "krmelec": "5.18", "krouzek": "6.2",
    "krizek": "6.1", "potrubi": "5.14", "nepr_potrubi": "5.14",
    # značky pro dotisk (ISOM 7): zvláštní řádky a sloupec H
    "pruchod": "15.3", "prvni_pomoc": "13.1", "obcerstveni": "13.2",
}
# Značky, kterým ISCD piktogram přiřazuje až ve verzi 2024 (v ISCD 2018 u jejich čísla ISOM chybí).
ISCD_ONLY_2024 = {
    "nezretelna_bazina": "ISOM 310 přibylo k 3.7 (s. 9)", "pole": "ISOM 412 přibylo k 4.1 (s. 9)",
    "sad": "ISOM 413 přibylo k 4.1 (s. 9)", "vinice": "ISOM 414 přibylo k 4.1 (s. 9)",
    "doplnkova": "ISOM 102 a 103 přibyly k 1.9 (s. 6–7)", "zeleznice": "5.24 Železnice je nový v 2024 (s. 11)",
}
for _k, _r in ISCD_REF.items():
    assert _k in ids, ("ISCD_REF: neznámé id", _k)
    assert _r in PICTO, ("ISCD_REF: neznámý piktogram", _k, _r)
for _k in ISCD_ONLY_2024: assert _k in ISCD_REF, _k

def picto_svg(ref): return f'<path d="{PICTO[ref]["d"]}" fill="{bk}" fill-rule="evenodd"/>'
DESC_REF = {k: r for k, r in ISCD_REF.items() if ISCD_2024 or k not in ISCD_ONLY_2024}
DESC = {k: picto_svg(r) for k, r in DESC_REF.items()}
for s in S:
    if s["id"] in DESC: s["desc"] = DESC[s["id"]]; s["iscd"] = DESC_REF[s["id"]]
if __name__ == "__main__": print("s popisem kontrol:", len(DESC), "z", len(S), "(ISCD_2024 =", ISCD_2024, ")")

# ---------- OSTROVY ----------
ISL = [
 # moře 1 – Papouščí
 dict(id="papousci", name="Ostrov papoušků", emoji="🦜", syms=["voda","louka","les"],
      intro="Papoušci hlídají první kousek mapy. Ukaž jim, že poznáš vodu, louku a běhací les!"),
 dict(id="bazina", name="Bažinatý ostrov", emoji="🐸", syms=["housti","bazina","potok"],
      intro="Fuj, tady to čvachtá! V bažině si namočíš boty, v hustníku se zamotáš do větví a přes potok musíš skočit."),
 dict(id="kameny", name="Kamenný ostrov", emoji="🪨", syms=["cesta","balvan","budova"],
      intro="Na Kamenném ostrově stojí stará pevnost. Vede k ní pěší cesta kolem velkých balvanů."),
 dict(id="sopka", name="Sopečný ostrov", emoji="🌋", syms=["kopec","kupka","jama"],
      intro="Sopka! Hnědé vrstevnice ukazují, jak je kopec strmý. Kolem jsou malé kupky a hluboké jámy."),
 dict(id="zavod", name="Závodní ostrov", emoji="🏁", syms=["start","kontrola","cil","spojnice"],
      intro="Tady piráti závodí! Od startu po spojnici přes kontroly až do cíle. Fialové značky ti ukážou trať."),
 dict(id="mlha1", name="Mlhova zátoka", emoji="🌫️", syms=[], boss=True,
      intro="V zátoce číhá kapitán Mlha s druhým kouskem mapy! Vyzývá tě na souboj: kdo přečte víc značek, než dohoří svíčka?"),
 # moře 2 – Mlžné
 dict(id="stiny", name="Ostrov zelených stínů", emoji="🌿", syms=["zelena_svetla","zelena_stredni","podrost","strom"],
      intro="Tady roste všechno možné. Světlá zelená trochu brzdí, tmavší víc, a v podrostu jdeš jako v trávě po pás. Uprostřed stojí obrovský strom."),
 dict(id="cesty", name="Ostrov cest", emoji="🛣️", syms=["silnice","vozovka","pesina","sirokasilnice","prusek"],
      intro="Ostrov je protkaný cestami: široká silnice pro auta, vozová cesta pro traktor, úzké pěšiny a rovný průsek lesem. Poznáš, která je která?"),
 dict(id="skaly", name="Skalní ostrov", emoji="🧗", syms=["shluk","velkybalvan","sraz","skala"],
      intro="Skály, srázy a hromady balvanů! Pozor: jedna tečka je balvan, trojúhelník je celá hromada."),
 dict(id="pole", name="Ostrov luk a polí", emoji="🌾", syms=["divoky","roztrousene","pole","sad"],
      intro="Zlaté lány, zarostlé paseky a voňavý sad. Žlutá má spoustu podob, koukej pozorně na puntíky."),
 dict(id="vodni", name="Vodní ostrov", emoji="🐟", syms=["studna","pramen","uzka_bazina","nezretelna_bazina"],
      intro="Všude bublá voda: prameny, studny a mokré pruhy v lese. Modrá tečka, čárka nebo háček, každá znamená něco jiného."),
 dict(id="mlha2", name="Mlhův útes", emoji="🌫️", syms=[], boss=True,
      intro="Na útesu se mračí kapitán Mlha. Má další kousek mapy a chce odvetu! Přečteš víc značek než on?"),
 # moře 3 – Bouřlivé
 dict(id="ploty", name="Ostrov plotů a zdí", emoji="🚧", syms=["plot","nepr_plot","zed","nepr_zed","pruchod_plot"],
      intro="Piráti si tu postavili ploty a zdi. Některé přelezeš, přes jiné se nesmí a musíš najít průchod. Dvojité čárky a tlusté tečky znamenají stop!"),
 dict(id="stavby", name="Ostrov staveb", emoji="🏰", syms=["zpevnena","zakaz","veza","posed","schody"],
      intro="Věže, posedy, schody a asfaltové plácky. A jedna olivová zahrada, kam se nesmí."),
 dict(id="draty", name="Ostrov drátů", emoji="⚡", syms=["vedeni","zeleznice","most","krizek","potrubi","nepr_potrubi"],
      intro="Nad hlavou bzučí elektrické dráty, dole hučí vlak a lesem vede potrubí. Přes potok vede most. A co je ten křížek? To řekne legenda!"),
 dict(id="teren", name="Ostrov strání", emoji="🏔️", syms=["prohluben","zemni_sraz","rozbity","ryha"],
      intro="Samé hnědé tvary: hlinité srázy, rýhy vymleté vodou, dolíky a hrbolatá zem."),
 dict(id="zahrady", name="Ostrov zahrad", emoji="🍇", syms=["ker","vinice","veg_x","hranice_veg"],
      intro="Vinice v řádcích, keře a vyvrácený strom. A tečkovaná čára, kde končí starý les."),
 dict(id="mlha3", name="Mlhova pevnost", emoji="🌫️", syms=[], boss=True,
      intro="Kapitán Mlha se zabarikádoval v pevnosti! Kousek mapy vydá jen tomu, kdo ho porazí v souboji."),
 # moře 4 – Ledové
 dict(id="trat", name="Ostrov závodníků", emoji="🏃", syms=["znaceny","nepristupna","prvni_pomoc","obcerstveni","pruchod","nepristupna_trasa"],
      intro="Velký pirátský závod! Fáborky, občerstvení, první pomoc, zakázané oblasti i zakázané cesty. Fialové značky říkají, co se smí."),
 dict(id="melciny", name="Ostrov mělčin", emoji="🌊", syms=["melka_voda","jama_s_vodou","prikop","vodni_objekt","pisek"],
      intro="Mělké tůně, vodní příkopy, jámy plné vody a písčitá pláž. Světlejší modrá je mělčina, kterou přebrodíš."),
 dict(id="balvany", name="Balvanový ostrov", emoji="🗿", syms=["nepr_sraz","balvanove_pole","kamenity","obrovsky","kamenna_jama"],
      intro="Obrovské balvany, kamenná pole a vysoké skalní stěny, přes které se nesmí. Tady čti mapu opravdu pozorně."),
 dict(id="tajemny", name="Tajemný ostrov", emoji="🏚️", syms=["zricenina","krouzek","mohyla","krmelec","zastreseni"],
      intro="Zřícenina starého hradu, hraniční kameny, přístřešek a krmelec pro srnky. A tajemný kroužek, který vysvětlí jen legenda."),
 dict(id="hnedy", name="Hnědý ostrov", emoji="🟤", syms=["val","protahla_kupka","teren_objekt","doplnkova"],
      intro="Poslední hnědé značky: zemní val, protáhlá kupka, pomocná vrstevnice a zvláštní terénní objekt. Pak už umíš úplně všechno!"),
 dict(id="mlha4", name="Ostrov kapitána Mlhy", emoji="🌫️", syms=[], boss=True,
      intro="Kapitán Mlha má poslední kousek mapy! Vyzývá tě na rozhodující souboj o Zlatý kompas.",
      crew=dict(id="kompas", emoji="🐈‍⬛", name="Kocour Kompas", say="Mlhův kocour Kompas přeběhl k tobě! Teď je v tvé posádce a vždycky ví, kde je sever.")),
]
# Fond posádky (ostrov bez vlastní crew dostane člena podle pořadí), moře a chvály
CREW = [
 ("🐒","Opička Kiki","Opička Kiki se přidává k posádce! Umí šplhat na stěžeň a hlídat zlaťáky."),
 ("🐢","Želva Ferda","Želva Ferda se přidává k posádce! Je pomalá, ale nikdy nezabloudí."),
 ("🦀","Krab Klepeto","Krab Klepeto se přidává k posádce! Klepety otevře každou truhlu."),
 ("🐙","Chobotnice Ola","Chobotnice Ola se přidává k posádce! Osmi rukama vytáhne kotvu jako nic."),
 ("🐬","Delfín Dan","Delfín Dan se přidává k posádce! Plave rychleji než každá loď."),
 ("🐈‍⬛","Kocour Kompas","Kocour Kompas se přidává k posádce! Vždycky ví, kde je sever."),
 ("🦭","Tuleň Tonda","Tuleň Tonda se přidává k posádce! Zatleská ploutvemi při každém zlaťáku."),
 ("🐧","Tučňák Pája","Tučňák Pája se přidává k posádce! Chodí v obleku i na palubě."),
 ("🦜","Papouščice Rózi","Papouščice Rózi se přidává k posádce! Je to Pepíkova sestřenice a umí zpívat."),
 ("🐕","Pes Bublina","Pes Bublina se přidává k posádce! Vyčenichá každý poklad."),
 ("🐸","Žába Kuňka","Žába Kuňka se přidává k posádce! Zná každou bažinu."),
 ("🦔","Ježek Bodlinka","Ježek Bodlinka se přidává k posádce! Nikdo mu mapu nesebere."),
 ("🐿️","Veverka Zrzka","Veverka Zrzka se přidává k posádce! Schovává oříšky i zlaťáky."),
 ("🦉","Sova Moudrá","Sova Moudrá se přidává k posádce! Vidí i v noci."),
 ("🐐","Koza Líza","Koza Líza se přidává k posádce! Vyleze na každý kopec."),
 ("🦊","Liška Ryška","Liška Ryška se přidává k posádce! Zná všechny lesní pěšinky."),
 ("🐝","Včelka Bzum","Včelka Bzum se přidává k posádce! Miluje louky plné květin."),
 ("🦩","Plameňák Filip","Plameňák Filip se přidává k posádce! Stojí na jedné noze i v bouři."),
 ("🐨","Koala Kuba","Koala Kuba se přidává k posádce! Prospí celou plavbu."),
 ("🦁","Lev Leo","Lev Leo se přidává k posádce! Jeho řev zažene každého piráta."),
]
SEAS = ["Papouščí moře","Mlžné moře","Bouřlivé moře","Ledové moře","Sluneční moře","Korálové moře","Půlnoční moře","Perlové moře"]
PRAISE = ["Arr! Zlaťák do truhly!","Jupí! Máš zlatou minci!","Výborně, námořníku!","Cink! Poklad se plní!","Paráda, správně čteš mapu!","Tak se čte mapa!"]
SYM_BY = {s["id"]: s for s in S}
def sname(s): return re.sub(r"\s*\(.*?\)", "", s["name"]).strip()
def crew_of(i):
    isl = ISL[i]
    if isl.get("crew"): return isl["crew"]
    e, n, say = CREW[i % len(CREW)]
    return dict(id="crew%d" % i, emoji=e, name=n, say=say)
def intro_of(i):
    isl = ISL[i]
    if isl.get("intro"): return isl["intro"]
    n = [sname(SYM_BY[x]).lower() for x in isl["syms"]]
    return "Na ostrově " + isl["name"] + " tě čekají nové značky: " + ", ".join(n) + ". Ukaž, že je poznáš!"

used = [s for i in ISL for s in i["syms"]]
assert len(used) == len(set(used)), "značka na dvou ostrovech"
missing = [i for i in ids if i not in used]
assert not missing, ("nezařazené značky", missing)
for i in ISL:
    for s in i["syms"]: assert s in ids, s

# ---------- OTÁZKY NA ROZUM ----------
CON = [
 dict(q="Kde si namočíš nohy?", emoji="🥾", ok=["voda","bazina","potok","melka_voda","jama_s_vodou","uzka_bazina","nezretelna_bazina","prikop"], no=["louka","les","housti","cesta","kopec","balvan","budova","silnice","divoky","pole","zpevnena"], hint="Mokro je tam, kde je na mapě modrá."),
 dict(q="Kudy poběžíš rychle?", emoji="🏃", ok=["louka","les","cesta","silnice","pesina","vozovka","sirokasilnice","zpevnena"], no=["housti","bazina","voda","zelena_stredni","podrost","balvanove_pole","rozbity"], hint="Rychle se běží po žluté, bílým lesem a po černých cestách."),
 dict(q="Kudy se běží špatně?", emoji="🐌", ok=["housti","bazina","zelena_stredni","podrost","balvanove_pole","rozbity"], no=["louka","les","cesta","silnice","pesina","divoky"], hint="Špatně se běží zelenou, bažinou a přes kamení."),
 dict(q="Kde se zamotáš do větví?", emoji="🌿", ok=["housti","zelena_stredni","zelena_svetla","podrost"], no=["louka","les","cesta","voda","bazina","silnice","pole"], hint="Do větví se zamotáš tam, kde je zelená."),
 dict(q="Kde se zadýcháš do kopce?", emoji="😮‍💨", ok=["kopec"], no=["louka","les","voda","bazina","cesta","silnice"], hint="Kopec kreslí hnědé vrstevnice."),
 dict(q="Co je z kamene?", emoji="🪨", ok=["balvan","velkybalvan","shluk","skala","balvanove_pole","obrovsky","kamenity"], no=["louka","les","voda","bazina","housti","kopec","strom","potok"], hint="Kameny a skály jsou černé nebo šedé."),
 dict(q="Kde bydlí lidi?", emoji="🏠", ok=["budova"], no=["louka","les","voda","bazina","housti","balvan","veza","posed","zricenina"], hint="Lidi bydlí v černé budově."),
 dict(q="Kudy jezdí auta?", emoji="🚗", ok=["silnice","sirokasilnice","vozovka"], no=["pesina","cesta","potok","plot","zed","vedeni","zeleznice"], hint="Auta jezdí po silnici, to je plná černá čára, nebo po vozové cestě."),
 dict(q="Kde závod začíná?", emoji="🚩", ok=["start"], no=["kontrola","cil","louka","les","voda","spojnice"], hint="Závod začíná na fialovém trojúhelníku."),
 dict(q="Kde si cvakneš čipem?", emoji="📟", ok=["kontrola"], no=["start","cil","louka","les","balvan","spojnice"], hint="Čipem cvakneš na kontrole, to je jedno kolečko."),
 dict(q="Kde je schovaný poklad?", emoji="💎", ok=["cil"], no=["start","kontrola","louka","les","budova","spojnice"], hint="Poklad je v cíli, to jsou dvě kolečka."),
 dict(q="Kam nesmíš vůbec vstoupit?", emoji="🚫", ok=["zakaz","nepristupna"], no=["louka","les","cesta","zpevnena","divoky","pole","sad"], hint="Zákaz je olivová plocha nebo fialová mřížka."),
 dict(q="Co nesmíš přelézt?", emoji="🧗", ok=["nepr_plot","nepr_zed","nepr_sraz","nepr_potrubi"], no=["plot","zed","sraz","cesta","louka","potrubi","pruchod_plot"], hint="Nepřekonatelné je to tlusté nebo s dvojitými čárkami."),
 dict(q="Kudy projdeš přes plot?", emoji="🚪", ok=["pruchod_plot"], no=["plot","nepr_plot","zed","nepr_zed","potrubi"], hint="Průchod je mezera v plotu se dvěma čárkami."),
 dict(q="Kudy je zakázáno běžet?", emoji="🚷", ok=["nepristupna_trasa","nepristupna","zakaz"], no=["cesta","silnice","louka","les","znaceny","pesina"], hint="Zákaz je fialový nebo olivový: křížky na cestě, mřížka nebo olivová plocha."),
 dict(q="Kde se napiješ?", emoji="🚰", ok=["studna","pramen","obcerstveni"], no=["balvan","budova","plot","kupka","krizek","posed"], hint="Voda je ve studni, v prameni nebo na občerstvení."),
 dict(q="Kde je díra v zemi?", emoji="🕳️", ok=["jama","kamenna_jama","jama_s_vodou","prohluben"], no=["kupka","balvan","strom","budova","protahla_kupka"], hint="Díra je véčko nebo miska."),
 dict(q="Kde je malý kopeček?", emoji="🐜", ok=["kupka","protahla_kupka"], no=["jama","prohluben","balvan","strom","ker"], hint="Kopeček je hnědá tečka."),
 dict(q="Kde ti pomůžou, když se zraníš?", emoji="🩹", ok=["prvni_pomoc"], no=["obcerstveni","kontrola","cil","start","znaceny"], hint="První pomoc má fialový kříž."),
 dict(q="Co postavili lidé?", emoji="🔨", ok=["budova","veza","posed","most","zeleznice","vedeni","zed","plot","zricenina","schody","krmelec","potrubi","zastreseni"], no=["voda","louka","les","balvan","kopec","strom","potok","bazina","ker"], hint="Co postavili lidé, je černé."),
 dict(q="Co tu roste?", emoji="🌳", ok=["strom","ker"], no=["balvan","budova","kupka","veza","krizek","mohyla"], hint="Rostliny jsou zelené."),
 dict(q="Kudy jezdí vlak?", emoji="🚂", ok=["zeleznice"], no=["silnice","vedeni","potok","cesta","plot"], hint="Vlak jede po tlusté černé čáře s mezerami."),
 dict(q="Kudy běžíš po fáborkách?", emoji="🎗️", ok=["znaceny"], no=["spojnice","nepristupna","silnice","cesta","potok"], hint="Fáborky značí fialová přerušovaná čára."),
 dict(q="Kudy teče voda?", emoji="🏞️", ok=["potok","prikop"], no=["cesta","silnice","plot","zed","kopec","vedeni","pesina"], hint="Voda teče po modré čáře."),
]
for c in CON:
    for s in c["ok"] + c["no"]: assert s in ids, ("concept", s)

# ---------- ZAMĚNITELNÉ ZNAČKY (CONF) ----------
# Skupiny značek, které se dětem pletou. Od 2. moře se mezi nabídky dává aspoň jedna ze skupiny cíle
# (od 4. moře až dvě), pokud ji dítě už zná.
CONF = [
 ["bazina","nezretelna_bazina","uzka_bazina"],
 ["balvan","velkybalvan","obrovsky","shluk"],
 ["zed","nepr_zed"],
 ["plot","nepr_plot","pruchod_plot"],
 ["sraz","nepr_sraz","zemni_sraz"],
 ["louka","roztrousene","divoky"],
 ["kupka","protahla_kupka"],
 ["jama","kamenna_jama","prohluben"],
 ["zelena_svetla","zelena_stredni","housti","podrost"],
 ["silnice","sirokasilnice","zpevnena"],
 ["vozovka","cesta","pesina"],
 ["krouzek","krizek"],
 ["voda","melka_voda"],
 ["potok","prikop"],
 ["potrubi","nepr_potrubi"],
 ["start","kontrola","cil"],
 ["zakaz","nepristupna","nepristupna_trasa"],
 ["kopec","doplnkova"],
 ["pole","sad","vinice"],
 ["veza","posed"],
 ["studna","pramen","vodni_objekt"],
]
for _g in CONF:
    for _s in _g: assert _s in ids, ("CONF: neznámé id", _s)

# ---------- GENEROVÁNÍ JS ----------
def js_str(s): return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'
def js_tpl(s):
    assert '`' not in s and '${' not in s
    return '`' + s + '`'

out = []
out.append("/* Piktogramy popisů kontrol (ISCD 2024) podle čísla piktogramu; značky se shodným číslem sdílejí tentýž řetězec */")
out.append("const PICTO={" + ",".join(f"{js_str(r)}:{js_tpl(picto_svg(r))}" for r in sorted(set(DESC_REF.values()), key=lambda x: [int(n) for n in x.split('.')])) + "};")
out.append("const SY=[")
for s in S:
    parts = [f'id:{js_str(s["id"])}', f'name:{js_str(s["name"])}', f'isom:{js_str(s["isom"])}', f'emoji:{js_str(s["emoji"])}', f'col:{js_str(s["col"])}']
    if s.get("fill"): parts.append(f'fill:{js_str(s["fill"])}')
    if s.get("base"): parts.append('base:true')
    parts.append(f'say:{js_str(s["say"])}')
    if s.get("cheer"): parts.append(f'cheer:{js_str(s["cheer"])}')
    parts.append(f'svg:{js_tpl(s["svg"])}')
    if s.get("deco"): parts.append(f'deco:{js_tpl(s["deco"])}')
    if s.get("tile"): parts.append(f'tile:{js_tpl(s["tile"])}')
    if s.get("desc"): parts.append(f'desc:PICTO[{js_str(s["iscd"])}]')
    out.append("  {" + ", ".join(parts) + "},")
out.append("];")
out.append("const SYM={}; SY.forEach(s=>SYM[s.id]=s);")
out.append("")
out.append("/* Ostrovy – scénář. Řadí se po šesti do moří; každý ostrov učí nové značky, dává kousek mapy a člena posádky. */")
out.append("const ISLANDS=[")
for i in ISL:
    parts = [f'id:{js_str(i["id"])}', f'name:{js_str(i["name"])}', f'emoji:{js_str(i["emoji"])}',
             'syms:[' + ",".join(js_str(x) for x in i["syms"]) + ']']
    if i.get("boss"): parts.append("boss:true")
    parts.append(f'intro:{js_str(i["intro"])}')
    if i.get("crew"):
        c = i["crew"]; parts.append('crew:{' + f'id:{js_str(c["id"])}, emoji:{js_str(c["emoji"])}, name:{js_str(c["name"])}, say:{js_str(c["say"])}' + '}')
    out.append("  {" + ", ".join(parts) + "},")
out.append("];")
out.append("/* Fond posádky – ostrov bez vlastní crew dostane člena podle pořadí */")
out.append("const CREW_POOL=[" + ",".join("{emoji:%s,name:%s,say:%s}" % (js_str(e), js_str(n), js_str(t)) for e, n, t in CREW) + "];")
out.append("const SEAS=[" + ",".join(js_str(x) for x in SEAS) + "];")
out.append("const PRAISE=[" + ",".join(js_str(x) for x in PRAISE) + "];")
out.append("/* Skupiny zaměnitelných značek (obtížnější nabídky od 2. moře) */")
out.append("const CONF=[" + ",".join("[" + ",".join(js_str(x) for x in g) + "]" for g in CONF) + "];")
SY_ISL_JS = "\n".join(out)

out = ["const CONCEPTS=["]
for c in CON:
    out.append("  {" + f'q:{js_str(c["q"])}, emoji:{js_str(c["emoji"])}, ok:[' + ",".join(js_str(x) for x in c["ok"]) + '], no:[' + ",".join(js_str(x) for x in c["no"]) + f'], hint:{js_str(c["hint"])}' + "},")
out.append("];")
CON_JS = "\n".join(out)

def write_html():
    html = io.open(HTML, encoding="utf-8").read()
    # 1) SY + ISLANDS blok: od "const SY=[" po konec "const ISLANDS=[...];"
    mk = "/* Piktogramy popisů kontrol (ISCD 2024)"
    a = html.index(mk) if mk in html else html.index("const SY=[")
    b = html.index("const SEA_SIZE=6;")
    html = html[:a] + SY_ISL_JS + "\n\n" + html[b:]
    # 2) CONCEPTS blok
    a = html.index("const CONCEPTS=[")
    b = html.index("];", a) + 2
    html = html[:a] + CON_JS + html[b:]
    io.open(HTML, "w", encoding="utf-8", newline="\n").write(html)
    print("symbols:", len(S), "islands:", len(ISL), "concepts:", len(CON), "html chars:", len(html))

if __name__ == "__main__":
    write_html()
