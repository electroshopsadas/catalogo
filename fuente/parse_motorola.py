import json,re
COL={'AZ':'Azul','AZUL':'Azul','VD':'Verde','VERDE':'Verde','AZ/CL':'Azul claro','AZ/C':'Azul claro','AZ/ES':'Azul oscuro','AZ/E':'Azul oscuro',
'VD/CL':'Verde claro','VD/C':'Verde claro','CI':'Gris','CINZA':'Gris','CINZ CLA':'Gris claro','LARANJA':'Naranja','PRETO':'Negro','VRM':'Rosa','MAR':'Caqui','ROSA':'Rosa'}
def model(n):
    m=n.split(' ')[0]
    m=re.sub(r'^EDGE(\d+)',r'Edge \1',m)
    rest=n.split(' ',1)[1]
    extra=re.match(r'(FUSION|PRO|NEO|ULTRA|POWER)\b',rest)
    if extra: m+=' '+extra.group(1).title()
    if m.startswith('Edge'): return 'Motorola '+m
    if m.startswith('RAZR'): return 'Motorola Razr '+m[4:]
    return 'Moto '+m
rows=[]
for i in json.load(open('src/motorola.json')):
    n=i['name'].replace('CEL MOTOROLA ','')
    mem=re.search(r'(\d+)G(?:B)?\+(\d+)G?B?',n); ram,rom=mem.groups()
    scr=re.search(r'(\d\.\d+)"',n).group(1)
    net='5G' if '5G' in n else '4G'
    sim='1 chip + eSIM' if '1CH+ES' in n else ('1 chip' if '1CH' in n else 'Dual SIM')
    notes=[]
    if re.search(r'CX ?SL',n): notes.append('Caja slim')
    if '3PIN' in n: notes.append('Cargador 3 pines')
    tail=re.split(r'\)|\d+MP?/\d+MP?|\d+/\d+',n)[-1].strip()
    color=COL.get(tail,'?'+tail)
    rows.append(dict(sub='Motorola',name=model(n),detail=f'{scr}" · {ram}GB+{rom}GB · {net} · {sim}',color=color,note=', '.join(notes),cod=i['cod'],pricing='cel',v=i['usd'],img=i['img']))
json.dump(rows,open('src/motorola_rows.json','w'),ensure_ascii=False,indent=0)
for r in rows: print(r['name'],'|',r['detail'],'|',r['color'],'|',r['note'],r['v'])
