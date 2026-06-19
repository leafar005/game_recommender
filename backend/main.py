from fastapi import FastAPI
from pydantic import BaseModel
from src.recommender import GameRecommender

import logging

from fastapi.middleware.cors import CORSMiddleware

import os

# Esto ayuda a Render a encontrar el archivo sin importar desde dónde se ejecute
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "data", "games.csv")

#Cargar el modelo de recomendación al iniciar la aplicación
recommender = GameRecommender(csv_path)

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Game Recommendation API")

origins = ["*"]  # Para desarrollo local, permite todas las URLs

# Configuración del middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definir el modelo de datos para la solicitud de recomendación
class RecommendationRequest(BaseModel):
    games: list[str]
    top_n: int = 5

# Endpoint raíz para verificar que la API está funcionando
@app.get("/")
def root():
    return {"message": "Game Recommender API is running"}

# Endpoint para obtener recomendaciones de juegos
@app.post("/recommend")
def recommend_games(request: RecommendationRequest):
    recommendations = recommender.recommend(
        request.games, 
        top_n=request.top_n
        )
    
    logger.info("Recommendations generated successfully")
    
    return {"recommendations": recommendations}

# Endpoint para buscar juegos por nombre
@app.get("/games")
def search_games(query: str):
    return {"results": recommender.search(query)}

# Endpoint para listar juegos (opcional)
@app.get("/games/all")
def list_games(limit: int = 50):
    return {"games": recommender.list_games(limit)}