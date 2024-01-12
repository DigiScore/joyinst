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
    N = 'arrowBlackUp'
    NW = 'arrowBlackUpLeft'
    NE = 'arrowBlackUpRight'
    W = 'arrowBlackLeft'
    E = 'arrowBlackRight'
    SW = 'arrowBlackDownLeft'
    SE = 'arrowBlackDownRight'
    S = 'arrowBlackDown'


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
    N = '#FF0000'
    NW = '#ffa500'
    NE = '#FFFF00'
    W = '#00FF00'
    E = '#006400'
    SW = '#800080'
    SE = '#FF00FF'
    S = '#FF0000'


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
game_staff = Staff((ZERO, Mm(100)), None, Mm(100), line_spacing=Mm(5))
Clef(ZERO, live_staff, 'treble_8va')
Clef(ZERO, game_staff, 'treble_8va')
my_arrow = MusicText((Mm(150), Mm(10)), live_staff, "coda",
                     alignment_x=AlignmentX.CENTER, alignment_y=AlignmentY.CENTER,
                     )
game_arrow = MusicText((Mm(150), Mm(10)), game_staff, "coda",
                       alignment_x=AlignmentX.CENTER, alignment_y=AlignmentY.CENTER,
                       )
my_solfa = Text((Mm(160), Mm(10)), live_staff, "-",
                alignment_x=AlignmentX.CENTER, alignment_y=AlignmentY.CENTER,
                )
game_solfa = Text((Mm(160), Mm(10)), game_staff, "-",
                  alignment_x=AlignmentX.CENTER, alignment_y=AlignmentY.CENTER,
                  )
notelist = []

js = Joystick()
n = Chordrest(live_staff.unit(10), live_staff, [], (1, 1))
sn = Chordrest(game_staff.unit(10), game_staff, [], (1, 1))


def build_bar(note):
    global n, my_arrow, my_solfa
    if n:
        n.remove()
        my_arrow.remove()
        my_solfa.remove()
    # compass = js.compass
    # colour = Colour(compass).value
    # make note
    n = Chordrest(live_staff.unit(10), live_staff, [js.neopitch], Duration(1, 2))

    # make arrow
    compass = js.compass
    arrow_direction = Arrow[compass].value
    arrow_colour = Colour[compass].value
    colour_brush = Brush(color=arrow_colour)
    my_arrow = MusicText((Mm(150), Mm(10)), live_staff, arrow_direction,
                         alignment_x=AlignmentX.CENTER, alignment_y=AlignmentY.CENTER,
                         brush=colour_brush
                         )

    # make solfa
    solfa = Solfa[compass].value
    my_solfa = Text((Mm(160), Mm(10)), live_staff, solfa,
                    alignment_x=AlignmentX.CENTER, alignment_y=AlignmentY.CENTER,
                    )


def refresh_loop(time):
    js.mainloop()
    if js.neopitch:
        build_bar(js.neopitch)


neoscore.show(refresh_func=refresh_loop,
              display_page_geometry=False,
              auto_viewport_interaction_enabled=False
              )
