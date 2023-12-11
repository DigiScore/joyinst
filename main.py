from joystick import Joystick
from time import sleep
from threading import Thread

from neoscore.common import *

neoscore.setup()
staff = Staff(ORIGIN, None, Mm(100))
Clef(ZERO, staff, 'treble')
n = Notehead(staff.unit(2), staff, "c", Duration(1, 2))

js = Joystick()


def refresh_loop(time):
    js.mainloop()
    n = Notehead(staff.unit(2), staff, js.neopitch, Duration(1, 2))

neoscore.show(refresh_func=refresh_loop,
              display_page_geometry=False)

