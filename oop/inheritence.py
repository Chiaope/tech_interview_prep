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
