from src.recommender import GameRecommender

recommender = GameRecommender("data/games.csv")

print("Escribe juegos separados por coma (ej. Dredge, Portal 2):")
user_input = input()

# Limpiar espacios y obtener lista de juegos
games = [g.strip() for g in user_input.split(",")]

# Obtener recomendaciones
recommendations = recommender.recommend(games, top_n=5)

# Imprimir recomendaciones
print("\nRecomendaciones generadas:")
print("-" * 30)

# Iterar sobre las recomendaciones
for game in recommendations:
    # Obtener nombre y cover (no se muestra en consola, pero se podría usar para una interfaz gráfica)
    game_name = game["name"]
    cover= game["cover_url"]

    print(f"Juego: {game_name}")

    # Aquí podrías agregar lógica para mostrar la portada si tuvieras una interfaz gráfica, por ejemplo:
    if cover:
        print(f"Portada disponible en: {cover}")
    else:
        print("No se encontró portada para este juego.")

    print("-" * 30)