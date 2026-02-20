import pandas as pd
import ast
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class GameRecommender:

    # Constructor
    def __init__(self, csv_path):
        # Cargar los datos
        self.df = pd.read_csv(csv_path)
        
        # Limpieza y preparación
        self._prepare_data()
        
        # Vectorización
        self._vectorize()

    # Métodos privados
    def _prepare_data(self):
        # Convertir string de lista a lista real
        # Si ya son listas o hay errores, manejamos la excepción
        self.df["genres"] = self.df["genres"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

        # Convertir lista a texto continuo para TF-IDF
        self.df["genres_text"] = self.df["genres"].apply(
            lambda genres: " ".join(genres) if isinstance(genres, list) else ""
        )

    # Vectorización
    def _vectorize(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["genres_text"])
        # Ya no necesitamos calcular la similarity_matrix completa de golpe, 
        # la calcularemos bajo demanda para ahorrar memoria.

    # Métodos públicos
    def search(self, query, limit=20):
        return self.df[
            self.df["name"].str.contains(query, case=False, na=False)
        ]["name"].head(limit).tolist()

    # Listar juegos (opcional, para mostrar al usuario)
    def list_games(self, limit=50):
        return self.df["name"].head(limit).tolist()
    
    # Recomendaciones
    def recommend(self, game_names, top_n=5):
        # Si el usuario pasa un solo juego como string, lo metemos en una lista
        if isinstance(game_names, str):
            game_names = [game_names]

        # Verificar qué juegos de la lista existen en nuestro CSV
        valid_indices = []
        encontrados_nombres = []
        for name in game_names:
            # Búsqueda flexible: busca si el texto está contenido en el nombre (sin importar mayúsculas)
            coincidencias = self.df[self.df["name"].str.contains(name, case=False, na=False)]
            
            if not coincidencias.empty:
                # Tomamos la primera coincidencia encontrada
                idx = coincidencias.index[0]
                nombre_real = coincidencias.iloc[0]["name"]
                
                valid_indices.append(idx)
                encontrados_nombres.append(nombre_real)
            else:
                print(f"Aviso: '{name}' no se encontró en la base de datos y será ignorado.")
        
        # Si no encontramos ninguno, devolvemos una lista con el error (para evitar el deletreo)
        if not valid_indices:
            return ["Lo siento, no he encontrado ninguno de esos juegos en mi base de datos."]


        # 1. Obtenemos los vectores (coordenadas) de los juegos que sí existen
        favorite_vectors = self.tfidf_matrix[valid_indices]

        # 2. Calculamos el vector promedio y lo convertimos a un array compatible
        mean_vector = np.asarray(favorite_vectors.mean(axis=0))

        # 3. Calculamos la similitud (asegurándonos de que mean_vector sea 2D)
        similarity_scores = cosine_similarity(mean_vector.reshape(1, -1), self.tfidf_matrix).flatten()

        # 4. Obtenemos los índices ordenados de mayor a menor similitud
        sorted_indices = similarity_scores.argsort()[::-1]

        recommendations = []
        for idx in sorted_indices:
            game_name = self.df.iloc[idx]["name"]

            # No recomendar juegos que el usuario ya ha dicho que le gustan
            if game_name in game_names:
                continue

            recommendations.append(game_name)

            # Parar cuando lleguemos al número deseado
            if len(recommendations) == top_n:
                break

        return recommendations

if __name__ == "__main__":
    # Prueba rápida interna
    recommender = GameRecommender("data/games.csv")
    # Prueba con varios juegos
    print(recommender.recommend(["The Witcher 3: Wild Hunt", "Portal 2"]))