import tomllib
import platform

from mingus.containers import Note
import fluidsynth as fs

with open('config.toml', 'rb') as config_file:
    config = tomllib.load(config_file)

"""
Currently running with africa.sf2:

https://www.polyphone-soundfonts.com/documents/27-instrument-sets/346-africa

 Herb Jimmerson  22 February 2017
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
Details
LicenseJust give credit


GIVE CREDIT
License on Creative Commons

The author allows a personal and commercial use of the soundfont along with derivative works whose distribution is
also allowed with no restrictions. The only condition is to give appropriate credit to the initial author by mentioning
its name (good practices for attribution are described here). This license is recommended for an optimal use and
distribution of a soundfont.
"""


class Joystick:
    """
    Manages the data from the joystick controls.
    Calculates the note values and makes a sound.
    """

    def __init__(self):
        super().__init__()
        # Instantiate the vars
        self.sensitivity = 20
        self.joystick_active_range = 0.95
        self.A_button = 0
        self.B_button = 0
        self.X_button = 0
        self.Y_button = 0

        # init midi synth
        """
        GM insts
        24 = nyatiti
        74 = recorder
        108 = kalimba
        110 = orutu fiddle
        
        africa.sf2
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

        # Download https://www.polyphone-soundfonts.com/documents/file/470-africa-sf2/latest/download?f7af2bbf653590fa8046b3fc31797913=1&return=aHR0cHMlM0ElMkYlMkZ3d3cucG9seXBob25lLXNvdW5kZm9udHMuY29tJTJGZG9jdW1lbnRzJTJGMjctaW5zdHJ1bWVudC1zZXRzJTJGMzQ2LWFmcmljYQ==
        sf2 = "assets/soundfonts/africa.sf2"
        self.fs = fs.Synth(gain=1.0)
        self.sfid = self.fs.sfload(sf2)
        self.fs.start()

        # self.sf = fluidsynth.init("africa.sf2")
        self.instrument = config['midi']['instrument']
        self.fs.program_select(1, self.sfid, 0, self.instrument)
        # self.fs.

        self.fs_is_playing = 0

        # midi vars
        self.compass = "N"
        self.octave = 4
        self.dynamic = 100
        self.add_accidental = 0

        # release vars
        self.rb_val = 0
        self.rt_val = 0
        self.rb_release = False
        self.rt_release = False

        # neoscore vars
        self.neopitch = None

    def get_data(self, joystick,
                 arrow_help,
                 name_help
                 ):
        """
        Parses the data from the joystick object.
        calculates the note values. Makes a sound

        :param joystick: object
        :return:
        """
        # reset vars
        self.compass = ""
        self.add_accidental = 0
        rb = 0
        rt = 0
        self.A_button = 0
        self.B_button = 0
        self.X_button = 0
        self.Y_button = 0

        # reset dictionaries
        axis_dict = {"0": 0.0,
                     "1": 0.0,
                     "2": 0.0,
                     "3": 0.0,
                     "4": 0.0,
                     "5": 0.0,
                     }
        button_dict = {"0": 0,
                       "1": 0,
                       "2": 0,
                       "3": 0,
                       "4": 0,
                       "5": 0,
                       "6": 0,
                       "7": 0,
                       "8": 0,
                       "9": 0,
                       }

        #######################
        # Get data from joystick
        #######################

        # get name
        name = joystick.get_name()

        # grab events from joystick
        buttons = joystick.get_numbuttons()
        for i in range(buttons):
            button = joystick.get_button(i)
            if button == 1:
                button_dict.update({str(i): button})

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        for i in range(axes):
            axis = joystick.get_axis(i)
            axis_dict.update({str(i): axis})

        #######################
        # Which Platform/ Joystick
        #######################

        # todo - come up with a better solution for this.
        # Accidental b or #
        if platform.system() == 'Windows' and name == "Logitech Dual Action":
            sharp = button_dict.get("4")
            flat = button_dict.get("6")
            octave_up = button_dict.get("5")
            octave_down = button_dict.get("7")
            north_south = axis_dict.get("3")
            east_west = axis_dict.get("2")
            volume = axis_dict.get("1")
            reset_octave = button_dict.get("10")

        elif (platform.system() == 'Darwin' or platform.system() == "Linux") and name == "Logitech Dual Action":
            sharp = button_dict.get("4")
            flat = axis_dict.get("2")
            octave_up = button_dict.get("5")
            octave_down = axis_dict.get("5")
            north_south = axis_dict.get("4")
            east_west = axis_dict.get("3")
            volume = axis_dict.get("1")
            reset_octave = button_dict.get("6")

        elif name == "Sony Interactive Entertainment Access Controller":
            sharp = button_dict.get("5")
            flat = button_dict.get("4")
            octave_up = button_dict.get("0")
            octave_down = button_dict.get("6")
            north_south = (axis_dict.get("1")) #  * -1
            east_west = (axis_dict.get("0")) #  * -1
            volume = 0  # button_dict.get("1")
            reset_octave = button_dict.get("1")

        else: # dummy controller for testing
            sharp = button_dict.get("5")
            flat = button_dict.get("4")
            octave_up = button_dict.get("0")
            octave_down = button_dict.get("6")
            north_south = (axis_dict.get("1")) #  * -1
            east_west = (axis_dict.get("0")) #  * -1
            volume = 0  # button_dict.get("1")
            reset_octave = button_dict.get("1")

        #######################
        # Buttons
        #######################

        if sharp >= 0.9:
            self.add_accidental = 1
        elif flat >= 0.9:
            self.add_accidental = -1

        # Calculate octave shift

        if octave_up >= 0.9:
            # self.octave += 1
            rb = 1
        elif octave_down >= 0.9:
            # self.octave -= 1
            rt = 1

        # PS buttons
        if button_dict["0"] == 1.0:
            self.A_button = True
        if button_dict["1"] == 1.0:
            self.B_button = True
        if button_dict["2"] == 1.0:
            self.X_button = True
        if button_dict["3"] == 1.0:
            self.Y_button = True

        #######################
        # Joysticks
        #######################

        # Calculate note joystick position for notes
        if north_south < -self.joystick_active_range:
            self.compass = "N"
        elif north_south >= self.joystick_active_range:
            self.compass = "S"
        elif east_west < -self.joystick_active_range:
            self.compass = "W"
        elif east_west >= self.joystick_active_range:
            self.compass = "E"

        elif north_south < -0.4 and east_west > 0.4:
            self.compass = "NE"
        elif north_south < -0.4 and east_west < -0.4:
            self.compass = "NW"
        elif north_south > 0.4 and east_west > 0.4:
            self.compass = "SE"
        elif north_south > 0.4 and east_west < -0.4:
            self.compass = "SW"

        #######################
        # Dynamics
        #######################

        dyn_axis_value = round(volume, 2)
        # round(dyn_axis_value, 2)
        if dyn_axis_value == 0:
            self.dynamic = 100

        # value < 0 increase volume up to 127
        elif dyn_axis_value < 0:
            # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
            self.dynamic = int((((dyn_axis_value - 0) * (127 - 100)) / (-1 - 0)) + 100)
        # value > 0 ->1 then scale between 0 and 100
        elif dyn_axis_value > 0:
            # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
            self.dynamic = int((((dyn_axis_value - 0) * (0 - 100)) / (1 - 0)) + 100)

        #
        # texture_axis_value = axis_dict["0"]
        # if texture_axis_value > 0.1:
        #     round(texture_axis_value, 2)
        #     # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
        #     self.dynamic = int((((texture_axis_value - -1) * (20 - 120)) / (1 - -1)) + 120)

        #######################
        # Octave
        #######################

        # check release of rb and rt
        if rb < self.rb_val:
            self.rb_release = True
            self.rb_val = rb
        else:
            self.rb_val = rb
            self.rb_release = False

        if rt < self.rt_val:
            self.rt_release = True
            self.rt_val = rt
        else:
            self.rt_val = rt
            self.rt_release = False

        # Calculate octave shift
        # if self.rb_release and self.rt_release:
        #     self.octave = 4
        if self.rb_release:  # RB
            self.octave += 1
        elif self.rt_release:  # RT
            self.octave += -1

        # reset octave to 4
        if reset_octave == 1.0:
            self.octave = 4

        # check octave range
        if self.octave <= 3:
            self.octave = 3
        elif self.octave > 5:
            self.octave = 5

        #######################
        # Sound
        #######################

        # make a sound or not
        if self.compass == "":
            # send a stop to the FS player
            if self.fs_is_playing != 0:
                self.stop_note(self.fs_is_playing)
                self.fs_is_playing = 0
            # reset CC volume
            self.fs.cc(1, 7, 100)
            self.neopitch = ""
        else:
            # get current octave
            octave = self.octave

            # match compass to notes
            match self.compass:
                case 'S':
                    note = 'C'
                case 'SE':
                    note = 'E'
                case 'E':
                    note = 'G'
                case 'NE':
                    note = 'B'
                case 'N':
                    note = 'C'
                    octave = self.octave + 1
                case 'NW':
                    note = 'A'
                case 'W':
                    note = 'F'
                case 'SW':
                    note = 'D'

            # print(note)
            # adjust note for enharmonic shift
            match self.add_accidental:
                case 1:
                    note = f"{note}#"
                case -1:
                    note = f"{note}b"

            # make fs style note str
            fs_note = f"{note}-{octave + 1}"

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

            #######################
            # Notation
            #######################

            # make into neoscore note value
            if note[-1] == "#":
                self.neopitch = f"{note[0].lower()}#"
            elif note[-1] == "b":
                self.neopitch = f"{note[0].lower()}b"
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
                elif octave == 1:
                    self.neopitch += ",,,"
                elif octave == 0:
                    self.neopitch += ",,,,"

            note_filename = self.neopitch + self.compass
            if arrow_help:
                note_filename += "_arrow"
            if name_help:
                note_filename += "_name"
            note_filename += ".png"

            self.note_to_show = note_filename

    def make_sound(self,
                   new_note,
                   dynamic,
                   ):
        self.fs.noteon(1, key=int(Note(new_note)), vel=dynamic)

    def stop_note(self, note_to_stop):
        self.fs.noteoff(1, key=int(Note(note_to_stop)))


if __name__ == "__main__":
    js = Joystick()
