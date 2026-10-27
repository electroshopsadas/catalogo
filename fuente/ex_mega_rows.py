# Catálogo "Mega Eletrônicos" en formato tabla (imagen | COD | PROD | VALOR)
import pymupdf,re,json,sys,os
src,outdir,outj=sys.argv[1:4]; os.makedirs(outdir,exist_ok=True)
d=pymupdf.open(src); out=[]
for p in d:
    sp=[s for b in p.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if s['text'].strip()]
    imgs=[i for i in p.get_image_info(xrefs=True) if i['bbox'][2]<80 and i['bbox'][1]>30]
    for s in sp:
        if not re.fullmatch(r'\d{6,8}',s['text'].strip()) or s['bbox'][0]>120: continue
        cod=s['text'].strip(); yc=(s['bbox'][1]+s['bbox'][3])/2
        row=[t for t in sp if abs((t['bbox'][1]+t['bbox'][3])/2-yc)<14 and t['bbox'][0]>125]
        name=' '.join(t['text'].strip() for t in sorted(row,key=lambda t:t['bbox'][1]) if not t['text'].startswith(('REF:','U$')) and t['bbox'][0]<500)
        ref=' '.join(t['text'].replace('REF:','').strip() for t in row if t['text'].startswith('REF:'))
        pr=[t['text'] for t in row if 'U$' in t['text']][0]
        im=[i for i in imgs if i['bbox'][1]-5<yc<i['bbox'][3]+5]
        f=None
        if im:
            x=d.extract_image(im[0]['xref']); f=f'{outdir}/{cod}.{x["ext"]}'; open(f,'wb').write(x['image'])
        out.append(dict(name=' '.join(name.split()),ref=ref,cod=cod,usd=float(re.search(r'[\d\.,]+',pr.replace('U$','')).group(0).replace('.','').replace(',','.')),img=f))
json.dump(out,open(outj,'w'),ensure_ascii=False,indent=0)
print(len(out),sum(1 for x in out if not x['img']))
