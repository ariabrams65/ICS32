import urllib, json
from urllib import request, error
import datetime
from ds_api import ds_api

class OpenWeather(ds_api):
    '''
    Object containing weather data of a specific zip code
    Subclass of ds_api.
    '''

    def __init__(self, zipcode:str, ccode:str, apikey:str):
        '''
        :param zipcode: The zipcode of where the weather information will be gathered.
        :param ccode: The country code using ISO 3166 standard.
        :param apikey: API key obtained from https://home.openweathermap.org/.
        '''
        self.zipcode = zipcode
        self.ccode = ccode
        self.apikey = apikey

        self._update()
        

 
    def _create_weather_data(self, json_obj):
        '''
        Creates class variables with weather data from json_obj.
        '''
        if json_obj == None:
            return
        
        self.longitude = json_obj['coord']['lon']
        self.latitude = json_obj['coord']['lat']
        self.description = json_obj['weather'][0]['description']
        self.temperature = json_obj['main']['temp']
        self.low_temperature = json_obj['main']['temp_min']
        self.high_temperature = json_obj['main']['temp_max']
        self.humidity = json_obj['main']['humidity']
        self.sunset = datetime.datetime.fromtimestamp(json_obj['sys']['sunset']).strftime("%H:%M")
        self.city = json_obj['name']



    def _create_url(self) -> str:
        '''
        Creates OpenWeatherAPI URL from zipcode, ccode, and apikey.
        Returns a string of the created URL.
        '''
        return f"https://api.openweathermap.org/data/2.5/weather?zip={self.zipcode},{self.ccode}&appid={self.apikey}&units=imperial"
        
        

    def _update(self):
        '''
        Sends request to OpenWeather API.
        Creates or updates class variables.
        '''
        url = self._create_url()
        json_obj = self._create_json_rsp_obj(url)
        self._create_weather_data(json_obj)



    def transclude(self, message:str) ->str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude.

        :returns: The transcluded message
        '''
        return message.replace("@weather", self.description)
        
        
