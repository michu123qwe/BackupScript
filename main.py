import os
import filecmp
from termcolor import colored

class Colors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'


def tabprint(s, tab, color):
    print(colored("{}{}".format("-"*tab*2, s), color))


def make_backup(backup_path, new_path, tab=1):
    backup_files = os.listdir(backup_path)
    new_files = os.listdir(new_path)

    # print(new_files)
    new = []
    different = []
    exact = []

    for file in new_files:
        if file not in backup_files:
            # tabprint("new file {}{}".format(file, Colors.WARNING), tab, 'red')
            new.append(os.path.join(new_path, file))
            continue

        else:
            if filecmp.cmp(
                    os.path.join(backup_path, file),
                    os.path.join(new_path, file)):
                # tabprint("two exact files {}{}".format(file, Colors.OKGREEN), tab, 'green')
                exact.append(os.path.join(new_path, file))
                pass
            else:
                if os.path.isdir(os.path.join(new_path, file)):
                    # tabprint("folder {}:".format(file), tab, 'white')
                    make_backup(os.path.join(backup_path, file), os.path.join(new_path, file), tab + 1)
                else:
                    # tabprint("two different files {}".format(file), tab, 'red')
                    different.append(os.path.join(new_path, file))

    if len(new) or len(different) or len(exact):
        print()
        print("Folder: {}".format(new_path))
        if len(new):
            print()
            for file in new:
                print(colored("new file: {}".format(file), 'red'))

        if len(different):
            print()
            for file in different:
                print(colored("different file: {}".format(file), 'red'))

        if len(exact):
            print()
            for file in exact:
                print(colored("exact file: {}".format(file), 'green'))


BACKUPPATH = 'backup/'
NEWPATH = 'new/'

make_backup(BACKUPPATH, NEWPATH)
