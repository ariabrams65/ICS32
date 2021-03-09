import socket
from ds_protocol import create_json_join, create_json_post, create_json_bio, extract_json
import json
import time

def join(server:str, port:int, username:str,  password:str, public_key:str) -> str:

    '''
    Sends a join message to server.
    Returns token or None if there is an error.
    '''

    json_msg = create_json_join(username, password, public_key)
    srv_msg = send_json(json_msg, server, port)
    
    tuple_srv_msg = extract_json(srv_msg)
    if tuple_srv_msg.response_type == "error":
        return None

    return tuple_srv_msg.token



def send_post(server:str, port:int, msg:str, timestamp:str, token:str) -> bool:

    '''
    Sends post message to server.
    Returns True if the send request was successful.
    '''

    json_msg = create_json_post(token, msg, timestamp)
    srv_msg = send_json(json_msg, server, port)

    tuple_srv_msg = extract_json(srv_msg)

    return tuple_srv_msg.response_type == "ok"



def send_bio(server:str, port:int, bio:str, token:str) -> bool:

    '''
    Sends user's bio to server.
    Returns True if the send request was successful.
    '''

    json_msg = create_json_bio(token, bio)
    srv_msg = send_json(json_msg, server, port)

    tuple_srv_msg = extract_json(srv_msg)

    return tuple_srv_msg.response_type == "ok"
    


def send_json(json_msg:str, server:str, port:int) -> str:

    '''
    Sends json formatted string to server.
    Returns json formatted response from server
    '''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((server, port))

        send = client.makefile('w')
        recv = client.makefile('r')

        send.write(json_msg + '\r\n')
        send.flush()

        return recv.readline()

    
                
def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    try:
        token = join(server, port, username, password)
    except socket.gaierror:
        print("ERROR: incorrect server address")
        return
    except Exception:
        print("ERROR: incorrect server address or port")
        return
    
    if token == None:
        raise Exception

    else:
        send_post(server, port, message, time.time(), token)

        if bio != None:
            send_bio(server, port, bio, token)
    
        

        
        

        

        
   
