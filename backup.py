import os
import shutil
import datetime


def create_dirpath_for_old_versions(backup_filepath):
    """Create directory path for old versions of file specified
    in backup_filepath.
    
    The directory path is the same as backup_filepath, except it is
    not path to file, but to directory named as follows: 
    _old_{backup_filepath without extension}
    the final name is without curly brackets.
    

    Args:
        backup_filepath (str): path to file to be backed up.

    Returns:
        str: path of directory for old versions.
    """
    
    backup_filename = os.path.split(backup_filepath)[-1]
    old_version_dirname = '_old_' + backup_filename.split('.')[0]
    old_version_dirpath = os.path.join(
        os.path.dirname(backup_filepath), 
        old_version_dirname)
    
    return old_version_dirpath


def create_filename_for_old_version(backup_filepath):
    """Create filename for old version of backup_filepath.
    
    The old version filename is named as follows:
    {current_datetime}_{backup_filename}
    the final name is without curly brackets.

    Args:
        backup_filepath (str): path to file to be backed up.

    Returns:
        str: filename of old version of given file.
    """
    
    backup_filename = os.path.split(backup_filepath)[-1]
    now = str(datetime.datetime.now())
    
    return f'{now}_{backup_filename}'


def create_directory_for_old_versions(backup_filepath):
    """Create directory for old versions of file in backup_filepath if
    it doesn't already exist.
    

    Args:
        backup_filepath (str): path to file to be backed up.

    Returns:
        str: path to created directory for old versions.
    """
    
    old_version_dirpath = create_dirpath_for_old_versions(backup_filepath)
    
    if not os.path.isdir(old_version_dirpath):
        os.mkdir(old_version_dirpath)
        
    return old_version_dirpath
    

def create_old_version_of_file(backup_filepath):
    """Create old version of file in backup_filepath.
    
    Copy file in given filepath to directory with old versions
    and give it proper old version name.

    Args:
        backup_filepath (str): path to file to be backed up.
    """
    
    old_version_dirpath = create_directory_for_old_versions(backup_filepath)
    old_version_filename = create_filename_for_old_version(backup_filepath)
    old_version_filepath = os.path.join(old_version_dirpath, old_version_filename)
    
    shutil.copyfile(backup_filepath, old_version_filepath)
    

def backup_file(original_filepath, backup_filepath):
    """Create backup of file in original_filepath and save it
    to backup_filepath and save older versions of file in
    backup_filepath if this file has been already backed up.

    Args:
        original_filepath (str):    path to file to be backed up,
        backup_filepath (str):      path to file to which the copy 
                                    will be saved.
    """
    if not os.path.isfile(original_filepath):
        # Original file doesn't exist.
        return None
    
    if os.path.isfile(backup_filepath):
        # Backup for this file already exists
        create_old_version_of_file(backup_filepath)
        os.remove(backup_filepath)

    shutil.copyfile(original_filepath, backup_filepath)


def backup_directory(original_dirpath, backup_dirpath):
    """Backup all files in original_dirpath and save them in 
    backup_dirpath preserving the same file tree. 

    Args:
        original_dirpath (str):     path to directory to be backed up,
        backup_dirpath ([type]):    path to directory to which the copies
                                    will be saved.
    """
    
    if not os.path.isdir(original_dirpath):
        # Original dir doesn't exist.
        return None
    
    if not os.path.isdir(backup_dirpath):
        # Backup dir doesn't exist, create it.
        os.mkdir(backup_dirpath)
        
    original_files = os.listdir(original_dirpath)
    
    for original_file in original_files:
        file_path = os.path.join(original_dirpath, original_file)
        backup_file_path = os.path.join(backup_dirpath, original_file)
        
        if os.path.isdir(file_path):
            backup_directory(file_path, backup_file_path)
        else:
            backup_file(file_path, backup_file_path)
            
            
if __name__ == "__main__":
    path1 = '/home/michal/code/BackupScript/test1'
    path2 = '/home/michal/code/BackupScript/test1des'
    
    backup_directory(path1, path2)