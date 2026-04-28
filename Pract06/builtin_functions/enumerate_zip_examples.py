#1 enumerate()
products = ["milk", "bread", "eggs"]

for i, item in enumerate(products):
    print(i, item)
#2
a = ["cat","dog","mouse"]

for i,words in enumerate(a):
    print(f"{i}:{words}",end = " ")
#1 zip()
names = ["Ali", "Omar", "John"]
ages = [18, 20, 19]

for name, age in zip(names, ages):
    print(name, age)
#2
letters = ["a", "b", "c"]
numbers = [1, 2, 3]

result = list(zip(letters, numbers))

print(result)