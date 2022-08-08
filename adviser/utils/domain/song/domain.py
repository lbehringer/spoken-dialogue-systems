### Domain file for Songfinder

### for imports, refer to examples/webapi/weather/domain.py

from typing import List, Iterable
import json

# from urllib.request import urlopen
import spotipy  # use this instead of urlopen
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

from utils.domain.lookupdomain import LookupDomain

# SPOTIPY_CLIENT_ID = "this_needs_to_be_environment_variable"
# SPOTIPY_CLIENT_SECRET = "this_needs_to_be_environment_variable"


### class SongDomain
class SongDomain(LookupDomain):
    """Domain for the Spotify API.

    Attributes:
        last_results (List[dict]): Current results which the user might request info about
    """

    def __init__(self):
        LookupDomain.__init__(self, "SongDomain", "songfinder")
        self.last_results = []
        self.spotify = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials()
        )

    def find_entities(self, constraints: dict, requested_slots: Iterable = iter(())):
        """Returns all entities from the data backend that meet the constraints.
        
        Args:
            constraints (dict): Slot-value mapping of constraints.
                                If empty, all entities in the database will be returned.
            requested_slots (Iterable): list of slots that should be returned in addition to the
                                        system requestable slots and the primary key
                        
        """
        #####print(f"last_results: {self.last_results}")
        if "artist_name" in constraints and "album_name" in constraints:

            if "track_name" in constraints:
                response = self._query(
                    constraints["artist_name"],
                    constraints["album_name"],
                    constraints["track_name"],
                )
            else:
                response = self._query(
                    constraints["artist_name"], constraints["album_name"]
                )
            if response is None:
                return []
            description = "description_placeholder"
            result_list = []
            # if type(response) == str:
            #     track_name = response
            #     track_id = track["id"]
            #     result_dict = {
            #     'artificial_id': track_id,
            #     'track_name': track_name,
            #     'description': description,
            #     'artist_name': constraints['artist_name'],
            #     'album_name': constraints['album_name']
            #     }
            if type(response) == list:
                if len(response) == 1:
                    track_name = response[0]["name"]
                    instrumentalness = response[0]["audio_features"]["instrumentalness"]
                    danceability = response[0]["audio_features"]["danceability"]
                    valence = response[0]["audio_features"]["valence"]
                    preview_url = response[0]["preview_url"]
                    if not preview_url:
                        preview_url = "none"
                    track_id = response[0]["id"]
                    result_dict = {
                        "artificial_id": track_id,
                        "track_name": track_name,
                        "preview_url": preview_url,
                        "instrumentalness": instrumentalness,
                        "danceability": danceability,
                        "valence": valence,
                        "artist_name": constraints["artist_name"],
                        "album_name": constraints["album_name"],
                    }
                elif len(response) > 1:
                    result_list = []
                    for i, track in enumerate(response):
                        track_name = track["name"]
                        instrumentalness = track["audio_features"]["instrumentalness"]
                        danceability = track["audio_features"]["danceability"]
                        valence = track["audio_features"]["valence"]
                        preview_url = track["preview_url"]
                        if not preview_url:
                            preview_url = "none"
                        track_id = track["id"]
                        result_dict = {
                            "artificial_id": track_id,
                            "track_name": track_name,
                            "preview_url": preview_url,
                            "instrumentalness": instrumentalness,
                            "danceability": danceability,
                            "valence": valence,
                            "artist_name": constraints["artist_name"],
                            "album_name": constraints["album_name"],
                        }
                        result_list.append(result_dict)

            elif type(response) == dict:
                track_name = response["name"]
                instrumentalness = response["audio_features"]["instrumentalness"]
                danceability = response["audio_features"]["danceability"]
                valence = response["audio_features"]["valence"]
                preview_url = response["preview_url"]
                if not preview_url:
                    preview_url = "none"
                track_id = response["id"]
                result_dict = {
                    "artificial_id": track_id,
                    "track_name": track_name,
                    "preview_url": preview_url,
                    "instrumentalness": instrumentalness,
                    "danceability": danceability,
                    "valence": valence,
                    "artist_name": constraints["artist_name"],
                    "album_name": constraints["album_name"],
                }

            if not result_list:

                if any(True for _ in requested_slots):
                    cleaned_result_dict = {
                        slot: result_dict[slot] for slot in requested_slots
                    }
                else:
                    cleaned_result_dict = result_dict
                self.last_results.append(cleaned_result_dict)
                return [cleaned_result_dict]

            else:
                cleaned_result_list = []
                for result_dict in result_list:
                    if any(True for _ in requested_slots):
                        cleaned_result_dict = {
                            slot: result_dict[slot] for slot in requested_slots
                        }
                    else:
                        cleaned_result_dict = result_dict
                    cleaned_result_list.append(cleaned_result_dict)
                self.last_results = cleaned_result_list
                #####print("returning list of results")
                #####print(cleaned_result_list)
                return cleaned_result_list
        else:
            return []

    def find_info_about_entity(self, entity_id, requested_slots: Iterable):
        """ Returns the values (stored in the data backend) of the specified slots for the
                specified entity.
            Args:
                entity_id (str): primary key value of the entity
                requested_slots (dict): slot-value mapping of constraints
            """
        #####print(f"requested_slots: {requested_slots}")
        #####print(f"last_results: {self.last_results}")
        for result in self.last_results:
            if result["artificial_id"] == entity_id:
                return [result]

    def get_requestable_slots(self) -> List[str]:
        """ Returns a list of all slots requestable by the user. """
        return [
            "track_name",
            "preview_url",
            "danceability",
            "valence",
            "instrumentalness",
        ]

    def get_system_requestable_slots(self) -> List[str]:
        """ Returns a list of all slots requestable by the system. """
        return ["artist_name", "album_name"]

    def get_informable_slots(self) -> List[str]:
        """ Returns a list of all informable slots. """
        return ["artist_name", "album_name"]

    def get_mandatory_slots(self) -> List[str]:
        """ Returns a list of all mandatory slots. """
        return ["artist_name", "album_name"]

    def get_default_inform_slots(self) -> List[str]:
        """ Returns a list of all default Inform slots. """
        return ["track_name", "preview_url"]
        # return []

    def get_possible_values(self, slot: str) -> List[str]:
        """ Returns all possible values for an informable slot

        Args:
            slot (str): name of the slot

        Returns:
            a list of strings, each string representing one possible value for
            the specified slot.
         """
        raise BaseException(
            "all slots in this domain do not have a fixed set of "
            "values, so this method should never be called"
        )

    def get_selectable_slots(self, result: dict) -> List[str]:
        """ Returns all selectable slots in a result

        Args:
            result (dict): dictionary containing several slots (i.e. keys)
        
        Returns: 
            a list of strings, each string representing one slot that can be used for 
            selecting a subset of a set of options.
        """
        blacklist = [
            "preview_url",
            "artificial_id",
            "album_name",
            "artist_name",
            "track_name",
        ]
        selectable_slots = [key for key in result.keys() if key not in blacklist]
        #####print(f"selectable_slots: {selectable_slots}")
        return selectable_slots

    def get_primary_key(self) -> str:
        """ Returns the slot name that will be used as the 'name' of an entry """
        return "artificial_id"

    def _query(self, artist_name, album_name, track_name=None):
        """if artist_name is None:
            artist_name = 'Rolling Stones'
        if album_name is None:
            album_name = 'Aftermath'"""
        type = "track"
        market = "DE"
        if not track_name:
            query = f"artist:{artist_name}, album:{album_name}"
            try:
                results = self.spotify.search(q=query, market=market, type=type)
                results_list = [track for track in results["tracks"]["items"]]
                track_id_list = [track["id"] for track in results_list]
                features_list = self.spotify.audio_features(track_id_list)
                for idx, features in enumerate(features_list):
                    results_list[idx]["audio_features"] = features
                return results_list
            except BaseException as e:
                raise (e)
                return None
        else:
            track_name = track_name.replace("'", "")
            query = f"artist:{artist_name}, album:{album_name}, track:{track_name}"
            try:
                results = self.spotify.search(q=query, market=market, type=type)
                #####print(f"SPOTIFY RESPONSE: {results}")
                if results["tracks"]["items"]:
                    result = results["tracks"]["items"][0]
                    track_id_list = [result["id"]]
                    features_list = self.spotify.audio_features(track_id_list)
                    result["audio_features"] = features_list[0]
                    return [result]
            except BaseException as e:
                raise (e)
                return None

    def _confirm_artist_id(self, artist_name):
        """if there is no exact match for artist_name string, suggest first result to user """
        market = "DE"
        query = f"artist:{artist_name}"
        results = self.spotify.search(query, market=market)
        #####print(results)
        pass

    def get_keyword(self):
        return "songfinder"

