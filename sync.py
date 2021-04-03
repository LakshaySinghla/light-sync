import pathlib
import argparse
import datetime
import time
import os
from shutil import copyfile, rmtree
from collections import defaultdict

#TODO: connect 2 vms using scp
#TODO: ignore some files mentioned by user

my_parser = argparse.ArgumentParser(prog="light-sync", description='Sync 2 folders')
my_parser.add_argument('source_path', metavar='src', type=str, help='the path of source folder')
my_parser.add_argument('destination_path', metavar='dest', type=str, help='the path of destination folder')


args = my_parser.parse_args()

src_path = args.source_path
dest_path = args.destination_path

print("src_path",src_path,"\ndest_path",dest_path)

src_name = pathlib.Path(src_path)
if not src_name.exists():
    print("Source folder path does not exist")
    exit()


dest_name = pathlib.Path(dest_path)
if not dest_name.exists():
    print("Destination folder does not exist. Creating it")
    os.makedirs(dest_path)


def initial_traverse(src_path, path_from_src, dest_path):
    files_dict = dict()
    for file in os.listdir(os.path.join(src_path,path_from_src)):
        path_to_file = os.path.join(src_path,path_from_src,file)
        print("Path to file:",path_to_file)
        
        if os.path.isfile(path_to_file):
            files_dict[file] = pathlib.Path(path_to_file).stat().st_mtime
            copyfile(path_to_file , os.path.join(dest_path,path_from_src,file))
        if os.path.isdir(path_to_file):
            if not os.path.exists(os.path.join(dest_path,path_from_src,file)):
                os.makedirs(os.path.join(dest_path,path_from_src,file))
            files_dict[file] = initial_traverse(src_path, os.path.join(path_from_src,file), dest_path)
    return files_dict

def traverse(src_path, path_from_src, dest_path, files_dict):
    curr_files = set(os.listdir(os.path.join(src_path,path_from_src)))
    prev_files = set(files_dict.keys())
    
    #Adding newly added files to src folder
    for file in curr_files-prev_files:
        path_to_file = os.path.join(src_path,path_from_src,file)
        if os.path.isfile(path_to_file):
            print("copying",path_to_file)
            files_dict[file] = pathlib.Path(path_to_file).stat().st_mtime
            copyfile(path_to_file , os.path.join(dest_path,path_from_src,file))
        if os.path.isdir(path_to_file):
            print("copying folder",path_to_file)
            if not os.path.exists(os.path.join(dest_path,path_from_src,file)):
                os.makedirs(os.path.join(dest_path,path_from_src,file))
            files_dict [file] = {}
            traverse(src_path, os.path.join(path_from_src,file), dest_path, files_dict[file])
        
    #Deleting removed files from src folder
    for file in prev_files - curr_files:
        files_dict.pop(file)
        path_to_file = os.path.join(dest_path,path_from_src,file)
        if os.path.isfile(path_to_file):
            print("removing",path_to_file)
            os.remove(path_to_file)
        if os.path.isdir(path_to_file):
            print("removing folder",path_to_file)
            rmtree(path_to_file)
            # os.rmdir(path_to_file)

    #Checking already existing files
    for file in curr_files.intersection(prev_files):
        path_to_file = os.path.join(src_path,path_from_src,file)
        if os.path.isfile(path_to_file) and files_dict[file] < pathlib.Path(path_to_file).stat().st_mtime:
            print("copying",path_to_file)
            files_dict[file] = pathlib.Path(path_to_file).stat().st_mtime
            copyfile(path_to_file , os.path.join(dest_path,path_from_src,file))
        if os.path.isdir(path_to_file):
            if not os.path.exists(os.path.join(dest_path,path_from_src,file)):
                os.makedirs(os.path.join(dest_path,path_from_src,file))
            traverse(src_path, os.path.join(path_from_src,file), dest_path, files_dict[file])


files_dict = initial_traverse(src_path, "", dest_path)
while True:
    traverse(src_path, "", dest_path, files_dict)
    print("light-syncing...")
    time.sleep(5)
