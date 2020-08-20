"""
Module with tests to run maunally, because they change
terminal, print information in color etc.
"""

from utils import (
    clear_terminal,
    colored,
)


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
        colored('test', 'black')
    except Exception as e:
        print(f'Unknown color: {e}')


if __name__ == "__main__":
    tests_to_run = [
        clear_terminal_test, # this test should be run first.
        colored_test,
    ]
    
    for test in tests_to_run:
        test()
