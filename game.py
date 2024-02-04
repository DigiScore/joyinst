from random import choice
from notation import Notation
from threading import Thread

class Game(Notation):
    """
    Class that runs the mecahnics for the learning game.
    If is_game is True, then it will check the realtime input of notes against the game note.

    """

    learning_dict = {"level_1": ["c", "c'"],
                     "level_2": ["f", "g"],
                     "level_3": ["c", "f", "g", "c'"],
                     "test_1": ["c", "g", "c'", "c", "f", "c'"]
                     }

    learning_seq = [
        "level_1", "level_2", "level_3", "test_1"
    ]

    def __init__(self):
        super().__init__()

        # first note of game
        self.first_note = False

        # keeps track of the number of tries per test
        self.tries = 0

        # number of lives
        self.lives = 3

        # navigates the learning sequence
        self.level = 0

        # sub-level associated with helpers on screen
        self.sub_level = 0

        # locks the game loop while dealing with guess
        self.game_lock = False

        # define notation helpers
        self.arrow_help = True
        self.name_help = True

        # game params
        self.current_game_note = 0
        self.current_level_list = self.learning_dict.get(self.learning_seq[self.level])
        print(self.current_level_list)
        self.melody_position = 0


    def get_random_note(self):
        """
        randomly gets a note from current level list if level, otherwise
        sequence through the melody test
        :return:
        """
        # check if its a level or test:
        learning_key = self.learning_seq[self.level][0]
        if learning_key == "l":
            self.current_game_note = choice(self.current_level_list)

        else:
            self.current_game_note = self.current_level_list[self.melody_position]

        return self.current_game_note

    def make_game_note_notation(self, current_game_note):

        # extract only the note name
        game_note = current_game_note[0]
        match game_note:
            case 'c':
                compass = 'N'
            case 'e':
                compass = 'SE'
            case 'g':
                compass = 'E'
            case 'b':
                compass = 'NE'
            case 'c':
                compass = 'N'
            case 'a':
                compass = 'NW'
            case 'f':
                compass = 'W'
            case 'd':
                compass = 'SW'

        # make the note glyph
        note = self.make_notation([current_game_note],
                           compass,
                           self.arrow_help,
                           self.name_help
                           )
        return note

    def check_notes_match(self, played_note):
        """
        check current played note against game note
        :played_note note guessed by player
        :compass
        :return: True if guess matches game note
        """
        if played_note == self.current_game_note:
            return True

    def update_game_states(self, result):
        # if correct match (True)
        if result:
            # sub-level goes up
            self.sub_level += 1
        else:
            self.sub_level -= 1

        # check sub-level status
        if self.sub_level < 0:
            self.sub_level = 0
            self.lives -= 1
            # self._get_random_note()

        # check if we are through sub-levels and move to next level
        if self.sub_level > 2:
            self.level += 1
            self.sub_level = 0
            # get the next level
            self.current_level_list = self.learning_dict.get(self.learning_seq[self.level])

        if self.lives == 0:
            print("Game Over. Lives back up to 3")
            self.lives = 3

    def check_helpers(self):
        """
        Checks the sub-level progress in a level and adjusts on screen helpers
        :return:
        """
        match self.sub_level:
            case 0:
                self.arrow_help = True
                self.name_help = True
            case 1:
                self.arrow_help = False
                self.name_help = True
            case 2:
                self.arrow_help = False
                self.name_help = False


class Test:
    def __init__(self):
        pass
