import os
import shutil
from datetime import datetime

import utils


def create_dirpath_for_old_versions(filepath):
    """Create directory path for old versions of file specified
    in filepath.
    
    The directory path is the same as filepath, except it is
    not path to file, but to directory named as follows: 
    _old_{filepath without extension}
    the final name is without curly brackets.
    

    Args:
        filepath (str): path to file.

    Returns:
        str: path of directory for old versions.
    """
    
    filename = os.path.split(filepath)[-1]
    old_version_dirname = '_old_' + filename.split('.')[0]
    old_version_dirpath = os.path.join(
        os.path.dirname(filepath), 
        old_version_dirname)
    
    return old_version_dirpath


def create_filename_for_old_version(backup_filepath):
    """Create filename for old version of backup_filepath.
    
    The old version filename is named as follows:
    {current_datetime}_{backup_filename}
    the final name is without curly brackets.
    
    Current datetime is in format: %Y-%m-%d_%H:%M:%S

    Args:
        backup_filepath (str): path to file.

    Returns:
        str: filename of old version of given file.
    """
    
    backup_filename = os.path.split(backup_filepath)[-1]
    now = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    
    return f'{now}_{backup_filename}'


def create_directory_for_old_versions(filepath):
    """Create directory for old versions of file in filepath if
    it doesn't already exist.
    

    Args:
        filepath (str): path to file.

    Returns:
        str: path to created directory for old versions.
    """
    
    old_version_dirpath = create_dirpath_for_old_versions(filepath)
    
    if not os.path.isdir(old_version_dirpath):
        os.mkdir(old_version_dirpath)
        
    return old_version_dirpath
    

def create_old_version_of_file(filepath):
    """Create old version of file in filepath.
    
    Copy file in given filepath to directory with old versions
    and give it proper old version name.

    Args:
        filepath (str): path to file.
    """
    
    old_version_dirpath = create_directory_for_old_versions(filepath)
    old_version_filename = create_filename_for_old_version(filepath)
    old_version_filepath = os.path.join(old_version_dirpath, old_version_filename)
    
    shutil.copyfile(filepath, old_version_filepath)
    

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
