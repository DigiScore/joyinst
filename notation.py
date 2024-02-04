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
    Inspired by Arrow notes concept
    https://digitlearning.co.uk/what-are-arrownotes/
    follows the rainbow from South (lower notes) -> North (higher)

    c = red N or S
    b = violet SE
    a = indigo SW
    g = blue E
    f = green W
    e = yellow NE
    d = orange NW
    c = red N or S

    """
    N = '#e81416'
    NE = '#70369d'
    NW = '#4b369d'
    W = '#79c314'
    E = '#487de7'
    SE = '#faeb36'
    SW = '#ffa500'
    S = '#e81416'

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

        # # make a blank note
        # self.n1 = None

        # save path
        self.save_path = "media/generated_notes/"

        # compile a list of generated png's to optimise any duplications
        self.notelist = os.listdir(self.save_path)

    def make_notation(self, notes: list,
                      compass: str,
                      arrow_help: bool = True,
                      name_help: bool = True
                      ) -> str:
        """
        Makes a new neoscore note on stave with option help indications of arrow and name

        :param notes: list of notes to put on stave
        :param compass: compass direction for mapping to arrow glyph and colour

        :return: path to created neoscore glyph
        """

        # setup an empty list for removal later
        list_of_objects = []

        # iterate through note list
        for i, note in enumerate(notes):
            # move position along for each note
            pos_offset_x = i * 10

            # make a new note name to build extra help factors
            note_filename = note
            if arrow_help:
                note_filename += "_arrow"
            if name_help:
                note_filename += "_name"
            note_filename += ".png"

            if note_filename in self.notelist:
                self.note_to_show = note_filename

            else:
                # make a new note and save
                empty_staff = Staff(ORIGIN, None, Mm(200), line_spacing=Mm(5))
                Clef(Mm(60), empty_staff, 'treble')

                n = Chordrest(Mm(100 + (pos_offset_x + 10)),
                               empty_staff,
                               [note],
                               Duration(1, 2))
                # add to existing note list
                list_of_objects.append(n)

                if arrow_help:
                    arrow_direction = Arrow[compass].value
                    arrow_colour = Colour[compass].value
                    colour_brush = Brush(color=arrow_colour)
                    help_arrow = MusicText((Mm(20), Mm(-20)), n, arrow_direction,
                                         alignment_x=AlignmentX.CENTER, alignment_y=AlignmentY.CENTER,
                                         brush=colour_brush,
                                           scale=2
                                         )
                    list_of_objects.append(help_arrow)
                    # note_filename = note_filename # + "_arrow"

                if name_help:
                    help_text = Text((Mm(-20), Mm(-15)), n, note,
                         alignment_x=AlignmentX.CENTER,
                         alignment_y=AlignmentY.CENTER,
                                     scale=4
                         )
                    list_of_objects.append(help_text)
                    # note_filename = note_filename # + "_name"

                # add new image to note list
                self.notelist.append(note_filename)

                # render new image
                # note_filename = note_filename + ".png"
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

                # delete them all
                for o in list_of_objects:
                    # print(o)
                    o.remove()

        return note_filename


if __name__ == "__main__":
    test = Notation()
