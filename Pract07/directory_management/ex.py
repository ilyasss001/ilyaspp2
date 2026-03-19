import os
import shutil

# 1. Create nested directories
os.makedirs("parent/child/grandchild", exist_ok=True)
print("1) Nested directories created")

# Create a sample file
file = open("parent/sample.txt", "w")
file.write("Hello file")
file.close()

# 2. List files and folders
print("\n2) Files and folders in 'parent':")
print(os.listdir("parent"))

# 3. Find files by extension (.txt)
print("\n3) .txt files:")
for file in os.listdir("parent"):
    if file.endswith(".txt"):
        print(file)

# 4. Copy file
shutil.copy("parent/sample.txt", "parent/child/sample_copy.txt")
print("\n4) File copied")

# Move file
shutil.move("parent/child/sample_copy.txt", "parent/child/grandchild/sample_moved.txt")
print("File moved")