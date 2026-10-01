# -*- coding: utf-8 -*-
"""Vyrobí kontrolní list piktogramů zdroje/kontrola-piktogramu.html (samostatná stránka bez závislostí).

Pro každou značku hry ukáže mapovou značku, piktogram z popisů kontrol tak, jak ho kreslí hra, a vedle něj
originální piktogram vyříznutý z ISCD 2024 (IOF), číslo piktogramu, český a anglický název, stranu ve specifikaci,
se kterými značkami piktogram sdílí, stav změny a poznámku. Majitel tak může očima porovnat hru se specifikací.

Data bere z gen_symbols.py (ISCD_REF, DESC, ISCD_2024), z iscd_piktogramy.json a z originálního PDF (trace_iscd.py).
Spuštění:  python zdroje/build_kontrola.py
"""
import base64, html, io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_symbols as g
from PIL import Image
import trace_iscd as tr

OUT = os.path.join(HERE, "kontrola-piktogramu.html")

# číslo piktogramu -> (český název z ČSOS 2024, anglický název z IOF 2024)
NAMES = {
    "1.4": ("Zemní sráz", "Earth bank"), "1.6": ("Zemní val", "Earth wall"), "1.7": ("Rýha", "Erosion gully"),
    "1.9": ("Kupa", "Hill"), "1.10": ("Kupka", "Knoll"), "1.13": ("Malá prohlubeň", "Small depression"),
    "1.14": ("Jáma", "Pit"), "1.15": ("Rozbitý povrch", "Broken ground"),
    "2.1": ("(Skalní) sráz", "Cliff, Crag"), "2.2": ("Skalní věž (obrovský balvan)", "Rock Pillar"),
    "2.4": ("Balvan", "Boulder"), "2.5": ("Balvanové pole", "Boulder field"), "2.6": ("Shluk balvanů", "Boulder cluster"),
    "2.7": ("Kamenitý povrch", "Stony ground"), "2.8": ("Holá skála", "Bare rock"),
    "3.1": ("Jezero", "Lake"), "3.2": ("Rybníček", "Pond"), "3.3": ("Jáma s vodou", "Waterhole"),
    "3.4": ("Řeka, potok", "River, Stream, Watercourse"), "3.5": ("Malý vodní příkop (meliorační rýha)", "Minor water channel, Ditch"),
    "3.6": ("Úzká bažina", "Narrow marsh"), "3.7": ("Bažina", "Marsh"), "3.9": ("Studna", "Well"), "3.10": ("Pramen", "Spring"),
    "4.1": ("Otevřený prostor", "Open land"), "4.2": ("Polootevřený prostor", "Semi-open land"), "4.3": ("Roh lesa", "Forest corner"),
    "4.5": ("Hustník", "Thicket"), "4.7": ("Hranice vegetace", "Vegetation boundary"), "4.9": ("Výrazný strom", "Prominent tree"),
    "4.10": ("Vývrat, pařez", "Prominent vegetation feature, e.g. root stock, tree stump"),
    "5.1": ("Silnice", "Road"), "5.2": ("Cesta, pěšina", "Track / Path"), "5.3": ("Průsek", "Ride"), "5.4": ("Most", "Bridge"),
    "5.5": ("Elektrické vedení", "Power line"), "5.8": ("Zeď", "Wall"), "5.9": ("Plot", "Fence"), "5.10": ("Průchod", "Crossing point"),
    "5.11": ("Budova", "Building"), "5.12": ("Zpevněná plocha", "Paved area"), "5.13": ("Zřícenina", "Ruin"),
    "5.14": ("Potrubí, bobová dráha", "Prominent man-made line feature, e.g. pipeline; bobsleigh/skeleton track"),
    "5.15": ("Věž, stožár", "Tower / Pylon"), "5.16": ("Posed", "Shooting platform"), "5.17": ("Hraniční kámen, mohyla", "Boundary stone, Cairn"),
    "5.18": ("Krmelec", "Fodder rack"), "5.19": ("Milíř, plošinka", "Charcoal burning ground, Platform"),
    "5.21": ("Zastřešení", "Canopy"), "5.22": ("Schodiště", "Stairway"), "5.23": ("Oblast se zákazem vstupu", "Out of Bounds area"),
    "5.24": ("Železnice", "Railway"), "6.1": ("Výrazný objekt / Zvláštní objekt", "Prominent feature / Special item"),
    "6.2": ("Výrazný objekt / Zvláštní objekt", "Prominent feature / Special item"), "8.8": ("Písčitý", "Sandy"),
    "13.1": ("Stanoviště první pomoci", "First Aid post"), "13.2": ("Občerstvovací stanice", "Refreshment point"),
    "15.3": ("Povinný bod přechodu/průběh", "Mandatory crossing point or points"),
}

