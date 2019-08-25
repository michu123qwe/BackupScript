import os
import filecmp
import datetime

# list with new files. Format: [new_file_path, backup_file_path]
new = []

# list with existing, but different files to be overwritten. Format:  [new_file_path, backup_file_path]
different = []

# list with old version directories to be created. Format: directory_path
directory = []

# list with old versions of file to be moved. Format: [old_file_path, old_version_file_path]
move = []


# fill new, different, directory, move lists
def list_backup(backup_path, new_path):

    # list of files in backup directory
    backup_files = os.listdir(backup_path)
    # list of files in new directory
    new_files = os.listdir(new_path)

    # look at every file
    for file in new_files:

        # don't add hidden directories
        if file[0] == '.':
            continue

        # paths for current file
        new_file_path = os.path.join(new_path, file)
        backup_file_path = os.path.join(backup_path, file)

        # don't add current backup folder
        if new_file_path == backup_path:
            continue

        # new file
        if file not in backup_files:

            # add new file
            new.append([new_file_path, backup_file_path])

        # existing file
        else:

            # check if files aren't the same
            if not filecmp.cmp(backup_file_path, new_file_path):

                # check if file is a directory
                if os.path.isdir(new_file_path):

                    # call function for directory
                    list_backup(backup_file_path, new_file_path)

                else:
                    # directory name for old version of current file
                    oldversion_directory_name = "oldversion {}".format(file)

                    # add old version directory if it doesn't exist
                    if oldversion_directory_name not in backup_files:
                        directory.append(os.path.join(backup_path, oldversion_directory_name))

                    # file name for old version of current file
                    date = str(datetime.datetime.now()).replace(' ', '-')
                    oldversion_file_name = "{}{}".format(date, file)

                    # move old file to old version folder
                    move.append(
                        [backup_file_path,
                         os.path.join(backup_path, oldversion_directory_name, oldversion_file_name)])

                    # replace existing file
                    different.append([new_file_path, backup_file_path])


BACKUPPATH = 'backup/'
NEWPATH = 'new/'

list_backup(BACKUPPATH, NEWPATH)

if len(new) > 0:
    print("New files:")
    for paths in new:
        print("{} -> {}".format(paths[0], paths[1]))

print()

if len(directory) > 0:
    print("Folders for old versions:")
    for path in directory:
        print("Create {}".format(path))

print()

if len(move) > 0:
    print("Move old versions:")
    for paths in move:
        print("{} -> {}".format(paths[0], paths[1]))

print()

if len(different) > 0:
    print("Different files:")
    for paths in different:
        print("{} -> {}".format(paths[0], paths[1]))





