from typing import Any, Callable, Optional as O
from pydantic import BaseModel
from graia.application.message.chain import MessageChain
import re

class NormalMatch(BaseModel):
    pass

class PatternReceiver(BaseModel):
    isGreed: bool = False

class FullMatch(BaseModel):
    pattern: str

    def __init__(self, pattern) -> None:
        super().__init__(pattern=pattern)
    
    def operator(self):
        return re.escape(self.pattern)

class Require(PatternReceiver):
    name: str
    checker: O[Callable[[MessageChain], bool]] = None
    translator: O[Callable[[MessageChain], Any]] = None

class Optional(PatternReceiver):
    name: str
    checker: O[Callable[[MessageChain], bool]] = None
    translator: O[Callable[[MessageChain], Any]] = None