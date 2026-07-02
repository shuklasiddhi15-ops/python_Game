# # game.py


import random
number = random.randint(1,100)

count = 0

while  True:
   count +=1
   user= int(input("enter the number:"))

   if user== number:
    print("you won man ")
    print(f"you took {count} to win!")
    break
 
   elif user< number:
    print(f"too low,guess high")

   elif user> number:
    print(f"too high, guess low")




