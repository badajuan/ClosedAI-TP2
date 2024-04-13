import requests
import sys
import ctypes
import json
import numbers
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def main(libraryName, displayGUI):

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
        return giniValues

    #Si el modo CLI fue activado
    if not displayGUI:
        print(f"    Modo CLI activado correctamente.")
        while True:
            desiredCountry = input("De que país desea conocer la evolución del indice GINI? (Ingrese la palabra 'quit' para terminar la ejecución): ").title()
            if(desiredCountry=="Quit"):
                break
            print(filterCountry(desiredCountry))
        sys.exit(0)
    
    #Si el modo GUI fue activado
    print(f"    Desplegando interfaz gráfica...")

    # Crea una ventana para la GUI
    root = tk.Tk()
    root.title("Evolución Indice GINI")
    root.eval('tk::PlaceWindow . center')

    #Pregunta inicial
    label = tk.Label(root, text="Seleccione el país que desea analizar:")
    label.pack(pady=15)
    
    # Crea un set con todos los paises encontrados en la response
    countryList = sorted(set(entry["country"]["value"] for entry in data[1]))

    # Utiliza el set de paises para crear una lista de selección
    selectedCountry = tk.StringVar(root)
    listbox = tk.Listbox(root, listvariable=selectedCountry, selectmode="browse", height=5, width=10, activestyle='underline')
    for country in countryList:
        listbox.insert(tk.END, country)
    listbox.pack(pady=5, fill=tk.BOTH, expand=True, anchor='center')

    # Crea un histograma en blanco y un canvas para mostrar los resultados en la ventana
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    #Funcion a llamar cada vez que hay un click del usuario en el boton "Analizar"
    def showGraph():
        #Toma la entrada ingresada en la lista de selección
        desiredCountry = listbox.get(listbox.curselection()[0])

        years, values = zip(*filterCountry(desiredCountry))

        # Limpia la info anterior (si la hay) del grafico
        ax.clear()

        # Grafica la nueva información
        ax.plot(years, values, marker='o')
        title = 'Evolución Indice GINI Por Año de ' + desiredCountry
        ax.set_title(title)
        ax.set_xlabel('Año')
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
    if len(sys.argv) < 2:
        print("Uso: python3 main.py libraryName")
        sys.exit(1)
    
    # Determina si hay que mostrar la interfaz gráfica o no segun si se incluyó el argumento '-c'
    displayGUI = not ("-c" in sys.argv)
    main(sys.argv[1], displayGUI)
