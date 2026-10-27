import json,re
COL={'BLACK':'Negro','BLUE':'Azul','PINK':'Rosa','TEAL':'Verde azulado','ULTRAMARINE':'Azul ultramar','WHITE':'Blanco','MIST BLUE':'Azul niebla',
'SAGE':'Verde salvia','COSMIC ORANGE':'Naranja cósmico','DEEP BLUE':'Azul profundo','SILVER':'Plateado','BURGUNDY':'Borgoña','GLACIER':'Glaciar','LAVENDER':'Lavanda'}
rows=[];seen=set()
for i in json.load(open('src/iphone.json')):
    if re.search(r'S/LAC',i['name']): continue  # sin precinto: no se publica
    n=i['name'].replace('CEL IPHONE ','')
    model='iPhone '+re.match(r'(.*?)\s+(?:DUAL\s+|ESIM\s+)*\d\.\d"',n).group(1).replace(' ESIM','').replace(' DUAL','').title()
    scr=re.search(r'(\d\.\d)"',n).group(1); mem=re.search(r'\d+GB\+\d+GB',n).group(0)
    sim=' · eSIM' if 'ESIM' in n else (' · Dual SIM' if 'DUAL' in n else '')
    note='Caja dañada' if 'CXF' in n else ''
    color=COL[re.sub(r'\s*\(?LL\)?$','',i['ref'].replace(' JP','').replace(' VC','')).strip()]
    k=(model,mem,color,note,i['usd'])
    if k in seen: continue
    seen.add(k)
    rows.append(dict(sub='iPhone',name=model,detail=f'{scr}" · {mem} · 5G{sim}',color=color,note=note,cod=i['cod'],pricing='cel',v=i['usd'],img=i['img']))
json.dump(rows,open('src/iphone_rows.json','w'),ensure_ascii=False,indent=0)
for r in rows: print(r['name'],'|',r['detail'],'|',r['color'],'|',r['note'],r['v'])