# Značky, které měly piktogram už před touto úpravou, a jejich dřívější kresba už tvarově odpovídala originálu
# (překryv starého a nového piktogramu po srovnání ohraničení ≥ 0,75). U ostatních je stav „změněno“.
OLD_SAME = {"voda", "kopec", "zed", "mohyla", "veza", "krouzek", "louka", "zricenina", "skala", "jama", "kamenna_jama", "vedeni",
            "silnice", "sirokasilnice", "krizek", "vodni_objekt", "balvan", "obrovsky", "veg_x", "kupka", "budova", "prvni_pomoc"}
# varianty, které ISCD nerozlišuje a které dřív měly vlastní jiný piktogram (teď sdílejí piktogram základní značky)
VARIANT_FIXED = {"protahla_kupka", "nepr_sraz", "velkybalvan", "nepr_zed", "nepr_plot", "nepr_potrubi", "pesina", "ker", "roztrousene"}
# značky, které piktogram před touto úpravou neměly a podle ISCD 2018 i 2024 mít mají
NEW_BOTH = {"zakaz", "teren_objekt"}

NOTES = {
    "protahla_kupka": "ISOM 109 i 110 → 1.10 (s. 7). Dřív samostatná protáhlá elipsa, nyní stejný piktogram jako Kupka.",
    "nepr_sraz": "ISOM 201 i 202 → 2.1 (s. 7). Dřív tučnější vlastní kresba, nyní stejný piktogram jako Skalní sráz.",
    "velkybalvan": "ISOM 204 i 205 → 2.4 (s. 8). Dřív větší trojúhelník, nyní stejný piktogram jako Balvan.",
    "nepr_zed": "ISOM 513 i 515 → 5.8 (s. 10). Dřív tlustší vlastní kresba, nyní stejný piktogram jako Zeď.",
    "nepr_plot": "ISOM 516 i 518 → 5.9 (s. 10). Dřív s dvojitými čárkami, nyní stejný piktogram jako Plot.",
    "nepr_potrubi": "ISOM 528 i 529 → 5.14 (s. 11). Dřív s dalšími čárkami, nyní stejný piktogram jako Potrubí.",
    "pesina": "ISOM 504–507 → 5.2 (s. 10). Dřív jemně čárkovaná čára, nyní stejný piktogram jako Cesta a Vozová cesta.",
    "vozovka": "ISOM 504–507 → 5.2 (s. 10).", "cesta": "ISOM 504–507 → 5.2 (s. 10).",
    "silnice": "ISOM 502 i 503 → 5.1 (s. 10).", "sirokasilnice": "ISOM 502 i 503 → 5.1 (s. 10).",
    "ker": "ISOM 417 i 418 → 4.9 (s. 10). Dřív kolečko na stopce; listnatost se v ISCD píše symbolem 8.10 do sloupce E, ne jiným obrázkem.",
    "roztrousene": "ISOM 402 → 4.2 (s. 9), tečkovaný kosočtverec. Dřív kosočtverec s tečkami uvnitř.",
    "divoky": "ROZPOR ZDROJŮ: ISCD 2018 i 2024 (s. 9) mapují ISOM 403 na 4.1 (a 4.4), tabulka v repu na tečkovaný kosočtverec (4.2). Nechal jsem podle tabulky (jako dřív); rozhodnutí je na majiteli.",
    "podrost": "ISOM 407 není v ISCD 2018 ani 2024 uvedeno. Ponechán piktogram hustníku (jako u 406 a 408); tabulka v repu má vlastní mřížku bez čísla ISCD.",
    "zelena_svetla": "ISOM 406 → 4.5 podle ISCD 2024 (s. 10) i tabulky v repu; v ISCD 2018 (s. 9) patří 406 k 4.8 Skupina stromů.",
    "zelena_stredni": "ISOM 408 → 4.5 (s. 10).", "housti": "ISOM 410 → 4.5 (s. 10).",
    "les": "ISOM 405 → 4.3 Roh lesa i 4.8 Skupina stromů (ISCD 2024, s. 9–10); v ISCD 2018 jen 4.8. Piktogram 4.3 odpovídá tabulce v repu a zůstal.",
    "veg_x": "ISOM 419 → 4.10 a 6.1 (ISCD 2024); v ISCD 2018 je 419 jen u 6.1. Piktogram 4.10 odpovídá tabulce v repu.",
    "kamenna_jama": "ISOM 203 → 1.14 Jáma (s kombinací 8.6) i 2.3 Jeskyně (s. 7–8). Ponechána 1.14, kamenná jáma = 1.14 + 8.6 ve sloupci E.",
    "pisek": "ISOM 213 → 4.1 Otevřený prostor v kombinaci s 8.8 Písčitý (s. 9 a 13). Hra ukazuje jen rozlišující symbol sloupce E (8.8).",
    "pruchod": "Fialový průchod (ISOM 710) odpovídá zvláštnímu řádku 15.3 (s. 17), nikoli sloupci D.",
    "prvni_pomoc": "Sloupec H, 13.1 (s. 16).", "obcerstveni": "Sloupec H, 13.2 (s. 16).",
    "pruchod_plot": "ISOM 519 → 5.10 (s. 11).",
    "teren_objekt": "ISOM 115 → 5.19 Milíř, plošinka (s. 11), v 2024 také 6.1 a 1.16. Zvolena plošinka podle tabulky v repu. Platí už v ISCD 2018.",
    "zakaz": "ISOM 520 → 5.23 (s. 11). Platí už v ISCD 2018.",
    "krouzek": "ISOM 530 → 6.2 (s. 12), také 5.19 a 5.20.", "krizek": "ISOM 531 → 6.1 (s. 12), také 5.20 Pomník.",
    "vodni_objekt": "ISOM 313 → 6.1 (s. 12).",
    "nezretelna_bazina": "Jen ISCD 2024: ISOM 310 přibylo k 3.7 (s. 9).",
    "pole": "Jen ISCD 2024: ISOM 412 přibylo k 4.1 (s. 9).",
    "sad": "Jen ISCD 2024: ISOM 413 přibylo k 4.1 (s. 9). Tabulka v repu (2018) kreslí sad tečkovaným kosočtvercem, ISCD 2024 diamantem 4.1; platí originál.",
    "vinice": "Jen ISCD 2024: ISOM 414 přibylo k 4.1 (s. 9).",
    "doplnkova": "Jen ISCD 2024: ISOM 102 a 103 přibyly k 1.1–1.3, 1.9, 1.11, 1.12 (s. 6–7). Zvolena 1.9 Kupa jako u Vrstevnice.",
    "kopec": "ISOM 101 → 1.1–1.3, 1.9, 1.11, 1.12; vrstevnice je ve hře znázorněna jako 1.9 Kupa.",
    "zeleznice": "Jen ISCD 2024: 5.24 Železnice je nový piktogram (ISOM 509, s. 11).",
    "uzka_bazina": "ISOM 309 → 3.6 (s. 8). Dřív vypadala stejně jako hranice vegetace a průsek, teď mají každá vlastní piktogram.",
    "hranice_veg": "ISOM 416 → 4.7 (s. 9). Dřív tečkovaná čára, nyní tečkovaný zalomený tvar podle originálu.",
    "prusek": "ISOM 508 → 5.3 (s. 10). Dřív tečkovaná čára, nyní dvě řady teček podle originálu.",
    "studna": "ISOM 311 → 3.9 Studna (s. 9), také 3.11 Vodní nádrž.",
    "most": "ISOM 512 → 5.4 Most (s. 10), také 5.7 Tunel.",
    "zemni_sraz": "ISOM 104 → 1.4 (s. 7), také 1.5 Lom.",
    "veza": "ISOM 524 → 5.15 (s. 11).", "posed": "ISOM 525 → 5.16 (s. 11), také 5.15.",
    "zastreseni": "ISOM 522 → 5.21 (s. 11), také 5.11.",
}


