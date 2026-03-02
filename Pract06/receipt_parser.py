#1 re.search()
import re

#Check if the string starts with "The" and ends with "Spain":

txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)

if x:
  print("YES! We have a match!")
else:
  print("No match")
#2 re.findall
import re

#Return a list containing every occurrence of "ai":

txt = "The rain in Spain"
x = re.findall("ai", txt)
print(x)
#3 re.findall
import re

txt = "The rain in Spain"

#Check if "Portugal" is in the string:

x = re.findall("Portugal", txt)
print(x)

if (x):
  print("Yes, there is at least one match!")
else:
  print("No match")
#4 re.search()
import re

txt = "The rain in Spain"
x = re.search("\s", txt)

print("The first white-space character is located in position:", x.start()) 
#5 re.search()
import re

txt = "The rain in Spain"
x = re.search("Portugal", txt)
print(x)
#6 re.split()
import re

#Split the string at every white-space character:

txt = "The rain in Spain"
x = re.split("\s", txt)
print(x)
#7 re.split()
import re

#Split the string at the first white-space character:

txt = "The rain in Spain"
x = re.split("\s", txt, 1)
print(x)
#8 re.sub()
import re

#Replace all white-space characters with the digit "9":

txt = "The rain in Spain"
x = re.sub("\s", "9", txt)
print(x)
#9 re.sub()
import re

#Replace the first two occurrences of a white-space character with the digit 9:

txt = "The rain in Spain"
x = re.sub("\s", "9", txt, 2)
print(x)
#10 re.match()
import re

text = "Python is powerful"

result = re.match(r"Python", text)

if result:
    print("Match found!")
else:
    print("No match")
#11 re match()
import re

text = "I love Python"

result = re.match(r"Python", text)

if result:
    print("Match found!")
else:
    print("No match")