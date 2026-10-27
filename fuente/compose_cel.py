import json,os
rows=[]
for b in ['iphone','samsung','xiaomi','motorola','realme','honor','doogee','ulefone']:
    f=f'src/{b}_rows.json'
    if os.path.exists(f): rows+=json.load(open(f))
json.dump(dict(id='celulares',label='Celulares',terms='<b>Precio minorista</b> por unidad. <b>Precio mayorista</b> comprando {minMay} unidades o más, combinables entre modelos y colores.',rows=rows),open('listas/01_celulares.json','w'),ensure_ascii=False)
print(len(rows))
