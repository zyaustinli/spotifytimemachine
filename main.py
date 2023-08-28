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

top_songs = []
no_1_song_title = soup.find(name="h3").getText()
top_songs.append(no_1_song_title)

songs = soup.find_all(name="h3", class_="c-title__link lrv-a-unstyle-link")
for song in songs:
    top_songs.append(song.getText())

top_song_titles = []
for song in top_songs:
    top_song_titles.append(song.strip())


print(top_song_titles)

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
for song in top_song_titles:
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
