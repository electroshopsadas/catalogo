import json,os
rows=[]
for b in ['ipad','samsung','xiaomi','lenovo','doogee','ulefone','honor']:
    f=f'src/tab_{b}_rows.json'
    if os.path.exists(f): rows+=json.load(open(f))
json.dump(dict(id='tablets',label='Tablets',terms='<b>Precio minorista</b> por unidad. <b>Precio mayorista</b> comprando {minMay} unidades o más, combinables entre modelos y colores.',rows=rows),open('listas/02_tablets.json','w'),ensure_ascii=False)
print(len(rows))
