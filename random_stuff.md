## Abstract Base Class (ABC) vs typing.Protocol
ABC is nominal subtyping while Protocol is structural subtyping. The main difference is that for ABC, this is implemented very explicitly, u have to actually pass ABC into the class while Protocol doesnt.

ABC is an inherited class while Protocol only checks whether the methods matches or not and doesnt throw error if it doenst match

```python
from typing import Protocol

class Greeter(Protocol):
    derp = True
    def greet(self, name: str) -> str:
        pass

# No inheritance from Greeter!
class CasualGreeter:
    def greet(self, name: str) -> str:
        return f"Hey, {name}!"

def send_greeting(g: Greeter, target: str) -> None:
    print(g.greet(target))

# Valid: type checkers (mypy/pyright) accept CasualGreeter because the shape matches
send_greeting(CasualGreeter(), "GK")
```