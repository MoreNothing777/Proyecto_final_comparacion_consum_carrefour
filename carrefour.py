import os
import json
import re
from bs4 import BeautifulSoup

def limpiar_nombre(nombre):

    nombre = nombre.lower()

    nombre = nombre.replace(".", "")
    nombre = nombre.replace(",", "")

    palabras_excluir = ["gr", "g", "kg", "unidad", "unidades", "pack", "packs"]

    palabras = []

    for palabra in nombre.split():
        if palabra not in palabras_excluir:
            palabras.append(palabra)

    return " ".join(palabras)


# Lista final de productos
productos_carrefour = []

# ID incremental
ID_producto = 1

# Carpeta donde están los HTML
ruta = "./html_carrefour"

# Recorrer todos los archivos HTML
for fichero in os.listdir(ruta):

    if not fichero.endswith(".html"):
        continue

    ruta_fichero = os.path.join(ruta, fichero)

    print(f"Procesando: {fichero}")

    with open(ruta_fichero, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "lxml")

    productos = soup.find_all("article")

    print(f"Productos encontrados: {len(productos)}")

    for producto in productos:

        # NOMBRE
        nombre_tag = producto.find(
            "a",
            {"data-test": "result-title"}
        )

        nombre_producto = (
            nombre_tag.text.strip()
            if nombre_tag
            else "N/A"
        )

        # PRECIO
        precio_tag = producto.find(
            "span",
            class_="x-currency"
        )

        if not precio_tag:
            print(f"ERROR → producto sin precio: {nombre_producto}")
            continue

        try:

            precio_producto = re.sub(
                r"\s+",
                " ",
                precio_tag.text
            ).strip()

            precio_limpio = (
                precio_producto
                .replace("€", "")
                .replace(",", ".")
                .strip()
            )

            precio_num = float(precio_limpio)

        except ValueError:

            print(
                f"ERROR en el producto: {nombre_producto}"
            )

            continue

        productos_carrefour.append({
            "ID": ID_producto,
            "nombre": nombre_producto,
            "precio": precio_num
        })

        ID_producto += 1

print(f"\nTotal productos guardados: {len(productos_carrefour)}")

# Guardar JSON
with open(
    "./JSON_CC/productos_carrefour.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        productos_carrefour,
        f,
        ensure_ascii=False,
        indent=4
    )

print("JSON generado correctamente.")