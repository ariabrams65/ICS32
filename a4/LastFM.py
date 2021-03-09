
import urllib, json
from urllib import request, error
from ds_api import ds_api

class LastFM(ds_api):
    '''
    Class containing music data from LastFM.
    Subclass of ds_api.
    '''

    def __init__(self, api_key="c4a1c7835447a0cd7870d45c5bc416da"):
        '''
        :param api_key: api key for LastFM
        '''
        self.apikey = api_key

        self._update()



    def _get_top_artist(self, json_obj):
        '''
        Creates class variables with top artist and their number of plays.
        '''
        if json_obj == None:
            return

        self.top_artist = json_obj['artists']['artist'][0]['name']
        self.num_plays = json_obj['artists']['artist'][0]['playcount']



    def _create_url(self) -> str:
        '''
        Creates LastFM URL.
        Returns created URL as string.
        '''
        return f"http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&limit=1&api_key={self.apikey}&format=json"



    def _update(self):
        '''
        Sends request to LastFM API.
        Creates or updates class variables.
        '''
        url = self._create_url()
        json_obj = self._create_json_rsp_obj(url)
        self._get_top_artist(json_obj)



    def transclude(self, message:str) ->str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude.

        :returns: The transcluded message
        '''
        return message.replace("@lastfm", self.top_artist + " with " + self.num_plays + " plays")
