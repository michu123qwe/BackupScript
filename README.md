# BackupScript
## Warning
Script is not well tested - use at your own risk.  
Currently working on Ubuntu 20, I haven't checked other operating systems.
## Info
Script to back-up files.

The script takes two paths: path to directory with files to back-up and path to directory where files will be copied. Then, after user's consent, script performs back-up.

If script is run two or more times on the same directories, it will create directories for older versions of previously saved files.  
For example:  
**/home/user/file.txt** is saved in **/home/user/backup/file.txt**  
Script runs again, current **/home/user/file.txt** is again saved in **/home/user/backup/file.txt** but the previous version of **/home/user/backup/file.txt** is moved to **/home/user/backup/\_old\_/_old_file_txt/2020-09-07_12:00:00_file.txt** (the datetime is equal to current datetime while performing back-up).



## Usage:
**Python 3** is needed to run this script.
1. Enter main directory of this repository.
2. Open terminal.
3. Run script: 
```
python3 main.py path_to_dir_with_files path_to_dir_where_files_will_be_copied
```
4. Follow instructions in terminal.
