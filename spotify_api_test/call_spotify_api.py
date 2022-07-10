import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

#### PART 1: Use Spotify Search to get artist IDs

utterance = "I'm looking for a song by the rolling stones"
nlu_artist_keyword = " by "
if nlu_artist_keyword in utterance:
    utterance, artist = utterance.split(nlu_artist_keyword, maxsplit=1)
    artist = f"artist:{artist}"
###### at this point, we have only extracted the artist info


# set a filter to narrow down results during search 
filter = None

type = "track"
artist_name = "rolling stones"
album_name = "aftermath"
track_name = "stupid girl"
# q is the query 
q = f"artist:{artist_name}, album:{album_name}, track:{track_name}"
#q = f"artist:Jinjer"
# specify market region (country code)
market = "DE"
results = spotify.search(q, market=market, type=type)
print(results)
for key in results.keys():
    print(key)
    for item in results[key]["items"]:
        #print(item)
        name = item["name"]
        pop = item["popularity"]
        print(f"Band: {name}, popularity: {pop}")



# birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
# #spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="stored_as_env_variable", client_secret="stored_as_env_variable"))
# results = spotify.artist_albums(birdy_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = spotify.next(results)
#     albums.extend(results['items'])

# for album in albums:
#     print(album['name'])