import os
from termcolor import colored


# return string with formatted size(B, KB, MB, GB)
def format_size(size_in_bytes):
    if size_in_bytes < 1000:
        return "{:.3f}B".format(size_in_bytes)
    elif size_in_bytes < 1000000:
        return "{:.3f}KB".format(size_in_bytes / 1000)
    elif size_in_bytes < 1000000000:
        return "{:.3f}MB".format(size_in_bytes / 1000000)
    else:
        return "{:.3f}GB".format(size_in_bytes / 1000000000)


# print how many bytes of data is to be copied/moved
def print_size_state(current_size, final_size):
    ratio = current_size/final_size
    current = format_size(current_size)
    final = format_size(final_size)

    print("{} of {}  ({:.2f}%)".format(current, final, ratio*100))


# print list with files and sizes
def print_files_list(files_list):
    files_weight = 0
    for paths in files_list:
        files_weight += paths[2]
        print("{} -> {} ({})".format(colored(paths[0], 'yellow'), colored(paths[1], 'green'),
                                     format_size(paths[2])))
        print()

    print("Weight of files: {}".format(format_size(files_weight)))


# get size of directory
def get_directory_size(start_path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += (os.path.getsize(fp) if os.path.isfile(fp) else 0)
    return total_size
