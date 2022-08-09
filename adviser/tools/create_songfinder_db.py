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
    # print("Artist found: " + results["artists"]["items"][0]["name"])
    return results["artists"]["items"][0]["id"]


def get_top_tracks(artist_id):
    results = spotify.artist_top_tracks(artist_id)
    return results["tracks"]


def get_minimum_album_number(min, results):
    """
    Check whether it's possible to retrieve <min> unique albums. 
    If there are less unique albums in the result than <min>, adjust <min>.
    
    Returns
        min (int)
    """
    num_unique = len(get_unique_albums(results))
    if num_unique < min:
        min = num_unique
    return min


def get_unique_albums(results):
    unique_albums = []
    for track in results:
        if not track["album"]["name"] in unique_albums:
            unique_albums.append(track["album"]["name"])
    return unique_albums


def get_track_data(track):
    track_name = track["name"]
    track_id = track["id"]
    album_name = track["album"]["name"]
    album_id = track["album"]["id"]
    return track_name, track_id, album_name, album_id


def get_artist_names(filepath):
    with open(filepath, "r") as f:
        return [line.rstrip() for line in f]


def create_and_connect_db(filepath):
    con = sqlite3.connect(filepath)
    cur = con.cursor()
    cur.execute(
        """CREATE TABLE songfinder (
        artist_name text,
        artist_id text,
        album_name text,
        album_id text,
        track_name text,
        track_id text
    )"""
    )
    con.commit()
    return con, cur


def connect_db(filepath):
    con = sqlite3.connect(filepath)
    cur = con.cursor()
    return con, cur


def add_row_to_db(con, cur, art_name, art_id, alb_name, alb_id, track_name, track_id):
    cur.execute(
        "INSERT INTO songfinder VALUES (?, ?, ?, ?, ?, ?)",
        (art_name, art_id, alb_name, alb_id, track_name, track_id),
    )


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
    # For each artist, retrieve albums and tracks for specified number of top tracks
    album_limit = 3
    # create file with albums and artists for users as information what can be requested
    csv_file = args.db_file.rstrip(".db") + "_db.csv"
    if os.path.isfile(csv_file):
        os.remove(csv_file)
    with open(csv_file, "a") as f:
        for artist_name in artist_names:

            artist_id = get_artist_id(artist_name)
            top_tracks = get_top_tracks(artist_id)
            album_limit = get_minimum_album_number(album_limit, top_tracks)
            unique_albums = get_unique_albums(top_tracks)
            num_added_items = 0
            i = 0
            while num_added_items < album_limit:
                track_name, track_id, album_name, album_id = get_track_data(
                    top_tracks[i]
                )
                # add to db if no track of this album has been added before
                if album_name in unique_albums:
                    unique_albums.remove(album_name)
                    # remove parentheses so the system will recognize user inform
                    album_name = (
                        album_name.replace("(", "")
                        .replace(")", "")
                        .replace(",", "")
                        .replace("[", "")
                        .replace("]", "")
                    )

                    f.write(f"{artist_name},{album_name}\n")

                    # print(f"adding {track_name}, {album_name}")

                    add_row_to_db(
                        con,
                        cur,
                        artist_name,
                        artist_id,
                        album_name,
                        album_id,
                        track_name,
                        track_id,
                    )
                    num_added_items += 1
                i += 1
        con.commit()
        con.close()
