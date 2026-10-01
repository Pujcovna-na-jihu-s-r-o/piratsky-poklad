import pathlib
from playwright.sync_api import sync_playwright

here = pathlib.Path(__file__).resolve().parent
src = (here / "karticky-tisk.html").as_uri()
outdir = here.parent / "deti-2trida"
outdir.mkdir(parents=True, exist_ok=True)
out = str(outdir / "karticky-obrazkove-tisk.pdf")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(src, wait_until="networkidle")
    try:
        pg.wait_for_function("window.__ready===true", timeout=10000)
    except Exception as e:
        print("warn wait:", e)
    pg.pdf(path=out, format="A4", print_background=True,
           margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
    b.close()

print("OK", out)
