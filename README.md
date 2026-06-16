# Comparador de precios entre Consum y Carrefour

Proyecto de extracción, tratamiento y comparación de precios de supermercado desarrollado en Python.  
El objetivo es obtener productos de **Consum** y **Carrefour**, normalizar los nombres, compararlos mediante similitud textual y mostrar los resultados en una interfaz gráfica con **Tkinter**.

---

## Resumen del proyecto

Este proyecto automatiza el análisis de productos de supermercado a partir de dos fuentes distintas:

- **Consum**: obtención de productos mediante Selenium y posterior generación de un JSON.
- **Carrefour**: procesamiento de HTML guardado localmente, extracción de productos y generación de un JSON.
- **Comparación**: emparejamiento de productos similares usando `SequenceMatcher`.
- **Interfaz gráfica**: panel de control en Tkinter para lanzar el proceso, visualizar logs y abrir el detalle de los resultados.

El flujo general es:

```text
HTML / páginas web
      ↓
Extracción de datos
      ↓
JSON
      ↓
Limpieza y comparación
      ↓
Resultados
      ↓
Interfaz gráfica
```

---

## Estructura del proyecto

```text
Proyecto_final/
│
├── html_carrefour/
│   ├── arroz_basmati.html
│   ├── atun_claro_calvo.html
│   ├── cerveza_1906.html
│   ├── champu_hs.html
│   ├── mayonesa_hellmans.html
│   ├── pañales_dodot.html
│   ├── solomillo.html
│   ├── pipas saladas.html
│   ├── pate cerdo.html
│   └── chocolate milka.html
│
├── JSON_CC/
│   ├── consum.json
│   └── productos_carrefour.json
│
├── resultados/
│   ├── comparaciones.json
│   └── sin_coincidencias.json
│
├── consum.py
├── carrefour.py
├── comparar.py
├── interfaz.py
└── README.md
```

> Nota: la carpeta `__pycache__/` y los archivos `.pyc` son generados automáticamente por Python y no forman parte lógica del proyecto.

---

## Objetivo funcional

El proyecto pretende responder a esta pregunta:

> ¿Qué supermercado ofrece un precio más competitivo para productos similares?

Para ello:

1. Se obtienen productos de Consum y Carrefour.
2. Se normalizan los nombres para reducir ruido.
3. Se calcula la similitud textual entre productos.
4. Se selecciona la mejor coincidencia.
5. Se calcula la diferencia de precio.
6. Se presentan los resultados de forma clara.

---

## Tecnologías utilizadas

- Python 3
- Selenium
- BeautifulSoup
- JSON
- Tkinter
- `difflib.SequenceMatcher`
- Expresiones regulares (`re`)
- `webdriver-manager`

---

## Módulos del proyecto

### `consum.py`
Este script realiza la obtención de productos desde Consum.

Características principales:

- Usa **Selenium** para navegar por la web.
- Realiza varias búsquedas definidas en una lista.
- Recorre las páginas encontradas para cada búsqueda.
- Extrae:
  - `ID`
  - `busqueda`
  - `nombre`
  - `precio`
- Guarda el resultado en `JSON_CC/consum.json`.

### `carrefour.py`
Este script procesa los archivos HTML guardados localmente en `html_carrefour/`.

Características principales:

- Recorre todos los archivos `.html` de la carpeta.
- Usa **BeautifulSoup** para analizar el contenido.
- Extrae:
  - `ID`
  - `nombre`
  - `precio`
- Guarda el resultado en `JSON_CC/productos_carrefour.json`.

### `comparar.py`
Este script carga ambos JSON, limpia los nombres y compara productos.

Características principales:

- Carga `consum.json` y `productos_carrefour.json`.
- Normaliza los nombres:
  - minúsculas
  - eliminación de números
  - eliminación de unidades y texto irrelevante
- Usa `SequenceMatcher` para medir similitud textual.
- Guarda:
  - `resultados/comparaciones.json`
  - `resultados/sin_coincidencias.json`

### `interfaz.py`
Este script crea la interfaz gráfica del proyecto con **Tkinter**.

Características principales:

- Botón para generar datos.
- Botón para comparar productos.
- Botón para ver resultados.
- Registro visual del proceso.
- Ventana secundaria con el detalle de cada comparación.

---

## Flujo de trabajo del proyecto

### 1. Obtención de datos de Consum
`consum.py` abre el navegador con Selenium, busca productos definidos en el script y genera `consum.json`.

### 2. Obtención de datos de Carrefour
`carrefour.py` lee archivos HTML previamente guardados en local, extrae productos con BeautifulSoup y genera `productos_carrefour.json`.

### 3. Comparación de productos
`comparar.py` carga ambos JSON y busca la coincidencia más parecida para cada producto de Consum.

### 4. Visualización
`interfaz.py` permite ejecutar todo el proceso desde una aplicación de escritorio sencilla.

