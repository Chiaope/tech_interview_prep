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
