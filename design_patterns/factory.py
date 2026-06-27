"""
Factory design pattern is important because it provides a way to create objects without specifying the exact class of object that will be created. 
It allows for greater flexibility and scalability in code, as new classes can be added without modifying existing code. 
The factory pattern also promotes the use of interfaces and abstract classes, which can lead to more maintainable and testable code.
"""

class ConcreteClassA:
    def do_something(self):
        return "ConcreteClassA doing something"

class ConcreteClassB:
    def do_something(self):
        return "ConcreteClassB doing something"

def create_concrete_object(class_name):
    if class_name == "A":
        return ConcreteClassA()
    elif class_name == "B":
        return ConcreteClassB()
    else:
        raise ValueError(f"Unknown class name: {class_name}")

if __name__ == "__main__":
    concrete_class_a = create_concrete_object("A")
    concrete_class_b = create_concrete_object("B")
    print(concrete_class_a.do_something())
    print(concrete_class_b.do_something())
    