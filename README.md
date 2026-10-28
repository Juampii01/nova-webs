# Nova Webs

Vidriera de muestras de webs a medida de Nova Softwares.

- `/` — la vidriera: cada muestra con su captura, "Ver web", "Ver en celular" y "Quiero una así" (WhatsApp).
- `/vauren` — Vauren, relojería de lujo.
- `/desvelo` — Desvelo, ropa urbana.

Todas las marcas de las muestras son inventadas.

## Publicar en Vercel

1. vercel.com → *Add New → Project* → importar `Juampii01/nova-webs`.
2. *Framework preset:* Other. Sin comando de build. *Output directory:* la raíz.
3. *Deploy.* Cada push a `main` vuelve a publicar.

## Sumar una muestra

Ver [CLAUDE.md](CLAUDE.md). Resumen: carpeta nueva con `index.html`, `img/` y `ficha.json`, y después:

```bash
python3 scripts/catalogo.py --capturas
```
