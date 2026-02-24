// Referencias a elementos del DOM usados en toda la pagina
const searchInput = document.getElementById("game-search");
const addButton = document.getElementById("add-game");
const favoritesList = document.getElementById("favorites-list");
const getRecommendations = document.getElementById("get-recommendations");
const resultsList = document.getElementById("results-list");
const aboutToggle = document.getElementById("about-toggle");
const aboutPanel = document.getElementById("about-panel");
const aboutClose = document.getElementById("about-close");

// Estado en memoria: lista de juegos favoritos seleccionados
let favorites = [];

// Contenedor donde se pintan las sugerencias de autocompletado
const autocompleteContainer = document.getElementById("autocomplete-results");

// Escucha del input: pide sugerencias al backend cuando hay al menos 3 caracteres
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

// Pinta la lista de sugerencias y permite elegir una para rellenar el buscador
function displaySuggestions(games) {
    autocompleteContainer.innerHTML = "";
    if (!games || games.length === 0) return;

    games.slice(0, 10).forEach(game => {
        const item = document.createElement("div");
        item.className = "autocomplete-item";

        if (game.cover_url) {
            const img = document.createElement("img");
            img.src = game.cover_url;
            img.alt = `Cover de ${game.name}`;
            item.appendChild(img);
        }

        const name = document.createElement("span");
        name.textContent = game.name;
        item.appendChild(name);

        item.addEventListener("click", () => {
            searchInput.value = game.name;
            autocompleteContainer.innerHTML = "";
        });

        autocompleteContainer.appendChild(item);
    });
}

// Crea un elemento de lista con texto e imagen opcional
function createGameListItem(game, withGenres = true) {
    const li = document.createElement("li");
    li.className = "game-item";

    if (game.cover_url) {
        const img = document.createElement("img");
        img.src = game.cover_url;
        img.alt = `Cover de ${game.name}`;
        img.className = "game-cover";
        li.appendChild(img);
    }

    const info = document.createElement("div");
    info.className = "game-main";

    const name = document.createElement("span");
    name.className = "game-name";
    name.textContent = game.name;
    info.appendChild(name);

    li.appendChild(info);

    if (withGenres) {
        const genre = document.createElement("span");
        genre.className = "game-genre";
        genre.textContent = game.genres ? game.genres.join(", ") : "Sin géneros";
        li.appendChild(genre);
    }

    return li;
}

// Re-pinta la lista de favoritos con el estado actual
function updateFavorites() {
    favoritesList.innerHTML = ""; // Limpiamos la lista actual
    favorites.forEach(game => {
        // Fabricamos el elemento y lo pegamos
        favoritesList.appendChild(createGameListItem(game, false));
    });
}

// Re-pinta la lista de recomendaciones con resultados nuevos
function updateResults(recommendations) {
    resultsList.innerHTML = ""; 
    recommendations.forEach(game => {
        resultsList.appendChild(createGameListItem(game, true));
    });
}

// Click en "Añadir": busca el mejor resultado y lo agrega a favoritos si no estaba
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

// Click en "Recomiéndame": envia solo los nombres y pinta las respuestas
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
// Limpia favoritos, recomendaciones y el campo de texto
clearButton.addEventListener("click", () => {
    favorites = [];
    updateFavorites();
    resultsList.innerHTML = ""; // Limpiamos también las recomendaciones

    searchInput.value = ""; // Vaciamos el buscador
});

// Pestaña About: alterna visibilidad del panel (se ejecuta solo si existe)
if (aboutToggle && aboutPanel) {
    aboutToggle.addEventListener("click", () => {
        aboutPanel.classList.toggle("open");
    });
}

if (aboutClose && aboutPanel) {
    aboutClose.addEventListener("click", () => {
        aboutPanel.classList.remove("open");
    });
}