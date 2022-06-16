import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
import argparse
import os

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def get_artist_id(artist_name):
    type = "artist"
    q = artist_name
    market = "DE"
    limit = 3
    results = spotify.search(q, type=type, market=market, limit=limit)
    print("Artist found: " + results["artists"]["items"][0]["name"])
    return results["artists"]["items"][0]["id"]

def get_top_track_album(artist_id):
    results = spotify.artist_top_tracks(artist_id)
    top_track = results["tracks"][0]
    track_name = top_track["name"]
    track_id = top_track ['id']
    album_name = top_track["album"]["name"]
    album_id = top_track["album"]["id"]
    return track_name, track_id, album_name , album_id


def get_artist_names(filepath):
    with open(filepath, "r") as f:
        return [line.rstrip() for line in f]

def create_and_connect_db(filepath):
    con = sqlite3.connect(filepath)
    cur = con.cursor()
    cur.execute("""CREATE TABLE songfinder (
        artist_name text,
        artist_id text,
        album_name text,
        album_id text,
        track_name text,
        track_id text
    )""")
    con.commit()
    return con, cur

def connect_db(filepath):
    con = sqlite3.connect(filepath)
    cur = con.cursor()
    return con, cur

def add_row_to_db(con, cur, art_name, art_id, alb_name, alb_id, track_name, track_id):
    cur.execute("INSERT INTO songfinder VALUES (?, ?, ?, ?, ?, ?)", (art_name, art_id, alb_name, alb_id, track_name, track_id))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("artists_file", help="file containing a list of artists")
    parser.add_argument("db_file", help="filepath where database will be stored")
    args = parser.parse_args()

    if not os.path.exists(args.db_file):
        con, cur = create_and_connect_db(args.db_file)
    else:
        con, cur = connect_db(args.db_file)

    artist_names = get_artist_names(args.artists_file)
    for artist_name in artist_names:
        artist_id = get_artist_id(artist_name)
        track_name, track_id, album_name, album_id = get_top_track_album(artist_id)
        add_row_to_db(con, cur, artist_name, artist_id, album_name, album_id, track_name, track_id)
    con.commit()
    con.close()