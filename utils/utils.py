# return string with formatted size(B, KB, MB, GB)
def format_size(size_in_bytes):
    if size_in_bytes < 1000:
        return "{}B".format(size_in_bytes)
    elif size_in_bytes >= 1000:
        return "{}KB".format(size_in_bytes / 1000)
    elif size_in_bytes >= 1000000:
        return "{}MB".format(size_in_bytes / 1000000)
    else:
        return "{}GB".format(size_in_bytes / 1000000000)


# print list with files and sizes
def print_files_list(files_list):
    files_weight = 0
    for paths in files_list:
        files_weight += paths[2]
        print("{} -> {} ({})".format(paths[0], paths[1], format_size(paths[2])))

    print("Weight of files: {}".format(format_size(files_weight)))
