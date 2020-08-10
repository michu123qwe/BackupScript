import os


def colored(string, color):
    """Print string in given available color.
    
    Available colors are:
        green
        red
        yellow

    Args:
        string (str): text to be printed,
        color (str): color in which text will be printed.

    Raises:
        Exception: when given color is not one of the available colors.
    """
    
    colors = {
        'green': '\033[92m',
        'red': '\033[91m',
        'yellow': '\033[93m'
    }
    end_color = '\033[0m'
    
    if color not in colors.keys():
        raise Exception('Exception: No such color.')
    
    print(colors[color], end='')
    print(string, end='')
    print(end_color)

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


if __name__ == "__main__":
    # Simple tests
    
    colored('test', 'green')
    colored('test', 'red')
    colored('test', 'yellow')
    
    try:
        colored('test', 'black')
    except Exception as e:
        print(e)
