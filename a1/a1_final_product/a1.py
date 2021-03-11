from pathlib import Path

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
    '''Returns True if the file satisfies a filename or extension requirement if they exist'''

    crit_met = True
    if filename != None:
        if file.name != filename:
            crit_met = False

    if extension != None:
        if file.suffix != '.' + extension:
            crit_met = False

    return crit_met



def list_files(path, command_tokens):
    '''Assigns specific variables for command requirements and calls file_search().'''
    
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



def create_file(path, command_tokens):
    '''Creates new .dsu file in given directory.'''
    
    if len(command_tokens) != 4 or command_tokens[2] != '-n':
        print("ERROR")
        return

    if not path.is_dir():
        print("ERROR")
        return
    
    file_path = path / (command_tokens[3] + ".dsu")
    file_path.touch()
    print(file_path)

    

def delete_file(path, command_tokens):
    '''Deletes file specified in path.'''

    if error_found(path, command_tokens):
        print("ERROR")
        return
    
    path.unlink()
    print(path, "DELETED")

    

def read_file(path, command_tokens):
    '''Prints contents of .dsu file or EMPTY if it is empty.'''

    if error_found(path, command_tokens):
        print("ERROR")
        return

    if path.read_text() == "":
        print("EMTPY")
        return

    print(path.read_text(), end="")
    


def error_found(path, command_tokens):
    '''Returns true if the command for read_file() or delete_file() is incorrect.'''

    error = False
    if len(command_tokens) != 2:
        error = True

    if not path.is_file():
        error = True

    if path.suffix != ".dsu":
        error = True

    return error

    
    
def main():
    while True:
        command = input().strip()
        if command == 'Q':
            break
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
            create_file(path, command_tokens)
        elif command_tokens[0] == 'D':
            delete_file(path, command_tokens)
        elif command_tokens[0] == 'R':
            read_file(path, command_tokens)
        else:
            print("ERROR")
            continue


if __name__ == "__main__":
    main()


    
    
