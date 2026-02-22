const searchInput = document.getElementById("game-search");
const addButton = document.getElementById("add-game");
const favoritesList = document.getElementById("favorites-list");
const getRecommendations = document.getElementById("get-recommendations");
const resultsList = document.getElementById("results-list");

// Lista para almacenar los juegos favoritos del usuario
let favorites = [];


const autocompleteContainer = document.getElementById("autocomplete-results");

searchInput.addEventListener("input", async () => {
    const query = searchInput.value.trim();
    
    // Limpiar sugerencias si el texto es muy corto
    if (query.length < 3) {
        autocompleteContainer.innerHTML = "";
        return;
    }

    try {
        const response = await fetch(`https://game-recommender-rl3g.onrender.com/games?query=${query}`);
        const data = await response.json();
        
        displaySuggestions(data.results);
    } catch (error) {
        console.error("Error buscando sugerencias:", error);
    }
});

function displaySuggestions(games) {
    autocompleteContainer.innerHTML = ""; // Limpiar anteriores

    games.forEach(game => {
        const div = document.createElement("div");
        div.className = "autocomplete-item";
        
        // Estructura: Imagen + Nombre
        div.innerHTML = `
            ${game.cover_url ? `<img src="${game.cover_url}">` : ''}
            <span>${game.name}</span>
        `;

        // Al hacer clic en una sugerencia
        div.addEventListener("click", () => {
            // Añadir directamente a favoritos
            if (!favorites.some(f => f.name === game.name)) {
                favorites.push(game);
                updateFavorites();
            }
            // Limpiar buscador y sugerencias
            searchInput.value = "";
            autocompleteContainer.innerHTML = "";
        });

        autocompleteContainer.appendChild(div);
    });
}

// 4. Cerrar sugerencias si se hace clic fuera del buscador
document.addEventListener("click", (e) => {
    if (e.target !== searchInput) {
        autocompleteContainer.innerHTML = "";
    }
});

function createGameListItem(game) {
    const li = document.createElement("li");
    li.style.display = "flex"; // Para alinear el texto y el botón
    li.style.alignItems = "center";
    li.style.marginBottom = "10px";

    if (game.cover_url) {

        // Crear elemento de imagen para la portada del juego
        const img = document.createElement("img");
        img.src = game.cover_url;
        img.alt = `Cover de ${game.name}`;
        img.style.width = "60px";
        img.style.height = "auto";
        img.style.borderRadius = "5px";
        img.style.marginRight = "15px";

        // Agregar la imagen al elemento de lista
        li.appendChild(img);
    }

    const span = document.createElement("span");
    span.textContent = game.name;
    li.appendChild(span);

    return li;
}

// Agregar juego a favoritos
function updateFavorites() {
    favoritesList.innerHTML = ""; // Limpiamos la lista actual
    favorites.forEach(game => {
        // Fabricamos el elemento y lo pegamos
        favoritesList.appendChild(createGameListItem(game));
    });
}

// Actualizar la lista de recomendaciones
function updateResults(recommendations) {
    resultsList.innerHTML = ""; 
    recommendations.forEach(game => {
        resultsList.appendChild(createGameListItem(game));
    });
}

// Evento para agregar juego a favoritos
addButton.addEventListener("click", async () => {
    const query = searchInput.value.trim();
    if (!query) return;

    // Pedimos al backend que busque el juego
    const response = await fetch(`https://game-recommender-rl3g.onrender.com/games?query=${query}`);
    const data = await response.json();

    if (data.results && data.results.length > 0) {
        const selectedGame = data.results[0]; // Nos quedamos con el mejor resultado
        
        // Comprobamos si el nombre de ese juego ya existe en nuestra lista de favoritos
        const alreadyInFavorites = favorites.some(game => game.name === selectedGame.name);
        
        if (!alreadyInFavorites) {
            favorites.push(selectedGame); // Guardamos el objeto completo (nombre + foto)
            updateFavorites();            // Actualizamos la pantalla
        }
    }

    searchInput.value = ""; // Vaciamos el buscador
});

// Evento para obtener recomendaciones
getRecommendations.addEventListener("click", async () => {
    if (favorites.length === 0) return;

    // .map() extrae solo los nombres de nuestra lista de objetos
    // favorites = [{name: "Dredge", cover_url: "..."}] ---> favoriteNames = ["Dredge"]
    const favoriteNames = favorites.map(game => game.name);

    // Hacemos la petición a Python enviándole solo los nombres
    const response = await fetch("https://game-recommender-rl3g.onrender.com/recommend", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ games: favoriteNames, top_n: 5 })
    });

    const data = await response.json();
    
    // Python ha hecho su magia y nos devuelve nuevos objetos con foto. Los pintamos.
    updateResults(data.recommendations);
});

const clearButton = document.getElementById("clear-list");
clearButton.addEventListener("click", () => {
    favorites = [];
    updateFavorites();
    resultsList.innerHTML = ""; // Limpiamos también las recomendaciones

    searchInput.value = ""; // Vaciamos el buscador
});