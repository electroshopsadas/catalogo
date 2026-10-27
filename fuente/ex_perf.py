import pymupdf,re,json,os,sys
F,tag,outj=sys.argv[1:4]
d=pymupdf.open(F); items=[]
for pn,p in enumerate(d):
    blocks=p.get_text('blocks')
    imgs=[i for i in p.get_image_info(xrefs=True) if i['width']!=199 and i['xref']]
    for b in blocks:
        m=re.search(r'U\$ ([\d\.]+,\d+) \| COD: (\d+)',b[4])
        if not m: continue
        cx=(b[0]+b[2])/2; py=b[1] if not m.start() else b[3]-8
        names=[x for x in blocks if abs((x[0]+x[2])/2-cx)<50 and py-50<x[1]<py-2 and 'U$' not in x[4] and not x[4].startswith('REF')]
        names.sort(key=lambda x:x[1])
        name=' '.join(' '.join(x[4].replace('\n',' ') for x in names).split())
        pre=b[4][:m.start()].strip()
        if pre: name=(name+' '+pre.replace('\n',' ')).strip()
        cand=[i for i in imgs if abs((i['bbox'][0]+i['bbox'][2])/2-cx)<50 and i['bbox'][3]<py and py-i['bbox'][3]<80]
        cand.sort(key=lambda i:py-i['bbox'][3])
        price=float(m.group(1).replace('.','').replace(',','.')); cod=m.group(2); f=None
        if cand:
            x=d.extract_image(cand[0]['xref']); f=f'raw/{tag}_{cod}.{x["ext"]}'; open(f,'wb').write(x['image'])
        items.append(dict(name=name,usd=price,cod=cod,img=f))
json.dump(items,open(outj,'w'),ensure_ascii=False)
print(len(items),len({i['cod'] for i in items}),sum(1 for i in items if not i['img']),min(i['usd'] for i in items),max(i['usd'] for i in items))
