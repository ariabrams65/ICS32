from pathlib import Path

def recursive_search(dirpath, filename=None, extension=None, onlyfiles=False):

    for child in dirpath.iterdir():
        if child.is_dir():
            if not onlyfiles:
                print(child)
            recursive_search(child, filename, extension, onlyfiles)
        elif filename != None:
           if child.name == filename:
               print(child)
        elif extension != None:
            split_name = child.name.split('.')
            if split_name[-1] == extension:
                print(child)
        else:
            print(child)


def normal_search(dirpath, filename=None, extension=None, onlyfiles=False):
    
        dir_list = []
        f_list = []
        for child in dirpath.iterdir():
            if child.is_dir():
                dir_list.append(child)
            elif filename != None:
                if child.name == filename:
                    f_list.append(child)
            elif extension != None:
                split_name = child.name.split('.')
                if split_name[-1] == extension:
                    f_list.append(child)
            else:
                f_list.append(child)
        for f in f_list:
            print(f)

        if not onlyfiles:
            for d in dir_list:
                print(d)


def list_files(path, command_tokens):
    
    recursive = False
    only_files = False
    extension = None
    filename = None
    get_input = (False, "")

    for token in command_tokens[2:]:
        if get_input[0]:
            if get_input[1] == '-s':
                filename = token
            elif get_input[1] == '-e':
                extension = token
            get_input = (False, "")

        elif token == "-r":
            recursive = True
        elif token == '-f':
            only_files = True
        elif token == '-s':
            only_files = True
            get_input = (True, '-s')
        elif token == '-e':
            only_files = True
            get_input = (True, '-e')
        else:
            print("ERROR")
            return
        
    if get_input[0]:
        print("ERROR")
        return

    if recursive:
        recursive_search(path, filename, extension, only_files)
    else:
        normal_search(path, filename, extension, only_files)


def create_file(path, command_tokens):
    
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

    if error_found(path, command_tokens):
        print("ERROR")
        return
    
    path.unlink()
    print(path, "DELETED")
    
    

def read_file(path, command_tokens):

    if error_found(path, command_tokens):
        print("ERROR")
        return

    if path.read_text() == "":
        print("EMTPY")
        return

    print(path.read_text())

    


def error_found(path, command_tokens):
    
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
        command = input()
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


main()


    
    
