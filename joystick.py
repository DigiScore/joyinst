
from mingus.containers import Note, NoteContainer, Bar, Track
from mingus.midi import fluidsynth
import hid
from time import sleep

class Joystick:
    def __init__(self):
        self.running = None
        self.compass = ""

        self.running = True

        self.gamepad = hid.device()
        self.gamepad.open(0x07b5, 0x0312)  # Logic PS controller USB. gamepad.open(0x045e, 0x02fd) = Bluetooth # XBOX One
        self.gamepad.set_nonblocking(True)
        self.sensitivity = 15

        # init midi synth
        fluidsynth.init("GeneralUserGSv1.471.sf2")
        fluidsynth.set_instrument(1, 74)
        fluidsynth.main_volume(1, 100) #  set volume control (7) to 70
        fluidsynth.modulation(1, 0)  # set modulation wheel to 0
        self.fs_is_playing = 0

        # midi vars
        self.octave = 5
        self.dynamic = 70
        self.add_accidental = 0

        # neoscore vars
        self.neopitch = 'c'

    def mainloop(self):
        # -------- Main Program Loop -----------
        # while self.running:
            # EVENT PROCESSING STEP
        report = self.gamepad.read(64)
        if report:
            print(report)

            # joystick range = (128 - 255) - 0 - (1 - 127)
            joystick_left_y = report[1]
            joystick_left_x = report[0]
            joystick_left_button = report[5]  # code 64
            joystick_right_x = report[3]
            joystick_right_y = report[2]

            buttons = report[5]  # 1 lb, 2 lt

            # reset vars
            self.compass = ""
            self.add_accidental = 0

            # Decode buttons
            if buttons == 1:  # LB
                self.add_accidental = 1
            elif buttons == 2:  # LT
                self.add_accidental = -1
            #
            #
            # if joystick_left_button == 64:
            #     self.octave = 4

            # decode joystick right (notes) as compass points
            if 128 <= joystick_right_y < (128 + self.sensitivity):
                self.compass += "N"
            elif (127 - self.sensitivity) < joystick_right_y <= 127:
                self.compass += "S"

            if 128 <= joystick_right_x < (128 + self.sensitivity):
                self.compass += "W"
            elif (127 - self.sensitivity) < joystick_right_x <= 127:
                self.compass += "E"

            print(self.compass)

            # Calculate dynamic joystick for dynamics
            if joystick_left_y <= 5 or joystick_left_y >= 250:
                vol_param = 70
            elif joystick_left_y >= 128:
                # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
                vol_param = int(((joystick_left_y - 255) * (120 - 70)) / (128 - 255)) + 70
            elif joystick_left_y < 128:
                # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
                vol_param = int(((joystick_left_y - 127) * (70 - 20)) / (1 - 127)) + 20

            if not self.fs_is_playing:
                self.dynamic = vol_param
            else:
                fluidsynth.main_volume(1, vol_param)

            # todo change this to mod wheel CC control fluidsynth.control_change(1, 1, n)
            # Calculate octave shift
            if buttons == 4:  # LB
                self.octave += 1
            elif buttons == 8:  # LT
                self.octave += -1
            elif buttons == 12:
                self.octave = 5

            if self.octave < 0:
                self.octave = 0
            elif self.octave > 8:
                self.octave = 8

            # change mod wheel/ expression
            if joystick_left_x <= 5 or joystick_left_x >= 250:
                fluidsynth.modulation(1, 0)
                fluidsynth.control_change(1, 2, 0)
            elif (127 - self.sensitivity) < joystick_left_x <= 127:
                print('modulation')
                # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
                mod_param = int(((joystick_left_x - 255) * (120 - 70)) / (128 - 255)) + 70
                fluidsynth.modulation(1, mod_param)

            elif 128 <= joystick_left_x < (128 + self.sensitivity):
                print('after touch')
                # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
                mod_param = int(((joystick_left_x - 127) * (70 - 20)) / (1 - 127)) + 20
                fluidsynth.control_change(1, 2, mod_param)

            # make a sound or not
            if self.compass == "":
                # send a stop to the FS player
                if self.fs_is_playing != 0:
                    self.stop_note(self.fs_is_playing)
                    self.fs_is_playing = 0
                # reset CC volume
                fluidsynth.main_volume(1, 100)
                self.neopitch = 'c'
            else:
                # get current octave
                octave = self.octave

                # match compass to notes
                match self.compass:
                    case 'N':
                        note = 'C'
                    case 'NE':
                        note = 'E'
                    case 'E':
                        note = 'G'
                    case 'SE':
                        note = 'B'
                    case 'S':
                        note = 'C'
                        octave = self.octave+1
                    case 'SW':
                        note = 'A'
                    case 'W':
                        note = 'F'
                    case 'NW':
                        note = 'D'

                # adjust note for enharmonic shift
                match self.add_accidental:
                    case 1:
                        note = f"{note}#"
                    case -1:
                        note = f"{note}b"

                # make fs style note str
                fs_note = f"{note}-{octave}"
                print(f"making note {fs_note}")

                # if not playing - make a note
                if self.fs_is_playing == 0:
                    self.make_sound(fs_note,
                                    self.dynamic
                                    )
                    self.fs_is_playing = fs_note

                # if already playing and new note called, change it
                elif fs_note != self.fs_is_playing:
                    # stop note
                    self.stop_note(self.fs_is_playing)
                    # play new note
                    self.make_sound(fs_note,
                                    self.dynamic
                                    )
                    self.fs_is_playing = fs_note

                # make into neoscore note value
                if note[-1] == "#":
                    self.neopitch = f"{note[0].lower()}s"
                elif note[-1] == "b":
                    self.neopitch = f"{note[0].lower()}f"
                else:
                    self.neopitch = note[0].lower()

                    # check octave in range and add octave indicator
                    # if octave out of range then make it middle C octave
                if 2 <= self.octave <= 6:

                    # add higher octave indicators "'"
                    if self.octave > 4:
                        ticks = self.octave - 4
                        for tick in range(ticks):
                            self.neopitch += "'"

                    # add lower octave indicators ","
                    elif self.octave < 4:
                        if self.octave == 3:
                            self.neopitch += ","
                        elif self.octave == 2:
                            self.neopitch += ",,"

            # Limit to n frames per second
            # sleep(0.1)

    def make_sound(self,
                   new_note,
                   dynamic,
                   ):

        fluidsynth.play_Note(Note(new_note,
                                  velocity=dynamic
                                  )
                             )

    def stop_note(self, note_to_stop):
        fluidsynth.stop_Note(Note(note_to_stop))

    # def terminate(self):
    #     fluids

if __name__ == "__main__":
    js = Joystick()
    js.mainloop()
