from neoscore.common import *


class Notation:
    """Builds all the notation images for the game"""

    def __init__(self):
        # init neoscore
        neoscore.setup()

        # note to print
        self.note_to_show = 'media/empty_staves/empty_treble.png'

        # compile a list of generated png's to optimise any duplications
        self.notelist = []


    # def make_notation(self, notes: list):
    #     # iterate through note list
    #     for i, n in enumerate(notes):
    #         if n in self.notelist:
    #
    #
    #     # if note is on notelist render that
    #     for
    #
    #
    #     empty_staff = Staff(ORIGIN, None, Mm(50), line_spacing=Mm(5))
    #     Clef(ZERO, empty_staff, 'treble')
    #
    #
    #
    #
    #         note = Chordrest(empty_staff.unit(10),
    #                      empty_staff,
    #                      [note],
    #                      Duration(1, 2))
    #         # else grab from note list
    #         # else:
    #
    #     neoscore.render_image(rect=None,
    #                           dest="media/empty_staves/empty_treble.png",
    #                           autocrop=True,
    #                           preserve_alpha=False
    #                           )




if __name__ == "__main__":
    test = Notation()
