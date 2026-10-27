import json,re,sys
exec(open('assemble.py').read().split("for o in json.load(open('lists.json')):")[0].split('P=[]')[1])
def clean(n):
    n=re.sub(r'^PERFUME (FEM|MAS|UNISS?EX)\s+','',n); n=n.replace('KIT PERFUME UNISSEX','KIT').replace('UNISSEX','UNISEX')
    for a,b in [('(CX FEIA)','(CAJA DAÑADA)'),('CX FEIA','CAJA DAÑADA'),('CX BRANCA','CAJA BLANCA'),('CX BRA','CAJA BLANCA'),('FRASCO DANIFICADO','FRASCO DAÑADO'),('FRASCO DANIFIC','FRASCO DAÑADO'),('(S/LACRE)',''),('S/LACRE','')]: n=n.replace(a,b)
    return re.sub(r'\s*\(\d{4,6}\)?\s*$','',tc(n)).strip()
src,sub,out=sys.argv[1:4]
rows=[]
for o in json.load(open(src)):
    if re.search(r'S/LAC',o['name']): continue
    rows.append(dict(sub=sub,name=clean(o['name']),detail='',color='',note='',cod=o['cod'],pricing='perf',v=o['usd'],img=o['img']))
json.dump(rows,open(out,'w'),ensure_ascii=False)
print(sub,len(rows)); [print(' ',r['name'],r['v']) for r in rows[::120]]
