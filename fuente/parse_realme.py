import json,re
COL={'CINZA':'Gris','CINZ':'Gris','AZUL':'Azul','AZU':'Azul','DOURA':'Dorado','DO':'Dorado','PRETO':'Negro','PRE':'Negro','PR':'Negro','BRANCO':'Blanco',
'ROX':'Violeta','ROXO':'Violeta','VRD':'Verde','VERDE':'Verde','VD':'Verde','VD ESC':'Verde oscuro','SIL':'Plateado'}
rows=[]
for i in json.load(open('src/realme.json')):
    n=i['name'].replace('CEL REALME ','')
    m=re.match(r'(.*?) RMX\d+ DUAL (\d\.\d+)" (\d+)GB\+(\d+)GB (LTE|5G)',n)
    mod,scr,ram,rom,net=m.groups()
    mod=mod.title().replace('Note ','Note ').replace('100I','100i').replace('100X','100x').replace('60X','60x')
    col=re.search(r'\d+MP?/\d+MP? (.*)$',n).group(1)
    rows.append(dict(sub='Realme',name='Realme '+mod,detail=f'{scr}" · {ram}GB+{rom}GB · {"4G" if net=="LTE" else "5G"} · Dual SIM',color=COL[col],note='',cod=i['cod'],pricing='cel',v=i['usd'],img=i['img']))
json.dump(rows,open('src/realme_rows.json','w'),ensure_ascii=False,indent=0)
for r in rows: print(r['name'],'|',r['detail'],'|',r['color'],r['v'])
