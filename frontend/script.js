const searchInput = document.getElementById("game-search");
const addButton = document.getElementById("add-game");
const favoritesList = document.getElementById("favorites-list");
const getRecommendations = document.getElementById("get-recommendations");
const resultsList = document.getElementById("results-list");

let favorites = [];

addButton.addEventListener("click", async () => {
    const query = searchInput.value.trim();
    if (!query) return;

    // Buscar juegos que coincidan en la API
    const response = await fetch(`http://127.0.0.1:8000/games?query=${query}`);
    const data = await response.json();

    if (data.results.length > 0) {
        const selectedGame = data.results[0]; // Elegir el primero
        if (!favorites.includes(selectedGame)) {
            favorites.push(selectedGame);
            updateFavorites();
        }
    }

    searchInput.value = "";
});

getRecommendations.addEventListener("click", async () => {
    if (favorites.length === 0) return;

    const response = await fetch("http://127.0.0.1:8000/recommend", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ games: favorites, top_n: 5 })
    });

    const data = await response.json();
    updateResults(data.recommendations);
});

function updateFavorites() {
    favoritesList.innerHTML = "";
    favorites.forEach(game => {
        const li = document.createElement("li");
        li.textContent = game;
        favoritesList.appendChild(li);
    });
}

function updateResults(recommendations) {
    resultsList.innerHTML = "";
    recommendations.forEach(game => {
        const li = document.createElement("li");
        li.textContent = game;
        resultsList.appendChild(li);
    });
}