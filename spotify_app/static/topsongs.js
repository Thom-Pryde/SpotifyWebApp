// JavaScript function to fetch top songs for the selected time range
function fetchTopSongs(time_range) {
  fetch(`/topsongs_api?time_range=${time_range}`)
    .then((response) => response.json())
    .then((data) => {
      const songList = data.items
        .map((item, index) => {
          const albumpic = item.album.images[2]?.url || "";
          const albumdate = item.album.release_date;
          const duration_ms = `${item.duration_ms / 1000} seconds`;
          const popularity = `${item.popularity}%`;

          return `
                    <div>
                        <img src="${albumpic}" alt="">
                        ${index + 1}. ${item.name} by ${item.artists
            .map((artist) => artist.name)
            .join(", ")}
                        <br>${albumdate}<br>${duration_ms}<br>${popularity}
                        <br><a href="${
                          item.external_urls.spotify
                        }" target="_blank">Listen on Spotify</a>
                    </div>
                `;
        })
        .join("<br>");

      document.getElementById("top-songs").innerHTML =
        songList || "No songs found.";
    })
    .catch((error) => {
      console.error("Error fetching top songs:", error);
      document.getElementById("top-songs").innerHTML = "Error loading songs.";
    });
}