---

## Criterio de comparación

La comparación se basa en una estrategia de dos pasos:

1. **Limpieza de nombres**  
   Se normalizan los textos para reducir diferencias irrelevantes.

2. **Similitud textual**  
   Se usa `SequenceMatcher` para calcular el porcentaje de similitud entre nombres.

Ejemplo:

- `Chocolate con Oreo 100 Gr`
- `Chocolate brownie Oreo Milka 100 g.`

Aunque no sean idénticos, el algoritmo detecta que son muy parecidos.

---

## Archivos generados

### `JSON_CC/consum.json`
Contiene los productos extraídos de Consum.

Ejemplo:

```json
{
    "ID": 1,
    "busqueda": "chocolate milka",
    "nombre": "Chocolate con Oreo 100 Gr",
    "precio": 1.99
}
```

### `JSON_CC/productos_carrefour.json`
Contiene los productos extraídos desde los HTML de Carrefour.

Ejemplo:

```json
{
    "ID": 99,
    "nombre": "Chocolate con leche y oreo Milka 100 g.",
    "precio": 2.19
}
```

### `resultados/comparaciones.json`
Almacena los productos que sí han encontrado coincidencia.

Ejemplo:

```json
{
    "id_consum": 4,
    "producto_consum": "Chocolate con Oreo 100 Gr",
    "precio_consum": 1.99,
    "id_carrefour": 88,
    "producto_carrefour": "Chocolate brownie Oreo Milka 100 g.",
    "precio_carrefour": 2.25,
    "similitud": 73.91,
    "más barato": "Consum es más barato",
    "diferencia": 0.26
}
```

### `resultados/sin_coincidencias.json`
Almacena los productos que no han encontrado una coincidencia fiable.

Ejemplo:

```json
{
    "producto_consum": "Leche Entera Brik 1 L",
    "precio_consum": 0.96
}
```

---

## Instalación

### 1. Requisitos previos
- Python 3.10 o superior
- Google Chrome instalado
- Conexión a internet para la parte de Selenium y las búsquedas de Consum

### 2. Instalar dependencias
Ejecuta:

```bash
pip install selenium webdriver-manager beautifulsoup4 lxml
```

> `tkinter` normalmente ya viene incluido con Python.

---

## Ejecución del proyecto

### Opción recomendada: usar la interfaz
Ejecuta:

```bash
python interfaz.py
```

Desde la interfaz podrás:

- Generar los datos.
- Comparar productos.
- Ver los resultados.

### Ejecución manual por módulos

Si prefieres ejecutar paso a paso:

```bash
python consum.py
python carrefour.py
python comparar.py
python interfaz.py
```

---

## Cómo funciona la interfaz

La interfaz está diseñada como un panel de control:

- **Generar datos**: ejecuta los scripts de extracción.
- **Comparar productos**: ejecuta la comparación entre JSON.
- **Ver resultados**: abre una ventana con el detalle de las comparaciones.
- **Registro de actividad**: muestra el progreso del proceso en tiempo real.

La información se presenta en ventanas separadas para que el resultado sea más claro y fácil de revisar.

---

## Limitaciones conocidas

Durante el desarrollo aparecieron varias dificultades:

- La web de Carrefour aplica protecciones anti-bot.
- Parte del contenido de Carrefour se trabajó a partir de HTML guardado localmente.
- La comparación textual no siempre identifica equivalencias perfectas, especialmente cuando los nombres son muy distintos aunque el producto sea similar.

Estas limitaciones fueron documentadas y forman parte del análisis del proyecto.

---

## Posibles mejoras futuras

- Añadir un sistema de categorías por tipo de producto.
- Mejorar el emparejamiento con reglas semánticas.
- Normalizar pesos y unidades para comparar productos más fielmente.
- Exportar los resultados a Excel o CSV.
- Añadir gráficos de diferencias de precio.
- Integrar filtros en la interfaz gráfica.

---

## Diagrama de flujo simplificado

```text
[Consum] ──> [Selenium] ──> [consum.json]
                                   │
                                   ▼
                              [comparar.py]
                                   ▲
                                   │
[Carrefour HTML] ──> [BeautifulSoup] ──> [productos_carrefour.json]
                                   │
                                   ▼
                         [comparaciones.json / sin_coincidencias.json]
                                   │
                                   ▼
                             [interfaz.py]
```

---

## Conclusión

Este proyecto demuestra un flujo completo de tratamiento de datos:

- extracción,
- limpieza,
- comparación,
- almacenamiento,
- y visualización.

Además, refleja un caso real de desarrollo donde se han encontrado problemas técnicos reales, se han documentado y se han resuelto con alternativas viables.
Salu2

---

## Autoría

Proyecto desarrollado como parte de un trabajo académico en Python, orientado al análisis comparativo de precios entre supermercados.
