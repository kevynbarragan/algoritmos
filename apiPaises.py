import requests

# URL con los campos que pide el servidor
url = "https://restcountries.com/v3.1/all?fields=name,capital,region,population"
respuesta = requests.get(url)

if respuesta.status_code == 200:
    paises = respuesta.json()
    print("Listado de países:\n")
    for pais in paises[:10]:  # solo mostramos 10
        nombre = pais["name"]["common"]
        capital = pais.get("capital", ["No tiene"])[0]
        region = pais.get("region", "Desconocida")
        poblacion = pais.get("population", "Desconocida")
        print("País:", nombre, "| Capital:", capital, "| Región:", region, "| Población:", poblacion)
else:
    print("Error en la petición. Código:", respuesta.status_code)
    print("Mensaje:", respuesta.text)
