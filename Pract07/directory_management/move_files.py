#1
import shutil

shutil.copy('file.txt', 'backup/file.txt')      # copy a file
shutil.copytree('dir1', 'dir1_backup')          # copy entire directory
shutil.move('file.txt', 'archive/')             # move file or directory
#2
import os
import shutil

os.remove('file.txt')       # delete a file
os.rmdir('empty_dir')       # delete an empty directory
shutil.rmtree('full_dir')   # delete a directory and ALL its contents