import requests
import os
from dotenv import load_dotenv
import pandas as pd

# Para gestionar los tokens temporales de IGDB
from datetime import datetime, timezone

load_dotenv()

# Cargamos el ID y el secret desde .env
CLIENT_ID = os.getenv("IGDB_CLIENT_ID")
CLIENT_SECRET = os.getenv("IGDB_CLIENT_SECRET")

# Función para obtener un token de acceso
def get_access_token():
    url = f"https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials"
    #Hacemos la petición POST para obtener el token
    response = requests.post(url)
    data = response.json()

    # Devolvemos el token de acceso
    return data["access_token"]

# Funcion para pedir resultados a IGDB
def fetch_games(access_token, offset=0):
    url = "https://api.igdb.com/v4/games"

    # Configuramos los headers con el token de acceso
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {access_token}"
    }

    #Consulta Apicalypse (similar a SQL pero para IGDB)
    # Obtenemos el nombre, rating (para poner primero los de mejor puntuación), géneros, temas, modos de juego (Single-player, Multiplayer), fecha de lanzamiento y URL de la portada
    body = f"""
    fields name, rating, genres.name, themes.name, game_modes.name, first_release_date, cover.url;
    where rating != null & genres != null & cover != null;
    limit 500;
    offset {offset};
    sort rating desc;
    """

    # Hacemos la petición POST a IGDB con la consulta
    response = requests.post(url, headers=headers, data=body)
    return response.json()

#Función para guardar los datos en un CSV
def save_games(num_pages=10): # 10 páginas de 500 juegos = 5000 juegos
    print("Obteniendo token de acceso...")
    access_token = get_access_token()

    if not access_token:
        print("Error: No se pudo obtener el token de acceso.")
        return
    
    all_games = []
    print("Obteniendo datos de juegos...")

    for page in range(num_pages):
        # Extraemos los juegos de la página actual
        offset = page * 500
        data = fetch_games(access_token, offset)

        for game in data:
            # Extraemos los géneros, temas y modos de juego como listas de nombres
            genres = [g["name"] for g in game.get("genres", [])] if "genres" in game else []
            themes = [t["name"] for t in game.get("themes", [])] if "themes" in game else []
            modes = [m["name"] for m in game.get("game_modes", [])] if "game_modes" in game else []

            #Unimos géneros, temas y modos en una sola lista para facilitar la recomendación
            all_tags = genres + themes + modes

            # Convertimos la fecha de lanzamiento a un formato legible
            released = ""
            if "first_release_date" in game:
                released = datetime.fromtimestamp(game["first_release_date"], timezone.utc).strftime('%Y-%m-%d')

            #Arreglamos la URL de la portada para obtener una imagen de alta resolución
            cover_url =""
            if "cover" in game and "url" in game["cover"]:
                cover_url = game["cover"]["url"].replace("t_thumb", "t_cover_big")

            # Agregamos el juego a la lista de todos los juegos
            all_games.append({
                "name": game.get("name", "Desconocido"),
                "rating": round(game.get("rating", 0.0), 2),
                "genres": all_tags,
                "release_date": released,
                "cover_url": cover_url
            })

    # Guardamos todos los juegos en un archivo CSV
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(all_games)
    df.to_csv("data/games.csv", index=False)
    print(f"Datos guardados en 'data/games.csv' con {len(all_games)} juegos.")

if __name__ == "__main__":
    # 4 paginas = 2000 juegos, 
    # 10 páginas = 5000 juegos
    # 20 páginas = 10000 juegos (puede ser demasiado)
    # Cuidado con el número de páginas porque IGDB tiene un límite de peticiones por minuto
    save_games(10) 