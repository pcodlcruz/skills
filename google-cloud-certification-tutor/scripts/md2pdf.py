#!/usr/bin/env python3
"""Convierte guías Markdown (tips, repaso de fallos...) en PDF imprimible.

Usa el paquete `markdown` (pip install markdown) y Chrome/Chromium en headless.
Uso, desde la raíz del proyecto:
    python3 scripts/md2pdf.py guia/tips.md guia/repaso-fallos.md
Genera el .pdf al lado de cada .md.
"""

import os
import shutil
import subprocess
import sys

try:
    import markdown
except ImportError:
    sys.exit("Falta el paquete 'markdown': pip3 install markdown")

CSS = """
@page { size: A4; margin: 16mm 14mm 18mm 14mm; }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: -apple-system, "Helvetica Neue", Arial, sans-serif;
       font-size: 10.2pt; line-height: 1.5; color: #1a1a1a; margin: 0; }
h1 { font-size: 21pt; border-bottom: 3px solid #1a73e8; padding-bottom: 6px;
     margin: 0 0 4px; color: #10275c; }
h2 { font-size: 15pt; color: #10275c; margin: 22px 0 8px; padding: 6px 10px;
     background: #eef3fc; border-left: 4px solid #1a73e8; border-radius: 3px;
     page-break-after: avoid; break-after: avoid; }
h3 { font-size: 12pt; color: #123; margin: 16px 0 6px;
     page-break-after: avoid; break-after: avoid; }
h2, h3, table, blockquote, pre { page-break-inside: avoid; }
p, li { orphans: 3; widows: 3; }
code { font-family: "SF Mono", Menlo, Consolas, monospace; font-size: 8.8pt;
       background: #f1f3f5; padding: 1px 4px; border-radius: 3px; color: #a3106b; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 8.9pt; }
th { background: #10275c; color: #fff; text-align: left; padding: 6px 8px;
     font-weight: 600; border: 1px solid #10275c; }
td { border: 1px solid #ccd3de; padding: 5px 8px; vertical-align: top; }
tr:nth-child(even) td { background: #f7f9fc; }
th code, td code { background: #e6ebf3; color: #7a0d50; font-size: 8.2pt; }
blockquote { margin: 10px 0; padding: 8px 12px; background: #fffbe9;
             border-left: 4px solid #f0b400; color: #4a3800; font-size: 9.5pt; }
blockquote code { background: #f3ead0; }
ul, ol { padding-left: 20px; margin: 8px 0; }
li { margin: 3px 0; }
hr { border: 0; border-top: 1px solid #d8dee8; margin: 18px 0; }
strong { color: #000; }
a { color: #1a73e8; text-decoration: none; }
"""

CANDIDATOS_CHROME = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


def buscar_chrome():
    for c in CANDIDATOS_CHROME:
        if os.path.exists(c):
            return c
    for nombre in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        ruta = shutil.which(nombre)
        if ruta:
            return ruta
    sys.exit("No encuentro Chrome/Chromium para generar el PDF.")


def convertir(md_path, pdf_path, chrome):
    with open(md_path, encoding="utf-8") as f:
        texto = f.read()
    html = markdown.markdown(texto, extensions=["tables", "fenced_code", "sane_lists", "attr_list"])
    titulo = os.path.basename(md_path)
    doc = (f'<!doctype html><html lang="es"><head><meta charset="utf-8">'
           f"<title>{titulo}</title><style>{CSS}</style></head><body>{html}</body></html>")
    tmp = pdf_path + ".html"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(doc)
    try:
        subprocess.run([chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        "--virtual-time-budget=4000", f"--print-to-pdf={pdf_path}",
                        "file://" + os.path.abspath(tmp)], check=True, capture_output=True)
    finally:
        os.remove(tmp)
    print(f"{pdf_path}  ({os.path.getsize(pdf_path) // 1024} KB)")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    chrome = buscar_chrome()
    for p in sys.argv[1:]:
        convertir(p, os.path.splitext(p)[0] + ".pdf", chrome)


if __name__ == "__main__":
    main()
