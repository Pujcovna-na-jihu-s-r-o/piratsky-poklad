# -*- coding: utf-8 -*-
"""Vytáhne piktogramy popisů kontrol z originálu ISCD 2024 (IOF) a převede je na SVG cesty.

Vstup:  zdroje/ISCD-2024-IOF.pdf (originál), zdroje/ISCD-2024-cz-CSOS.pdf (jen pro čísla stran)
Výstup: zdroje/iscd_piktogramy.json  { "1.14": {"d": "M…Z…", "pageIOF": 7, "pageCZ": 7}, … }

Piktogramy jsou v originále rastrové obrázky (cca 105 px), proto se vektorizují: obrázek se zvětší,
hranice černé/bílé se najde (marching squares) a zjednoduší na malé polygony. Výsledek věrně kopíruje
originál včetně tloušťky čar; kreslí se jako vyplněná cesta (fill-rule evenodd) ve čtverci 100×100,
buňka originálu (cca 22,7 pt) odpovídá 70 jednotkám.
Řádky 15.x (vektory v PDF) se vyrenderují ve velkém rozlišení a vektorizují stejně.

Spuštění:  python zdroje/trace_iscd.py     (vyžaduje pymupdf, opencv-python, scikit-image, numpy, pillow)
"""
import io, json, os, re
import cv2, numpy as np, pymupdf
from PIL import Image
from skimage import measure

HERE = os.path.dirname(os.path.abspath(__file__))
IOF = os.path.join(HERE, "ISCD-2024-IOF.pdf")
CZ = os.path.join(HERE, "ISCD-2024-cz-CSOS.pdf")
OUT = os.path.join(HERE, "iscd_piktogramy.json")

CELL_PT = 22.7      # velikost buňky piktogramu v originále (pt)
CELL_UNITS = 70.0   # …a její velikost v jednotkách viewBoxu 100×100
UP = 4              # zvětšení před vektorizací
RENDER_DPI = 600    # rozlišení, ve kterém se renderuje vektorový řádek 15.3
TOL = 2.5           # tolerance zjednodušení polygonu (v pixelech zvětšeného obrazu)


def trace(gray, units_per_px):
    """gray: 2D float 0..1 (1 = bílá). Vrací řetězec SVG cesty se středem obrázku v bodě 50,50."""
    h, w = gray.shape
    big = np.clip(cv2.resize(gray, (w * UP, h * UP), interpolation=cv2.INTER_CUBIC), 0, 1)
    big = np.pad(big, 2, constant_values=1.0)
    parts = []
    for c in measure.find_contours(big, 0.5):
        c = c - 2
        if len(c) < 4:
            continue
        c = measure.approximate_polygon(c, TOL)
        if len(c) < 4:
            continue
        y, x = c[:, 0], c[:, 1]
        if 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))) < 6:   # šum
            continue
        pts = [(50 + (xx / UP - w / 2) * units_per_px, 50 + (yy / UP - h / 2) * units_per_px) for yy, xx in c[:-1]]
        parts.append("M" + "L".join(f"{px:.1f} {py:.1f}" for px, py in pts) + "Z")
    return "".join(parts)


def ref_words(page):
    return [w for w in page.get_text("words") if re.fullmatch(r"\d+\.\d+", w[4]) and w[0] < 100]


def glyph_images():
    """Rastry piktogramů z originálu: {ref: {"img": PIL.Image (RGB, bílé pozadí), "wpt": šířka buňky v pt, "page": strana IOF}}.
    15.3 (vektor v PDF) se vyrenderuje; jeho "wpt" je šířka výřezu v pt."""
    out = {}
    d = pymupdf.open(IOF)
    for pn in range(5, 17):
        p = d[pn]
        words = ref_words(p)
        for b in p.get_text("dict")["blocks"]:
            if b["type"] != 1 or b["bbox"][0] > 130 or not words:
                continue
            yc = (b["bbox"][1] + b["bbox"][3]) / 2
            w = min(words, key=lambda w: abs((w[1] + w[3]) / 2 - yc))
            im = Image.open(io.BytesIO(b["image"])).convert("RGBA")
            bg = Image.new("RGBA", im.size, "white")
            bg.alpha_composite(im)
            out[w[4]] = {"img": bg.convert("RGB"), "wpt": b["bbox"][2] - b["bbox"][0], "page": pn + 1}
    # 15.3 – vektorová kresba v tabulce zvláštních řádků (s. 17), vyrenderuje se ve vysokém rozlišení
    r = pymupdf.Rect(154.4 - 1, 123.1 - 1, 181.6 + 1, 134.1 + 1)
    pm = d[16].get_pixmap(dpi=RENDER_DPI, clip=r)
    out["15.3"] = {"img": Image.frombytes("RGB", (pm.width, pm.height), pm.samples), "wpt": r.width, "page": 17}
    return out


def main():
    out = {}
    for ref, g in glyph_images().items():
        gray = np.asarray(g["img"].convert("L"), dtype=np.float32) / 255.0
        if ref == "15.3":
            upx = 2.7 * 72.0 / RENDER_DPI       # řádky 15.x jsou větší než buňka: 2,7 jednotky na pt
        else:
            upx = (CELL_UNITS / CELL_PT) * g["wpt"] / gray.shape[1]
        out[ref] = {"d": trace(gray, upx), "pageIOF": g["page"]}
    # čísla stran českého překladu
    c = pymupdf.open(CZ)
    for pn in range(5, 19):
        for w in ref_words(c[pn]):
            if w[4] in out and "pageCZ" not in out[w[4]]:
                out[w[4]]["pageCZ"] = pn + 1
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, sort_keys=True, indent=0)
    print("piktogramů:", len(out), "znaků:", sum(len(v["d"]) for v in out.values()))


if __name__ == "__main__":
    main()
