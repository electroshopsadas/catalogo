import json,os
rows=[]
for b in ['fem','masc','uni']:
    f=f'src/perf_{b}_rows.json'
    if os.path.exists(f): rows+=json.load(open(f))
json.dump(dict(id='perfumes',label='Perfumes',terms='Perfumes originales importados. <b>Compra mínima: {minPerf} unidades</b>, combinables.',rows=rows),open('listas/02b_perfumes.json','w'),ensure_ascii=False)
print(len(rows))
