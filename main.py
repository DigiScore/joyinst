from joystick import Joystick
from time import sleep
from threading import Thread

from neoscore.common import *

neoscore.setup()
staff = Staff(ORIGIN, None, Mm(100))
Clef(ZERO, staff, 'treble')
n = Chordrest(staff.unit(2), staff, ["c"], (1, 2))

js = Joystick()

joystick_thread = Thread(target=js.mainloop)
joystick_thread.start()

neoscore.show()

