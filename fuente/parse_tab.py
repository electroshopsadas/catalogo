import json,re
REFC={'SILVER':'Plateado','BLUE':'Azul','PINK':'Rosa','SPACE GRAY':'Gris espacial','STARLIGHT':'Blanco estelar','PURPLE':'Violeta','SPACE BLACK':'Negro espacial'}
PT={'CINZA':'gris','CINZ':'gris','CI':'gris','CIN':'gris','PRETO':'negro','AZUL':'azul','AZ':'azul','VERDE':'verde','ROXO':'violeta','ROSA':'rosa','SILVER':'plateado','BRANCO':'blanco','LARANJA':'naranja','LARANJ':'naranja','DOURADO':'dorado','DOURAD':'dorado'}
def col(s):
    p=[PT[x] for x in s.split('/') if x in PT]
    if not p: return ''
    t=' y '.join(p); return t[0].upper()+t[1:]
rows=[];skipped=[]
for i in json.load(open('src/tab.json')):
    if re.search(r'S/LAC',i['name']): continue  # sin precinto: no se publica
    n=i['name']; u=i['usd']
    if u<80: skipped.append(n); continue
    note=[]
    if 'CX FEIA' in n: note.append('Caja dañada')
    if re.search(r'\+CAPA? TRANSP',n): note.append('Incluye funda transparente y kit' if 'KIT' in n else 'Incluye funda transparente')
    elif re.search(r'\+\s*CAPA?|\+CAP ',n): note.append('Incluye funda y kit' if re.search(r'\+\s*KI?T|KT\b',n) else 'Incluye funda')
    n2=re.sub(r'\(S/LACRE\)|CX FEIA','',n)
    if n.startswith('IPAD'):
        m=re.match(r'IPAD (11 \(A16\)|AIR|PRO) \S+ WIFI \((\d{4})\)(?: (M\d))? (\d+GB) (\d+)"',n2)
        kind,yr,chip,rom,scr=m.groups()
        name={'11 (A16)':'iPad 11" (A16)','AIR':f'iPad Air {scr}" {chip}','PRO':f'iPad Pro {scr}" {chip}'}[kind]
        conn='Wi-Fi + celular' if re.search(r'\bCEL',n2) else 'Wi-Fi'
        rows.append(dict(sub='iPad',name=name,detail=f'{rom} · {conn} · {yr}',color=REFC[i['ref']],note=', '.join(note),cod=i['cod'],pricing='tab',v=u,img=i['img']))
        continue
    t=n2.replace('TABLET ','')
    m=re.match(r'(.*?)\s+(?:DUAL\s+)?(\d+(?:\.\d+)?)"(?:\s*\(.*?\))?\s+(\d+)GB\+(\d+)GB\s*(WIFI|LTE|5G)?\s*(.*)$',t)
    if not m: print('FAIL',n); continue
    mod,scr,ram,rom,net,rest=m.groups()
    c=col(re.split(r'\+',rest)[0].strip().replace(' ',''))
    brand=mod.split()[0]
    if mod.startswith('BLACK SHARK'): brand='Black Shark'
    mod=' '.join(w if re.search(r'\d',w) and not w.isdigit() else w.title() for w in mod.split()).replace('Poco','POCO').replace('Pad Se','Pad SE')
    brand={'XIAOMI':'Xiaomi','SAMSUNG':'Samsung','BLACKVIEW':'Blackview','DOOGEE':'Doogee','HOTWAV':'Hotwav','ULEFONE':'Ulefone','MOX':'MOX'}.get(brand,brand)
    if brand=='Samsung': mod=mod.replace('Samsung X133','Samsung Galaxy Tab').replace('Samsung X135G','Samsung Galaxy Tab').replace('Samsung X230','Samsung Galaxy Tab')
    conn={'WIFI':'Wi-Fi','LTE':'4G con chip · Wi-Fi','5G':'5G con chip · Wi-Fi',None:'4G con chip · Wi-Fi' if 'DUAL' in n else 'Wi-Fi'}[net]
    rows.append(dict(sub=brand,name=re.sub(r'Vip Edit(ion)?','VIP Edition',mod).replace('(A)','').replace('Mox ','MOX '),detail=f'{scr}" · {ram}GB+{rom}GB · {conn}',color=c,note=', '.join(note),cod=i['cod'],pricing='tab',v=u,img=i['img']))
# dedupe same name/detail/color/note keep cheapest
best={}
for r in rows:
    k=(r['name'],r['detail'],r['color'],r['note'])
    if k not in best or r['v']<best[k]['v']: best[k]=r
rows=[r for r in rows if best[(r['name'],r['detail'],r['color'],r['note'])] is r]
json.dump(dict(id='tablets',label='Tablets',terms='<b>Precio minorista</b> por unidad. <b>Precio mayorista</b> comprando {minMay} unidades o más, combinables entre modelos y colores.',rows=rows),open('listas/02_tablets.json','w'),ensure_ascii=False)
print(len(rows),'skipped',skipped)
for r in rows: print(r['sub'],'|',r['name'],'|',r['detail'],'|',r['color'],'|',r['note'],r['v'])
