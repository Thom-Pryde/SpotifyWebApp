document.querySelector("#search_button").addEventListener("click", (event) => {
  //# included as its an id not class
  const search_query = document.getElementById("search").value;

  if (search_query) {
    searchItems(search_query);
  } else {
    //input empty
    document.querySelector(".artitssongsearchdiv").innerHTML = "";
  }
});

const searchItems = async (search_query) => {
  if (!search_query) {
    //if empty or just a wrong thing to enter
    document.querySelector(".artitssongsearchdiv").innerHTML = ""; //search bar now gonan be empty incase they dont know if they typed in blank shit
    return;
  }
  try {
    const response = await fetch(
      `/artistsearch_api?search_query=${search_query}`
    );
    const data = await response.json();

    const searchresults = data.tracks.items
      .map((item) => {
        const albumpic = item.album.images[2]?.url || "";
        const name = item.name;
        const link = item.external_urls.spotify;
        const artistnames = item.artists
          .map((artist) => artist.name)
          .join(", ");

        return `
            <div class="search-item">
            <div class ="inside-item">
                <img src="${albumpic}" />
                <p>${name} by ${artistnames}</p>
                <a href="${link}" target="_blank">Listen on Spotify</a>

              </div>
            </div>
        `;
      })
      .join("");

    document.querySelector(".artitssongsearchdiv").innerHTML =
      searchresults || "No results found.";
  } catch (error) {
    console.error("Error fetching search results:", error);
    document.querySelector(".artitssongsearchdiv").innerHTML =
      "Error loading results.";
  }
};
