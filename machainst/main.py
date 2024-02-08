# import python libraries
from enum import Enum
import pygame as pg
import pygame.font
import pygame_widgets
from pygame_widgets.dropdown import Dropdown
from threading import Thread
from time import sleep

# import project modules
from joystick import Joystick
from game import Game
from constants.user_interface import Colors, WindowSize


class TextPrint(object):
    """
    This is a simple class that will help us print to the screen
    It has nothing to do with the joysticks, just outputting the
    information.
    """

    def __init__(self):
        self.reset()
        self.x_pos = 10
        self.y_pos = 10
        self.font = pg.font.Font(None, 20)

    def print(self, my_screen, text_string):
        """ Draw text onto the screen. """
        text_bitmap = self.font.render(text_string, True, Colors.BLACK.value)
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
    Inspired by Figure Notes
    https://figurenotes.org/what-is-figurenotes/

    And Arrow notes concept
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


class UI(Joystick, Game):
    """Main class for running UI. Inherits the joystick and instrument objects"""

    # todo - transpositions!!! this is in C only. Tonic & position & arrows
    #  needs to be related to parent key.

    def __init__(self,
                 playing_game: bool = True,
                 smoothing: int = 300
                 ):
        super().__init__()
        pg.init()

        # Set the width and depth of the screen [width,depth]
        size = [WindowSize.WIDTH, WindowSize.HEIGHT]

        # ui images
        self.ui_background_dots = pg.image.load("assets/ui/images/bg_dots.svg")
        self.ui_background_character = pg.image.load("assets/ui/images/bg_character.png")

        # font
        self.ibm_plex_condensed_font = pygame.font.Font("assets/ui/fonts/IBMPlexSansCondensed-Medium.ttf", 22)

        # set game params
        self.playing_game = playing_game
        self.game_note_path = 0

        self.screen = pg.display.set_mode(size)

        pg.display.set_caption("machAInst")

        # Used to manage how fast the screen updates
        self.clock = pg.time.Clock()

        # Initialize the joysticks
        pg.joystick.init()

        # make dropdown menu for instrument choice
        self.dropdown = Dropdown(
            self.screen, 1126, 76, 385, 50, name='     SELECT INSTRUMENT',
            choices=[
                "     VOCALS/FX's",
                '     HMMM',
                '     MOOG',
                '     HI PAD SLIDE A',
                '     TOM SLIDER C&A',
                '     LO PAD SLIDE A',
                '     SHOFARS',
                '     KALIMBA',
                '     FLUTE W WARBLE',
                '     FLUTE W BLOW',
                '     BASS',
            ],
            colour=Colors.DROPDOWN.value,
            hoverColour=Colors.DROPDOWN_HOVER.value,
            pressedColour=Colors.DROPDOWN_HOVER.value,
            values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            direction='down',
            textHAlign='left',
            font=self.ibm_plex_condensed_font
        )

        # setup inst & notation vars
        self.inst = self.instrument
        self.path_to_generated_images = "assets/ui/images/generated_notes/"

        # event vars
        self.last_guess = pg.time.get_ticks()
        self.smoothing = smoothing

    def mainloop(self):
        # Get ready to print
        text_print = TextPrint()

        # init vars
        done = False
        button_down = False  # might be useful later on

        while not done:
            # EVENT PROCESSING STEP
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    done = True

                # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN
                # JOYBUTTONUP JOYHATMOTION
                if event.type == pg.JOYBUTTONDOWN:
                    button_down = True
                    # print("Joystick button pressed.")
                if event.type == pg.JOYBUTTONUP:
                    # print("Joystick button released.")
                    button_down = False
                # if event.type == pg.JOYAXISMOTION:
                #     print("Joystick axis motion.")

            # Get instrument choice
            if self.dropdown.getSelected():
                self.inst = self.dropdown.getSelected()
                self.fs.program_select(1, self.sfid, 0, self.inst)

            # DRAWING STEP
            # First, clear the screen. Don't put other drawing commands
            self.screen.fill(Colors.BACKGROUND.value)
            text_print.reset()

            # Get count of joysticks
            joystick_count = pg.joystick.get_count()

            # todo - this is a hack, to get around issue with Logitech gamepad
            # For each joystick:
            for i in range(joystick_count):
                joystick = pg.joystick.Joystick(i)
                joystick.init()
                # # Get the joystick data
                # joystick = pg.joystick.Joystick(0)
                # joystick.init()

                # Parse data with Joystick class
                self.get_data(joystick,
                              self.arrow_help,
                              self.name_help
                              )

                text_print.print(self.screen, "Compass")
                text_print.print(self.screen, "arrow_direction")
                text_print.print(self.screen, "arrow_colour")
                text_print.print(self.screen, "note")
                text_print.print(self.screen, "solfa")
                text_print.print(self.screen, "level    {}".format(self.level))
                text_print.print(self.screen, "sub-level    {}".format(self.sub_level))
                text_print.print(self.screen, "goes at sub level    {}".format(self.sub_level_rounds))
                text_print.print(self.screen, "guesses    {}".format(self.tries))
                text_print.print(self.screen, "lives    {}".format(self.lives))

                #############
                # JOYSTICK LOOP
                #############

                if self.compass:
                    # make arrow
                    compass = self.compass
                    arrow_direction = Arrow[compass].value
                    arrow_colour = Colour[compass].value

                    # make solfa
                    solfa = Solfa[compass].value

                    # print to screen
                    self.screen.fill(Colors.BACKGROUND.value)
                    text_print.reset()

                    text_print.print(self.screen, "Compass    {}".format(compass))
                    text_print.print(self.screen, "arrow_direction    {}".format(arrow_direction))
                    text_print.print(self.screen, "arrow_colour   {}".format(arrow_colour))
                    text_print.print(self.screen, "note   {}".format(self.neopitch))
                    text_print.print(self.screen, "solfa  {}".format(solfa))
                    text_print.print(self.screen, "level    {}".format(self.level))
                    text_print.print(self.screen, "sub-level    {}".format(self.sub_level))
                    text_print.print(self.screen, "goes at sub level    {}".format(self.sub_level_rounds))
                    text_print.print(self.screen, "guesses    {}".format(self.tries))
                    text_print.print(self.screen, "lives    {}".format(self.lives))

                    # freeze guess on screen if game_lock
                    # if not self.game_lock:
                    note_to_show = self.note_to_show

                    path_to_new_image = self.path_to_generated_images + note_to_show
                    self.show_note(path_to_new_image)

                    #############
                    # GAME GUESS
                    #############

                    if self.playing_game:
                        if not self.game_lock:
                            if joystick.get_axis(3) or joystick.get_axis(4):
                                now = pg.time.get_ticks()
                                if now - self.last_guess >= self.smoothing:
                                    # reset the smoothing
                                    self.last_guess = now
                                    print("guessed note = ", self.compass)

                                    # lock the game loop to avoide multiple answers
                                    self.game_lock = True

                                    # run game loop
                                    gl_thread = Thread(target=self.game_loop)
                                    gl_thread.start()

                else:
                    # put empty stave on screen
                    path_to_new_image = 'assets/ui/images/empty_staves/empty_treble.png'
                    self.show_note(path_to_new_image)

                #############
                # GAME IMAGE
                #############

                # if there is joystick movement (self.compass), and playing game
                if self.playing_game:
                    if not self.first_note:
                        self.game_note_path = self.first_game_note()
                        self.first_note = True

                else:
                    # if not playing put empty game stave on screen
                    self.game_note_path = 'assets/ui/images/empty_staves/empty_treble.png'

                self.show_game_note(self.game_note_path)

                # Go ahead and update the screen with what we've drawn.
                self.screen.blit(self.ui_background_dots, (0, 0))
                self.screen.blit(self.ui_background_character, (0, 164))
                pygame_widgets.update(events)
                pg.display.flip()
                # Limit to 60 frames per second
                self.clock.tick(60)

    def first_game_note(self):
        # put first game image on screen
        # get a new note from current list
        self._game_new_note = self.get_random_note()
        print(self._game_new_note)
        note_to_show = self.make_game_note_notation(self._game_new_note)
        # print(note_to_show)
        game_note_path = self.path_to_generated_images + note_to_show
        return game_note_path
        # self.show_game_note(self.game_note_path)

    def game_loop(self):
        # todo - this is a verbose sequence - we can optimise later
        # check if current note matches. Lock so as not to repeat comparisons

        result = self.check_notes_match(self.neopitch)
        print("guess result = ", result)
        sleep(0.5)

        # blank the game staff
        previous_game_note_path = self.game_note_path
        self.game_note_path = 'assets/ui/images/empty_staves/empty_treble.png'

        # update game status depending on result
        self.update_game_states(result)
        print("\t\tchecking game stats")
        # print("\t\tlevel = ", self.level)
        # print("\t\tsub-level = ", self.sub_level)
        # print("\t\tgoes at sub level = ", self.sub_level_rounds)
        # print("\t\tguesses = ", self.tries)
        # print("\t\tlives = ", self.lives)
        sleep(0.5)

        # update visual helpers on the note
        self.check_helpers()
        print("adjusting helpers")
        sleep(0.5)

        # if correct guess
        if result:
            print("Picking new note")
            sleep(0.5)
            # get a new note from current list
            self._game_new_note = self.get_random_note()
            note_to_show = self.make_game_note_notation(self._game_new_note)
            self.game_note_path = self.path_to_generated_images + note_to_show

        # false guess
        else:
            print("RETRY")
            sleep(0.5)
            # show same note with adjusted helps?
            note_to_show = self.make_game_note_notation(self._game_new_note)
            self.game_note_path = self.path_to_generated_images + note_to_show

        self.game_lock = False

    def show_note(self, path_to_new_image):
        note = pg.image.load(path_to_new_image).convert_alpha()
        note = pg.transform.scale_by(note, 0.3)
        # Create a rect with the size of the image.
        rect = note.get_rect()
        rect.center = (WindowSize.WIDTH / 2, (WindowSize.HEIGHT / 2) - 100)
        self.screen.blit(note, rect)

    def show_game_note(self, path_to_new_image):
        note = pg.image.load(path_to_new_image).convert_alpha()
        note = pg.transform.scale_by(note, 0.3)
        # Create a rect with the size of the image.
        rect = note.get_rect()
        rect.center = (WindowSize.WIDTH / 2, (WindowSize.HEIGHT / 2) + 150)
        self.screen.blit(note, rect)


if __name__ == "__main__":
    ui = UI(playing_game=True,
            smoothing=500
            )
    ui.mainloop()
