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

When multiple child inherit from multiple parent class and if there are **same** attributes or methods, the **order** where the parents are inherited matters. Priority will be given to the parameter that is in front.
```python
class Animal:
    species = "Animal"

    def __init__(self, name: str):
        self.name = name.upper()

    def speak(self):
        print("Animal speaking")

class Mammal:
    species = "Mammal"

    def __init__(self, name):
        self.name = name.lower()
    
    def speak(self):
        print("Mammal speaking")


class AnimalHuman(Animal, Mammal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MammalHuman(Mammal, Animal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


animal_human = AnimalHuman("Animal Human Name")
print(animal_human.species)  # this will give "Animal"
print(animal_human.name)  # this will give "ANIMAL HUMAN NAME"
animal_human.speak()  # this will give "Animal speaking"
mammal_human = MammalHuman("Mammal Human Name")
print(mammal_human.species)  # this will give "Mammal"
print(mammal_human.name)  # this will give "mammal human name"
mammal_human.speak()  # this will give "Mammal speaking"
```

## Polymorphism
Polymorphism means overwritting parent's function or attributes to fit child's needs.

```python
class Mammal:
    species = "Mammal"

    def __init__(self, name):
        self.name = name.lower()
        self.blood_color = "red"

    def speak(self):
        print("Mammal speaking")


class Human(Mammal):
    species = "Human"

    def __init__(self, name):
        super().__init__(name)
        # need to be after super() if not self.name will be overwritten
        self.name = name

    def speak(self):
        print("Human speaking")


human = Human("Human Name")
print(human.species)  # this will give "Human"
print(human.blood_color)  # this will give "red"
print(human.name)  # this will give "Human Name"
human.speak()  # this will give "Human speaking"
```

## Encapsulation
Encapsulation is trying to hide some attributes and it cannot be access outside of the class itself, it can only be access in the class itself. This is to prevent accidental overwritting attributes.

There are 3 different type of class members, `private`, `protected`, `public` and they can be set by using leading underscores when naming a variable.

`private` members are variable name that starts with double underscore `__` and these are attributes or methods that can only be access at the class level itself. 

`protected` members are variable name that starts with single underscore `_` these are attributes or methods that **suggest** other developers not to use these attributes or methods but there is no strict blocking.

`public` members are everything else


**NOTE:** **leading** and **trailing** double underscore are magic methods reserved in python, so it is fully public

**Access private member:** private members can be accessed by using `name mangling`, basically adding an leading underscore plus class name before the member. eg. `child._MyChild__secret`

```python
class MyParent:
    __secret = "Parent Secret"

    def get_secret(self):
        return self.__secret

    def set_secret(self, new_secret):
        self.__secret = new_secret

    def __secret_method(self):
        print("Parent Secret Method")

    def access_secret_method(self):
        self.__secret_method()

    def _protected_method(self):
        print("Parent Protected Method")


class MyChild(MyParent):
    __secret = "Child Secret"
    _protected = "Child Protected"

    def get_parent_secret(self):
        return super().get_secret()

    def set_parent_secret(self, new_secret):
        return super().set_secret(new_secret)

    def access_parent_secret_method(self):
        super().access_secret_method()

    def _parent_protected_method(self):
        super()._protected_method()

    def get_secret(self):
        return self.__secret

    def set_secret(self, new_secret):
        self.__secret = new_secret

    def __secret_method(self):
        print("Child Secret Method")

    def access_secret_method(self):
        self.__secret_method()

    def _protected_method(self):
        print("Child Protected Method")


if __name__ == "__main__":
    child = MyChild()
    print(child.get_secret())  # output: Child Secret
    print(child.get_parent_secret())  # output: Parent Secret
    print(child._protected)  # output: Child Protected
    child.access_secret_method()  # output: Child Secret Method
    child.access_parent_secret_method()  # output: Parent Secret Method
    child._protected_method()  # output: Child Protected Method
    child._parent_protected_method()  # output: Parent Protected Method
    try:
        print(child.__secret)
    except Exception as e:
        print(e)  # output: 'MyChild' object has no attribute '__secret'
        print(child._MyChild__secret)  # output: Child Secret

    try:
        child.__secret_method()
    except Exception as e:
        print(e)  # output: 'MyChild' object has no attribute '__secret_method'
        child._MyChild__secret_method() # output: Child Secret Method

    child.set_secret("Child New Secret")
    child.set_parent_secret("Parent New Secret")
    print(child.get_secret())  # output: Child New Secret
    print(child.get_parent_secret())  # output: Parent New Secret
    child._protected = "Child New Protected"
    print(child._protected)  # output: Child New Protected
```