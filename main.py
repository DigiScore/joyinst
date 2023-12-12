from joystick import Joystick
from time import sleep
from threading import Thread

from neoscore.common import *

neoscore.setup()
staff = Staff(ORIGIN, None, Mm(100))
Clef(ZERO, staff, 'treble')
notelist = []
js = Joystick()

def build_bar(note):
    for nt in notelist:
        nt.remove()
    n = Notehead(staff.unit(2), staff, js.neopitch, Duration(1, 2))
    notelist.append(n)

def refresh_loop(time):
    js.mainloop()
    if not js.fs_is_playing:
        if js.neopitch:
            build_bar(js.neopitch)

neoscore.show(refresh_func=refresh_loop,
              display_page_geometry=False)

