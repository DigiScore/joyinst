
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
        fluidsynth.control_change(1, 7, 70) #  set volume control (7) to 70
        fluidsynth.control_change(1, 1, 0)  # set modulation wheel to 0
        self.fs_is_playing = 0

        # midi vars
        self.octave = 5
        self.dynamic = 70
        self.add_accidental = 0

    def mainloop(self):
        # -------- Main Program Loop -----------
        while self.running:
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

                if joystick_left_button == 64:
                    self.octave = 4

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
                    print("dynamic up")
                    # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
                    vol_param = (((joystick_left_y - 255) * (120 - 70)) / (128 - 255)) + 70
                elif joystick_left_y < 128:
                    print("dynamic down")
                    # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
                    vol_param = (((joystick_left_y - 127) * (70 - 20)) / (1 - 127)) + 20

                if not self.fs_is_playing:
                    self.dynamic = vol_param
                else:
                    fluidsynth.control_change(1, "volume", vol_param)

                # todo change this to RB and RT
                # todo change this to mod wheel CC control fluidsynth.control_change(1, 1, n)
                # Calculate octave shift
                if (127 - self.sensitivity) < joystick_left_x <= 127:
                    self.octave += 1
                elif 128 <= joystick_left_x < (128 + self.sensitivity):
                    self.octave -= 1

                if self.octave < 0:
                    self.octave = 0
                elif self.octave > 8:
                    self.octave = 8

                # make a sound or not
                if self.compass == "":
                    # send a stop to the FS player
                    if self.fs_is_playing != 0:
                        self.stop_note(self.fs_is_playing)
                        self.fs_is_playing = 0
                    # reset CC volume
                    fluidsynth.control_change(1, 7, 70)
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

            # Limit to n frames per second
            sleep(0.1)

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
