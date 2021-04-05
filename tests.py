import unittest
from sync import *
import os
from shutil import rmtree

def initiate_src_folder(src_path):
    f = open(os.path.join(src_path,"file1.txt"), "w")
    f.write("This is file 1")
    f.close()
    os.makedirs(os.path.join(src_path,"level 2"))
    f = open(os.path.join(src_path,"level 2","file2.txt"), "w")
    f.write("This is file 2")
    f.close()
    os.makedirs(os.path.join(src_path,"level 2","level 3"))
    f = open(os.path.join(src_path,"level 2","level 3","file3.txt"), "w")
    f.write("This is file 3")
    f.close()

def check_src_match_dest(src_path,path_from_src, dest_path):
    for file in os.listdir(os.path.join(src_path,path_from_src)):
        path_to_file = os.path.join(src_path,path_from_src,file)
        print("Checking Path to file:",path_to_file)
        dest_name = pathlib.Path(os.path.join(dest_path,path_from_src,file))
        if not dest_name.exists():
            return False
        if os.path.isdir(path_to_file):
            if not check_src_match_dest(src_path,os.path.join(path_from_src,file), dest_path):
                return False
    return True



class TestSyncing(unittest.TestCase):
    def setUp(self):
        base_folder = os.path.dirname(os.path.abspath(__file__))
        self.src_path = os.path.join(base_folder,"build","from")
        self.dest_path = os.path.join(base_folder,"build","to")
        os.makedirs(self.src_path)
        initiate_src_folder(self.src_path)
    
    def tearDown(self):
        rmtree(self.src_path)
        rmtree(self.dest_path)

    def test_dest_path_not_exist(self):
        check_dest_folder_exists(self.dest_path)
        files_dict = initial_traverse(self.src_path, "", self.dest_path)
        self.assertTrue(check_src_match_dest(self.src_path,"", self.dest_path))
        f = open(os.path.join(self.src_path,"file11.txt"), "w")
        f.write("This is file 11")
        f.close()
        self.assertFalse(check_src_match_dest(self.src_path,"", self.dest_path))
        print("PASSED test_dest_path_not_exist")

    def test_already_existing_files_unchanged(self):
        check_dest_folder_exists(self.dest_path)
        f = open(os.path.join(self.dest_path,"file11.txt"), "w")
        f.write("This is file 11")
        f.close()
        files_dict = initial_traverse(self.src_path, "", self.dest_path)
        self.assertTrue(check_src_match_dest(self.src_path,"", self.dest_path))
        my_dest_file = pathlib.Path(os.path.join(self.dest_path,"file11.txt"))
        self.assertTrue(my_dest_file.exists())
        my_src_file = pathlib.Path(os.path.join(self.src_path,"file11.txt"))
        self.assertFalse(my_src_file.exists())
        print("PASSED test_already_existing_files_unchanged")


if __name__ == '__main__':
    unittest.main()