from neoscore.common import *
from enum import Enum
import os



class Arrow(Enum):
    """
    Smufl Arrows
    https://w3c.github.io/smufl/latest/tables/arrows-and-arrowheads.html
    N U+EB68 arrowWhiteUp
    NW U+EB6F arrowWhiteUpLeft
    NE U+EB69 arrowWhiteUpRight
    W U+EB6E arrowWhiteLeft
    E U+EB6A arrowWhiteRight
    SW U+EB6D arrowWhiteDownLeft
    SE U+EB6B arrowWhiteDownRight
    S U+EB6C arrowWhiteDown
    """
    N = 'arrowBlackUp'
    NW = 'arrowBlackUpLeft'
    NE = 'arrowBlackUpRight'
    W = 'arrowBlackLeft'
    E = 'arrowBlackRight'
    SW = 'arrowBlackDownLeft'
    SE = 'arrowBlackDownRight'
    S = 'arrowBlackDown'

class Colour(Enum):
    """
    Arrow notes COLOURS
    https://digitlearning.co.uk/what-are-arrownotes/

    c = red N or S
    d = orange NW
    e = yellow NE
    f = light green W
    g = dark green E
    a = purple SW
    b = pink SE
    c = red N or S
    """
    N = '#FF0000'
    NW = '#ffa500'
    NE = '#FFFF00'
    W = '#00FF00'
    E = '#006400'
    SW = '#800080'
    SE = '#FF00FF'
    S = '#FF0000'

class Solfa(Enum):
    """
    Sol Fa translation of compass points
    to do, re, mi, fa, sol, la, ti, do.
    Flats and sharps COULD be represented by 'a' and 'e'
    or simply 'b' and '#'
    """
    # todo - flats and sharps
    N = 'do'
    NW = 're'
    NE = 'mi'
    W = 'fa'
    E = 'sol'
    SW = 'la'
    SE = 'ti'
    S = 'do'


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
