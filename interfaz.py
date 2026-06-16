import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import threading
import json
import os


# =====================================================
# FUNCIONES
# =====================================================

def escribir_log(texto):

    log_text.insert(tk.END, texto + "\n")

    log_text.see(tk.END)

    ventana.update()


# =====================================================
# GENERAR DATOS
# =====================================================

def generar_datos():

    def tarea():

        try:

            escribir_log("===================================")
            escribir_log("INICIO GENERACIÓN DE DATOS")
            escribir_log("===================================")

            escribir_log("Ejecutando consum.py...")

            subprocess.run(
                ["python", "consum.py"],
                check=True
            )

            escribir_log("✔ consum.json generado")


            escribir_log("Ejecutando carrefour.py...")

            subprocess.run(
                ["python", "carrefour.py"],
                check=True
            )

            escribir_log("✔ carrefour.json generado")

            escribir_log("")
            escribir_log("Proceso finalizado correctamente")

            estado_label.config(
                text="Datos generados correctamente",
                fg="green"
            )

            btn_comparar.config(
                state="normal"
            )

        except Exception as e:

            escribir_log(f"ERROR: {e}")

            estado_label.config(
                text="Error durante la generación",
                fg="red"
            )

    threading.Thread(
        target=tarea
    ).start()


# =====================================================
# COMPARAR
# =====================================================

def comparar_productos():

    def tarea():

        try:

            escribir_log("")
            escribir_log("===================================")
            escribir_log("COMPARANDO PRODUCTOS")
            escribir_log("===================================")

            subprocess.run(
                ["python", "comparar.py"],
                check=True
            )

            escribir_log("✔ comparaciones.json generado")

            estado_label.config(
                text="Comparación completada",
                fg="green"
            )

            btn_resultados.config(
                state="normal"
            )

        except Exception as e:

            escribir_log(f"ERROR: {e}")

    threading.Thread(
        target=tarea
    ).start()


# =====================================================
# RESULTADOS
# =====================================================

def ver_resultados():

    if not os.path.exists(
        "./resultados/comparaciones.json"
    ):

        messagebox.showerror(
            "Error",
            "No existe comparaciones.json"
        )

        return

    with open(
        "./resultados/comparaciones.json",
        "r",
        encoding="utf-8"
    ) as f:

        datos = json.load(f)

    ventana_resultados = tk.Toplevel()

    ventana_resultados.title(
        "Resultados"
    )

    ventana_resultados.geometry(
        "900x600"
    )


    lista = tk.Listbox(
        ventana_resultados,
        font=("Arial", 11)
    )

    lista.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )


    for item in datos:

        lista.insert(
            tk.END,
            item["producto_consum"]
        )


    def abrir_detalle(event):

        seleccion = lista.curselection()

        if not seleccion:
            return

        indice = seleccion[0]

        dato = datos[indice]

        detalle = tk.Toplevel()

        detalle.title(
            "Detalle de comparación"
        )

        detalle.geometry(
            "700x450"
        )

        texto = tk.Text(
            detalle,
            font=("Consolas", 11)
        )

        texto.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        contenido = f"""
PRODUCTO CONSUM
----------------------------------------

{dato['producto_consum']}

Precio:
{dato['precio_consum']} €


PRODUCTO CARREFOUR
----------------------------------------

{dato['producto_carrefour']}

Precio:
{dato['precio_carrefour']} €


SIMILITUD
----------------------------------------

{dato['similitud']} %


DIFERENCIA
----------------------------------------

{dato['diferencia']} €
"""

        texto.insert(
            "1.0",
            contenido
        )

        texto.config(
            state="disabled"
        )

    lista.bind(
        "<Double-Button-1>",
        abrir_detalle
    )


# =====================================================
# VENTANA PRINCIPAL
# =====================================================

ventana = tk.Tk()

ventana.title(
    "Comparador Consum vs Carrefour"
)

ventana.geometry(
    "1000x700"
)


# =====================================================
# TÍTULO
# =====================================================

titulo = tk.Label(
    ventana,
    text="COMPARADOR DE PRECIOS",
    font=("Arial", 22, "bold")
)

titulo.pack(
    pady=10
)


# =====================================================
# BOTONES
# =====================================================

frame_botones = tk.Frame(
    ventana
)

frame_botones.pack(
    pady=10
)


btn_generar = tk.Button(
    frame_botones,
    text="Generar datos",
    width=20,
    height=2,
    command=generar_datos
)

btn_generar.grid(
    row=0,
    column=0,
    padx=10
)


btn_comparar = tk.Button(
    frame_botones,
    text="Comparar productos",
    width=20,
    height=2,
    state="disabled",
    command=comparar_productos
)

btn_comparar.grid(
    row=0,
    column=1,
    padx=10
)


btn_resultados = tk.Button(
    frame_botones,
    text="Ver resultados",
    width=20,
    height=2,
    state="disabled",
    command=ver_resultados
)

btn_resultados.grid(
    row=0,
    column=2,
    padx=10
)


# =====================================================
# ESTADO
# =====================================================

estado_label = tk.Label(
    ventana,
    text="Esperando ejecución",
    font=("Arial", 12, "bold")
)

estado_label.pack(
    pady=10
)


# =====================================================
# LOG
# =====================================================

label_log = tk.Label(
    ventana,
    text="Registro de actividad",
    font=("Arial", 14, "bold")
)

label_log.pack()


log_text = tk.Text(
    ventana,
    height=25,
    font=("Consolas", 10)
)

log_text.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


ventana.mainloop()