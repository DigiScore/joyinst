from joystick import Joystick
from time import sleep
from threading import Thread

from mingus.core import scales, meter, chords, progressions
from mingus.containers import Note, NoteContainer, Bar, Track
from mingus.midi import fluidsynth
from random import randint, random, choice
from mingus.containers.instrument import Instrument, Piano, Guitar

fluidsynth.init("GeneralUserGSv1.471.sf2")
# sleep(2)

js = Joystick()

js.mainloop()

# joy_thread = Thread(target=js.mainloop)
# joy_thread.start()

fluidsynth.play_Note(Note("C-5"))


while True:
    if js.compass == "N":
        fluidsynth.play_Note(Note("C-5"))

    sleep(0.1)
