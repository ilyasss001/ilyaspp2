#1 Write a Python program to convert degree to radian.
import math
n = int(input())
radian = n * math.pi/180
print(radian)
#2 Write a Python program to calculate the area of a trapezoid.
import math
height,first_value,second_value = map(int,input().split())
area = (first_value + second_value) * (height/2)
print(area)
#3 Write a Python program to calculate the area of regular polygon.
import math
number_sides = int(input())
length_side = float(input())
area = (length_side ** 2 * number_sides)/(4 * math.tan(math.pi / number_sides))
print(area)
#4 Write a Python program to calculate the area of a parallelogram.
import math
length,height = map(float,input().split())
area = length * height
print(area)