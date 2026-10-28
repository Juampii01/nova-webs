# Nova Webs

Vidriera de muestras de webs de Nova Softwares. Se usa para vender webs a medida:
el cliente abre la vidriera, mira las muestras en computadora y celular, y escribe por WhatsApp.

## Estructura

- `index.html` — la vidriera. La lista de muestras está en `<script id="catalogo">` y la genera `scripts/catalogo.py`: no se edita a mano.
- `<carpeta>/` — una muestra por carpeta, en la raíz (la carpeta es la URL: `/vauren`). Cada una tiene:
  - `index.html` — la web, autocontenida (CSS y JS adentro)
  - `img/` — sus imágenes
  - `ficha.json` — nombre, rubro, estructura, descripcion, destacado, fecha, orden
  - `portada.jpg` (1600×1000) y `celular.jpg` (390×844 @2x) — capturas para la vidriera
- `scripts/catalogo.py` — lee las fichas, saca capturas y actualiza la vidriera.

## Sumar una muestra nueva

1. Diseñarla y construirla con la skill `web-crear` (pack Web Agent Skills): estructura del rubro, plan de diseño propio, cero señales de plantilla.
2. Guardarla en una carpeta nueva en la raíz, con nombre corto en minúsculas y sin espacios (`maison-ivre`, `casa-norte`).
3. Correr el detector y no seguir hasta que dé 90 o más:
   `python3 <ruta a web-crear>/scripts/revisar.py <carpeta>/index.html`
4. Escribir su `ficha.json` (ver `vauren/ficha.json`).
5. `python3 scripts/catalogo.py --capturas` para sumar la captura y actualizar la vidriera.
6. Revisar la vidriera en el navegador (`python3 -m http.server` y abrir http://localhost:8000) y probar "Ver en celular".

## Reglas de las muestras

- **Marcas inventadas siempre.** Nada de nombres, logos ni productos de marcas reales. La vidriera lo aclara en el pie.
- **Cada muestra con identidad propia:** paleta, tipografía y momento memorable distintos de las demás. Si dos muestras se parecen, una sobra.
- Imágenes generadas o propias; nunca fotos de personas reales sacadas de internet.
- Sin datos inventados que parezcan reales (reseñas con nombre de personas reales, cifras de clientes).
- Librerías desde CDN con versión fija (GSAP, ScrollTrigger, Lenis) y respeto por `prefers-reduced-motion`.

## Publicación

Sitio estático. En Vercel: importar el repo, sin framework ni comando de build, carpeta raíz `/`. Cada push a `main` publica.

## WhatsApp

El número está en la constante `WHATSAPP` al principio del script de `index.html`.
