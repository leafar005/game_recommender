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
        # Convertir la columna 'genres' de string a lista
        self.df["genres"] = self.df["genres"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

        # El algoritmo TF-IDF no funciona con listas, así que convertimos las listas de géneros a strings
        self.df["genres_text"] = self.df["genres"].apply(
            lambda genres: " ".join(genres) if isinstance(genres, list) else ""
            )
        
        # Asegurarnos de que la columna 'cover_url' existe
        if "cover_url" in self.df.columns:
            self.df["cover_url"] = self.df["cover_url"].fillna("")
        
    # Vectorización de los géneros usando TF-IDF, lo que nos permitirá calcular similitudes entre juegos
    def _vectorize(self):
        # Crear el vectorizador TF-IDF y transformar la columna 'genres_text' en una matriz de características
        # El parámetro stop_words="english" se utiliza para eliminar palabras comunes en inglés que no aportan mucho significado (como "the", "and", etc.)  
        self.vectorizer = TfidfVectorizer(stop_words="english")

        # La matriz resultante tendrá una fila por juego y una columna por término (género), con valores que representan la importancia de cada género para cada juego
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["genres_text"])

    # Método para obtener recomendaciones de juegos
    def search(self, query, limit=20):
        # Buscar juegos que contengan el término de búsqueda en su título
        results = self.df[self.df["name"].str.contains(query, case=False, na=False)].head(limit)
        
        # Crear una lista de resultados
        lista_resultados = []

        # Iterar sobre los resultados y agregarlos a la lista
        for _, row in results.iterrows():
            lista_resultados.append({
                "name": row["name"],
                "cover_url": row["cover_url"]
            })
        return lista_resultados
    
    # Método para recomendar juegos similares a una lista de juegos proporcionada por el usuario
    def list_games(self, limit=50):
        # Listar los juegos disponibles
        return self.df["name"].head(limit).tolist()
    
    # Método para recomendar juegos similares a una lista de juegos proporcionada por el usuario
    def recommend(self, game_names, top_n=5):
        # Verificar que los juegos proporcionados por el usuario existan en el dataset
        if isinstance(game_names, str):
            game_names = [game_names]

        #Buscar los índices de los juegos proporcionados por el usuario
        valid_indices = []
        for name in game_names:
            # Buscar juegos que contengan el término de búsqueda en su título
            coincidencias = self.df[self.df["name"].str.contains(name, case=False, na=False)]
            # Si se encuentran coincidencias, agregar el índice del primer resultado a la lista de índices válidos
            if not coincidencias.empty:
                valid_indices.append(coincidencias.index[0])
            
        # Si no se encontraron índices válidos, devolver una lista vacía
        if not valid_indices:
            return [{"name": "No se encontraron juegos válidos", "cover_url": ""}]
        
        # Obtener los vectores TF-IDF de los juegos proporcionados por el usuario
        favorite_vectors = self.tfidf_matrix[valid_indices]

        # Calcular el vector promedio de los juegos favoritos del usuario
        mean_vector = np.asarray(favorite_vectors.mean(axis=0))

        # Calcular la similitud coseno entre el vector promedio y todos los vectores de juegos en el dataset
        similarity_scores = cosine_similarity(mean_vector.reshape(1, -1), self.tfidf_matrix).flatten()

        # Obtener los índices de los juegos más similares (excluyendo los juegos proporcionados por el usuario)
        sorted_indices = similarity_scores.argsort()[::-1]

        # Crear una lista de resultados
        recommendations = []
        for idx in sorted_indices:
            # Obtener el nombre del juego y la URL de la portada
            # El método iloc se utiliza para acceder a una fila específica del DataFrame por su índice. En este caso, se accede a la fila correspondiente al índice idx, 
            # que es uno de los índices de los juegos más similares calculados anteriormente.
            row = self.df.iloc[idx]
            game_name = row["name"]
            cover_url = row.get("cover_url", "")
            genres = row.get("genres", [])

            # Saltar los juegos proporcionados por el usuario
            if game_name in game_names:
                continue  

            # Agregar el juego a la lista de recomendaciones
            recommendations.append({
                "name": game_name,
                "cover_url": cover_url,
                "genres": genres
            })

            if len(recommendations) == top_n:
                break

        return recommendations
    
if __name__ == "__main__":
    recommender = GameRecommender("data/games.csv")
    print("Probando recomendaciones para Dredge:")
    print(recommender.recommend(["Dredge"]))