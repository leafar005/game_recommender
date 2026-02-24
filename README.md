# 🎮 Sistema de Recomendación de Videojuegos

Un motor de recomendación de videojuegos basado en contenido, construido con **Python**, **FastAPI** y técnicas de **Machine Learning**. El sistema analiza metadatos de miles de juegos para ofrecer sugerencias personalizadas basadas en la similitud de géneros, temas y modos de juego.

## 🌐 Página web
Puedes ver el proyecto en funcionamiento [aquí](https://leafar005.github.io/game_recommender/).

## 🚀 Características principales

- **Extracción de datos:** Conexión automática con la **API de IGDB** (v4) para obtener información actualizada como nombres, ratings y portadas en alta resolución.
- **Procesamiento de datos:** Limpieza y estructuración de metadatos (géneros, temas y modos de juego) utilizando **Pandas**.
- **Inteligencia del motor:** Implementación de vectorización **TF-IDF** para convertir etiquetas de texto en datos numéricos procesables.
- **Algoritmo de similitud:** Uso del **Coseno de Similitud** para calcular y recomendar los juegos más parecidos a tus favoritos.
- **API REST:** Backend desarrollado con **FastAPI** que permite buscar juegos y obtener recomendaciones mediante endpoints.

## 🧠 Stack Tecnológico

- **Lenguaje:** Python 3.10+.
- **Análisis de Datos:** Pandas.
- **Machine Learning:** Scikit-learn (TF-IDF y Similitud Coseno).
- **Backend:** FastAPI & Uvicorn.
- **Seguridad:** Python-dotenv para la gestión de API Keys de IGDB.

## 📂 Estructura del Proyecto

```text
game-recommender/
├── data/               # Archivos CSV con los datos de los juegos
├── docs/               # Interfaz web para GitHub Pages (HTML, CSS, JS)
├── src/                # Código fuente del proyecto
│   ├── data_loader.py  # Script para extraer datos de la API de IGDB
│   └── recommender.py  # Lógica del motor de recomendación
├── .env                # Variables de entorno (API Keys - No incluido en Git)
├── main.py             # Punto de entrada de la API FastAPI
├── Procfile            # Configuración para despliegue en la nube
├── requirements.txt    # Librerías necesarias para el proyecto
└── test_recommender.py # Script para probar recomendaciones por consola
```
## 🛠️ Instalación y Uso

### 1. Configurar el entorno
Instala las dependencias necesarias:
```bash
pip install -r requirements.txt
```

### 2. Configurar API Keys

Crea un archivo .env con tus credenciales de IGDB:
```bash
IGDB_CLIENT_ID=tu_client_id
IGDB_CLIENT_SECRET=tu_client_secret
```

### 3. Cargar datos

Ejecuta el script para generar el archivo data/games.csv:
```Bash
python src/data_loader.py
```

### 4. Probar el recomendador (Consola)

Puedes probar el motor directamente sin iniciar el servidor:
```Bash
python test_recommender.py
```

### 5. Ejecutar la API

Inicia el servidor de FastAPI:
```Bash
uvicorn main:app --reload
```

## 📡 Endpoints Principales

- **POST /recommend:** Recibe una lista de juegos y devuelve las mejores recomendaciones.

- **GET /games?query={nombre}:** Busca juegos específicos por nombre.

- **GET /games/all:** Lista los juegos disponibles en el sistema.
