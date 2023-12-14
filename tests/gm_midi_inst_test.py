from mingus.midi import fluidsynth
from time import sleep

fluidsynth.init("../GeneralUserGSv1.471.sf2")

inst_list = [24, 74, 108, 110]

for inst in inst_list:
    fluidsynth.set_instrument(1, inst)

    for n in range(20):
        note = n + 50
        fluidsynth.play_Note(note)
        sleep(0.2)
        fluidsynth.stop_Note(note)