import json,re
COL={'PRETO':'Negro','PRET':'Negro','PRE':'Negro','PR':'Negro','VERDE':'Verde','VRD':'Verde','VD':'Verde','AZUL':'Azul','AZU':'Azul','AZ':'Azul',
'BRANCO':'Blanco','BRAN':'Blanco','BRA':'Blanco','BR':'Blanco','ROXO':'Violeta','ROX':'Violeta','RX':'Violeta','DOURADO':'Dorado','DOURA':'Dorado',
'SILVER':'Plateado','SI':'Plateado','CINZA':'Gris','LARANJ':'Naranja','LAR':'Naranja','LA':'Naranja','AMA':'Amarillo','MA':'Marrón','AZU CL':'Celeste'}
OVR={'1607635':'Beige','1607642':'Beige'}
rows=[]
for i in json.load(open('src/xiaomi.json')):
    n=i['name'].replace('CEL XIAOMI ','')
    n=re.sub(r'(\d)"(\d)',r'\1" \2',n)
    m=re.match(r'(.*?)\s+DU(?:AL)?\s*(\d\.\d+)"',n)
    model=m.group(1).replace('17 ULT','17 ULTRA').replace('ULTRARA','ULTRA'); scr=m.group(2)
    mm=re.search(r'(\d+)G?B?\+(\d+)(GB|G|TB)?',n); ram,rom,u=mm.groups(); rom=rom+('TB' if u=='TB' else 'GB')
    net='5G' if ' 5G' in n else '4G'
    notes=[]
    if re.search(r'CX ?SL',n): notes.append('Caja slim')
    if re.search(r'CXF|CX FE',n): notes.append('Caja dañada')
    if 'CARRE' in n: notes.append('Incluye cargador')
    if '3PIN' in n: notes.append('Cargador 3 pines')
    if 'CN SF GL' in n: notes.append('Versión China (idioma inglés/chino)')
    t=re.sub(r'\+CARREG?$','',n.strip()); t=re.sub(r'\s*SG$','',t); t=re.sub(r'SG$','',t)
    if t.endswith('AZU CL'): c='AZU CL'
    else: c=re.split(r'[\s\)]',t)[-1]
    c=re.sub(r'^(GLOBAL|GLOBA|GLOB|GLO|GL)','',c)
    color=OVR.get(i['cod'],COL.get(c,'?'+c))
    fam=model.split()[0]
    sub='POCO' if model.startswith('POCO') else ('Redmi' if model.startswith('REDMI') else 'Xiaomi')
    mod=model.title().replace('Poco','POCO')
    if not mod.startswith(('POCO','Redmi')): mod='Xiaomi '+mod
    rows.append(dict(sub=sub,name=mod,detail=f'{scr}" · {ram}GB+{rom} · {net}',color=color,note=', '.join(notes),cod=i['cod'],pricing='cel',v=i['usd'],img=i['img']))
json.dump(rows,open('src/xiaomi_rows.json','w'),ensure_ascii=False,indent=0)
bad=[r for r in rows if r['color'].startswith('?')]
print(len(rows),'bad',bad)
for r in rows[:12]+rows[100:106]: print(r['name'],'|',r['detail'],'|',r['color'],'|',r['note'],r['v'])
