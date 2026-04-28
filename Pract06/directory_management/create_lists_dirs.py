#1 Creating folder
import os

os.mkdir("my_folder")
#2 Creating several folders
import os

os.makedirs("parent/child/grandchild")
#3 
import os

# create folders: folder/subfolder
os.makedirs("project/data/files", exist_ok=True)

print("Folders created!")

