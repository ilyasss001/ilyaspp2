#1
class Dog:
    species = "Canine"  

dog1 = Dog()
dog2 = Dog()

print(dog1.species)
print(dog2.species)
#2
class Dog:
    species = "Canine"

dog1 = Dog()
dog2 = Dog()

Dog.species = "Wolf"

print(dog1.species)
print(dog2.species)
#3
class Dog:
    species = "Canine"  
    def __init__(self, name):
        self.name = name  

dog1 = Dog("Rex")
dog2 = Dog("Bob")

print(dog1.name)     
print(dog2.name)     
print(dog1.species)  
print(dog2.species) 
