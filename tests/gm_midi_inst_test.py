from mingus.midi import fluidsynth
from time import sleep

# fluidsynth.init("../GeneralUserGSv1.471.sf2")

fluidsynth.init("../africa.sf2")
"""
Bank	Preset	Name
0	1	Vocals/FX's
0	2	Hmmm
0	3	Moog
0	4	Hi Pad slide A
0	5	Tom slider C&A
0	6	Lo Pad slide A
0	7	Shofars
0	8	Kalimba
0	9	FIute w warble
0	10	FIute w blow
0	11	Bass
"""
# bank 0, present 1-11, SoundFont 1

for i in range(12):
    fluidsynth.set_instrument(1, i + 1, 0)
    print(i)
    for n in range(128):
        print(i+1, n)
        fluidsynth.play_Note(n)
        sleep(0.5)
        fluidsynth.stop_Note(n)
#
# inst_list = [24, 74, 108, 110]
#
# for c in range(128):
#     for inst in range(128):
#         fluidsynth.set_instrument(c, inst)
#
#         for n in range(1):
#             note = n + 50
#             fluidsynth.play_Note(note)
#             sleep(0.2)
#             fluidsynth.stop_Note(note)