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


def format_size(size_in_bytes):
    """Return string with formatted size (B, KB, MB, GB)
    and 3 floating point numbers.

    Args:
        size_in_bytes (Union[int, float]): size to format.

    Returns:
        (str): formatted size.
    """
    
    if size_in_bytes < 1000:
        return '{:.3f}B'.format(size_in_bytes)
    elif size_in_bytes < 1000000:
        return '{:.3f}KB'.format(size_in_bytes / 1000)
    elif size_in_bytes < 1000000000:
        return '{:.3f}MB'.format(size_in_bytes / 1000000)
    else:
        return '{:.3f}GB'.format(size_in_bytes / 1000000000)


def get_list_of_relative_filepaths(dirpath):
    """Return list of all relative filepaths in 
    given dirpath.

    Args:
        dirpath (str): Path to directory with files to list.

    Returns:
        List[str]: List with relative filepaths.
    """
    
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
    
    # Clear terminal.
    print('You should not see this.')
    clear_terminal()
    print('If this is first line, clear terminal test passed.')
    
    # Print colored text.
    print(colored('green', 'green'))
    print(colored('red', 'red'))
    print(colored('yellow', 'yellow'))
    print(colored('blue', 'blue'))
    
    try:
        colored('test', 'black')
    except Exception as e:
        print(e)
        
    # Size formatting
    sizes = [5, 50, 500, 5000, 50000, 500000, 5000000, 5000000000]
    answers = ['5.000B', '50.000B', '500.000B', '5.000KB', 
               '50.000KB', '500.000KB', '5.000MB', '5.000GB']
    for size, answer in zip(sizes, answers):
        formatted = format_size(size)
        assert formatted == answer
        
        print(f'{formatted}', colored('OK', 'green'))
