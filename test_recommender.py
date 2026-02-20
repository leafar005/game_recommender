from src.recommender import GameRecommender

recommender = GameRecommender("data/games.csv")

print("Escribe juegos separados por coma:")
user_input = input()

games = [g.strip() for g in user_input.split(",")]

recommendations = recommender.recommend(games, top_n=5)

print("\nRecomendaciones:")
for game in recommendations:
    print("-", game)