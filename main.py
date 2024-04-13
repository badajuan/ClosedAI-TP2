import requests
import sys
import ctypes
import json
import numbers
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def main(libraryName):

    # Carga la librería
    library = ctypes.CDLL(libraryName)

    # Define los argumentos y retornos de la función de la librería
    library.floatToInt.argtypes = [ctypes.c_float]
    library.floatToInt.restype = ctypes.c_int

    # Define un wrapper para llamar a la función de C
    def floatToInt(value):
        return library.floatToInt(value)
    
    #Indice de todos los paises
    url = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"
    #Indice de Argentina
    #url = "https://api.worldbank.org/v2/en/country/ARG/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1"
    
    resp = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if resp.status_code == 200:
        print("    Request exitosa.")
    else:
        # Imprimir un mensaje de error si la solicitud falló
        print("Error al realizar la solicitud:", resp.status_code)
        sys.exit(1)

    #Guarda la respuesta en un wrapper json
    data = json.loads(resp.text)

    #Filtra los valores de GINI desde la request a partir del nombre del país deseado y devuelve una tupla con los años y valores encontrados
    def filterCountry(desiredCountry):
        giniValues = [(entry["date"], entry["value"]) for entry in data[1] if entry["country"]["value"] == desiredCountry]

        for i, (year, value) in enumerate(giniValues):
            if isinstance(value, numbers.Number):
                giniValues[i] = (year, floatToInt(value))

        giniValues.sort(key=lambda x: x[0]) # Ordenamos los años de menor a mayor
        return zip(*giniValues)

    # Crea una ventana para la GUI
    root = tk.Tk()
    root.title("Evolución Indice GINI")

    #Pregunta inicial + Campo para tomar la input del usuario
    label = tk.Label(root, text="De que país desea conocer el indice GINI?:")
    label.pack(pady=15)
    entry = tk.Entry(root)
    entry.pack(pady=5)

    # Creo un grafico en blanco y un canvas para mostrar los resultados en la ventana
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    #Funcion a llamar cada vez que hay un click del usuario en el boton "Analizar"
    def showGraph():
        #Tomo la entrada ingresada en el campo de texto
        desiredCountry = entry.get().title()
        message = f"Pais ingresado: {desiredCountry}. Si "
        label.config(text=message)

        years, values = filterCountry(desiredCountry)    

        # Limpia la info anterior (si la hay) en el grafico
        ax.clear()

        # Grafica la nueva información
        ax.plot(years, values, marker='o')
        title = 'Evolución Indice GINI Por Año de ' + desiredCountry
        ax.set_title(title)
        ax.set_xlabel('Años')
        ax.set_ylabel("Indice GINI")
        ax.grid(True)

        # Actualiza el canvas
        canvas.draw()

    
    # Crea un wrapper para los botones que estarán disponibles para el usuario
    button_frame = tk.Frame(root)
    button_frame.pack()

    button = tk.Button(button_frame, text="Analizar", command=showGraph) #Actualiza el grafico en base al país ingresado
    button.pack(side='left', padx=5, pady=5)

    close_button = tk.Button(button_frame, text="Cerrar", command=root.destroy) #Cierra la ventana y detiene la ejecución
    close_button.pack(side='left', padx=5, pady=5)

    # Le doy control de repetición a la ventana
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 main.py libraryName")
        sys.exit(1)
    main(sys.argv[1])
