from joystick import Joystick
from enum import Enum
import pygame
import pygame_widgets
from pygame_widgets.dropdown import Dropdown
import os

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class TextPrint(object):
    """
    This is a simple class that will help us print to the screen
    It has nothing to do with the joysticks, just outputting the
    information.
    """

    def __init__(self):
        """ Constructor """
        self.reset()
        self.x_pos = 10
        self.y_pos = 10
        self.font = pygame.font.Font(None, 20)

    def print(self, my_screen, text_string):
        """ Draw text onto the screen. """
        text_bitmap = self.font.render(text_string, True, BLACK)
        my_screen.blit(text_bitmap, [self.x_pos, self.y_pos])
        self.y_pos += self.line_height

    def reset(self):
        """ Reset text to the top of the screen. """
        self.x_pos = 10
        self.y_pos = 10
        self.line_height = 15

    def indent(self):
        """ Indent the next line of text """
        self.x_pos += 10

    def unindent(self):
        """ Unindent the next line of text """
        self.x_pos -= 10


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


class UI(Joystick):
    """Main class for running UI. Inherits the joystick and instrument objects"""
    # todo - transpositions!!! this is in C only. Tonic & position & arrows
    #  needs to be related to parent key.

    def __init__(self):
        super().__init__()
        pygame.init()

        # Set the width and depth of the screen [width,depth]
        self.WIDTH = 500
        self.DEPTH = 750
        size = [self.WIDTH, self.DEPTH]

        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("MachAInst - basic output")

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

        # Initialize the joysticks
        pygame.joystick.init()

        # make dropdown menu for instrument choice
        self.dropdown = Dropdown(
            self.screen, 120, 120, 150, 50, name='Select Instrument',
            choices=[
                "Vocals/FX's",
                'Hmmm',
                'Moog',
                'Hi Pad slide A',
                'Tom slider C&A',
                'Lo Pad slide A',
                'Shofars',
                'Kalimba',
                'Flute w warble',
                'Flute w blow',
                'Bass',
            ],
            borderRadius=3,
            colour=pygame.Color('green'),
            values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            direction='down',
            textHAlign='left'
        )
        # setup inst & notation vars
        self.inst = self.instrument
        self.path_to_generated_images = "media/generated_notes/"


    def mainloop(self):
        # Get ready to print
        textPrint = TextPrint()

        # init vars
        done = False
        button_down = False # might be useful later on

        while not done:
            # EVENT PROCESSING STEP
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    done = True

                # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN
                # JOYBUTTONUP JOYHATMOTION
                if event.type == pygame.JOYBUTTONDOWN:
                    button_down = True
                    print("Joystick button pressed.")
                if event.type == pygame.JOYBUTTONUP:
                    print("Joystick button released.")
                    button_down = False
                # if event.type == pygame.JOYAXISMOTION:
                #     print("Joystick axis motion.")

            # Get instrument choice
            if self.dropdown.getSelected():
                self.inst = self.dropdown.getSelected()
                self.fs.program_select(1, self.sfid, 0, self.inst)

            # DRAWING STEP
            # First, clear the screen to white. Don't put other drawing commands
            self.screen.fill(WHITE)
            textPrint.reset()

            # Get the joystick data
            joystick = pygame.joystick.Joystick(0)
            joystick.init()

            # Parse data with Joystick class
            self.get_data(joystick)

            textPrint.print(self.screen, "Compass")
            textPrint.print(self.screen, "arrow_direction")
            textPrint.print(self.screen, "arrow_colour")
            textPrint.print(self.screen, "note ")
            textPrint.print(self.screen, "solfa ")

            if self.compass:
                # make arrow
                compass = self.compass
                arrow_direction = Arrow[compass].value
                arrow_colour = Colour[compass].value

                # make solfa
                solfa = Solfa[compass].value

                # print to screen
                self.screen.fill(WHITE)
                textPrint.reset()

                textPrint.print(self.screen, "Compass    {}".format(compass))
                textPrint.print(self.screen, "arrow_direction    {}".format(arrow_direction))
                textPrint.print(self.screen, "arrow_colour   {}".format(arrow_colour))
                textPrint.print(self.screen, "note   {}".format(self.neopitch))
                textPrint.print(self.screen, "solfa  {}".format(solfa))

                # put note image on screen
                note_to_show = self.note_to_show
                path_to_new_image = self.path_to_generated_images + note_to_show
                self.show_note(path_to_new_image)

            else:
                # put empty stave on screen
                path_to_new_image = 'media/empty_staves/empty_treble.png'
                self.show_note(path_to_new_image)

            # Go ahead and update the screen with what we've drawn.
            pygame_widgets.update(events)
            pygame.display.update()
            # Limit to 60 frames per second
            self.clock.tick(60)

    def show_note(self, path_to_new_image):
        # print(path_to_new_image)
        note = pygame.image.load(path_to_new_image).convert_alpha()
        note = pygame.transform.scale(note, (200, 100))
        # Create a rect with the size of the image.
        rect = note.get_rect()
        rect.center = (self.WIDTH / 2, self.DEPTH / 2)
        self.screen.blit(note, rect)


if __name__ == "__main__":
    ui = UI()
    ui.mainloop()
