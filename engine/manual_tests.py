"""
Module with tests to run maunally, because they change
terminal, print information in color etc.
"""
import os

from utils import (
    clear_terminal,
    colored,
    print_backup_objects,
    print_proceed_info,
    formatted_size_state
)
from backup import SingleFileBackup


def clear_terminal_test():
    print('You should not see this.')
    clear_terminal()
    print('If this is first line, clear terminal test passed.')
    

def colored_test():
    print(colored('green', 'green'))
    print(colored('red', 'red'))
    print(colored('yellow', 'yellow'))
    print(colored('blue', 'blue'))
    
    try:
        colored('test', 'black') # This should raise exception.
        print('Test did not pass.')
    except Exception as e:
        print(f'Unknown color: {e}')


def print_proceed_info_test():
    print('Start of print_proceed_info_test')
    print_proceed_info()
    print('End of print_proceed_info_test')
    

def print_backup_objects_test():
    file1 = __file__
    file2 = os.path.join(os.path.dirname(__file__), '__file2.txt')
    file3 = os.path.join(os.path.dirname(__file__), '__file3.py')
    file4 = os.path.join(os.path.dirname(__file__), '__file4.c')
    
    # Create files for tests.
    open(file2, 'w+').close()
    open(file3, 'w+').close()
    open(file4, 'w+').close()
    
    # Create backup objects for tests.
    backup_objects = [
        SingleFileBackup(file1, 'backup_path1', 'old_v_path1'),
        SingleFileBackup(file2, 'backup_path2', 'old_v_path2'),
        SingleFileBackup(file3, 'backup_path3', 'old_v_path3'),
        SingleFileBackup(file4, 'backup_path4', 'old_v_path4')
    ]
    
    print('Print only objects:')
    print_backup_objects(backup_objects)
    
    print('Print objects with size sum as 1000 bytes:')
    print_backup_objects(backup_objects, 1000)
    
    print('Print objects with size sum as 1000 bytes and limit files to 2.')
    print_backup_objects(backup_objects, 1000, 2)
    
    # Delete created files.
    os.remove(file2)
    os.remove(file3)
    os.remove(file4)
    

def formatted_size_state_test():
    current = 50
    final = 150
    print(f'Formatted size state with current: {current} final: {final}')
    print(formatted_size_state(current, final))
    
    current = 21.37
    final = 42
    print(f'Formatted size state with current: {current} final: {final}')
    print(formatted_size_state(current, final))
    

if __name__ == "__main__":
    tests_to_run = [
        clear_terminal_test, # this test should be run first.
        colored_test,
        print_proceed_info_test,
        print_backup_objects_test,
        formatted_size_state_test
    ]
    
    for idx, test in enumerate(tests_to_run):
        print('*'*50)
        print(f'Test #{idx}:')
        print('*'*50)
        test()
