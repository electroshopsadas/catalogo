import json,re
C={'PRETO':'negro','PRE':'negro','PR':'negro','SILVE':'plateado','SILVER':'plateado','AZUL':'azul','BRANCO':'blanco','CINZA':'gris'}
def col(s):
    p=[C[x] for x in s.split('/') if x]; t=' y '.join(p) if len(p)>1 else p[0]; return t[0].upper()+t[1:]
cel=[];tab=[]
for i in json.load(open('src/ulefone.json')):
    n=i['name']; note=[]
    if 'WALKIE' in n: note.append('Con walkie talkie')
    if 'THERMAL' in n: note.append('Cámara térmica')
    if '+CAPA' in n: note.append('Incluye funda')
    n=n.replace(' WALKIE TALKIE','').replace(' THERMAL','').replace('+CAPA','').replace(' ULT ',' ULTRA ')
    istab=n.startswith('TABLET')
    n=re.sub(r'^(CEL|TABLET) ULEFONE ','',n)
    m=re.match(r'(.*?) DU(?:AL)? (\d+(?:\.\d+)?)" (\d+)G(?:B)?\+(\d+)(?:GB|G)?(TB)? (LTE|5G) .*?(\S+)\s*$',n)
    if not m: print("FAIL",n); continue
    mod,scr,ram,rom,tb,net,c=m.groups(); rom=rom+('TB' if tb else 'GB')
    mod=' '.join(w.title() if not re.match(r'^\d',w) else w.upper() for w in mod.split()).replace('Rugking','RugKing')
    if istab:
        tab.append(dict(sub='Ulefone',name='Ulefone '+mod,detail=f'{scr}" · {ram}GB+{rom} · 4G con chip · Wi-Fi',color=col(c),note=', '.join(note),cod=i['cod'],pricing='tab',v=i['usd'],img=i['img']))
    else:
        cel.append(dict(sub='Ulefone',name='Ulefone '+mod,detail=f'{scr}" · {ram}GB+{rom} · {"4G" if net=="LTE" else "5G"} · Dual SIM',color=col(c),note=', '.join(note),cod=i['cod'],pricing='celdu',v=i['usd'],img=i['img']))
json.dump(cel,open('src/ulefone_rows.json','w'),ensure_ascii=False,indent=0)
json.dump(tab,open('src/tab_ulefone_rows.json','w'),ensure_ascii=False,indent=0)
for r in cel+tab: print(r['pricing'],r['name'],'|',r['detail'],'|',r['color'],'|',r['note'],r['v'])
