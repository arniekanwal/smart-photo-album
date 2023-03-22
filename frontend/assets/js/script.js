// Titles: https://omdbapi.com/?s=thor&page=1&apikey=fc1fef96
// details: http://www.omdbapi.com/?i=tt3896198&apikey=fc1fef96

const photoSearchBox = document.getElementById('photo-search-box');
const searchList = document.getElementById('search-list');
const resultGrid = document.getElementById('result-grid');

// load photos from API
async function loadphotos(searchTerm){
    const URL = `https://omdbapi.com/?s=${searchTerm}&page=1&apikey=fc1fef96`;
    const res = await fetch(`${URL}`);
    const data = await res.json();
    // console.log(data.Search);
    if(data.Response == "True") displayphotoList(data.Search);
}

function findphotos(){
    let searchTerm = (photoSearchBox.value).trim();
    if(searchTerm.length > 0){
        searchList.classList.remove('hide-search-list');
        loadphotos(searchTerm);
    } else {
        searchList.classList.add('hide-search-list');
    }
}

function displayphotoList(photos){
    searchList.innerHTML = "";
    for(let idx = 0; idx < photos.length; idx++){
        let photoListItem = document.createElement('div');
        photoListItem.dataset.id = photos[idx].imdbID; // setting photo id in  data-id
        photoListItem.classList.add('search-list-item');
        if(photos[idx].Poster != "N/A")
            photoPoster = photos[idx].Poster;
        else 
            photoPoster = "image_not_found.png";

        photoListItem.innerHTML = `
        <div class = "search-item-thumbnail">
            <img src = "${photoPoster}">
        </div>
        <div class = "search-item-info">
            <h3>${photos[idx].Title}</h3>
            <p>${photos[idx].Year}</p>
        </div>
        `;
        searchList.appendChild(photoListItem);
    }
    loadphotoDetails();
}

function loadphotoDetails(){
    const searchListphotos = searchList.querySelectorAll('.search-list-item');
    searchListphotos.forEach(photo => {
        photo.addEventListener('click', async () => {
            // console.log(photo.dataset.id);
            searchList.classList.add('hide-search-list');
            photoSearchBox.value = "";
            const result = await fetch(`http://www.omdbapi.com/?i=${photo.dataset.id}&apikey=fc1fef96`);
            const photoDetails = await result.json();
            // console.log(photoDetails);
            displayphotoDetails(photoDetails);
        });
    });
}

function displayphotoDetails(details){
    resultGrid.innerHTML = `
    <div class = "photo-poster">
        <img src = "${(details.Poster != "N/A") ? details.Poster : "image_not_found.png"}" alt = "photo poster">
    </div>
    <div class = "photo-info">
        <h3 class = "photo-title">${details.Title}</h3>
        <ul class = "photo-misc-info">
            <li class = "year">Year: ${details.Year}</li>
            <li class = "rated">Ratings: ${details.Rated}</li>
            <li class = "released">Released: ${details.Released}</li>
        </ul>
        <p class = "genre"><b>Genre:</b> ${details.Genre}</p>
        <p class = "writer"><b>Writer:</b> ${details.Writer}</p>
        <p class = "actors"><b>Actors: </b>${details.Actors}</p>
        <p class = "plot"><b>Plot:</b> ${details.Plot}</p>
        <p class = "language"><b>Language:</b> ${details.Language}</p>
        <p class = "awards"><b><i class = "fas fa-award"></i></b> ${details.Awards}</p>
    </div>
    `;
}


window.addEventListener('click', (event) => {
    if(event.target.className != "form-control"){
        searchList.classList.add('hide-search-list');
    }
});