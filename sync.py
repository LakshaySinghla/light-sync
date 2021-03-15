import pathlib
import argparse
import datetime
import time
import os
from shutil import copyfile
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


def initial_traverse(src_path, path_from_src, dest_path, time_stamp_src_files):
    for file in os.listdir(os.path.join(src_path,path_from_src)):
        path_to_file = os.path.join(src_path,path_from_src,file)
        print("Path to file:",path_to_file)
        
        if os.path.isfile(path_to_file):
            time_stamp_src_files[path_to_file] = pathlib.Path(path_to_file).stat().st_mtime
            copyfile(path_to_file , os.path.join(dest_path,path_from_src,file))
        if os.path.isdir(path_to_file):
            if not os.path.exists(os.path.join(dest_path,path_from_src,file)):
                os.makedirs(os.path.join(dest_path,path_from_src,file))
            initial_traverse(src_path, os.path.join(path_from_src,file), dest_path, time_stamp_src_files)

#BUG: if user delete a file, then it won't be deleted in dest path
def traverse(src_path, path_from_src, dest_path, time_stamp_src_files):
    for file in os.listdir(os.path.join(src_path,path_from_src)):
        path_to_file = os.path.join(src_path,path_from_src,file)
        
        if os.path.isfile(path_to_file):
            if time_stamp_src_files[path_to_file] < pathlib.Path(path_to_file).stat().st_mtime:
                print("copying",path_to_file)
                time_stamp_src_files[path_to_file] = pathlib.Path(path_to_file).stat().st_mtime
                copyfile(path_to_file , os.path.join(dest_path,path_from_src,file))
        if os.path.isdir(path_to_file):
            if not os.path.exists(os.path.join(dest_path,path_from_src,file)):
                os.makedirs(os.path.join(dest_path,path_from_src,file))
            traverse(src_path, os.path.join(path_from_src,file), dest_path, time_stamp_src_files)


time_stamp_src_files = defaultdict(int)
initial_traverse(src_path, "", dest_path, time_stamp_src_files)


while True:
    traverse(src_path, "", dest_path, time_stamp_src_files)
    print("light-syncing...")
    time.sleep(5)
