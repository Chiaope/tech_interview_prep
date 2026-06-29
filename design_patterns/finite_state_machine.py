"""
Finite State Machine (FSM) design pattern is important because it allows for the modeling of complex systems with a finite number of states and transitions between those states.
It provides a clear and organized way to manage state-dependent behavior, making it easier to understand, maintain, and extend the system.
FSMs are widely used in various applications, including game development, user interface design, and control systems.
"""


class CarFiniteStateMachine:
    def __init__(self):
        self.state = "stopped"
        self.transitions = {
            "stopped": {"stop": self.__stop, "start": self.__start},
            "started": {
                "start": self.__start,
                "drive": self.__drive,
                "stop": self.__stop,
            },
            "driving": {"drive": self.__drive, "stop": self.__stop},
        }

    def event(self, event):
        event_function = self.transitions.get(self.state, {}).get(event)
        if event_function is None:
            print(f"Unable to {event}.")
        else:
            event_function()

    def __start(self):
        self.state = "started"
        print("Car started.")

    def __drive(self):
        self.state = "driving"
        print("Car is driving.")

    def __stop(self):
        self.state = "stopped"
        print("Car stopped.")


if __name__ == "__main__":
    my_car = CarFiniteStateMachine()
    my_car.event("stop")
    my_car.event("drive")
    my_car.event("start")
    my_car.event("drive")
    my_car.event("stop")
