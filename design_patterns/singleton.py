class SingletonMetaclass(type):
    _instances = {}
    def __call__(cls, *args, **kwds):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwds)
        return cls._instances[cls]

class MySingleton(metaclass=SingletonMetaclass):
    pass

class MyAnotherSingleton(metaclass=SingletonMetaclass):
    pass

if __name__ == '__main__':
    class_1 = MySingleton()
    class_2 = MySingleton()
    a_class_1 = MyAnotherSingleton()
    a_class_2 = MyAnotherSingleton()
    print(f"""
class_1 is class_2: {class_1 is class_2}
a_class_1 is a_class_2: {a_class_1 is a_class_2}
class_1 is a_class_1: {class_1 is a_class_1}
a_class_1 is class_2: {a_class_1 is class_2} 
""")