from enum import Enum, verify, UNIQUE, IntEnum
from pygame import Color


@verify(UNIQUE)
class Colors(Enum):
    BLACK = Color(0, 0, 0)
    WHITE = Color(255, 255, 255)
    BACKGROUND = Color(239, 229, 186)


class WindowSize(IntEnum):
    WIDTH = 1920
    HEIGHT = 1080
