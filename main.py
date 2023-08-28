import requests
from bs4 import BeautifulSoup
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth

URL = "https://www.billboard.com/charts/hot-100/"

date = input("Which year do you want to travel to? Type the date in this format: YYYY-MM-DD: ")

response = requests.get(f"{URL}{date}")
contents = response.text
soup = BeautifulSoup(contents, "html.parser")

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]


print(song_names)

client_id = ""
client_secret = ""
redirect_url = "https://example.com"

spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_url,
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt",
        #username = ""
    )
)
user_id = spotify.current_user()["id"]

year = date.split("-")[0]
track_uris = []
for song in song_names:
    try:
        result = spotify.search(q=f"track:{song} year:{year}", type="track")
        track_uri = result["tracks"]['items'][0]['uri']
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
    else:
        track_uris.append(track_uri)

playlist = spotify.user_playlist_create(
    user=user_id,
    name=f"{date} Billboard 100",
    public=False,
)

spotify.user_playlist_add_tracks(
    user=user_id,
    playlist_id=playlist['id'],
    tracks=track_uris,
)
