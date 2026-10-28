#!/usr/bin/env python3
"""
catalogo.py — arma la vidriera de Nova Webs a partir de las carpetas de muestras.

Cada carpeta en la raíz que tenga un ficha.json es una muestra. El script:
  1. lee todas las fichas y las ordena por "orden" (y después por fecha),
  2. las escribe dentro de index.html (bloque <script id="catalogo">),
  3. con --capturas, saca portada.jpg (1600×1000) y celular.jpg (390×844)
     de cada muestra que no las tenga (o de todas con --rehacer).

Uso:
    python3 scripts/catalogo.py               # solo actualiza la vidriera
    python3 scripts/catalogo.py --capturas    # + capturas que falten
    python3 scripts/catalogo.py --capturas --rehacer

Las capturas necesitan Playwright para Python:
    pip install playwright && python3 -m playwright install chromium
"""
import http.server
import json
import re
import sys
import threading
from functools import partial
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CAMPOS = ["nombre", "rubro", "estructura", "descripcion", "destacado"]
ESPERA_MS = 4500  # deja terminar la animación de entrada antes de capturar


def leer_fichas():
    fichas, errores = [], []
    for carpeta in sorted(p for p in RAIZ.iterdir() if p.is_dir() and (p / "ficha.json").exists()):
        try:
            f = json.loads((carpeta / "ficha.json").read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errores.append(f"{carpeta.name}/ficha.json no es JSON válido: {e}")
            continue
        faltan = [c for c in CAMPOS if not f.get(c)]
        if faltan:
            errores.append(f"{carpeta.name}/ficha.json: faltan {', '.join(faltan)}")
        if not (carpeta / "index.html").exists():
            errores.append(f"{carpeta.name}: falta index.html")
        f["carpeta"] = carpeta.name
        fichas.append(f)
    fichas.sort(key=lambda f: (f.get("orden", 999), f.get("fecha", "")))
    return fichas, errores


def escribir_vidriera(fichas):
    index = RAIZ / "index.html"
    html = index.read_text(encoding="utf-8")
    datos = [{k: f.get(k, "") for k in CAMPOS + ["carpeta"]} for f in fichas]
    bloque = json.dumps(datos, ensure_ascii=False, indent=2).replace("</", "<\\/")
    nuevo, n = re.subn(r'(<script id="catalogo" type="application/json">)(.*?)(</script>)',
                       lambda m: m.group(1) + bloque + m.group(3), html, flags=re.S)
    if n != 1:
        sys.exit('No encontré <script id="catalogo" type="application/json"> en index.html')
    index.write_text(nuevo, encoding="utf-8")


def capturar(fichas, rehacer):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("Falta Playwright: pip install playwright && python3 -m playwright install chromium")
    manejador = partial(http.server.SimpleHTTPRequestHandler, directory=str(RAIZ))
    manejador.log_message = lambda *a: None
    servidor = http.server.ThreadingHTTPServer(("127.0.0.1", 0), manejador)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{servidor.server_port}"
    tomas = [("portada.jpg", {"width": 1600, "height": 1000}), ("celular.jpg", {"width": 390, "height": 844})]
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for f in fichas:
            for archivo, tam in tomas:
                destino = RAIZ / f["carpeta"] / archivo
                if destino.exists() and not rehacer:
                    continue
                pagina = nav.new_page(viewport=tam, device_scale_factor=2 if tam["width"] < 500 else 1)
                pagina.goto(f"{base}/{f['carpeta']}/", wait_until="networkidle")
                pagina.wait_for_timeout(ESPERA_MS)
                pagina.screenshot(path=str(destino), type="jpeg", quality=82)
                pagina.close()
                print(f"  captura {f['carpeta']}/{archivo}")
        nav.close()
    servidor.shutdown()


def main():
    fichas, errores = leer_fichas()
    if errores:
        print("Revisá esto antes de seguir:")
        for e in errores:
            print("  -", e)
        sys.exit(1)
    if "--capturas" in sys.argv:
        capturar(fichas, "--rehacer" in sys.argv)
    escribir_vidriera(fichas)
    print(f"Vidriera actualizada con {len(fichas)} muestra(s): {', '.join(f['nombre'] for f in fichas)}")


if __name__ == "__main__":
    main()
