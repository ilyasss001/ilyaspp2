#1 Open file
f = open("demofile.txt", "r")

print(f.read())
#2 If the file is located in a different location
f = open("D:\\myfiles\welcome.txt", "r")

print(f.read())
#3 Using the with statement
with open("demofile.txt", "r") as f:
  print(f.read())
#4 Close files
f = open("demofile.txt", "r")

print(f.readline())

f.close()
#5 Read only the parts of the file
with open("demofile.txt", "r") as f:
  print(f.read(5))
