#1 To delete file we use os.remove()
import os
os.remove("demofile.txt")
#2 Check if file exists, then delete it
import os
if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
else:
  print("The file does not exist")
#3 To delete an entire folder, use the os.rmdir() method
import os
os.rmdir("myfolder")