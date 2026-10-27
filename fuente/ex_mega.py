# Extrae celdas de catálogos "Mega Eletrônicos" (formato { CEL ... REF: COD: VALOR U$)
import pymupdf,re,json,sys,os
def extract(src,outdir):
    os.makedirs(outdir,exist_ok=True)
    d=pymupdf.open(src); out=[]
    for p in d:
        bl=p.get_text('blocks'); imgs=[i for i in p.get_image_info(xrefs=True) if i['width']>=250 and i['height']>=250]
        for s in bl:
            if not s[4].lstrip().startswith('{'): continue
            cell=[b for b in bl if abs(b[0]-s[0])<40 and s[1]-1<=b[1]<s[1]+110]
            t=' '.join(b[4] for b in sorted(cell,key=lambda b:b[1])).replace('\n',' ')
            m=re.search(r'\{\s*(.*?)\s+REF:\s*(.*?)\s+COD:\s*(\d+).*?VALOR U\$\s*([\d\.,]+)',t)
            if not m: print('SKIP',t[:80]); continue
            name,ref,cod,pr=m.groups()
            c=[i for i in imgs if abs(i['bbox'][0]-s[0])<45 and i['bbox'][3]<=s[1]+3 and s[1]-i['bbox'][3]<70]
            c.sort(key=lambda i:s[1]-i['bbox'][3])
            f=None
            if c:
                x=d.extract_image(c[0]['xref']); f=f'{outdir}/{cod}.{x["ext"]}'; open(f,'wb').write(x['image'])
            out.append(dict(name=' '.join(name.split()),ref=' '.join(ref.split()),cod=cod,usd=float(pr.replace('.','').replace(',','.')),img=f))
    return out
if __name__=='__main__':
    r=extract(sys.argv[1],sys.argv[2]); json.dump(r,open(sys.argv[3],'w'),ensure_ascii=False,indent=0)
    print(len(r),sum(1 for x in r if not x['img']))
    for x in r: print(x['cod'],x['usd'],x['name'],'|',x['ref'])
