import argparse
from sync import *

#TODO: connect 2 vms using scp
#TODO: ignore some files mentioned by user
#TODO: support when file path provided instead of folder path

my_parser = argparse.ArgumentParser(prog="light-sync", description='Sync 2 folders')
my_parser.add_argument('source_path', metavar='src', type=str, help='the path of source folder')
my_parser.add_argument('destination_path', metavar='dest', type=str, help='the path of destination folder')

args = my_parser.parse_args()

src_path = args.source_path
dest_path = args.destination_path

print("src_path",src_path,"\ndest_path",dest_path)

check_src_folder_exists(src_path)
check_dest_folder_exists(dest_path)

run(src_path, dest_path)