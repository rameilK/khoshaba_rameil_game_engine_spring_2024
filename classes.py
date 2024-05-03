# This file was created by: Chris Cozort

# Classes are foundational to object oriented programming

# They serve as blueprints or templates for things...

print("Today we are learning about Classes")

# create a class
class Hero:
    # create init method/function that allows us to assign properties
    def __init__(self, name, hitpoints):
        self.name = name
        self.hitpoints = hitpoints
        # 3-5 properties that define your hero type
    # create method to allow Hero to jump
        #3-5 methods that represent things that hero can do...
    def jump(self):
        print(self.name, "has jumped!!!")

class Monster:
    def __init__(self, name):
        self.name = name

p1 = Hero("Link", 100)

print(p1.name)
print(p1.hitpoints)
print(p1.name , "has" , str(p1.hitpoints) , "hitpoints.")

p1.jump()
