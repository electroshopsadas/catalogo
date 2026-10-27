// Cotización USDT/ARS: promedio de las primeras 5 ofertas de compra en Binance P2P.
// Se guarda en caché hasta el próximo corte de las 9:00 o 21:00 (hora Argentina).
const BINANCE = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search";

function proximoCorte(now) {
  // Argentina = UTC-3. Cortes: 12:00 y 00:00 UTC (9:00 y 21:00 ART).
  const t = new Date(now);
  const h = t.getUTCHours();
  const next = new Date(Date.UTC(t.getUTCFullYear(), t.getUTCMonth(), t.getUTCDate(), h < 12 ? 12 : 24, 0, 0));
  return next.getTime();
}

export async function onRequestGet(context) {
  const cache = caches.default;
  const key = new Request(new URL("/api/usdt", context.request.url).toString());
  const hit = await cache.match(key);
  if (hit) return hit;
  try {
    const r = await fetch(BINANCE, {
      method: "POST",
      headers: { "Content-Type": "application/json", "User-Agent": "Mozilla/5.0" },
      body: JSON.stringify({ asset: "USDT", fiat: "ARS", tradeType: "BUY", page: 1, rows: 5, payTypes: [], publisherType: null }),
    });
    const j = await r.json();
    const precios = (j.data || []).map((x) => parseFloat(x.adv.price)).filter((x) => x > 0);
    if (precios.length < 3) throw new Error("sin ofertas");
    const dolar = Math.round((precios.reduce((a, b) => a + b, 0) / precios.length) * 10) / 10;
    const now = Date.now();
    const body = JSON.stringify({ dolar, ofertas: precios, actualizado: new Date(now).toISOString() });
    const ttl = Math.max(60, Math.floor((proximoCorte(now) - now) / 1000));
    const resp = new Response(body, { headers: { "Content-Type": "application/json", "Cache-Control": `public, max-age=${ttl}` } });
    context.waitUntil(cache.put(key, resp.clone()));
    return resp;
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e) }), { status: 502, headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
  }
}
