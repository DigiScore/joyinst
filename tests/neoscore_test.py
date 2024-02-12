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
    b = green NE
    a = yellow NW
    g = black E
    f = Blue W
    e = grey SE
    d = brown SW
    c = red N or S

    """
    N = '#ff0000'
    NE = '#33cc33'
    NW = '#ffff66'
    W = '#0099ff'
    E = '#000000'
    SE = '#d9d9d9'
    SW = '#996633'
    S = '#ff0000'

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

def change_all_chordrest_colors(cr: Chordrest):
    """Change the colors of all Chordrest component objects.

    This does not change any attached beams.
    """

    for notehead in cr.noteheads:
        notehead.brush = Brush.from_existing(notehead.brush, color)
    for accidental in cr.accidentals:
        accidental.brush = Brush.from_existing(accidental.brush, color)
    for ledger in cr.ledgers:
        ledger.pen = Pen.from_existing(ledger.pen, color=color)
    for dot in cr.dots:
        dot.brush = Brush.from_existing(ledger.brush, color)
    if cr.stem:
        cr.stem.pen = Pen.from_existing(cr.stem.pen, color=color)
    if cr.flag:
        cr.flag.brush = Brush.from_existing(cr.flag.brush, color)
    if cr.rest:
        cr.rest.brush = Brush.from_existing(cr.rest.brush, color)

pos_offset_x = 10

note = "gn'"
arrow_help = True
name_help = True

compass = 'W'

neoscore.setup()
neoscore.set_background_brush(Brush("#0000"))
color = "#FFF"  # make everthing white

# make a new note and save
empty_staff = Staff((Mm(10), Mm(100)), None, Mm(400), line_spacing=Mm(5), pen=Pen(color))
clef = Clef(Mm(150), empty_staff, 'treble', pen=Pen(color), brush=Brush(color))
#
# n = Chordrest(Mm(200),
#               empty_staff,
#               [note],
#               Duration(1, 2))
#
# change_all_chordrest_colors(n)
#
#
# if arrow_help:
#     arrow_direction = Arrow[compass].value
#     arrow_colour = Colour[compass].value
#     colour_brush = Brush(color=arrow_colour)
#     if compass == "E":
#         pen = Pen(color=color, thickness=Mm(0.5))
#     else:
#         pen = Pen(color=arrow_colour)
#     help_arrow = MusicText((Mm(85), Mm(-35)), clef, arrow_direction,
#                            alignment_x=AlignmentX.CENTER, alignment_y=AlignmentY.CENTER,
#                            brush=colour_brush,
#                            pen=pen,
#                            scale=2
#                            )
#
# if name_help:
#     upper_note = note[0].upper() + note[1:]
#     help_text = Text((Mm(10), Mm(-25)), clef, upper_note,
#                      brush=Brush(color), pen=Pen(color),
#                      # alignment_x=AlignmentX.CENTER,
#                      # alignment_y=AlignmentY.CENTER,
#                      scale=3
#                      )

# neoscore.show(display_page_geometry=False)

save_dest = "../machainst/assets/ui/images/empty_staves/empty_treble.png"
neoscore.render_image(rect=(ZERO, ZERO, Mm(420), Mm(200)),
                      dest=save_dest,
                      autocrop=False,
                      preserve_alpha=True,
                      wait=True
                      )
print(f"Saving new image to {save_dest}")