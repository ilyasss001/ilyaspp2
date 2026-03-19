#1 Filter()
numbers = [1, 2, 3, 4, 5, 6]

result = list(filter(lambda x: x > 3, numbers))

print(result)
#2
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

result = list(filter(lambda x: x % 2 == 0 , numbers))

print(result)
#1 Map()
numbers = [1, 2, 3, 4]

result = list(map(lambda x: x * 2, numbers))

print(result)
#2
words = ["apple", "banana", "kiwi"]

result = list(map(lambda x: len(x), words))

print(result)
#1 Reduce()
from functools import reduce

numbers = [1, 2, 3, 4]

result = reduce(lambda x, y: x * y, numbers)

print(result)
#2
from functools import reduce

numbers = [1, 2, 3, 4]

result = reduce(lambda x, y: x + y, numbers)

print(result)