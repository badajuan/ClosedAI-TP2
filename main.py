import requests
import sys
import ctypes
import json
import numbers
import matplotlib.pyplot as plt

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
    
    data =json.loads(resp.text)
    
    while(True):
        desiredCountry = input("De que país desea conocer el indice GINI? (Ingrese la palabra 'quit' para terminar la ejecución): ").title()
        if(desiredCountry=="Quit"):
            break

        giniValues = [(entry["date"], entry["value"]) for entry in data[1] if entry["country"]["value"] == desiredCountry]

        if not giniValues:
            print(f"ERROR: El país '{desiredCountry}' no se encontró en la base de datos.")
            continue

        for i, (year, value) in enumerate(giniValues):
            if isinstance(value, numbers.Number):
                giniValues[i] = (year, floatToInt(value))

        
        
        giniValues.sort(key=lambda x: x[0]) #Ordenamos los años de menor a mayor
        years, values = zip(*giniValues)

        # Grafica los valores
        plt.plot(years, values, marker='o')
        plt.title('Evolución indice GINI por año')
        plt.xlabel('Año')
        ylabel = "Indice GINI de " + desiredCountry
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 main.py libraryName")
        sys.exit(1)
    main(sys.argv[1])
