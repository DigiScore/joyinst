from neoscore.common import *
from enum import Enum

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


pos_offset_x = 10

note = "gb'"
arrow_help = True
name_help = True

compass = 'NW'

neoscore.setup()

# make a new note and save
empty_staff = Staff(ORIGIN, None, Mm(300), line_spacing=Mm(5))
clef = Clef(Mm(80), empty_staff, 'treble')

n = Chordrest(Mm(150),
              empty_staff,
              [note],
              Duration(1, 2))

# add to existing note list


if arrow_help:
    arrow_direction = Arrow[compass].value
    arrow_colour = Colour[compass].value
    colour_brush = Brush(color=arrow_colour)
    help_arrow = MusicText((Mm(120), Mm(-35)), clef, arrow_direction,
                           alignment_x=AlignmentX.CENTER, alignment_y=AlignmentY.CENTER,
                           brush=colour_brush, scale=2
                           )

if name_help:
    upper_note = note[0].upper() + note[1:]
    help_text = Text((Mm(25), Mm(-20)), clef, upper_note,
                     # alignment_x=AlignmentX.CENTER,
                     # alignment_y=AlignmentY.CENTER,
                     scale=3
                     )

neoscore.show(display_page_geometry=False)

# save_dest = "../machainst/assets/ui/images/empty_staves/empty_treble.png"
# neoscore.render_image(rect=None,
#                       dest=save_dest,
#                       autocrop=True,
#                       preserve_alpha=True,
#                       wait=True
#                       )
# print(f"Saving new image to {save_dest}")