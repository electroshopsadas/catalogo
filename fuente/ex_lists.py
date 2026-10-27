import pymupdf,re,json,os
O='/mnt/user-data/outputs/'
os.makedirs('raw',exist_ok=True)
def num(t): return int(t.replace('$','').replace('.','').strip())
CT=[(0,150,40,25),(150,300,50,30),(300,500,70,35),(500,800,75,40),(800,1300,85,50),(1300,2000,100,60),(2000,3000,130,70)]
def usd_cel(may,mn):
    for lo,hi,mi,ma in CT:
        u=round(may/1602-ma,2)
        if lo<u<=hi+0.999 and abs((u+mi)*1602-mn)<2: return u
    raise ValueError((may,mn))
PT=[(0,20,8),(20,70,12),(70,120,15),(120,9999,20)]
def usd_perf(a):
    for lo,hi,inc in PT:
        u=round(a/1600-inc,2)
        if lo<u<=hi: return u
    raise ValueError(a)
def img_save(d,xref,tag):
    x=d.extract_image(xref); f=f'raw/{tag}.{x["ext"]}'; open(f,'wb').write(x['image']); return f
out=[]
for fn,brand in [('iPhone','iPhone'),('Xiaomi','Xiaomi'),('Realme','Realme'),('Motorola','Motorola'),('Samsung','Samsung')]:
    d=pymupdf.open(O+f'Lista_Precios_{"iPhone" if fn=="iPhone" else "Celulares_"+fn}_ARS.pdf')
    for p in d:
        sp=[s for b in p.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if s['text'].strip()]
        imgs=[i for i in p.get_image_info(xrefs=True) if i['bbox'][0]<80 and i['bbox'][1]>110]
        for c in sp:
            m=re.search(r'Cód\. (\d+)',c['text'])
            if not m: continue
            y=c['bbox'][1]
            row=[s for s in sp if y-18<s['bbox'][1]<y+16 and s['bbox'][0]>80]
            name=[s for s in row if s['font']=='Helvetica-Bold' and s['size'] in (9,9.5) and s['bbox'][1]<y][-1]
            spec=[s['text'] for s in row if s['font']=='Helvetica' and abs(s['bbox'][1]-name['bbox'][1])<3]
            color=[s['text'] for s in row if s['text'].startswith('Color:')][0].replace('Color: ','')
            note=[s['text'] for s in row if 'Oblique' in s['font'] and s['bbox'][1]>y]
            pr=sorted([s for s in row if s['text'].startswith('$')],key=lambda s:s['bbox'][0])
            may,mn=num(pr[0]['text']),num(pr[1]['text'])
            im=[i for i in imgs if i['bbox'][1]-25<y<i['bbox'][3]+10]
            out.append(dict(cat='celulares',sub=brand,name=name['text'],detail=(spec[0] if spec else '').replace('  ·  ',' · ').replace('  ',' '),color=color,note=note[0] if note else '',cod=m.group(1),usd=usd_cel(may,mn),pricing='cel',img=img_save(d,im[0]['xref'],m.group(1))))
for fn,sub in [('Femeninos','Femeninos'),('Masculinos','Masculinos'),('Unisex','Unisex')]:
    d=pymupdf.open(O+f'Lista_Precios_Perfumes_{fn}_ARS.pdf')
    for p in d:
        sp=[s for b in p.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if s['text'].strip()]
        imgs=[i for i in p.get_image_info(xrefs=True) if i['bbox'][1]>110]
        for c in sp:
            m=re.search(r'Cód\. (\d+)',c['text'])
            if not m: continue
            cx=(c['bbox'][0]+c['bbox'][2])/2; y=c['bbox'][1]
            nm=[s for s in sp if abs((s['bbox'][0]+s['bbox'][2])/2-cx)<50 and y-50<s['bbox'][1]<y-2 and abs(s['size']-6.6)<0.1]
            nm.sort(key=lambda s:s['bbox'][1])
            pr=[s for s in sp if abs((s['bbox'][0]+s['bbox'][2])/2-cx)<50 and y<s['bbox'][1]<y+25 and s['text'].startswith('$')][0]
            im=[i for i in imgs if abs((i['bbox'][0]+i['bbox'][2])/2-cx)<50 and i['bbox'][3]<y and y-i['bbox'][3]<90]
            im.sort(key=lambda i:y-i['bbox'][3])
            out.append(dict(cat='perfumes',sub=sub,name=' '.join(s['text'] for s in nm),detail='',color='',note='',cod=m.group(1),usd=usd_perf(num(pr['text'])),pricing='perf',img=img_save(d,im[0]['xref'],m.group(1))))
json.dump(out,open('lists.json','w'),ensure_ascii=False)
import collections; print(len(out),collections.Counter((o['cat'],o['sub']) for o in out))
