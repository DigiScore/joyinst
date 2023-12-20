
from mingus.containers import Note, NoteContainer, Bar, Track
from mingus.midi import fluidsynth
import hid
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read('config.ini')


class Joystick:
    def __init__(self):
        # Instantiate the game device
        self.gamepad = hid.device()
        self.gamepad.open(0x2563, 0x0575)  # PC/PS3/Android. gamepad.open(0x045e, 0x02fd) = Bluetooth # XBOX One
        self.gamepad.set_nonblocking(True)
        self.sensitivity = 20

        # init midi synth
        """
        GM insts
        24 = nyatiti
        74 = recorder
        108 = kalimba
        110 = orutu fiddle
        """

        fluidsynth.init("GeneralUserGSv1.471.sf2")
        instrument = config_object['MIDI'].getint('instrument')
        fluidsynth.set_instrument(1, instrument)
        fluidsynth.main_volume(1, 100) #  set volume control (7) to 70
        fluidsynth.modulation(1, 0)  # set modulation wheel to 0
        if instrument == 74 or instrument == 110:
            fluidsynth.control_change(1, 5, 100)
        self.fs_is_playing = 0

        # midi vars
        self.compass = ""
        self.octave = 5
        self.dynamic = 70
        self.add_accidental = 0

        # neoscore vars
        self.neopitch = None

    def mainloop(self):
        # -------- Main Program Loop -----------
        report = self.gamepad.read(64)
        if report:
            # print(report)

            ####
            #  wired USB PS2
            ####
            # joystick range = (128 - 255) - 0 - (1 - 127)
            joystick_left_y = report[1]
            joystick_left_x = report[0]
            joystick_left_button = report[5]  # code 64
            joystick_right_x = report[3]
            joystick_right_y = report[2]
            buttons = report[5]  # 1 lb, 2 lt

            ####
            # wireless PC/PS3/Android
            ####
            joystick_left_y = report[4]
            joystick_left_x = report[3]
            joystick_left_button = report[5]  # code 64
            joystick_right_x = report[5]
            joystick_right_y = report[0]
            buttons = report[5]  # 1 lb, 2 lt

            # reset vars
            self.compass = ""
            self.add_accidental = 0

            # Decode buttons
            if buttons == 16:  # LB
                self.add_accidental = 1
            elif buttons == 64:  # LT
                self.add_accidental = -1

            # decode joystick right (notes) as compass points
            if 128 <= joystick_right_y < (128 + self.sensitivity):
                self.compass += "N"
            elif (127 - self.sensitivity) < joystick_right_y <= 127:
                self.compass += "S"

            if 128 <= joystick_right_x < (128 + self.sensitivity):
                self.compass += "W"
            elif (127 - self.sensitivity) < joystick_right_x <= 127:
                self.compass += "E"

            # print(self.compass)

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
            if buttons == 32:  # LB
                self.octave += 1
            elif buttons == 128:  # LT
                self.octave += -1
            elif buttons == 160:
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
                # print('modulation')
                # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
                mod_param = int(((joystick_left_x - 255) * (120 - 70)) / (128 - 255)) + 70
                fluidsynth.modulation(1, mod_param)

            elif 128 <= joystick_left_x < (128 + self.sensitivity):
                # print('after touch')
                # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
                mod_param = int(((joystick_left_x - 127) * (70 - 20)) / (1 - 127)) + 20
                fluidsynth.control_change(1, 68, mod_param)

            # make a sound or not
            if self.compass == "":
                # send a stop to the FS player
                if self.fs_is_playing != 0:
                    self.stop_note(self.fs_is_playing)
                    self.fs_is_playing = 0
                # reset CC volume
                fluidsynth.main_volume(1, 100)
                self.neopitch = ""
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
                # print(f"making note {fs_note}")

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

                # add higher octave indicators "'"
                if octave > 4:
                    ticks = octave - 4
                    for tick in range(ticks):
                        self.neopitch += "'"

                # add lower octave indicators ","
                elif octave < 4:
                    if octave == 3:
                        self.neopitch += ","
                    elif octave == 2:
                        self.neopitch += ",,"

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
