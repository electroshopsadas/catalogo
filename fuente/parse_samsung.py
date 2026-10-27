import json,re
COL={'DOURADO':'Dorado','PRETO':'Negro','PRET':'Negro','ROXO':'Violeta','VERDE':'Verde','CINZA':'Gris','AZUL':'Azul','BRANCO':'Blanco','BRAN':'Blanco',
'CINZA/VERDE':'Gris verdoso','CINZA CLARO':'Gris claro','CINZA/CLARO':'Gris claro','ROSA':'Rosa','AZUL CLARO':'Celeste','AZUL/SILV':'Celeste',
'TIT BLACK':'Titanio negro','TIT GRAY':'Titanio gris','TIT SIL/BLU':'Titanio plateado'}
rows=[]
for i in json.load(open('src/samsung.json')):
    n=i['name'].replace('CEL SAMSUNG ','').replace(' ULTR DU ',' ULTRA DUAL ')
    m=re.match(r'(\S+)/DS (.*?) DUAL (\d\.\d)" (\d+)(?:GB)?\+(\d+)(?:GB)?\s*\(?(LTE|5G)',n)
    code,mod,scr,ram,rom,net=m.groups()
    col=re.search(r'\d+MP?/\d+MP? (.*)$',n).group(1)
    mod='Galaxy '+mod.replace('ULTRA','Ultra')
    rows.append(dict(sub='Samsung',name=f'{mod} ({code})',detail=f'{scr}" · {ram}GB+{rom}GB · {"4G" if net=="LTE" else "5G"} · Dual SIM',color=COL[col],note='',cod=i['cod'],pricing='cel',v=i['usd'],img=i['img']))
json.dump(rows,open('src/samsung_rows.json','w'),ensure_ascii=False,indent=0)
for r in rows: print(r['name'],'|',r['detail'],'|',r['color'],r['v'])
