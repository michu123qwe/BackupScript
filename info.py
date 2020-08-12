import os

import utils


def print_proceed_info():
    utils.colored('\nProceed?(', 'blue')
    utils.colored('y', 'green')
    utils.colored('/', 'blue')
    utils.colored('n', 'red')
    utils.colored(') ', 'blue')


def print_filepath_to_backup(filepath, size):
    size_formatted = utils.format_size(size)
    utils.colored(f'{filepath} ', 'green')
    utils.colored(f'{size_formatted}\n', 'blue')


def print_list_of_files(files_to_print, sizes_of_files, files_to_print_limit):
    
    for i in range(min(len(files_to_print), files_to_print_limit)):
        print_filepath_to_backup(files_to_print[i], sizes_of_files[i])
    
    if len(files_to_print) > files_to_print_limit:
        remaining = len(files_to_print) - files_to_print_limit
        utils.colored(f'...and ', 'green')    
        utils.colored(f'{remaining} ', 'blue')    
        utils.colored(f'more.\n', 'green')
    
    size_sum = sum(sizes_of_files)
    utils.colored(f'Size: ', 'green')
    utils.colored(f'{size_sum}\n', 'blue')
    

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
    current = utils.format_size(current_size)
    final = utils.format_size(final_size)
    
    utils.colored(current, 'blue')
    print(' of ', end='')
    utils.colored(final, 'blue')
    utils.colored(f' {ratio}%\n', 'blue')
