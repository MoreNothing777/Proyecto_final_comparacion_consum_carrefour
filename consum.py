from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import time, random, re, json

# función para ayudar a cargar las página con varios intentos
def intentos_cargar_pagina(url, intentos=3):
    for intento in range(intentos):
        try:
            wd.get(url)

            WebDriverWait(wd, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "widget-product")))

            return True

        except Exception:
            print(f"Reintento {intento+1}")

    return False

options = webdriver.ChromeOptions()
options.add_argument('--headless') #sin interfaz gráfica (segundo plano)
options.add_argument("--disable-blink-features=AutomationControlled") # evita el anti-bot
options.add_argument("user-agent=Mozilla/5.0") #confundir con un navegador normal
options.add_argument("--no-sandbox") #eliminamos el sandox para evitar errores (mal carga).
options.add_argument("--disable-dev-shm-usage") #prevenir fallos por poca memória (recomendación).

wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

busquedas = [
    "chocolate milka",
    "arroz basmati",
    "atun claro",
    "cerveza 1906",
    "champu hs",
    "mayonesa hellmanns",
    "pate cerdo",
    "pipas saladas",
    "solomillo",
    "pañales dodot"
    ]

dicc_productos_consum = []
ID_producto = 1

for busqueda in busquedas:

    print("\n========================")
    print(f"BUSCANDO: {busqueda}")
    print("========================")

    termino = busqueda.replace(" ", "%20")

    base_url = (
        "https://tienda.consum.es/es/s/"
        + termino +
        "?showProducts=true&originProduct=Grid_Search_Organic&orderById=13&"
    )

    url = base_url + "page=1"

    try:

        wd.get(url)

        WebDriverWait(wd, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "widget-product")
            )
        )

        soup = BeautifulSoup(wd.page_source, "lxml")

    except Exception:

        print("No se pudo cargar la búsqueda")
        continue

    total_pag = 1

    for span in soup.find_all("span"):

        texto = span.text.strip()

        if texto.startswith("de"):

            match = re.search(r"(\d+)", texto)

            if match:

                total_pag = int(match.group(1))
                break

    print(f"Páginas encontradas: {total_pag}")

    for page in range(1, total_pag + 1):

        try:

            url = base_url + f"page={page}"

            if not intentos_cargar_pagina(url):

                print(f"Saltando página {page}")
                continue

            soup = BeautifulSoup(
                wd.page_source,
                "lxml"
            )

            productos = soup.find_all(
                "div",
                class_="widget-product"
            )

            if not productos:
                continue

            print(
                f"Página {page}: "
                f"{len(productos)} productos"
            )

            for producto in productos:

                nombre_tag = producto.find(
                    "h3",
                    class_=lambda x:
                    x and (
                        "u-title-3" in x
                        or
                        "u-size" in x
                    )
                )

                nombre_producto = (
                    nombre_tag.text.strip()
                    if nombre_tag
                    else "N/A"
                )

                precio_tag = producto.find(
                    "span",
                    class_=lambda x:
                    x and "price" in x
                )

                precio_num = None

                if precio_tag:

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
                        )

                        precio_num = float(
                            precio_limpio
                        )

                    except ValueError:

                        print(
                            f"ERROR en "
                            f"{nombre_producto}"
                        )
                        continue

                dicc_productos_consum.append({

                    "ID": ID_producto,

                    "busqueda": busqueda,

                    "nombre": nombre_producto,

                    "precio": precio_num

                })

                ID_producto += 1

            time.sleep(
                random.uniform(2, 5)
            )

        except Exception as e:

            print(
                f"Error en página "
                f"{page}: {e}"
            )

wd.quit()

# guardar JSON
with open("./JSON_CC/consum.json", "w", encoding="utf-8") as f:
    json.dump(dicc_productos_consum, f, ensure_ascii=False, indent=4)


# leer JSON
with open("./JSON_CC/consum.json", "r", encoding="utf-8") as f:
    dicc_productos_consum = json.load(f)

print(dicc_productos_consum)

