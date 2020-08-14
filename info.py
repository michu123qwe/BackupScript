import os

from utils import format_size, colored

# todo: look how many you use and maybe move them to utils

def print_proceed_info():
    """Print info with question to proceed with backup.
    """
    
    print(
        colored('\nProceed?(', 'blue'),
        colored('y', 'green'),
        colored('/', 'blue'),
        colored('n', 'red'),
        colored(') ', 'blue'),
        sep=''
    )


def print_filepath_to_backup(filepath, size_in_bytes):
    """Print formatted filepath with its size.

    Args:
        filepath (str): filepath to print,
        size_in_bytes (Union[int, float]): size in bytes of filepath.
    """
    
    size_formatted = format_size(size_in_bytes)
    print(
        colored(f'{filepath}', 'green'),
        colored(f'{size_formatted}', 'blue')
    )

def print_backup_objects(backup_objects, size_sum=None, files_limit=None):
    # todo docstring
    
    backup_objects_length = len(backup_objects)
    files_limit = backup_objects_length if not files_limit else files_limit
    
    for i in range(min(backup_objects_length, files_limit)):
        print(backup_objects[i])
        
    remaining = backup_objects_length - 50
    if remaining > 0:
        print(f'...and {remaining} more.')
    
    if size_sum:
        print('Size:', format_size(size_sum))


def print_list_of_files(files_to_print, sizes_of_files, files_to_print_limit):
    """Print formatted list of filepaths with their sizes and size 
    of all files. If there are more files than specified in 
    files_to_print_limit, the excess is not printed.

    Args:
        files_to_print (List[str]): list of filepaths to print,
        sizes_of_files (List[Union[int, float]]): list of sizes of files,
        files_to_print_limit (int): limit of printed files.
    """
    
    for i in range(min(len(files_to_print), files_to_print_limit)):
        print_filepath_to_backup(files_to_print[i], sizes_of_files[i])
    
    if len(files_to_print) > files_to_print_limit:
        remaining = len(files_to_print) - files_to_print_limit
        print(
            colored(f'...and', 'green'),
            colored(f'{remaining}', 'blue'),
            colored(f'more.', 'green')
        )
    
    size_sum = format_size(sum(sizes_of_files))
    print(
        colored(f'Size:', 'green'),
        colored(f'{size_sum}', 'blue')
    )
    

def print_list_of_files_to_backup(filepaths_list):
    """Print formatted list of filepaths with their sizes and size 
    of all files with limit of 50 files printed.

    Args:
        filepaths_list (List[str]): list of filepaths to print.
    """
    
    files_limit = 50
    sizes_of_files = [os.path.getsize(filepath) for filepath in filepaths_list]
    
    print_list_of_files(filepaths_list, sizes_of_files, files_limit)
    

def print_relative_list_of_files_to_backup(relative_filepaths_list, dirpath):
    """Print formatted list of relative filepaths with their 
    sizes and size of all files with limit of 50 files printed.

    Args:
        relative_filepaths_list (List[str]): list of filepaths to print,
        dirpath (str): path to directory which filepaths in 
                       list are relative to.
    """
    
    files_limit = 50
    sizes_of_files = [os.path.getsize(os.path.join(dirpath, filepath)) for filepath in relative_filepaths_list]
    
    print_list_of_files(relative_filepaths_list, sizes_of_files, files_limit)
    

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
