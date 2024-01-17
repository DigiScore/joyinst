from mingus.containers import Note, NoteContainer, Bar, Track
from mingus.midi import pyfluidsynth as fs
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read('config.ini') 


class Joystick:
    """
    Manages the data from the joystick controls.
    Calculates the note values and makes a sound.
    """
    def __init__(self):
        # Instantiate the vars
        self.sensitivity = 20
        self.joystick_active_range = 0.8

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

        sf2 = "africa.sf2"
        self.fs = fs.Synth()
        self.sfid = self.fs.sfload(sf2)
        self.fs.start()

        # self.sf = fluidsynth.init("africa.sf2")
        self.instrument = config_object['MIDI'].getint('instrument')
        self.fs.program_select(1, self.sfid, 0, self.instrument)


        # self.sf.set_instrument(1, self.instrument)
        # self.sf.main_volume(1, 100) #  set volume control (7) to 70
        # self.sf.modulation(1, 0)  # set modulation wheel to 0
        # if self.instrument == 74 or self.instrument == 110:
        #     self.sf.control_change(1, 5, 100)
        self.fs_is_playing = 0

        # midi vars
        self.compass = ""
        self.octave = 5
        self.dynamic = 70
        self.add_accidental = 0

        # release vars
        self.rb_val = 0
        self.rt_val = 0
        self.rb_release = False
        self.rt_release = False

        # neoscore vars
        self.neopitch = None

    def get_data(self, joystick):
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

        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()

        # Calc # or b using buttons 4 & 5
        buttons = joystick.get_numbuttons()
        for i in range(buttons):
            button = joystick.get_button(i)

            # Accidental b or #
            if i == 4 and button == 1:
                self.add_accidental = 1
            if i == 5 and button == 1:
                self.add_accidental = -1

            # Calculate octave shift
            if i == 6 and button == 1:
                # self.octave += 1
                rb = 1
            elif i == 7 and button == 1:
                # self.octave -= 1
                rt = 1

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()

        for i in range(axes):
            axis = joystick.get_axis(i)

            # Calculate note joystick position for notes
            if i == 2 and axis < -self.joystick_active_range:
                self.compass += "N"
            elif i == 2 and axis >= self.joystick_active_range:
                self.compass += "S"

            if i == 3 and axis < -self.joystick_active_range:
                self.compass += "W"
            elif i == 3 and axis >= self.joystick_active_range:
                self.compass += "E"

            # todo - Calculate dynamic joystick for dynamics
            if i == 1:
                round(axis, 2)
                # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
                self.dynamic = (((axis - -1) * (20 - 120)) / (1 - -1)) + 120
                # print(self.dynamic)

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
            if self.rb_release and self.rt_release:
                self.octave = 5
            elif self.rb_release:  # RB
                self.octave += 1
            elif self.rt_release:  # RT
                self.octave += -1

            if self.octave < 0:
                self.octave = 0
            elif self.octave > 8:
                self.octave = 8

            # print(f" rb = {rb}, self.rb_val = {self.rb_val}; octave = {self.octave}")

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

            # print(note)
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

        # self.fs.(Note(new_note,
        #                           velocity=dynamic
        #                           )
        #                      )
        self.fs.noteon(1, key=new_note, vel=dynamic)

    def stop_note(self, note_to_stop):
        # self.sf.stop_Note(Note(note_to_stop))
        self.fs.noteoff(1, key=note_to_stop)

if __name__ == "__main__":
    js = Joystick()
