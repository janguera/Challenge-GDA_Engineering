import requests

def get_comments(subfeddit_id, skip, limit):
    # Construir la URL con los parámetros proporcionados
    url = f"http://localhost:8080/api/v1/comments/?subfeddit_id={subfeddit_id}&skip={skip}&limit={limit}"

    # Realizar la solicitud GET a la API
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Parsear la respuesta JSON
        comments = response.json()
        return comments
    else:
        # Manejar errores de solicitud
        print(f"Error: {response.status_code}")
        return None

# Definir los parámetros
subfeddit_id = 1
skip = 0
limit = 10

# Obtener los comentarios
comments = get_comments(subfeddit_id, skip, limit)

# Mostrar los comentarios
if comments:
    for comment in comments:
        print(comment)
