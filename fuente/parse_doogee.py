import json,re
C={'ROXO':'violeta','PRETO':'negro','VERDE':'verde','SILVER':'plateado','AMARELO':'amarillo','CINZA':'gris','AZUL':'azul','CI':'gris'}
def col(s):
    p=[C[x] for x in s.split('/')]; t=' y '.join(p) if len(p)>1 else p[0]; return t[0].upper()+t[1:]
cel=[];tab=[]
for i in json.load(open('src/doogee.json')):
    n=i['name']
    if n.startswith('CEL '):
        n=n.replace('CEL DOOGEE ','')
        m=re.match(r'(.*?) DUAL (\d\.\d+)" (\d+)GB\+(\d+)(GB|TB) (LTE|5G) \S+ (\S+)$',n)
        mod,scr,ram,rom,u,net,c=m.groups(); rom=rom+u
        mod=re.sub(r'BLADE(\d+)',r'Blade \1',mod).title().replace('V Max Lr','V Max LR').replace('S200 Ultra','S200 Ultra')
        cel.append(dict(sub='Doogee',name='Doogee '+mod,detail=f'{scr}" · {ram}GB+{rom} · {"4G" if net=="LTE" else "5G"} · Dual SIM',color=col(c),note='',cod=i['cod'],pricing='celdu',v=i['usd'],img=i['img']))
    else:
        n=n.replace('TABLET DOOGEE ','')
        note=''
        if re.search(r'\+CAPA? TRANSPARENT',n): note='Incluye funda transparente y kit'
        elif re.search(r'\+CAPA?|CAP CI',n): note='Incluye funda y kit'
        m=re.match(r'(.*?)\s+(?:DUAL\s+)?(\d+(?:\.\d)?)"\s+(\d+)GB\+(\d+)GB\s+(WIFI|LTE)\s+(\S+?)(?:\+|\s|$)',n)
        mod,scr,ram,rom,net,c=m.groups()
        mod=mod.replace('VIP EDIT AGILE','Agile VIP Edition').replace('VIP EDITION','VIP Edition').replace('(A)','')
        mod=' '.join(w if w in('VIP',) else w.title() for w in mod.split())
        conn='Wi-Fi' if net=='WIFI' else '4G con chip · Wi-Fi'
        tab.append(dict(sub='Doogee',name='Doogee '+mod,detail=f'{scr}" · {ram}GB+{rom}GB · {conn}',color=col(c),note=note,cod=i['cod'],pricing='tab',v=i['usd'],img=i['img']))
json.dump(cel,open('src/doogee_rows.json','w'),ensure_ascii=False,indent=0)
json.dump(tab,open('src/tab_doogee_rows.json','w'),ensure_ascii=False,indent=0)
for r in cel+tab: print(r['pricing'],r['name'],'|',r['detail'],'|',r['color'],'|',r['note'],r['v'])
