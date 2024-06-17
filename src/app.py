from os import getenv
from random import choices
from spotipy import Spotify
from secrets import token_hex
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, redirect, send_file, render_template

app = Flask(__name__, template_folder = "app/templates", static_folder = "app/static")
app.secret_key = token_hex(16)

def get_all_playlists():

    spotify = Spotify(
        auth_manager = SpotifyOAuth(
            scope = getenv("SPOTIFY_SCOPE"),
            client_id = getenv("SPOTIPY_CLIENT_ID"),
            redirect_uri = getenv("SPOTIPY_REDIRECT_URI"),
            client_secret = getenv("SPOTIPY_CLIENT_SECRET")
        )
    )

    total = spotify.current_user_playlists()["total"]
    for offset in range(0, total, 50):
        for playlist in spotify.current_user_playlists(offset = offset)["items"]:
            yield {
                "id": playlist["id"],
                "name": playlist["name"],
                "image": playlist["images"][0]["url"]
            }

def get_all_playlist_track(id):

    spotify = Spotify(
        auth_manager = SpotifyOAuth(
            scope = getenv("SPOTIFY_SCOPE"),
            client_id = getenv("SPOTIPY_CLIENT_ID"),
            redirect_uri = getenv("SPOTIPY_REDIRECT_URI"),
            client_secret = getenv("SPOTIPY_CLIENT_SECRET")
        )
    )

    total = spotify.playlist_items(id)["total"]
    for offset in range(0, total, 100):
        for track in spotify.playlist_items(id, offset = offset)["items"]:
            yield {
                "id": track["track"]["album"]["id"],
                "name": track["track"]["album"]["name"],
                "artist": track["track"]["artists"][0]["name"],
                "image": track["track"]["album"]["images"][1]["url"]
            }

@app.route("/")
def index(): return render_template("index.html", playlists = list(get_all_playlists()))

@app.route("/playlist/<id>")
def playlist(id): return render_template("playlist.html", tracks = list(get_all_playlist_track(id)))

@app.get("/robots.txt")
@app.get("/sitemap.xml")
@app.get("/manifest.json")
@app.get("/service-worker.js")
@app.get("/.well-known/assetlinks.json")
def serve_file(): return send_file(f"app/{request.path}")

@app.errorhandler(404)
@app.errorhandler(405)
def error(_): return redirect("/")

if __name__ == "__main__": app.run()