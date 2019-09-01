import os
import shutil
import filecmp
import datetime
import utils.utils as utils


# print how many bytes of data is to be copied/moved
def print_backup_state(current_size, final_size):
    current = current_size
    final = final_size
    size_type = "B"
    if final_size >= 1000:
        current = current_size/1000
        final = final_size/1000
        size_type = "KB"
    elif final_size >= 1000000:
        current = current_size/1000000
        final = final_size/1000000
        size_type = "MB"
    elif final_size >= 1000000000:
        current = current_size/1000000000
        final = final_size/1000000000
        size_type = "GB"
    print("{}{} of {}{}  ({:.2f}%)".format(current, size_type, final, size_type, (current/final)*100))


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
            if os.path.isdir(new_file_path):
                size = utils.get_directory_size(new_file_path)
            else:
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


def make_backup(new, different, directory, move):

    all_size = 0
    for paths in new:
        all_size += paths[2]
    for paths in different:
        all_size += paths[2]
    for paths in move:
        all_size += paths[2]

    curr_size = 0

    # create old version directories
    for file in directory:
        os.mkdir(file)

    # move old version files
    for paths in move:
        curr_size += paths[2]
        print_backup_state(curr_size, all_size)
        os.rename(paths[0], paths[1])

    # move new and different files to backup folder
    for paths in new:
        curr_size += paths[2]
        print_backup_state(curr_size, all_size)
        try:
            if os.path.isdir(paths[0]):
                shutil.copytree(paths[0], paths[1])
            else:
                shutil.copy(paths[0], paths[1])
        except:
            print("Problem with file: {}. Skipped.".format(paths[0]))
            continue
    for paths in different:
        curr_size += paths[2]
        print_backup_state(curr_size, all_size)
        try:
            shutil.copy(paths[0], paths[1])
        except:
            print("Problem with file: {}. Skipped.".format(paths[0]))
            continue
