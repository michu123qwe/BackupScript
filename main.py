import os
import backup
import utils.utils as utils


BACKUPPATH = '/home/michal/backup'
NEWPATH = '/home/michal'

# try to open backup folder
if not os.path.isdir(BACKUPPATH):
    print("Cannot open {}".format(BACKUPPATH))
    input("Click enter to exit...")
    quit()

# try to open new folder
if not os.path.isdir(NEWPATH):
    print("Cannot open {}".format(NEWPATH))
    input("Click enter to exit...")
    quit()

files_new, files_different, files_move, files_directory = backup.list_backup(BACKUPPATH, NEWPATH)

if len(files_new) > 0:
    print("New files:")
    utils.print_files_list(files_new)

print()

if len(files_directory) > 0:
    print("Folders for old versions:")
    for path in files_directory:
        print("Create {}".format(path))

print()

if len(files_move) > 0:
    print("Move old versions:")
    utils.print_files_list(files_move)

print()

if len(files_different) > 0:
    print("Different files:")
    utils.print_files_list(files_different)

ans = input("\nProceed?(y/n) ")
if ans.lower() == "y":
    backup.make_backup(files_new, files_different, files_directory, files_move)
else:
    print("Goodbye")
    quit()


