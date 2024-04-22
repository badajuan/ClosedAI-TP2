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
    
    #Filtra los valores de GINI desde la request a partir del nombre del país deseado y devuelve una tupla con los años y valores encontrados
    def filterCountry(desiredCountry, data):
        giniValues = [(entry["date"], entry["value"]) for entry in data[1] if entry["country"]["value"] == desiredCountry]

        for i, (year, value) in enumerate(giniValues):
            if isinstance(value, numbers.Number):
                giniValues[i] = (year, floatToInt(value))

        giniValues.sort(key=lambda x: x[0]) # Ordenamos los años de menor a mayor
        return giniValues

    #Testeo de las funciones
    def test1():
    # Llama a la función con tres números flotantes diferentes
        number_1 = 3.6
        number_2 = -2.8
        number_3 = 0.5

        # Obtiene y muestra los resultados de la función
        result_1 = library.floatToInt((number_1))
        result_2 = library.floatToInt((number_2))
        result_3 = library.floatToInt((number_3))

        expected_result_1 = 5
        expected_result_2 = -2
        expected_result_3 = 1

        print("Test 1:")
        print(f"    Test para {number_1}: {result_1}","(Exitoso)" if result_1==expected_result_1 else "(Fallido)")
        print(f"    Resultado para {number_2}: {result_2}","(Exitoso)" if result_2==expected_result_2 else "(Fallido)")
        print(f"    Resultado para {number_3}: {result_3}","(Exitoso)" if result_3==expected_result_3 else "(Fallido)")
    
    test1()
    
    #Testea la función filterCountry
    def test2():
        # Abre el archivo con una response de ejemplo
        with open("response.txt","r") as file:
            testData = json.loads(file.read())

        # Caso 1: Comparamos los resultados de filtrar los valores de un pais conocido en una response de ejemplo
        desiredCountry = "Wakanda"
        filtered_data = filterCountry(desiredCountry,testData)
        # Se esperan estos datos para Wakanda (año, valor)
        expected_data = [('2018', 3), ('2019', 2), ('2020', 2)]

        print(f"Test 2 - Caso 1:",end="")
        # Comparación de los resultados obtenidos con los esperados
        if filtered_data == expected_data:
            print(" La función filtrar país SI pasó la prueba.")
        else:
            print(" La función filtrar país NO pasó la prueba.")
        
        print("     Datos filtrados:", filtered_data)
        print("     Datos esperados:", expected_data)

        #Caso 2: Intentamos filtrar un país que sabemos que no se encuentra en la response de ejemplo
        desiredCountry = "Narnia"
        filtered_data = filterCountry(desiredCountry,testData)
        # Se espera un arreglo vacío
        expected_data = []

        print(f" Test 2 - Caso 2:",end="")
        # Comparación de los resultados obtenidos con los esperados
        if filtered_data == expected_data:
            print("La función filtrar país SI pasó la prueba.")
        else:
            print("La función filtrar país NO pasó la prueba.")
        
        print("     Datos filtrados:", filtered_data)
        print("     Datos esperados:", expected_data)

    test2()
    
    #Indice de todos los paises
    url = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"
    
    resp = requests.get(url)
    
    #Testeamos que el codigo de la respuesta sea correcta
    def test3(resp):
    # Verificar si la solicitud fue exitosa
        if resp.status_code == 200:
            print("Test 3:  Request exitosa.")
        else:
        # Imprimir un mensaje de error si la solicitud falló
            print("Error al realizar la solicitud:", resp.status_code)
            sys.exit(1)

    test3(resp)

    #Guarda la respuesta en un wrapper json
    data = json.loads(resp.text)

    #Si el modo CLI fue activado
    if not displayGUI:
        print(f"\nModo CLI activado correctamente.")
        while True:
            desiredCountry = input("De que país desea conocer la evolución del indice GINI? (Ingrese la palabra 'quit' para terminar la ejecución): ").title()
            if(desiredCountry=="Quit"):
                break
            print(filterCountry(desiredCountry,data))
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

        years, values = zip(*filterCountry(desiredCountry,data))

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
