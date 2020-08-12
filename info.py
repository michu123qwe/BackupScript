import os

from utils import format_size, colored


def print_proceed_info():
    print(
        colored('\nProceed?(', 'blue'),
        colored('y', 'green'),
        colored('/', 'blue'),
        colored('n', 'red'),
        colored(') ', 'blue'),
        sep=''
    )


def print_filepath_to_backup(filepath, size):
    size_formatted = format_size(size)
    print(
        colored(f'{filepath}', 'green'),
        colored(f'{size_formatted}', 'blue')
    )


def print_list_of_files(files_to_print, sizes_of_files, files_to_print_limit):
    
    for i in range(min(len(files_to_print), files_to_print_limit)):
        print_filepath_to_backup(files_to_print[i], sizes_of_files[i])
    
    if len(files_to_print) > files_to_print_limit:
        remaining = len(files_to_print) - files_to_print_limit
        print(
            colored(f'...and', 'green'),
            colored(f'{remaining}', 'blue'),
            colored(f'more.', 'green')
        )
    
    size_sum = sum(sizes_of_files)
    print(
        colored(f'Size:', 'green'),
        colored(f'{size_sum}', 'blue')
    )
    

def print_list_of_files_to_backup(filepaths_list):
    files_limit = 50
    sizes_of_files = [os.path.getsize(filepath) for filepath in filepaths_list]
    
    print_list_of_files(filepaths_list, sizes_of_files, files_limit)
    

def print_relative_list_of_files_to_backup(relative_filepaths_list, dirpath):
    files_limit = 50
    sizes_of_files = [os.path.getsize(os.path.join(dirpath, filepath)) for filepath in relative_filepaths_list]
    
    print_list_of_files(relative_filepaths_list, sizes_of_files, files_limit)
    
# print how many bytes of data is to be copied/moved
def print_size_state(current_size, final_size):
    ratio = (current_size/final_size) * 100
    current = format_size(current_size)
    final = format_size(final_size)
    
    print(
        colored(current, 'blue'),
        'of',
        colored(final, 'blue'),
        colored(f'({ratio}%)', 'green')
    )

# return how many data is already copied.
def formatted_size_state(current_size, final_size):
    ratio = (current_size/final_size) * 100
    current = colored(format_size(current_size), 'blue')
    final = colored(format_size(final_size), 'blue')
    
    return f'{current} of {final} ({ratio}%)'
