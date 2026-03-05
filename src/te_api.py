from typing import Any
from varname.core import argname

# That is the most horrendous code i have ever written

class Mutable[T]:
    def __init__(self, v: T) -> None:
        self.v: T = v

class teAPIClass:
    pass

teAPI = teAPIClass()
apiGlobals = {"te": teAPI}

def addToAPI(module: str, value: Any) -> None:
    if not hasattr(teAPI, module):
        setattr(teAPI, module, type(module, (object,), {}))
    setattr(getattr(teAPI, module), str(argname('value')), value)

