from pathlib import Path
from NaClProfile import NaClProfile
import Profile
import ds_client
from OpenWeather import OpenWeather
from LastFM import LastFM

def file_search(dirpath, filename=None, extension=None, onlyfiles=False, recursive=False):  
    '''
    Lists files in given directory that match the specified requirements.
    If recursive = True, all subdirectories contents are displayed.
    ''' 
    dir_list = []
    for child in dirpath.iterdir():
        if child.is_file():
            if file_meets_criteria(child, filename, extension):
                print(child)
        else:
            dir_list.append(child)
    
    for d in dir_list:
        if not onlyfiles:
            print(d)
        if recursive:
            file_search(d, filename, extension, onlyfiles, recursive)



def file_meets_criteria(file, filename, extension):
    '''
    Returns True if the file satisfies a filename or extension requirement if they exist.
    '''
    crit_met = True
    if filename != None:
        if file.name != filename:
            crit_met = False

    if extension != None:
        if file.suffix != '.' + extension:
            crit_met = False

    return crit_met



def list_files(path, command_tokens):
    '''
    Assigns specific variables for command requirements and calls file_search().
    '''  
    recursive = False
    only_files = False
    extension = None
    filename = None

    #whether the next token is an input
    get_input = False
    input_type = ""

    for token in command_tokens[2:]:
        if get_input:
            if input_type == '-s':
                filename = token
            elif input_type == '-e':
                extension = token
            get_input = False
            input_type = ""

        elif token == "-r":
            recursive = True
        elif token == '-f':
            only_files = True
        elif token == '-s':
            only_files = True
            get_input = True
            input_type = "-s"
        elif token == '-e':
            only_files = True
            get_input = True
            input_type = "-e"
        else:
            print("ERROR")
            return
        
    if get_input:
        print("ERROR")
        return

    file_search(path, filename, extension, only_files, recursive)



def create_file(path, command_tokens, profile) -> str:
    '''
    -Creates new .dsu file in given directory.
    -Prompts user for Profile input and populates the profile object along with the created file.
    -Returns path of created file
    '''
    if len(command_tokens) != 4 or command_tokens[2] != '-n':
        print("ERROR")
        return

    if not path.is_dir():
        print("ERROR")
        return
    
    file_path = path / (command_tokens[3] + ".dsu")
    file_path.touch()
    print(file_path)

    profile.dsuserver = input("Enter dsu server:\n")
    profile.username = input("Enter username:\n")
    profile.password = input("Enter password:\n")
    
    try:
        profile.save_profile(file_path)
    except Profile.DsuFileError:
        print("ERROR: Couldn't save profile to file")
        return

    prompt_bio(profile)
    prompt_post(profile)

    return file_path
    


def delete_file(path, command_tokens):
    '''
    Deletes file specified in path.
    '''
    if error_found(path, command_tokens):
        print("ERROR")
        return
    
    path.unlink()
    print(path, "DELETED")

    

def read_file(path, command_tokens):
    '''
    Prints contents of .dsu file or EMPTY if it is empty.
    '''
    if error_found(path, command_tokens):
        print("ERROR")
        return

    if path.read_text() == "":
        print("EMTPY")
        return

    print(path.read_text(), end="")
    


def error_found(path, command_tokens):
    '''
    Returns true if the command for read_file(), delete_file(), or load_file() is incorrect.
    '''
    error = False
    if len(command_tokens) != 2:
        error = True

    if not path.is_file():
        error = True

    if path.suffix != ".dsu":
        error = True

    return error



def load_file(path, command_tokens, profile) -> str:
    '''
    Populates the profile object with information in the specified .dsu file.
    Returns path of specified file.
    '''
    if error_found(path, command_tokens):
        print("ERROR")
        return

    try:
        profile.load_profile(str(path))
    except Profile.DsuProfileError:
        print("ERROR: Couldn't load file")
        return
    
    prompt_bio(profile)
    prompt_post(profile)

    return str(path)



def command_info():
    '''
    prints available commands 
    '''
    print("COMMANDS:")
    print("list files -- [L [DIRECTORY] [[-]OPTION] [INPUT]]")
    print("create file -- [C [DIRECTORY] -n [FILE]]")
    print("delete file --[D [FILE]]")
    print("read file -- [R [FILE]]")
    print("load file -- [O [FILE]]")
    print("write post -- [P]")
    print("write bio -- [B]")
    print("quit -- [Q]")
    print()

    

