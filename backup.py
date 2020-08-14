import os
import shutil
from datetime import datetime

import utils


class SingleFileBackup:
    # todo: docstrings and maybe refactor
    def __init__(self, original_filepath, backup_filepath, 
                 old_version_dirpath, old_version_filepath):
        self.original_filepath = original_filepath
        self.backup_filepath = backup_filepath
        self.old_version_dirpath = old_version_dirpath
        self.old_version_filepath = old_version_filepath

    def make_old_version(self):
        if not os.path.isdir(self.old_version_dirpath):
            os.makedirs(self.old_version_dirpath)
                
        shutil.copy(self.backup_filepath, self.old_version_filepath)

    def make_backup(self):
        if os.path.isfile(self.backup_filepath):
             # File has been already saved, create old version for it.
            self.make_old_version()
        
        backup_dirpath = os.path.dirname(self.backup_filepath)
        if not os.path.isdir(backup_dirpath):
            os.makedirs(backup_dirpath)
        
        shutil.copyfile(self.original_filepath, self.backup_filepath)
        
    def get_size(self):
        return os.path.getsize(self.original_filepath)
        
    def __str__(self):
        size_formatted = utils.format_size(
            os.path.getsize(self.original_filepath))
        filepath = utils.colored(self.original_filepath, 'green')
        size_formatted = utils.colored(f'{size_formatted}', 'blue')
        
        return f'{filepath} {size_formatted}'


def parse_backup_objects(relative_filepaths, original_dirpath, backup_dirpath):
    """Parse given paths to single-file backup objects.

    Args:
        relative_filepaths (str): relative paths to files to backup,
        original_dirpath (str): path to directory with files to be copied,
        backup_dirpath (str): path to directory to which save copied files.

    Returns:
        List[SingleFileBackup]: list of single-file backup objects.
    """
    
    backup_objects = []
    
    for rel_filepath in relative_filepaths:
        original_filepath = os.path.join(original_dirpath, rel_filepath)
        backup_filepath = os.path.join(backup_dirpath, rel_filepath)
        old_version_dirpath = get_dirpath_for_old_versions(backup_filepath)
        old_version_filepath = os.path.join(old_version_dirpath, get_filename_for_old_version(backup_filepath))
        
        backup_object = SingleFileBackup(
            original_filepath,
            backup_filepath,
            old_version_dirpath,
            old_version_filepath
        )
        backup_objects.append(backup_object)
    
    return backup_objects


def get_dirpath_for_old_versions(filepath):
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


def get_filename_for_old_version(backup_filepath):
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
