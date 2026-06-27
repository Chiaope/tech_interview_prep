"""
Observer design pattern allows a subject to notify a list of observers when it has an update.
"""


class Observer:
    def __init__(self):
        self.subject_list = []

    def update(self, message):
        for subject in self.subject_list:
            subject.notify(message)


class Subject:
    def attach(self, observer):
        observer.subject_list.append(self)

    def detach(self, observer):
        observer.subject_list.remove(self)

    def notify(self, message):
        print(f"Message: {message}")


if __name__ == "__main__":
    observer = Observer()
    subject1 = Subject()
    subject2 = Subject()

    subject1.attach(observer)
    subject2.attach(observer)

    observer.update("Hello, World!")

    subject1.detach(observer)

    observer.update("New message after detaching subject1.")
