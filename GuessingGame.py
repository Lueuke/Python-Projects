import random 
import math

print("Welcome to the Guessing Game\n")

UpperBound = int(input("Enter the Upper Bound of the Random Number generator: "))

LowerBound = int(input("\nEnter the Lower Bound of the Random Number generator: "))

RandomNumber = random.randrange(UpperBound,LowerBound)


