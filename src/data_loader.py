import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# Configura tu clave de API y la URL base
API_KEY = os.getenv("RAWG_API_KEY")
BASE_URL = "https://api.rawg.io/api/games"

# Define una función para pedir una página de resultados
def fetch_games(page=1):
    params = {
        "key": API_KEY,
        "page": page,
        "page_size": 40
    }

    # Realiza la solicitud a la API y devuelve los datos en formato JSON
    response = requests.get(BASE_URL, params=params)
    return response.json()

# Función para guardar los juegos en un archivo CSV
def save_games(num_pages=5):
    all_games = []

    for page in range(1, num_pages + 1):
        data = fetch_games(page)
        for game in data["results"]:
            all_games.append({
                "name": game["name"],
                "rating": game["rating"],
                "genres": [g["name"] for g in game["genres"]],
                "released": game["released"]
            })

    # Guarda los datos en un archivo CSV
    df = pd.DataFrame(all_games)
    df.to_csv("data/games.csv", index=False)

# Llama a la función para guardar los juegos
if __name__ == "__main__":
    save_games(10)