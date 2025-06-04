class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.__class__.__name__}({self.name}, age={self.age})"

    def __eq__(self, other):
        return isinstance(other, Animal) and self.name == other.name and self.age == other.age

class Cat(Animal):
    pass

class Dog(Animal):
    pass

class Bird(Animal):
    pass
