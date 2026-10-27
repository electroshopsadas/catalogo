import json,re
L=json.load(open('lists.json'))
KEEP=None
exec(open('assemble.py').read().split("for o in json.load(open('lists.json')):")[0].split('P=[]')[1])  # tc()
def phones(o):
    if o['sub']=='iPhone':
        if o['note'].startswith('Incluye'): return None
        if o['note']=='Sin precinto': o['note']=''
        if 'sin precinto' in o['note']: o['note']='Caja dañada'
        n=o['name']; mem=re.search(r'\d+GB\+\d+GB',n).group(0); scr=re.search(r'(\d\.\d)"',n).group(1)
        o['name']=re.split(r' \d\.\d"',n)[0].replace(' eSIM','')
        o['detail']=f'{scr}" · {mem} · 5G'+(' · eSIM' if 'eSIM' in n else '')
        o['color']={'Black':'Negro','Blue':'Azul','Pink':'Rosa','White':'Blanco','Lavender':'Lavanda','Cosmic Orange':'Naranja cósmico','Deep Blue':'Azul profundo','Silver':'Plateado'}.get(o['color'],o['color'])
    return o
def row(o,pricing,v): return dict(sub=o['sub'],name=o['name'],detail=o.get('detail',''),color=o.get('color',''),note=o.get('note',''),cod=o.get('cod',''),pricing=pricing,v=v,img=o['img'])
cel=[];seen=set()
for o in L:
    if o['cat']!='celulares': continue
    o=phones(o)
    if not o: continue
    k=(o['name'],o['detail'],o['color'],o['note'],o['usd'])
    if k in seen: continue
    seen.add(k); cel.append(row(o,'cel',o['usd']))
perf=[]
for o in L:
    if o['cat']=='perfumes':
        o['name']=re.sub(r'\s*\(\d{4,6}\)?\s*$','',tc(o['name'])).strip(); perf.append(row(o,'perf',o['usd']))
def eq(fn,cot,subf):
    out=[]
    for o in json.load(open(fn)):
        o['sub']=subf(o['name']); out.append(row(o,'eq',round(o['ars']/cot,4)))
    return out
def djifam(n):
    for k in ['Neo 2','Neo','Lito X1','Lito 1','Mini 5 Pro','Air 3S','Avata 2','Avata 360']:
        if f'DJI {k}' in n: return 'DJI '+k
def camfam(n):
    for k in ['Osmo 360','Osmo Action','Osmo Nano','Osmo Pocket']:
        if k in n: return k
LISTAS=[
 dict(id='celulares',label='Celulares',orden=1,terms='<b>Precio minorista</b> por unidad. <b>Precio mayorista</b> comprando {minMay} unidades o más, combinables entre modelos y colores.',rows=cel),
 dict(id='perfumes',label='Perfumes',orden=2,terms='Perfumes originales importados. <b>Compra mínima: {minPerf} unidades</b>, combinables.',rows=perf),
 dict(id='drones',label='Drones DJI',orden=3,promo=True,terms='<b>Promo por tiempo limitado</b>, del 22/10 al 04/11 o hasta agotar stock. Originales DJI, nuevos y sellados.',rows=eq('dji.json',1665,djifam)),
 dict(id='camaras-dji',label='Cámaras DJI',orden=4,terms='Originales DJI, nuevos y sellados, <b>con garantía oficial por 1 año</b>.',rows=eq('cam.json',1660,camfam)),
 dict(id='estabilizadores',label='Estabilizadores DJI',orden=5,terms='Originales DJI, nuevos y sellados, <b>con garantía oficial por 1 año</b>.',rows=eq('est.json',1660,lambda n:'Osmo Mobile' if 'Mobile' in n else 'Ronin RS')),
 dict(id='monopatines',label='Monopatines',orden=6,terms='Monopatines eléctricos nuevos y sellados, <b>con garantía por 3 meses</b>.',rows=eq('mono.json',1660,lambda n:n.split()[0])),
]
for l in LISTAS: json.dump(l,open(f"listas/{l['orden']:02d}_{l['id']}.json",'w'),ensure_ascii=False,indent=0)
print([(l['id'],len(l['rows'])) for l in LISTAS])
