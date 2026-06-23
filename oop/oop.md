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