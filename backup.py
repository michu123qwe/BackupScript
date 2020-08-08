import os
import shutil
import datetime


def create_dirpath_for_old_versions(backup_filepath):
    backup_filename = os.path.split(backup_filepath)[-1]
    old_version_dirname = '_old_' + backup_filename.split('.')[0]
    old_version_dirpath = os.path.join(
        os.path.dirname(backup_filepath), 
        old_version_dirname)
    
    return old_version_dirpath


def create_filename_for_old_version(backup_filepath):
    backup_filename = os.path.split(backup_filepath)[-1]
    now = str(datetime.datetime.now())
    
    return f'{now}_{backup_filename}'


def create_directory_for_old_versions(backup_filepath):
    old_version_dirpath = create_dirpath_for_old_versions(backup_filepath)
    
    if not os.path.isdir(old_version_dirpath):
        os.mkdir(old_version_dirpath)
        
    return old_version_dirpath
    

def create_old_version_of_file(backup_filepath):
    old_version_dirpath = create_directory_for_old_versions(backup_filepath)
    old_version_filename = create_filename_for_old_version(backup_filepath)
    old_version_filepath = os.path.join(old_version_dirpath, old_version_filename)
    
    shutil.copyfile(backup_filepath, old_version_filepath)
    

def backup_file(original_filepath, backup_filepath):
    if not os.path.isfile(original_filepath):
        # Original file doesn't exist.
        return None
    
    if os.path.isfile(backup_filepath):
        # Backup for this file already exists
        create_old_version_of_file(backup_filepath)
        os.remove(backup_filepath)

    shutil.copyfile(original_filepath, backup_filepath)


def backup_directory(original_dirpath, backup_dirpath):
    
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