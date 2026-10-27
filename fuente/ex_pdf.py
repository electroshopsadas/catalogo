import pymupdf,re,json,sys,os
src,tag,outj=sys.argv[1],sys.argv[2],sys.argv[3]
os.makedirs('raw',exist_ok=True)
d=pymupdf.open(src); res=[]
for pn,p in enumerate(d):
    spans=[s for b in p.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if s['text'].strip()]
    imgs=p.get_image_info(xrefs=True)
    for s in spans:
        if not re.match(r'^\$ [\d\.]+$',s['text'].strip()): continue
        cx=(s['bbox'][0]+s['bbox'][2])/2; py=s['bbox'][1]
        col=[t for t in spans if abs((t['bbox'][0]+t['bbox'][2])/2-cx)<110 and py-120<t['bbox'][1]<py-2 and 'PRECIO' not in t['text']]
        big=max(col,key=lambda t:t['size']); name=big['text'].strip()
        det=' '.join(t['text'].strip() for t in col if t['bbox'][1]>big['bbox'][1]+2 and t['size']<big['size'])
        c=[i for i in imgs if i['xref'] and abs((i['bbox'][0]+i['bbox'][2])/2-cx)<110 and i['bbox'][3]<=big['bbox'][3]+2 and big['bbox'][1]-i['bbox'][3]<150 and i['bbox'][2]-i['bbox'][0]>30 and i['bbox'][1]>90]
        c.sort(key=lambda i:big["bbox"][1]-i["bbox"][3])
        if not c: print("NOIMG",pn,name,[ [round(v) for v in i["bbox"]] for i in imgs]); continue
        x=d.extract_image(c[0]['xref']); f=f'raw/{tag}_{len(res)}.{x["ext"]}'; open(f,'wb').write(x['image'])
        res.append(dict(name=name,detail=det,ars=int(s['text'].replace('$','').replace('.','').strip()),img=f))
json.dump(res,open(outj,'w'),ensure_ascii=False,indent=0)
for r in res: print(r['name'],'|',r['detail'],'|',r['ars'],r['img'])
