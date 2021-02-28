import urllib, json
from urllib import request, error

class ds_api:
    '''
    Parent class of OpenWeather and LastFM.
    '''

    def __init__(self):
        pass



    def _create_json_rsp_obj(self, url:str):
        '''
        Sends a request to the given url.
        Returns a json response object.
        '''

        response = None
        r_obj = None

        try:
            response = urllib.request.urlopen(url)
            json_results = response.read()
            r_obj = json.loads(json_results)

        except urllib.error.HTTPError as e:
            print("ERROR: {}, ".format(e.code), end="")
            
            if e.code == 404:
                print("Incorrect API information")
            elif e.code == 503:
                print("The API is currently unable to handle the request")
            else:
                print("HTTPError")

        except urllib.error.URLError as e:
            print("ERROR: Loss of connection to the Internet")

        except ValueError:
            print("ERROR: Invalid data formatting from API")
            

        finally:
            if response != None:
                response.close()

        return r_obj



    def set_apikey(self, apikey:str) -> None:
        '''
        Sets the apikey required to make requests to a web API.
        :param apikey: The apikey supplied by the API service
        '''
        
        self.apikey = apikey
        self._update()



    def _update(self):
        '''
        Overridden in respective child classes.
        Resends request to respective API
        '''
        pass




        
