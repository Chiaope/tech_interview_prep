# Notes

## super()
```
super() calls the parent class
```

## `super().__new__(cls, name, bases, dct)`
```
cls: refers to the current class
name: refers to the current class name
bases: refers to the parent classes, eg. class MyClass(Animal, Machine), bases will be (Animal, Machine) 
dct: refers to the everything that is contained in the class, the attributes, the methods, etc
```

## `__new__` vs `__init__`
```
__new__ is the one that actually allocates resourcess to the creation of the new object and creates the object

__init__ initialise the object AFTER the object have been created 
```

## `__call__`
```
__call__ allows the object itself to be callable
all classes have something called metaclass and by default the metaclass is `type`
eg.
my_class = MyClass() # this is an example of metaclass, `type`, being called
my_class() # the created object becomes callable
```

## `__dir__()`
```
__dir__() will show all of the methods, attributes and hidden methods available for the object instance
```

## Inheritence
When class inherit a parent class, they will take their attributes and methods too but the methods or attributes can be overwritten in the child class itself.

When multiple child inherit from multiple parent class and if there are **same** attributes or methods, the order where the parents are inherited matters. Priority will be given to the parameter that is in front.
```python
class Animal:
    species = "Animal"
class Mammal:
    species = "Mammal"
class AnimalHuman(Animal, Mammal):
    pass
class MammalHuman(Mammal, Animal):
    pass
class Human(Animal, Mammal):
    species = "Human"

animal_human = AnimalHuman()
print(animal_human.species) # this will give "Animal"
mammal_human = MammalHuman()
print(mammal_human.species) # this will give "Mammal"
human = Human()
print(human.species) # this will give "Human" 
```