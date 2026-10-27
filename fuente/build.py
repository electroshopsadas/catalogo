import json,glob,os
from PIL import Image
T=160;N=10;per=N*N
cats=[];rows=[];files=[]
for f in sorted(glob.glob('listas/*.json')):
    l=json.load(open(f))
    cats.append({k:l[k] for k in ('id','label','terms') if k in l}|{'promo':l.get('promo',False)})
    R=l['rows']
    for sh in range((len(R)+per-1)//per):
        cv=Image.new('RGB',(T*N,T*N),'white')
        for ix,r in enumerate(R[sh*per:(sh+1)*per]):
            im=Image.open(r['img'])
            if im.mode!='RGB':
                im=im.convert('RGBA'); bg=Image.new('RGB',im.size,'white'); bg.paste(im,mask=im.split()[3]); im=bg
            im.thumbnail((T-6,T-6)); cv.paste(im,((ix%N)*T+(T-im.width)//2,(ix//N)*T+(T-im.height)//2))
        fn=f"img_{l['id']}_{sh}.jpg"; cv.save('pub/'+fn,quality=74,optimize=True,progressive=True); files.append(fn)
    for k,r in enumerate(R):
        rows.append([l['id'],r['sub'],r['name'],r['detail'],r['color'],r['note'],r['cod'],r['pricing'],f"img_{l['id']}_{k//per}.jpg",k%per,r['v']])
json.dump({'listas':cats,'productos':rows},open('pub/productos.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump(files,open('sprites.json','w'))
print(len(cats),len(rows),files)
