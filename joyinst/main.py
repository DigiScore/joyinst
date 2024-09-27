# import python libraries
import tomllib
from enum import Enum
import pygame as pg
import pygame.font
import pygame_widgets
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
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
        # self.font = pg.font.Font(None, 60)
        self.font = pg.font.Font("assets/ui/fonts/IBMPlexSansCondensed-Medium.ttf", 28)

    def print(self, my_screen, text_string):
        """ Draw text onto the screen. """
        text_bitmap = self.font.render(text_string, True, Colors.BLACK.value)
        my_screen.blit(text_bitmap, [self.x_pos, self.y_pos])
        self.y_pos += self.line_height

    def reset(self):
        """ Reset text to the top of the screen. """
        self.x_pos = 10
        self.y_pos = 10
        self.line_height = 30

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

    def __init__(self):
        super().__init__()
        pg.init()

        # Load users
        try:
            with open('settings/users.toml', 'rb') as users_file:
                self.users = tomllib.load(users_file)
                self.users = self.users["users"]
        except FileNotFoundError:
            self.users = []

        # Set the width and depth of the screen [width,depth]
        size = [WindowSize.WIDTH, WindowSize.HEIGHT]

        # show text?
        self.show_text = False

        # populate Levels dropdown with number of levels
        user_levels_list = []
        user_levels_str = []
        for l in range(self.num_of_levels_from_csv):
            user_levels_list.append(l + 1)
            user_levels_str.append(str(l).rjust(6))

        # ui images
        self.ui_background_dots = pg.image.load("assets/ui/images/mascot/bg_dots.svg")
        self.ui_background_mouth_character = pg.image.load("assets/ui/images/mascot/character_mouth.png")
        self.ui_background_character = pg.image.load("assets/ui/images/mascot/character_body.png")
        self.ui_background_hands_character = pg.image.load("assets/ui/images/mascot/character_hands.svg")
        # self.ui_background_life_counter = [pg.image.load("assets/ui/images/life_counter/0_lives_left.svg"),
        #                                    pg.image.load("assets/ui/images/life_counter/1_live_left.svg"),
        #                                    pg.image.load("assets/ui/images/life_counter/2_lives_left.svg"),
        #                                    pg.image.load("assets/ui/images/life_counter/3_lives_left.svg")]

        # font
        self.ibm_plex_condensed_font = pygame.font.Font("assets/ui/fonts/IBMPlexSansCondensed-Medium.ttf", 22)

        # set game params
        self.playing_game = False
        self.game_note_path = 0

        # set sfx params
        self.correct_sound = pg.mixer.Sound("assets/sx/game_sound_correct.wav")
        self.correct_sound.set_volume(0.1)
        self.wrong_sound = pg.mixer.Sound("assets/sx/game_sound_wrong.wav")
        self.wrong_sound.set_volume(0.1)

        self.screen = pg.display.set_mode(size)

        pg.display.set_caption("JoyInst")

        # Used to manage how fast the screen updates
        self.clock = pg.time.Clock()

        # Initialize the joysticks
        pg.joystick.init()

        self.play_mode = Dropdown(
            self.screen, 204, 50, 385, 50, name='     PLAY MODE',
            choices=[
                '     OPEN PLAY',
                '     LEARN GAME',

            ],
            colour=Colors.DROPDOWN.value,
            hoverColour=Colors.DROPDOWN_HOVER.value,
            pressedColour=Colors.DROPDOWN_HOVER.value,
            values=[1, 2],
            direction='down',
            textHAlign='left',
            font=self.ibm_plex_condensed_font
        )

        self.instrument_dropdown = Dropdown(
            self.screen, 610, 50, 385, 50, name='     SELECT INSTRUMENT',
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

        self.level_dropdown = Dropdown(
            self.screen, 1015, 50, 192, 50, name='     LEVEL',
            choices=user_levels_str,
            colour=Colors.DROPDOWN.value,
            hoverColour=Colors.DROPDOWN_HOVER.value,
            pressedColour=Colors.DROPDOWN_HOVER.value,
            values=user_levels_list,
            direction='down',
            textHAlign='left',
            font=self.ibm_plex_condensed_font
        )

        self.user_names = Dropdown(
            self.screen, 204, 50, 385, 50, name='     SELECT YOUR USER',
            choices=[f'     {user[0]}' for user in self.users],
            colour=Colors.DROPDOWN.value,
            hoverColour=Colors.DROPDOWN_HOVER.value,
            pressedColour=Colors.DROPDOWN_HOVER.value,
            values=[user[1] for user in self.users],
            direction='down',
            textHAlign='left',
            font=self.ibm_plex_condensed_font
        )

        self.new_user = TextBox(self.screen, 610, 50, 385, 53,
                                colour=Colors.DROPDOWN.value,
                                fontSize=40,
                                textOffsetLeft=1000,
                                borderColour=(0, 0, 0),
                                textColour=(0, 0, 0),
                                borderThickness=3,
                                font=self.ibm_plex_condensed_font,
                                placeholderText="ENTER NEW USER NAME",
                                onTextChanged=self.reset_user_names_dropdown
                                )

        self.play_button = Button(self.screen, 1015, 50, 100, 53,
                                  text="PLAY!",
                                  font=self.ibm_plex_condensed_font,
                                  colour=Colors.DROPDOWN.value,
                                  hoverColour=Colors.DROPDOWN_HOVER.value,
                                  pressedColour=Colors.DROPDOWN_HOVER.value,
                                  borderThickness=3,
                                  onClick=self.mainloop,
                                  )

        self.user_selection_running = True

        # setup inst & notation vars
        self.inst = self.instrument
        self.path_to_generated_images = "assets/ui/images/generated_notes/"

        # event vars
        self.last_guess = pg.time.get_ticks()
        self.smoothing = 300

    def reset_user_names_dropdown(self):
        self.user_names.reset()

    def user_selection(self):
        self.play_mode.hide()
        self.instrument_dropdown.hide()
        self.level_dropdown.hide()

        while self.user_selection_running:
            events = pg.event.get()
            self.screen.fill(Colors.BACKGROUND.value)
            self.screen.blit(self.ui_background_dots, (0, 0))
            self.screen.blit(self.ui_background_mouth_character, (326, 359))
            self.screen.blit(self.ui_background_character, (0, 164))

            # Go ahead and update the screen with what we've drawn.
            pygame_widgets.update(events)
            pg.display.flip()
            # Limit to 60 frames per second
            self.clock.tick(60)

    def mainloop(self):
        self.user_selection_running = False

        # Get ready to print
        text_print = TextPrint()

        self.new_user.hide()
        self.play_button.hide()
        self.user_names.hide()

        self.play_mode.show()
        self.instrument_dropdown.show()
        self.level_dropdown.show()

        # init vars
        done = False
        button_down = False  # might be useful later on

        while not done:
            # EVENT PROCESSING STEP
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    done = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.show_text = not self.show_text

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
            if self.instrument_dropdown.getSelected():
                self.inst = self.instrument_dropdown.getSelected()
                self.fs.program_select(1, self.sfid, 0, self.inst)

            # Get play mode choice
            if self.play_mode.getSelected():
                game_mode = self.play_mode.getSelected()
                if game_mode == 1:
                    self.playing_game = False
                    # first note of game
                    self.first_note = False

                    # remove text
                    self.show_text = False

                elif game_mode == 2:
                    self.playing_game = True

                    # show text
                    self.show_text = True

                    # reset game
                    if not self.first_note:
                        self.reset(self.level)

            # Get level choice
            if self.level_dropdown.getSelected():
                self.level = self.level_dropdown.getSelected() - 1
                self.reset(level=self.level)
                self.playing_game = False
                # self.play_mode.setDropped(0)
                self.level_dropdown.reset()
                self.play_mode.reset()
                self.show_text = False

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

                # draw the backgrounds.
                self.screen.blit(self.ui_background_dots, (0, 0))
                self.screen.blit(self.ui_background_mouth_character, (326, 359))

                if self.show_text:
                    text_print.print(self.screen, "Level    {}".format(self.level))
                    text_print.print(self.screen, "Sub-level    {}".format(self.sub_level))
                    text_print.print(self.screen, "Guesses    {}".format(self.tries))
                    text_print.print(self.screen, "Lives    {}".format(self.lives))
                    text_print.print(self.screen, "Feedback    {}".format(self.feedback))

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

                self.screen.blit(self.ui_background_character, (0, 164))

                text_print.reset()

                # text_print.print(self.screen, "Compass    {}".format(compass))
                # text_print.print(self.screen, "arrow_direction    {}".format(arrow_direction))
                # text_print.print(self.screen, "arrow_colour   {}".format(arrow_colour))
                # text_print.print(self.screen, "note   {}".format(self.neopitch))
                # text_print.print(self.screen, "solfa  {}".format(solfa))
                if self.show_text:
                    text_print.print(self.screen, "Level    {}".format(self.level))
                    text_print.print(self.screen, "Sub-level    {}".format(self.sub_level))
                    # text_print.print(self.screen, "Goes at sub level    {}".format(self.sub_level_rounds))
                    text_print.print(self.screen, "Guesses    {}".format(self.tries))
                    text_print.print(self.screen, "Lives    {}".format(self.lives))
                    text_print.print(self.screen, "Feedback    {}".format(self.feedback))

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
                self.screen.blit(self.ui_background_hands_character, (0, 475))

                # self.screen.blit(self.ui_background_life_counter[self.lives], (1060, 49))

                # Go ahead and update the screen with what we've drawn.
                pygame_widgets.update(events)
                pg.display.flip()
                # Limit to 60 frames per second
                self.clock.tick(60)

    def first_game_note(self):
        # put first game image on screen
        # get a new note from current list

        self._game_new_note = self.get_random_note()
        print("new note = ", self._game_new_note)
        note_to_show = self.make_game_note_notation(self._game_new_note)
        # print(note_to_show)
        game_note_path = self.path_to_generated_images + note_to_show
        return game_note_path
        # self.show_game_note(self.game_note_path)

    def game_loop(self):
        # check if current note matches. Lock so as not to repeat comparisons

        result = self.check_notes_match(self.neopitch)
        print("guess result = ", result)
        sleep(0.2)

        # blank the game staff
        previous_game_note_path = self.game_note_path
        self.game_note_path = 'assets/ui/images/empty_staves/empty_treble.png'

        # update game status depending on result
        self.update_game_states(result)
        print("\t\tchecking game stats")
        if self.lives == 0:
            self.play_mode.reset()
            self.show_text = False
            self.reset(level=self.level)
            self.playing_game = False
        sleep(0.2)

        # update visual helpers on the note
        self.check_helpers()
        print("adjusting helpers")
        sleep(0.2)

        # if correct guess
        if result:
            self.correct_sound.play()
            print("Picking new note")
            sleep(0.2)
            # get a new note from current list
            self._game_new_note = self.get_random_note()
            note_to_show = self.make_game_note_notation(self._game_new_note)
            self.game_note_path = self.path_to_generated_images + note_to_show

        # false guess
        else:
            self.wrong_sound.play()
            print("RETRY")
            sleep(0.2)
            # show same note with adjusted helps?
            note_to_show = self.make_game_note_notation(self._game_new_note)
            self.game_note_path = self.path_to_generated_images + note_to_show

        self.game_lock = False

    def show_note(self, path_to_new_image):
        # top stave
        note = pg.image.load(path_to_new_image).convert_alpha()
        # Create a rect with the size of the image.
        rect = note.get_rect()
        rect.center = ((WindowSize.WIDTH / 2) + 10, 430)
        self.screen.blit(note, rect)

    def show_game_note(self, path_to_new_image):
        # bottom stave
        note = pg.image.load(path_to_new_image).convert_alpha()
        # Create a rect with the size of the image.
        rect = note.get_rect()
        rect.center = ((WindowSize.WIDTH / 2) + 10, 600)
        self.screen.blit(note, rect)


if __name__ == "__main__":
    ui = UI()
    ui.user_selection()
