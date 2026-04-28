import os
import shutil

# 1.Creating a text file and writing sample data
file = open("sample.txt", "w")
file.write("Hello\n")
file.write("This is first line\n")
file.close()

print("1) File created and data written")

# 2. Reading file
file = open("sample.txt", "r")
content = file.read()
print("\n2) File content:")
print(content)
file.close()

# 3. Append new lines
file = open("sample.txt", "a")
file.write("New line 1\n")
file.write("New line 2\n")
file.close()

# Verifying the content
file = open("sample.txt", "r")
print("\n3) After append:")
print(file.read())
file.close()

# 4. Copying file
shutil.copy("sample.txt", "backup.txt")
print("\n4) File copied to backup.txt")

# 5. Deleting file safely
os.remove("backup.txt")
print("5) backup.txt deleted")