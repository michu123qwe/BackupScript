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


def print_proceed_info():
    """Print info with question to proceed with backup.
    """
    
    print(
        colored('Proceed?(', 'blue'),
        colored('y', 'green'),
        colored('/', 'blue'),
        colored('n', 'red'),
        colored(') ', 'blue'),
        sep='',
        end=' '
    )


def print_backup_objects(backup_objects, size_sum=None, files_limit=None):
    """Print backup objects, limiting their number to files_limit
    if specified and print size of all files if specified in size_sum.

    Args:
        backup_objects (List[SingleFileBackup]): list of backup objects
                                                 to print.
        size_sum (int, optional): Sum of sizes of all files in backup 
                                  objects. Defaults to None.
        files_limit (int, optional): Limit of how many backup objects to
                                     print. Defaults to None.
    """
    
    backup_objects_length = len(backup_objects)
    files_limit = backup_objects_length if not files_limit else files_limit
    
    for i in range(min(backup_objects_length, files_limit)):
        print(backup_objects[i])
        
    remaining = backup_objects_length - 50
    if remaining > 0:
        print(f'...and {remaining} more.')
    
    if size_sum:
        print('Size:', format_size(size_sum))
    

def formatted_size_state(current_size, final_size):
    """Return formatted information of how much data
    is already copied.

    Args:
        current_size (Union[int, float]): current size of data,
        final_size (Union[int, float]): final size of data.

    Returns:
        str: formatted information of how much data
             is already copied.
    """
    
    ratio = (current_size/final_size) * 100
    ratio = colored(f'{ratio:.2f}', 'green')
    current = colored(format_size(current_size), 'blue')
    final = colored(format_size(final_size), 'blue')
    
    return f'{current} of {final} ({ratio}%)'

def quit_with_error(text):
    """Quit programme printing given text in red.

    Args:
        text (str): error text.
    """
    print(colored(text, 'red'))
    quit()
