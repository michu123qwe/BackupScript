import os


def clear_terminal():
    print('\033[H\033[J')
    

def colored(string, color):
    """Return string in given available color.
    
    Available colors are:
        green
        red
        yellow
        blue

    Args:
        string (str): text to be returned,
        color (str): color in which text will be printed.

    Raises:
        Exception: when given color is not one of the available colors.

    Returns:
        str: given text in desired color.
    """
    
    colors = {
        'green': '\033[92m',
        'red': '\033[91m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
    }
    end_color = '\033[0m'
    
    if color not in colors.keys():
        raise Exception('Exception: No such color.')
    
    return f'{colors[color]}{string}{end_color}'


# return string with formatted size(B, KB, MB, GB)
def format_size(size_in_bytes):
    if size_in_bytes < 1000:
        return "{:.3f}B".format(size_in_bytes)
    elif size_in_bytes < 1000000:
        return "{:.3f}KB".format(size_in_bytes / 1000)
    elif size_in_bytes < 1000000000:
        return "{:.3f}MB".format(size_in_bytes / 1000000)
    else:
        return "{:.3f}GB".format(size_in_bytes / 1000000000)


# returns list of all relative filepaths in given
# directory and its subdirectories.
def get_list_of_relative_filepaths(dirpath):
    # First element is empty, because first relative path
    # is basically path given in dirpath argument.
    relative_dirs_stack = ['']
    files_list = []
    
    while relative_dirs_stack:
        # Pop the top of the stack with dirs.
        current_dir = relative_dirs_stack[-1]
        del relative_dirs_stack[-1]
        
        current_dirpath = os.path.join(dirpath, current_dir)
        files_in_dir = os.listdir(current_dirpath)
        
        for file in files_in_dir:
            file_relative_path = os.path.join(current_dir, file)
            file_absolute_path = os.path.join(current_dirpath, file)
            
            if os.path.isdir(file_absolute_path):
                relative_dirs_stack.append(file_relative_path)
            else:
                files_list.append(file_relative_path)
        
    return files_list


if __name__ == "__main__":
    # Simple tests
    
    print(colored('test', 'green'))
    print(colored('test', 'red'))
    print(colored('test', 'yellow'))
    print(colored('test', 'blue'))
    
    try:
        colored('test', 'black')
    except Exception as e:
        print(e)