def prompt_post(profile):
    '''
    Prompts the user if they would like to write a post.
    '''
    if input("Would you like to write a post? (Y/N)\n") == "Y":
        write_post(profile)


        
def write_post(profile):
    '''
    Saves post to profile object.
    Sends to server if indicated by the user.
    '''
    if not profile_is_loaded(profile):
        print("ERROR: No profile is currently loaded.")
        return
    
    print()
    print("*TRANSCLUDE OPTIONS*")
    print("@weather -- short description of current weather")
    print("@lastfm -- current top artist along with their play count")
    print()

    msg = input("Enter message:\n")
    msg = transclusion_check(msg)
    post = Profile.Post()
    post.set_entry(msg)
        
    profile.add_post(post)

    if input("Would you like to post your message online? (Y/N)\n") == "Y":
        token = ds_client.join(profile.dsuserver, 2021, profile.username, profile.password, profile.public_key)

        if token == None:
            print("ERROR: There was an error when trying to join the server")
            return
        
        encrypted_post = profile.encrypt_entry(profile.get_posts()[-1].get_entry(), token).decode(encoding='UTF-8')
        if ds_client.send_post(profile.dsuserver, 2021, encrypted_post, post.get_time(), profile.public_key) == False:
            print("ERROR: There was an error when trying to post your message")
            return


def transclusion_check(msg:str) ->str:
    '''
    Checks whether msg has any predefined transclusion keywords.
    Returns msg with the keywords replaced with their transcluded information.
    '''
    try:
        if "@weather" in msg:
            open_weather = OpenWeather("92660", "US", "965cf2e5bf9db105ac06164bddce42d6")
            msg = open_weather.transclude(msg)

        if "@lastfm" in msg:
            lastfm = LastFM("c4a1c7835447a0cd7870d45c5bc416da")
            msg = lastfm.transclude(msg)

    except AttributeError:
        print("Your message failed to transclude\n")
    
    return msg
    
    

def prompt_bio(profile):
    '''
    Prompts the user if they would like to write a bio.
    '''
    if input("Would you like to create a bio? (Y/N)\n") == "Y":
        write_bio(profile)

def write_bio(profile):
    '''
    Saves bio to profile object.
    Posts bio to dsuserver if indicated by user.
    '''
    if not profile_is_loaded(profile):
        print("ERROR: No profile is currently loaded.")
        return
    
    bio = input("Enter bio:\n")
    profile.bio = bio

    if input("Would you like to post your bio online? (Y/N)\n") == "Y":
        token = ds_client.join(profile.dsuserver, 2021, profile.username, profile.password, profile.public_key)

        if token == None:
            print("ERROR: There was an error when trying to join the server")
            return

        encrypted_bio = profile.encrypt_entry(profile.bio , token).decode(encoding='UTF-8')
        if ds_client.send_bio(profile.dsuserver, 2021, encrypted_bio, profile.public_key) == False:
            print("ERROR: There was an error when trying to post your bio")
            return



def profile_is_loaded(profile) -> bool:
    '''
    returns True if a profile was already created or loaded
    '''
    return profile.dsuserver != None


    
def main():
    
    profile = NaClProfile()
    profile_path = ""

    command_info()
    
    while True:
        if profile_is_loaded(profile):
            try:
                profile.save_profile(profile_path)
            except Profile.DsuFileError:
                print("ERROR: Couldn't save profile to file")
        
        command = input().strip()
        if command == 'Q':
            break
        elif command == "P":
            write_post(profile)
            continue
        elif command == "B":
            write_bio(profile)
            continue
            
        command_tokens = command.split()
        if len(command_tokens) < 2:
            print("ERROR")
            continue
        
        path = Path(command_tokens[1])
        if not path.exists():
            print("ERROR")
            continue
        if command_tokens[0] == 'L':
            list_files(path, command_tokens)
        elif command_tokens[0] == 'C':
            profile = NaClProfile() #resets profile to remove any existing profile 
            profile_path = create_file(path, command_tokens, profile)
        elif command_tokens[0] == 'D':
            delete_file(path, command_tokens)
        elif command_tokens[0] == 'R':
            read_file(path, command_tokens)
        elif command_tokens[0] == 'O':
            profile = NaClProfile() #resets profile to remove any existing profile
            profile_path = load_file(path, command_tokens, profile)
        else:
            print("ERROR")
            continue


if __name__ == "__main__":
    main()


    
    
