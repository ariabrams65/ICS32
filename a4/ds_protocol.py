import time
from collections import namedtuple
import json

def create_json_join(username:str, password:str, token:str) -> str:

    '''
    Returns JSON formatted string with username and password.
    '''

    JSON_msg = "{{\"join\": {{\"username\": \"{}\", \"password\": \"{}\", \"token\":\"{}\"}}}}"
    JSON_msg = JSON_msg.format(username, password, token)
    return JSON_msg

def create_json_post(token:str, post:str, timestamp:str) ->str:

    '''
    Returns JSON formatted string with connected user's post.
    '''

    JSON_msg = "{{\"token\":\"{}\", \"post\": {{\"entry\": \"{}\",\"timestamp\": \"{}\"}}}}"
    JSON_msg = JSON_msg.format(token, post, timestamp)
    return JSON_msg
    


def create_json_bio(token:str, bio:str) :

    '''
    Returns JSON formatted string with connected user's bio.
    '''

    JSON_msg = "{{\"token\":\"{}\", \"bio\": {{\"entry\": \"{}\",\"timestamp\": \"{}\"}}}}"
    JSON_msg = JSON_msg.format(token, bio, time.time())
    return JSON_msg

    

srv_response = namedtuple('srv_response', ['response_type', 'msg', 'token'])

def extract_json(json_msg:str) -> srv_response:

    '''
    Calls the json.load function on a json string and converts it to a srv_response object.
    '''

    try:
        json_obj = json.loads(json_msg)
        response_type = json_obj["response"]["type"]
        msg = json_obj["response"]["message"]
        token = None

        try:
            token = json_obj["response"]["token"]
        except KeyError:
            pass
        
    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return srv_response(response_type, msg, token)
