import json,re,os,collections
from PIL import Image
P=[]
KEEP={'EDP','EDT','EDC','ML','KIT','DE','CK','YSL','DKNY','JPG','CH','II','XS','UNISEX','EAU','PARFUM'}
def tc(n):
    n=n.replace('…','').strip()
    out=[]
    for w in re.split(r'(\s+)',n):
        if w.isspace() or not w: out.append(w); continue
        core=re.sub(r'[^A-Z]','',w)
        if core in ('EDP','EDT','EDC') or re.match(r'^\(?\d',w) or core in ('ML',) : out.append(w.replace('ML','ml') if re.match(r'^\d',w) else w)
        else: out.append(w.capitalize() if w.isalpha() else re.sub(r'[A-Za-z]+',lambda m:m.group(0).capitalize(),w))
    s=''.join(out)
    s=re.sub(r'\b(\d+)Ml\b',r'\1ml',s)
    return s
for o in json.load(open('lists.json')):
    if o['sub']=='iPhone':
        if o['note'].startswith('Incluye'): continue
        if o['note']=='Sin precinto': o['note']=''
        if 'sin precinto' in o['note']: o['note']='Caja dañada'
        n=o['name']; mem=re.search(r'\d+GB\+\d+GB',n).group(0); scr=re.search(r'(\d\.\d)"',n).group(1)
        o['name']=re.split(r' \d\.\d"',n)[0].replace(' eSIM','')
        o['detail']=f'{scr}" · {mem} · 5G'+(' · eSIM' if 'eSIM' in n else '')
        o['color']={'Black':'Negro','Blue':'Azul','Pink':'Rosa','White':'Blanco','Lavender':'Lavanda','Cosmic Orange':'Naranja cósmico','Deep Blue':'Azul profundo','Silver':'Plateado'}.get(o['color'],o['color'])
    if o['cat']=='perfumes': o['name']=re.sub(r'\s*\(\d{4,6}\)?\s*$','',tc(o['name'])).strip()
    P.append(o)
def fam(n):
    for k in ['Neo 2','Neo','Lito X1','Lito 1','Mini 5 Pro','Air 3S','Avata 2','Avata 360']:
        if f'DJI {k}' in n: return k
for o in json.load(open('dji.json')):
    P.append(dict(cat='drones',sub='DJI '+fam(o['name']),name=o['name'],detail=o['detail'],color='',note='',cod='',ars=o['ars'],pricing='fixed',img=o['img']))
for o in json.load(open('mono.json')):
    P.append(dict(cat='monopatines',sub=o['name'].split()[0],name=o['name'],detail=o['detail'],color='',note='',cod='',ars=o['ars'],pricing='fixed',img=o['img']))
os.makedirs('pub',exist_ok=True)
T=160; N=10; per=N*N
for k,p in enumerate(P): p['sp']=k
sheets=(len(P)+per-1)//per
for sh in range(sheets):
    cv=Image.new('RGB',(T*N,T*N),'white')
    for k in range(sh*per,min(len(P),(sh+1)*per)):
        im=Image.open(P[k]['img'])
        if im.mode!='RGB':
            im=im.convert('RGBA'); bg=Image.new('RGB',im.size,'white'); bg.paste(im,mask=im.split()[3]); im=bg
        im.thumbnail((T-6,T-6)); ix=k%per
        cv.paste(im,((ix%N)*T+(T-im.width)//2,(ix//N)*T+(T-im.height)//2))
    cv.save(f'pub/s{sh}.jpg',quality=74,optimize=True,progressive=True)
keys=['cat','sub','name','detail','color','note','cod','pricing','sp']
rows=[[p[k] for k in keys]+[p.get('usd',p.get('ars'))] for p in P]
json.dump(rows,open('pub/productos.json','w'),ensure_ascii=False,separators=(',',':'))
print(len(P),sheets,collections.Counter((p['cat']) for p in P))
for p in P[::150]: print(p['name'],'|',p['detail'],p['color'])
