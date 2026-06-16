import json
from difflib import SequenceMatcher
import re

comparaciones = []
sin_coincidencias = []

win_consum = 0
win_carrefour = 0
empates = 0

# Cargar JSON
with open("./JSON_CC/consum.json", "r", encoding="utf-8") as f:
    productos_consum = json.load(f)

with open("./JSON_CC/productos_carrefour.json", "r", encoding="utf-8") as f:
    productos_carrefour = json.load(f)


# Limpiar nombres

def limpiar_nombre(nombre):

    nombre = nombre.lower()

    nombre = re.sub(r"\d+[.,]?\d*", "", nombre)

    nombre = nombre.replace(".", "")
    nombre = nombre.replace(",", "")

    palabras_excluir = [
        "gr", "g", "kg", "gramos", "kilogramos", "g.", "G", "Gr",
        "unidad", "unidades",
        "pack", "packs",
        "litro", "litros", "l", "L", "ml", "Ml"
    ]

    palabras_limpias = []

    for palabra in nombre.split():

        if palabra not in palabras_excluir:
            palabras_limpias.append(palabra)

    return " ".join(palabras_limpias)

# Comparar productos
for producto_consum in productos_consum:

    mejor_similitud = 0
    mejor_producto = None

    nombre_consum = limpiar_nombre(
        producto_consum["nombre"]
    )

    for producto_carrefour in productos_carrefour:

        nombre_carrefour = limpiar_nombre(
            producto_carrefour["nombre"]
        )

        similitud = SequenceMatcher(
            None,
            nombre_consum,
            nombre_carrefour
        ).ratio()

        if similitud > mejor_similitud:

            mejor_similitud = similitud
            mejor_producto = producto_carrefour

    print("\n-----------------------------")
    print("CONSUM")
    print(producto_consum["nombre"])
    print("Precio:", producto_consum["precio"])

    if mejor_producto and mejor_similitud >= 0.70:

        print("\nCARREFOUR")
        print(mejor_producto["nombre"])
        print("Precio:", mejor_producto["precio"])

        print(
            "\nSimilitud:",
            round(mejor_similitud * 100, 2),
            "%"
        )

        diferencia = (mejor_producto["precio"] - producto_consum["precio"])

        if diferencia > 0:
            resultado = "Consum es más barato"

        elif diferencia < 0:
            resultado = "carrefour es más barato"

        else:
            resultado = "Mismo precio"


        comparaciones.append({
            "id_consum": producto_consum["ID"],
            "producto_consum": producto_consum["nombre"],
            "precio_consum": producto_consum["precio"],
            "id_carrefour": mejor_producto["ID"],
            "producto_carrefour": mejor_producto["nombre"],
            "precio_carrefour": mejor_producto["precio"],
            "similitud": round(mejor_similitud * 100, 2),
            "más barato": resultado,
            "diferencia": round(abs(diferencia), 2),
        })

    if producto_consum["precio"] < producto_carrefour["precio"]:
        win_consum += 1

    elif producto_consum["precio"] > producto_carrefour["precio"]:
        win_carrefour += 1

    else:
        empates += 1

else:

    sin_coincidencias.append({
        "producto_consum": producto_consum["nombre"],
        "precio_consum": producto_consum["precio"]
    })

with open("./resultados/comparaciones.json", "w", encoding="utf-8") as f:
    json.dump(comparaciones, f, ensure_ascii=False, indent=4)

with open("./resultados/sin_coincidencias.json", "w", encoding="utf-8") as f:
    json.dump(sin_coincidencias, f, ensure_ascii=False, indent=4)

total = len(comparaciones)

comparaciones.sort(key=lambda x: x["similitud"], reverse=True)