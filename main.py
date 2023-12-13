from joystick import Joystick
from time import sleep
from threading import Thread

from neoscore.common import *

# class enum(ENUM)
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
    n = Chordrest(live_staff.unit(10), live_staff, [js.neopitch], Duration(1, 2))
    # notelist.append(n)

def refresh_loop(time):
    js.mainloop()
    # if not js.fs_is_playing:
    if js.neopitch:
        build_bar(js.neopitch)

neoscore.show(refresh_func=refresh_loop,
              display_page_geometry=False,
              auto_viewport_interaction_enabled=False
              )

