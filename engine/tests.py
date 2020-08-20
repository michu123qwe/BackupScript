from unittest import TestCase
import os
from datetime import datetime

from utils import format_size, get_list_of_relative_filepaths
from backup import (
    get_dirpath_for_old_versions,
    get_filename_for_old_version,
) 


class BackupTests(TestCase):
    """Tests for backup.py module
    """
    
    def test_get_dirpath_for_old_versions(self):
        test_filepaths = [
            '/home/user/file.txt', # Simple file.
            '/home/user/file.with.comma.py', # File with multiple commas.
            '/home/user/.gitignore', # File starting with comma.
        ]
        answers = [
            '/home/user/_old_/_old_file_txt',
            '/home/user/_old_/_old_file_with_comma_py',
            '/home/user/_old_/_old__gitignore',
        ]
        
        for filepath, answer in zip(test_filepaths, answers):
            result = get_dirpath_for_old_versions(filepath)
            self.assertEqual(result, answer)
            
    def test_get_filename_for_old_version(self):  
        filename = 'file.txt'
        result = get_filename_for_old_version(filename)
        now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        answer = f'{now}_{filename}'
        
        # Both answer and result use datetime.now() called in different
        # moments, but the test is so short that the answer should be 
        # the same, because it is with accuracy of a second.
        self.assertEqual(result, answer)


class UtilsTests(TestCase):
    """Tests for utils
    """
    
    def test_format_size(self):
        sizes_in_bytes = [5, 50, 500, 5000, 50000, 500000, 5000000, 5000000000]
        answers = ['5.000B', '50.000B', '500.000B', '5.000KB', 
                '50.000KB', '500.000KB', '5.000MB', '5.000GB']
        
        for size, answer in zip(sizes_in_bytes, answers):
            formatted = format_size(size)
            self.assertEqual(formatted, answer)
    
    def test_get_list_of_relative_filepaths(self):
        """
        Created files for tests:
        ./backup_tests/test1.txt
        ./backup_tests/testdir1/
        ./backup_tests/testdir2/test2.txt
        ./backup_tests/testdir2/testdir3/
        ./backup_tests/testdir2/testdir4/test3.txt
        
        Files are removed after test passed.
        """
        
        # Create all needed files and directories.
        current_dirpath = os.path.abspath(os.path.dirname(__file__))
        test_path = os.path.join(current_dirpath, 'backup_tests')
        testdir1 = os.path.join(test_path, 'testdir1')
        testdir2 = os.path.join(test_path, 'testdir2')
        testdir3 = os.path.join(testdir2, 'testdir3')
        testdir4 = os.path.join(testdir2, 'testdir4')
        
        os.makedirs(testdir1)
        os.makedirs(testdir3)
        os.makedirs(testdir4)
        
        testfile1 = os.path.join(test_path, 'test1.txt')
        testfile2 = os.path.join(testdir2, 'test2.txt')
        testfile3 = os.path.join(testdir4, 'test3.txt')
        
        open(testfile1, 'w+').close()
        open(testfile2, 'w+').close()
        open(testfile3, 'w+').close()
        
        answer = [
            os.path.relpath(testfile1, test_path),
            os.path.relpath(testfile2, test_path),
            os.path.relpath(testfile3, test_path)
        ]
        
        # Testing
        result = get_list_of_relative_filepaths(test_path)
        self.assertEqual(len(answer), len(result))
        for path in answer:
            self.assertIn(path, result)
        
        # Remove all created files and directories.
        os.remove(testfile1)
        os.remove(testfile2)
        os.remove(testfile3)
        os.removedirs(testdir1)
        os.removedirs(testdir3)
        os.removedirs(testdir4)
