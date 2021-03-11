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

 
command = input()
while command != 'Q':
    command = command.split()

    path = Path(command[1])
    if not path.exists():
        print("ERROR")
        command = input()
        continue
    
    if len(command) == 2:
        normal_search(path)
    else:
        if command[2] == '-r':
            if len(command) == 3:
                recursive_search(path)
            elif command[3] == '-f':
                recursive_search(path, onlyfiles=True)
            elif command[3] == '-s':
                recursive_search(path, filename=command[4], onlyfiles=True)
            elif command[3] == '-e':
                recursive_search(path, extension=command[4], onlyfiles=True)
                
        elif command[2] == '-f':
            normal_search(path, onlyfiles=True)
        elif command[2] == '-s':
            normal_search(path, filename=command[3], onlyfiles=True)
        elif command[2] == '-e':
            normal_search(path, extension=command[3],onlyfiles=True)

    command = input()


    
    
