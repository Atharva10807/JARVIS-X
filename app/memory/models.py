from dataclasses import dataclass


@dataclass
class Memory:
    content: str
    category: str
    importance: float
    key: str = ""
    value: str = ""