def b64png(img):
    buf = io.BytesIO(); img.save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


def status_of(sid, has):
    if sid in g.ISCD_ONLY_2024: return "jen 2024"
    if not has: return "beze změny"
    if sid in NEW_BOTH: return "nové"
    if sid in VARIANT_FIXED: return "změněno"
    return "beze změny" if sid in OLD_SAME else "změněno"


def section(s):
    n = int(s["isom"].split()[0])
    return {1: "Terénní tvary", 2: "Skály a balvany", 3: "Voda a bažiny", 4: "Vegetace", 5: "Umělé objekty", 7: "Značky pro dotisk"}[n // 100]


def main():
    rasters = tr.glyph_images()
    used = sorted({g.DESC_REF[s["id"]] for s in g.S if s["id"] in g.DESC_REF}, key=lambda r: [int(x) for x in r.split(".")])
    syms = ['<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>']
    for r in used:
        syms.append(f'<symbol id="n{r}" viewBox="0 0 100 100"><rect width="100" height="100" fill="#fff"/>{g.picto_svg(r)}</symbol>')
        im = rasters[r]["img"]
        # originál ve stejném měřítku jako hra: buňka originálu (CELL_PT) = 70 jednotek, výřez má 100 × 100 jednotek (u 15.3: 2,7 j. na pt)
        wpt = rasters[r]["wpt"]
        units_wide = wpt * (2.7 if r == "15.3" else tr.CELL_UNITS / tr.CELL_PT)
        size = int(round(im.width * 100.0 / units_wide))
        canvas = Image.new("RGB", (size, size), "white")
        canvas.paste(im, ((canvas.width - im.width) // 2, (canvas.height - im.height) // 2))
        syms.append(f'<symbol id="o{r}" viewBox="0 0 100 100"><image href="data:image/png;base64,{b64png(canvas)}" width="100" height="100"/></symbol>')
    syms.append("</defs></svg>")

    byref = {}
    for sid, r in g.DESC_REF.items(): byref.setdefault(r, []).append(sid)
    nm = {s["id"]: s for s in g.S}
    rows, counts = [], {}
    cur = None
    for s in sorted(g.S, key=lambda s: (int(s["isom"].split()[0]), s["id"])):
        sec = section(s)
        if sec != cur:
            rows.append(f'<tr class="sec"><th colspan="8">{sec}</th></tr>'); cur = sec
        sid = s["id"]; has = sid in g.DESC_REF
        st = status_of(sid, has); counts[st] = counts.get(st, 0) + 1
        if has:
            r = g.DESC_REF[sid]; cz, en = NAMES[r]
            page = f'IOF s. {tr_page(rasters, r)}'
            mates = [nm[x]["name"] for x in byref[r] if x != sid]
            pic = f'<svg class="p"><use href="#n{r}"/></svg>'; org = f'<svg class="p"><use href="#o{r}"/></svg>'
            iscd = f'<b>{r}</b> {html.escape(cz)}<br><span class="en">{html.escape(en)}</span><br><span class="pg">{page}</span>'
            share = html.escape(", ".join(mates)) if mates else "–"
        else:
            pic = org = '<span class="none">–</span>'
            iscd = "bez piktogramu"; share = "–"
        note = NOTES.get(sid, "")
        if has and not note and st == "změněno": note = "Dřívější kresba se lišila od originálu, překresleno podle něj."
        if not has: note = note or "Značka z kapitoly 7 ISOM (dotisk), ISCD pro ni piktogram nemá."
        rows.append(
            f'<tr class="{st.replace(" ", "-")}" data-st="{st}"><td><svg class="m" viewBox="0 0 100 100">{s["svg"]}</svg></td>'
            f'<td><b>{html.escape(s["name"])}</b><br><span class="isom">{html.escape(s["isom"])}</span></td>'
            f'<td class="c">{org}</td><td class="c">{pic}</td><td>{iscd}</td><td>{share}</td>'
            f'<td><span class="st">{st}</span></td><td class="note">{html.escape(note)}</td></tr>')

    groups = [[nm[x]["name"] for x in v] for r, v in sorted(byref.items(), key=lambda kv: [int(x) for x in kv[0].split(".")]) if len(v) > 1]
    glist = "".join(f"<li><b>{html.escape(r)}</b> {html.escape(NAMES[r][0])}: {html.escape(', '.join(nm[x]['name'] for x in v))}</li>"
                    for r, v in sorted(byref.items(), key=lambda kv: [int(x) for x in kv[0].split(".")]) if len(v) > 1)
    only24 = ", ".join(nm[k]["name"] for k in g.ISCD_ONLY_2024)
    page = f'''<!DOCTYPE html>
<html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kontrola piktogramů ISCD</title>
<style>
body{{font:15px/1.4 system-ui,Segoe UI,sans-serif;margin:16px;color:#222;background:#fff}}
h1{{font-size:24px;margin:0 0 4px}} h2{{font-size:18px;margin:22px 0 6px}}
.meta{{color:#555;max-width:900px}} .legend span{{display:inline-block;margin:2px 10px 2px 0}}
table{{border-collapse:collapse;width:100%;margin-top:10px}}
th,td{{border:1px solid #ccc;padding:6px 8px;vertical-align:middle;text-align:left}}
thead th{{background:#eee;position:sticky;top:0}} tr.sec th{{background:#dde6ee;font-size:16px}}
svg.m{{width:60px;height:60px;display:block;background:#fff;border:1px solid #bbb}}
svg.p{{width:84px;height:84px;display:block;background:#fff;border:1px solid #888}}
td.c{{text-align:center;width:96px}} .none{{color:#999}}
.isom,.en,.pg{{color:#666;font-size:13px}} .st{{font-weight:700;white-space:nowrap}}
tr.změněno .st{{color:#b45f00}} tr.nové .st{{color:#0a7d2c}} tr.jen-2024 .st{{color:#7a2fb0}} tr.beze-změny .st{{color:#555}}
.note{{font-size:13px;max-width:360px}}
.filter label{{margin-right:14px;cursor:pointer}}
ul{{max-width:900px}}
@media (max-width:800px){{.note{{max-width:none}}}}
</style></head><body>
{"".join(syms)}
<h1>Kontrola piktogramů popisů kontrol</h1>
<p class="meta">Závazný zdroj: ISCD 2024 (originál IOF <code>ISCD-2024-IOF.pdf</code>, český překlad ČSOS <code>ISCD-2024-cz-CSOS.pdf</code>), přepínač <code>ISCD_2024 = {g.ISCD_2024}</code> v <code>gen_symbols.py</code>.
Sloupec <b>Originál</b> je výřez přímo z PDF, sloupec <b>V&nbsp;hře</b> je vektorizovaná kopie, kterou hra kreslí (obě ve stejném měřítku, mají se krýt).
Strany jsou z originálu IOF 2024. Stránku generuje <code>zdroje/build_kontrola.py</code>.</p>
<p class="legend"><b>Stav:</b>
<span><b>změněno</b> – piktogram se oproti dřívější hře liší</span><span><b>nové</b> – značka piktogram dřív neměla, ISCD 2018 i 2024 ho dávají</span>
<span><b>jen 2024</b> – přiřazuje až ISCD 2024 ({html.escape(only24)})</span><span><b>beze změny</b> – dřívější kresba tvarově odpovídala originálu (nebo značka piktogram nemá)</span></p>
<p class="filter"><b>Zobrazit:</b> <label><input type="checkbox" data-f="změněno" checked> změněno ({counts.get("změněno",0)})</label>
<label><input type="checkbox" data-f="nové" checked> nové ({counts.get("nové",0)})</label>
<label><input type="checkbox" data-f="jen 2024" checked> jen 2024 ({counts.get("jen 2024",0)})</label>
<label><input type="checkbox" data-f="beze změny" checked> beze změny ({counts.get("beze změny",0)})</label></p>
<h2>Značky se sdíleným piktogramem</h2>
<ul>{glist}</ul>
<h2>Všechny značky hry ({len(g.S)}, z toho {len(g.DESC_REF)} s piktogramem)</h2>
<table><thead><tr><th>Mapová značka</th><th>Název a ISOM</th><th>Originál ISCD 2024</th><th>V&nbsp;hře</th><th>Číslo ISCD, název, strana</th><th>Sdílí piktogram s</th><th>Stav</th><th>Poznámka</th></tr></thead><tbody>
{"".join(rows)}
</tbody></table>
<script>
document.querySelectorAll(".filter input").forEach(i=>i.onchange=()=>{{ const on=new Set([...document.querySelectorAll(".filter input:checked")].map(x=>x.dataset.f)); document.querySelectorAll("tbody tr[data-st]").forEach(r=>r.hidden=!on.has(r.dataset.st)); }});
</script>
</body></html>
'''
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f: f.write(page)
    print("zapsáno", OUT, "| stavy:", counts, "| velikost", len(page))


def tr_page(rasters, r): return rasters[r]["page"]


if __name__ == "__main__":
    main()
