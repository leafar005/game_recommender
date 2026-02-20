# 🎮 Sistema de Recomendación de Videojuegos

Un motor de recomendación de videojuegos basado en contenido, construido con Python y técnicas de Machine Learning. El sistema analiza las características de miles de juegos para ofrecer sugerencias personalizadas basadas en la similitud de metadatos.

## 🚀 Características principales

- **Extracción de datos:** Conexión automática con la API de RAWG para obtener información actualizada de videojuegos.
- **Procesamiento de datos:** Limpieza y estructuración de metadatos (géneros, etiquetas y valoraciones).
- **Inteligencia del motor:** Implementación de vectorización **TF-IDF** para convertir texto en datos numéricos.
- **Algoritmo de similitud:** Uso del **Coseno de Similitud** para calcular y recomendar los juegos más parecidos a tus favoritos.

## 🧠 Stack Tecnológico

- **Lenguaje:** Python 3.10+
- **Análisis de Datos:** Pandas
- **Machine Learning:** Scikit-learn (NLP)
- **Backend:** FastAPI (en desarrollo)
- **Seguridad:** Python-dotenv para la gestión de API Keys

## 📂 Estructura del Proyecto

```text
game-recommender/
├── data/               # Archivos CSV con los datos de los juegos
├── notebooks/          # Experimentos y análisis exploratorio de datos
├── src/                # Código fuente del proyecto
│   ├── data_loader.py  # Script para descargar datos de la API
│   └── recommender.py  # Lógica del motor de recomendación
├── .env                # Variables de entorno (API Keys - No incluido en Git)
├── .gitignore          # Archivos excluidos del control de versiones
├── requirements.txt    # Librerías necesarias para el proyecto
└── README.md           # Documentación del proyecto
```

## 📌 Futuras mejoras

- Recomendaciones múltiples
- Perfiles de usuario
- Panel de control web
- Implementación
