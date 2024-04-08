import requests
import sys
import ctypes
import json
import numbers

def main(libraryName):
    ""
    #Indice de todos los paises
    url = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"
    #Indice de Argentina
    #url = "https://api.worldbank.org/v2/en/country/ARG/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1"
    

    resp = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if resp.status_code == 200:
        print(f"Request exitosa.")
    else:
        # Imprimir un mensaje de error si la solicitud falló
        print("Error al realizar la solicitud:", resp.status_code)
        sys.exit(1)
    ""
    data =json.loads(resp.text)
    
    #desiredCountry = input("De que país desea conocer el indice gini? ")
    desiredCountry= "Argentina"

    giniValues = [(entry["date"], entry["value"]) for entry in data[1] if entry["country"]["value"] == desiredCountry]

    print(f"Valores numéricos para {desiredCountry}(año, valor):", giniValues)

    # Carga la librería
    library = ctypes.CDLL(libraryName)

    # Define los argumentos y retornos de la función de la librería
    library.calcGeany.argtypes = [ctypes.c_float]
    library.calcGeany.restype = ctypes.c_int

    # Define un wrapper para llamar a la función de C
    def calcGeany(value):
        return library.calcGeany(value)

    for _, value in giniValues:
        if isinstance(value, numbers.Number):
            print(calcGeany(value))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 main.py libraryName")
        sys.exit(1)
    main(sys.argv[1])
