### Domain file for Songfinder

### for imports, refer to examples/webapi/weather/domain.py

from typing import List, Iterable
import json
#from urllib.request import urlopen
import spotipy # use this instead of urlopen
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
        LookupDomain.__init__(self, 'SongDomain', 'songfinder')
        self.last_results = []
        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    def find_entities(self, constraints: dict, requested_slots: Iterable = iter(())):
        """Returns all entities from the data backend that meet the constraints.
        
        Args:
            constraints (dict): Slot-value mapping of constraints.
                                If empty, all entities in the database will be returned.
            requested_slots (Iterable): list of slots that should be returned in addition to the
                                        system requestable slots and the primary key
                        
        """
        if 'artist_name' in constraints and 'album_name' in constraints:

            if 'track_name' in constraints:
                response = self._query(constraints['artist_name'], constraints['album_name'], constraints['track_name'])
            else:
                response = self._query(constraints['artist_name'], constraints['album_name'])
            if response is None:
                return []
            description = "description_placeholder"
            result_list = []
            if type(response) == str:
                track_name = response
                result_dict = {
                'artificial_id': str(len(self.last_results)),
                'track_name': track_name,
                'description': description,
                'artist_name': constraints['artist_name'],
                'album_name': constraints['album_name'],
                }
            elif type(response) == list:
                if len(response) == 1:
                    track_name = response[0]
                    result_dict = {
                    'artificial_id': str(len(self.last_results)),
                    'track_name': track_name,
                    'description': description,
                    'artist_name': constraints['artist_name'],
                    'album_name': constraints['album_name'],
                    }
                elif len(response) > 1:
                    result_list = []
                    for track_name in response:
                        result_dict = {
                        'artificial_id': str(len(self.last_results)),
                        'track_name': track_name,
                        'description': description,
                        'artist_name': constraints['artist_name'],
                        'album_name': constraints['album_name'],
                        }
                        result_list.append(result_dict)

            if not result_list:
                    
                if any(True for _ in requested_slots):
                    cleaned_result_dict = {slot: result_dict[slot] for slot in requested_slots}
                else:
                    cleaned_result_dict = result_dict
                self.last_results.append(cleaned_result_dict)
                return [cleaned_result_dict]
          
            else:
                cleaned_result_list = []
                for result_dict in result_list:
                    if any(True for _ in requested_slots):
                        cleaned_result_dict = {slot: result_dict[slot] for slot in requested_slots}
                    else:
                        cleaned_result_dict = result_dict
                    cleaned_result_list.append(cleaned_result_dict)
                    self.last_results.append(cleaned_result_list)
                #####print("returning list of results")
                #####print(cleaned_result_list)
                return cleaned_result_list
        else:
            return []       

    def get_requestable_slots(self) -> List[str]:
        """ Returns a list of all slots requestable by the user. """
        return ['track_name']

    def get_system_requestable_slots(self) -> List[str]:
        """ Returns a list of all slots requestable by the system. """
        return ['artist_name', 'album_name']

    def get_informable_slots(self) -> List[str]:
        """ Returns a list of all informable slots. """
        return ['artist_name', 'album_name']

    def get_mandatory_slots(self) -> List[str]:
        """ Returns a list of all mandatory slots. """
        return ['artist_name', 'album_name']
        
    def get_default_inform_slots(self) -> List[str]:
        """ Returns a list of all default Inform slots. """
        return ['track_name']
        #return []

    def get_possible_values(self, slot: str) -> List[str]:
        """ Returns all possible values for an informable slot

        Args:
            slot (str): name of the slot

        Returns:
            a list of strings, each string representing one possible value for
            the specified slot.
         """
        raise BaseException('all slots in this domain do not have a fixed set of '
                            'values, so this method should never be called')

    def get_selectable_values(self, slot: str) -> List[str]:
        """ Returns all selectable values for a requestable slot with several values
        
        Args:
            slot (str): name of the slot
        
        Returns: 
            a list of strings, each string representing one selectable value for
            the specified slot.
        """

    def get_primary_key(self) -> str:
        """ Returns the slot name that will be used as the 'name' of an entry """
        return 'artificial_id'

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
                track_names_list = [track["name"] for track in results["tracks"]["items"]]
                #####print("printing results of API call in domain.py")
                #####print(f"resulting list of tracks: {track_names_list}")
                return track_names_list
            except BaseException as e:
                raise(e)
                return None
        else:
            query = f"artist:{artist_name}, album:{album_name}, track:{track_name}"
            try:
                results = self.spotify.search(q=query, market=market, type=type)
                track_name = results["tracks"]["items"][0]["name"]
                return track_name
            except BaseException as e:
                raise(e)
                return None


    def _confirm_artist_id(self, artist_name):
        """if there is no exact match for artist_name string, suggest first result to user """
        market = "DE"
        query = f"artist:{artist_name}"
        results = self.spotify.search(query, market=market)
        #####print(results)
        pass



    def get_keyword(self):
        return 'songfinder'
