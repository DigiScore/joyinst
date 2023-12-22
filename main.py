from joystick import Joystick
from time import sleep, time
from threading import Thread
from enum import Enum

from neoscore.common import *

class Arrow(Enum):
    """
    Smufl Arrows
    https://w3c.github.io/smufl/latest/tables/arrows-and-arrowheads.html
    N U+EB68 arrowWhiteUp
    NW U+EB6F arrowWhiteUpLeft
    NE U+EB69 arrowWhiteUpRight
    W U+EB6E arrowWhiteLeft
    E U+EB6A arrowWhiteRight
    SW U+EB6D arrowWhiteDownLeft
    SE U+EB6B arrowWhiteDownRight
    S U+EB6C arrowWhiteDown
    """
    N = 'arrowWhiteUp'
    NW = 'arrowWhiteUpLeft'
    NE = 'arrowWhiteUpRight'
    W = 'arrowWhiteLeft'
    E = 'arrowWhiteRight'
    SW = 'arrowWhiteDownLeft'
    SE = 'arrowWhiteDownRight'
    S = 'arrowWhiteDown'

class Colour(Enum):
    """
    Arrow notes COLOURS
    https://digitlearning.co.uk/what-are-arrownotes/

    c = red N or S
    d = orange NW
    e = yellow NE
    f = light green W
    g = dark green E
    a = purple SW
    b = pink SE
    c = red N or S
    """
    c = 'red'
    d = 'orange'
    e = 'yellow'
    f = 'light_green'
    g = 'dark_green'
    a = 'purple'
    b = 'pink'

class Solfa(Enum):
    """
    Sol Fa translation of compass points
    to do, re, mi, fa, sol, la, ti, do.
    Flats and sharps COULD be represented by 'a' and 'e'
    or simply 'b' and '#'
    """
    N = 'do'
    NW = 're'
    NE = 'mi'
    W = 'fa'
    E = 'sol'
    SW = 'la'
    SE = 'ti'
    S = 'do'


# todo - transpositions!!! this is in C only. Tonic & position & arrows
#  needs to be related to parent key.


neoscore.setup()
live_staff = Staff(ORIGIN, None, Mm(100), line_spacing=Mm(5))
simon_staff = Staff((ZERO, Mm(40)), None, Mm(100), line_spacing=Mm(5))
Clef(ZERO, live_staff, 'treble_8va')
Clef(ZERO, simon_staff, 'treble_8va')
notelist = []

js = Joystick()
n = Chordrest(live_staff.unit(10), live_staff, [], (1,1))
sn = Chordrest(simon_staff.unit(10), simon_staff, [], (1,1))

def build_bar(note):
    global n
    if n:
        n.remove()
    # compass = js.compass
    # colour = Colour(compass).value
    n = Chordrest(live_staff.unit(10), live_staff, [js.neopitch], Duration(1, 2))
    MusicText((Mm(150), Mm(10)), live_staff, "arrowWhiteUp",
              alignment_x=AlignmentX.CENTER, alignment_y=AlignmentY.CENTER,
              # colour=colour
              )

def refresh_loop(time):
    js.mainloop()
    if js.neopitch:
        build_bar(js.neopitch)

neoscore.show(refresh_func=refresh_loop,
              display_page_geometry=False,
              auto_viewport_interaction_enabled=False
              )

