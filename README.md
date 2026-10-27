# Catálogo Electro Shop Sadas

- `sitio/` → la página publicada (Cloudflare Pages, carpeta de salida: `sitio`).
  - `sitio/index.html`: diseño y configuración (cotización USDT, recargos, WhatsApp).
  - `sitio/productos.json`: todos los productos.
  - `sitio/img_*.jpg`: fotos de los productos.
- `fuente/` → listas de origen y scripts para regenerar el catálogo.

La cotización (línea `dolar:` en `sitio/index.html`) se actualiza a las 9:00 y 21:00 con el promedio de las primeras 5 ofertas de USDT en Binance P2P.
