function handleButtonClick(button, timeRange) {
  // Remove the 'active' class from all buttons
  const timeRangeButtons = document.querySelectorAll(".toggle_buttons");
  timeRangeButtons.forEach((btn) => btn.classList.remove("active"));

  // Add the 'active' class to the clicked button
  button.classList.add("active");

  // Fetch the songs for the selected time range
  fetchTopSongs(timeRange);
}

function fetchTopSongs(time_range) {
  fetch(`/topsongs_api?time_range=${time_range}`)
    .then((response) => response.json())
    .then((data) => {
      const songList = data.items
        .map((item, index) => {
          const albumpic = item.album.images[2]?.url || "";
          const albumdate = item.album.release_date;
          const duration_ms = `${formatTime(item.duration_ms / 1000)}`;
          const popularity = `${item.popularity}%`;
          const albumlink = item.external_urls.spotify;

          return `
          <div class="song_item">
              <div class="album_info">
                  <img class="album_img" src="${albumpic}" alt="Album cover">

                  <div class="song_details">
                      <p class="song_index">${index + 1}.</p>
                      <p class="song_name">${item.name}</p> by 
                      <p class="artists">${item.artists
                        .map((artist) => artist.name)
                        .join(", ")}</p>
                  </div>
              </div>
              <div class="song_extra_info">
                  <span class="album-date">Release Date: ${albumdate}</span>
                  <span class="duration">track length: ${duration_ms}</span>
                  <span class="popularity">Popularity: ${popularity} (This popularity is based on the total number of plays the track has had and how recent those plays are.)</span> 
              </div>
              <div class="spotify_link">
                  <a href="${albumlink}" target="_blank">Listen on Spotify</a>
              </div>
          </div>
        `;
        })
        .join("");

      document.getElementById("top-songs").innerHTML =
        songList || "No songs found.";
    })
    .catch((error) => {
      console.error("Error fetching top songs:", error);
      document.getElementById("top-songs").innerHTML = "Error loading songs.";
    });
}

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = Math.floor(seconds % 60);
  return `${minutes} minutes and ${remainingSeconds} seconds`;
}
