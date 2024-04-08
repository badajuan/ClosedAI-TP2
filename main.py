import requests
import sys
import ctypes

def main(libraryName):
    respose_path="response.txt"
    """
    #Indice de todos los paises
    #url = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"
    #Indice de Argentina
    url = "https://api.worldbank.org/v2/en/country/ARG/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1"
    

    resp = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if resp.status_code == 200:
        print(f"Request exitosa, guardando la respuesta en '{respose_path}'.")
        with open("response.txt","w") as file:
            file.write(resp.text)
    else:
        # Imprimir un mensaje de error si la solicitud falló
        print("Error al realizar la solicitud:", resp.status_code)
        sys.exit(1)
    """
    # Carga la librería
    library = ctypes.CDLL(libraryName)

    # Define los argumentos y retornos de la función de la librería
    library.calcGeany.argtypes = (ctypes.c_char_p, ctypes.c_char_p)
    library.calcGeany.restype = ctypes.c_int

    # Define un wrapper para llamar a la función de C
    def calcGeany(requestPath, country):
        return library.calcGeany(requestPath.encode(), country.encode())

    #ToDo: pedir al usuario el país a filtrar
    print("Retorno de la función: ",calcGeany(respose_path,"Argentina"))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 main.py libraryName")
        sys.exit(1)
    main(sys.argv[1])
