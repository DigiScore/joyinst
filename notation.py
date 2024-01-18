from neoscore.common import *
from glob import glob
import os

class Notation:
    """Builds all the notation images for the game"""

    def __init__(self):
        # init neoscore
        neoscore.setup()

        # note to print
        self.note_to_show = None

        # make a blank note
        self.n1 = None

        # save path
        self.save_path = "media/generated_notes/"

        # compile a list of generated png's to optimise any duplications
        self.notelist = os.listdir(self.save_path)

    def make_notation(self, notes: list):
        # iterate through note list
        for i, note in enumerate(notes):
            note_filename = note + ".png"
            if note_filename in self.notelist:
                self.note_to_show = note_filename
            else:
                # make a new note and save
                empty_staff = Staff(ORIGIN, None, Mm(50), line_spacing=Mm(5))
                Clef(ZERO, empty_staff, 'treble')

                self.n1 = Chordrest(Mm(10),
                               empty_staff,
                               [note],
                               Duration(1, 2))
                # add to existing note list
                self.notelist.append(note_filename)

                # render new image
                save_dest = self.save_path + note_filename
                neoscore.render_image(rect=None,
                                      dest=save_dest,
                                      autocrop=True,
                                      preserve_alpha=False,
                                      wait=True
                                      )
                print(f"Saving new image to {save_dest}")
                # hand name back to mainloop
                self.note_to_show = note_filename
                self.n1.remove()


if __name__ == "__main__":
    test = Notation()
