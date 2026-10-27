# Actualiza sitio/cotizacion.json con el USDT de Binance P2P (promedio de las primeras 5 ofertas).
# Si Binance no responde desde el servidor, usa CriptoYa (que lee las ofertas de Binance P2P).
import json, urllib.request, datetime, sys
def binance():
    body=json.dumps({"asset":"USDT","fiat":"ARS","tradeType":"BUY","page":1,"rows":5,"payTypes":[],"publisherType":None}).encode()
    req=urllib.request.Request("https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search",data=body,headers={"Content-Type":"application/json","User-Agent":"Mozilla/5.0"})
    d=json.load(urllib.request.urlopen(req,timeout=30))["data"]
    p=[float(x["adv"]["price"]) for x in d]
    assert len(p)>=3
    return round(sum(p)/len(p),1),"binance"
def criptoya():
    req=urllib.request.Request("https://criptoya.com/api/binancep2p/USDT/ARS/100",headers={"User-Agent":"Mozilla/5.0"})
    k=json.load(urllib.request.urlopen(req,timeout=30))
    assert k["totalAsk"]>0
    return round(k["totalAsk"],1),"criptoya-binancep2p"
try: dolar,fuente=binance()
except Exception as e:
    print("Binance falló:",e); dolar,fuente=criptoya()
prev=json.load(open("sitio/cotizacion.json"))["dolar"]
if abs(dolar-prev)/prev>0.15: sys.exit(f"Cambio sospechoso {prev} -> {dolar}, no se publica")
ar=datetime.datetime.utcnow()-datetime.timedelta(hours=3)
json.dump({"dolar":dolar,"actualizado":ar.strftime("%d/%m/%Y %H:%M"),"fuente":fuente},open("sitio/cotizacion.json","w"),ensure_ascii=False)
print(prev,"->",dolar,fuente)
