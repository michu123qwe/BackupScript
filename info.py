import os

import utils


def print_proceed_info():
    utils.colored('\nProceed?(', 'blue')
    utils.colored('y', 'green')
    utils.colored('/', 'blue')
    utils.colored('n', 'red')
    utils.colored(') ', 'blue')


def print_filepath_to_backup(filepath):
    size_formatted = utils.format_size(os.path.getsize(filepath))
    utils.colored(f'{filepath} ', 'green')
    utils.colored(f'{size_formatted}\n', 'blue')


def print_list_of_files_to_backup(filepaths_list):
    files_limit = 50
    size_sum = utils.format_size(
        sum([os.path.getsize(path) for path in filepaths_list]))
    
    for i in range(min(files_limit, len(filepaths_list))):
        print_filepath_to_backup(filepaths_list[i])
    
    if len(filepaths_list) > files_limit:
        remaining = len(filepaths_list) - files_limit
        utils.colored(f'...and ', 'green')    
        utils.colored(f'{remaining} ', 'blue')    
        utils.colored(f'more.\n', 'green')    
    
    utils.colored(f'Size: ', 'green')
    utils.colored(f'{size_sum}\n', 'blue')
    
    
# print how many bytes of data is to be copied/moved
def print_size_state(current_size, final_size):
    ratio = (current_size/final_size) * 100
    current = utils.format_size(current_size)
    final = utils.format_size(final_size)
    
    utils.colored(current, 'blue')
    print(' of ', end='')
    utils.colored(final, 'blue')
    utils.colored(f' {ratio}%\n', 'blue')
