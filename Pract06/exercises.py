#1 Write a Python program that matches a string that has an 'a' followed by zero or more 'b''s.
import re

text = input()

if re.match(r"^ab*", text):
    print("Match")
else:
    print("No match")
#2 Write a Python program that matches a string that has an 'a' followed by two to three 'b'.
import re

text = input()

if re.match(r"^ab{2,3}$", text):
    print("Match")
else:
    print("No match")
#3 Write a Python program to find sequences of lowercase letters joined with a underscore.
import re

text = input()

if re.match(r"^[a-z]+_[a-z]+$", text):
    print("Match")
else:
    print("No match")
#4 Write a Python program to find the sequences of one upper case letter followed by lower case letters.
import re

text = input()

if re.match(r"^[A-Z][a-z]+$", text):
    print("Match")
else:
    print("No match")
#5 Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.
import re

text = input()

if re.match(r"^a.*b$", text):
    print("Match")
else:
    print("No match")
#6 Write a Python program to replace all occurrences of space, comma, or dot with a colon.
import re

text = input()

result = re.sub(r"[ ,\.]", ":", text)

print(result)

#7 Write a python program to convert snake case string to camel case string.
import re

text = input()

parts = text.split("_")

result = parts[0]

for word in parts[1:]:
    result += word.capitalize()

print(result)
#8 Write a Python program to split a string at uppercase letters.
import re

text = input()

result = re.findall(r"[A-Z][^A-Z]*", text)

print(result)
#9 Write a Python program to insert spaces between words starting with capital letters.
import re

text = input()

result = re.sub(r"([A-Z])", r" \1", text).strip()

print(result)
#10 Write a Python program to convert a given camel case string to snake case.
import re

text = input()

result = re.sub(r"([A-Z])", r"_\1", text).lower()

print(result)