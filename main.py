import requests
import sys
import ctypes

def main(libraryName):
    #url = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"
    url = "https://api.worldbank.org/v2/en/country/ARG/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1"

    resp = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if resp.status_code == 200:
        print("Request exitosa, guardando la respuesta en 'response.txt'.")
        with open("response.txt","w") as file:
            file.write(resp.text)
    else:
        # Imprimir un mensaje de error si la solicitud falló
        print("Error al realizar la solicitud:", resp.status_code)
        sys.exit(1)

    # Carga la librería
    libhello = ctypes.CDLL(libraryName)

    # Define los argumentos y retornos de la función
    libhello.hello.argtypes = ()
    libhello.hello.restype = None

    # Define un wrapper para llamar a la función de C
    def hello():
        libhello.hello()    

    hello()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script_name.py library_name")
        sys.exit(1)
    main(sys.argv[1])
