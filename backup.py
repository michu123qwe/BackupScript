import os
import filecmp
import datetime


# fill:
# list with new files. Format: [[new_file_path, backup_file_path, size_in_bytes]],
# list with existing files to be overwritten. Format:  [[new_file_path, backup_file_path, size_in_bytes]],
# list with old version directories to be created. Format: [[directory_path]],
# list with old versions of file to be moved. Format: [[old_file_path, old_version_file_path, size]]
def list_backup(backup_path, new_path, new=None, different=None, directory=None, move=None, main=True):

    if move is None:
        move = []
    if directory is None:
        directory = []
    if different is None:
        different = []
    if new is None:
        new = []

    # list of files in backup directory
    backup_files = os.listdir(backup_path)
    # list of files in new directory
    new_files = os.listdir(new_path)

    # look at every file
    for file in new_files:

        # don't add hidden directories
        if file[0] == '.':
            continue

        # don't take old version folder into consideration, name conflict
        if file.startswith("oldversion_"):
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
            size = os.path.getsize(new_file_path)
            new.append([new_file_path, backup_file_path, size])

        # existing file
        else:

            # check if files aren't the same
            if not filecmp.cmp(backup_file_path, new_file_path):

                # check if file is a directory
                if os.path.isdir(new_file_path):

                    # call function for directory
                    list_backup(backup_file_path, new_file_path, new, different, directory, move, False)

                else:
                    # directory name for old version of current file
                    oldversion_directory_name = "oldversion_{}".format(file)

                    # add old version directory if it doesn't exist
                    if oldversion_directory_name not in backup_files:
                        directory.append(os.path.join(backup_path, oldversion_directory_name))

                    # file name for old version of current file
                    date = str(datetime.datetime.now()).replace(' ', '-')
                    oldversion_file_name = "{}{}".format(date, file)

                    # move old file to old version folder
                    size = os.path.getsize(backup_file_path)
                    move.append(
                        [backup_file_path,
                         os.path.join(backup_path, oldversion_directory_name, oldversion_file_name), size])

                    # replace existing file
                    size = os.path.getsize(new_file_path)
                    different.append([new_file_path, backup_file_path, size])

    if main:
        return new, different, move, directory
