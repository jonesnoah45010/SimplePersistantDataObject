# SimplePersistantDataObject
This module allows mac, linux and windows users to create simple memory() objects that mimic basic data types like ints, floats, lists, tuples and dictionaries with the added feature of persisting after the program exits.

Examples...

1. Counting how many times a program is run

from memory import *
counter = memory("counter") # object instantiated and "counter.txt" file created in current working directory
mem += 1 
print("this program has run " + str(counter) + " times")



2. Adding inputs to saved list

from memory import *
saved = memory("saved") # object instantiated and "saved.txt" file created in current working directory
savethis = input("what would you like to save to the list?")
saved.append(savethis)
print(saved)




