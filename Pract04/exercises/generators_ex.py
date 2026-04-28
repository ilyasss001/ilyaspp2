#1 Create a generator that generates the squares of numbers up to some number N
def gen(n):
    for i in range(1,n+1):
        yield i**2
n = int(input())
for x in gen(n):
    print(x)
#2 Write a program using generator to print the even numbers between 0 and n in comma separated form where n is input from console
def even_numbers(n):
    for i in range(0,n+1,2):
        yield i
n = int(input())
result = ",".join(str(x) for x in even_numbers(n))
print(result)
#3 Define a function with a generator which can iterate the numbers, which are divisible by 3 and 4, between a given range 0 and n.
def divisible(n):
    for i in range(0,n+1):
        if i%3 == 0 and i%4 == 0:
            yield i
n= int(input())
result = ",".join(str(x) for x in divisible(n))
print(result)
#4 Implement a generator called squares to yield the square of all numbers from (a) to (b). Test it with a "for" loop and print each of the yielded values.
def squares(a,b):
    for i in range(a,b+1):
        yield i**2
a,b = map(int,input().split())
for x in squares(a,b):
    print(x)
#5 Implement a generator that returns all numbers from (n) down to 0
def Return(n):
    for i in range(n,-1,-1):
        yield i
n = int(input())
for x in Return(n):
    print(x)