
# Method Overriding
# We start with a base class and then a subclass that "overrides" the speak method.
class Animal:
    def speak(self):
        return "I am an animal."

class Dog(Animal):
    def speak(self):
        return "Woof!"

print(Dog().speak())

# 2 Duck Typing
class Cat:
    def speak(self):
        return "Meow!"

def make_animal_speak(animal):
    # This function works for both Dog and Cat because they both have a 'speak' method.
    return animal.speak()

print(make_animal_speak(Cat()))
print(make_animal_speak(Dog()))

# 3 Operator Overloading
# We create a simple class that customizes the '+' operator.
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        # This special method defines the behavior of the '+' operator.
        return Vector(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(2, 3)
v2 = Vector(4, 5)
v3 = v1 + v2

print(v3)