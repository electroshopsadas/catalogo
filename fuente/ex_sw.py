import pymupdf,re,json,os
F='/root/.claude/uploads/de8d6e17-235e-562c-b51f-ddb92eb1056e/480af95a-LISTA_SMARTWATCH_ELECTROSHOP.SADAS_5.10.pdf'
d=pymupdf.open(F); out=[]; brand=''
for pn,p in enumerate(d):
    sp=sorted([s for b in p.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if s['text'].strip()],key=lambda s:(s['bbox'][1],s['bbox'][0]))
    imgs=[i for i in p.get_image_info(xrefs=True) if i['bbox'][1]>(140 if pn==0 else 20)]
    heads=[(s['bbox'][1],s['text'].strip()) for s in sp if s['size']==11.0 and s['font']=='Helvetica-Bold']
    for s in sp:
        if not re.match(r'^\$ [\d\.]+$',s['text'].strip()) or s['size']!=10.0: continue
        cx=(s['bbox'][0]+s['bbox'][2])/2; py=s['bbox'][1]
        col=[t for t in sp if abs((t['bbox'][0]+t['bbox'][2])/2-cx)<48 and py-40<t['bbox'][1]<py-1 and t['size']<9]
        name=' '.join(t['text'].strip() for t in col if t['font']=='Helvetica-Bold')
        color=' '.join(t['text'].strip() for t in col if t['font']=='Helvetica')
        top=min(t['bbox'][1] for t in col)
        im=[i for i in imgs if abs((i['bbox'][0]+i['bbox'][2])/2-cx)<48 and i['bbox'][3]<=top+2 and top-i['bbox'][3]<30]
        hb=[h for y,h in heads if y<top]
        b=hb[-1] if hb else brand; brand=b
        f=None
        if im:
            x=d.extract_image(im[0]['xref']); f=f'raw/sw_{len(out)}.{x["ext"]}'; open(f,'wb').write(x['image'])
        out.append(dict(brand=b,name=name,color=color,ars=int(s['text'].replace('$','').replace('.','').strip()),img=f))
json.dump(out,open('sw.json','w'),ensure_ascii=False)
import collections
print(len(out),sum(1 for o in out if not o['img']),collections.Counter(o['brand'] for o in out))
for o in out[::25]: print(o)
