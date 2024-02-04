from random import choice
from notation import Notation
from threading import Thread

class Game(Notation):
    """
    Class that runs the mecahnics for the learning game.
    If is_game is True, then it will check the realtime input of notes against the game note.
    Each level is different set of notes,
    each level has 4 sub-levels:
        0 = sequence through each note, unlimited goes and full help
        1 = randomly choosen note from list, full help
        2 = randomly choosen note from list, name help only
        3 = randomly choosen note from list, no help, note only

    Sub-level's 1-3 has 3 rounds

    """

    learning_dict = {"level_1": ["c", "c'"],
                     "level_2": ["f", "g"],
                     "level_3": ["c", "f", "g", "c'"],
                     "level_4": ["c", "g", "c'", "c", "f", "c'"],
                     "level_5": ["c", "d", "e"],
                     "level_6": ["c", "d", "e", "f", "g"],
                     }

    learning_seq = [
        "level_1", "level_2", "level_3", "level_4", "level_5" , "level_6"
    ]

    correct_words = ["Way to go!",
                     "Great job",
                     "Nice going",
                     "You rock",
                     "You rule",
                     "good",
                     "job",
                     "kudos",
                     "phenomenal",
                     "bravo/brava",
                     "shout-out",
                     "nailed it",
                     "stellar",
                     "on fire",
                     "impressive"
                     ]

    wrong_words = ["Try Again",
                   "You got this",
                   "You can do it",
                   "Nealry",
                   "C'mon, one more",
                   "close",
                   "We believe in you"
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
        self.sub_level_rounds = 3

        # locks the game loop while dealing with guess
        self.game_lock = False

        # define notation helpers
        self.arrow_help = True
        self.name_help = True

        # game params
        self.current_game_note = 0
        self.current_level_list = self.learning_dict.get(self.learning_seq[self.level])
        self.len_current_level_list = len(self.current_level_list)
        print(self.len_current_level_list)
        self.melody_position = 0

    def get_random_note(self):
        """
        randomly gets a note from current level list if level, otherwise
        sequence through the melody test
        :return:
        """
        # if sub-level 0 sequence through list
        if self.sub_level == 0:
            self.current_game_note = self.current_level_list[self.melody_position]
            # self.melody_position += 1
            # for any other sub-level:
        else:
            # self.melody_position = 0
            # check if its a level or test:
            learning_key = self.learning_seq[self.level][0]
            if learning_key == "l":
                self.current_game_note = choice(self.current_level_list)

            # todo - melody test (not implemented yet - can simply be sub;level 0 and no follow on sub-levels
            else:
                self.current_game_note = self.current_level_list[self.melody_position]

        print(self.current_game_note)
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
                compass = 'S'
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
        # is sub-level 0?
        if self.sub_level == 0:
            # unlimited goes at sub-level 0
            if result:
                print(choice(self.correct_words), "CORRECT")
                self.melody_position += 1
                # reached end of level list? Now onto game
                if self.melody_position >= self.len_current_level_list:
                    self.sub_level += 1
                    self.melody_position = 0
        else:
            # if > sub-level 0 correct match (True)
            if result:
                print(choice(self.correct_words), "next note")
                self.sub_level_rounds -=1

                if self.sub_level_rounds <= 0:
                    print(choice(self.correct_words), "on to next sub-level - we've reduced the help")
                    # sub-level goes up
                    self.sub_level += 1
                    self.sub_level_rounds = 3

            else:
                print(choice(self.wrong_words), "have another go")
                # if incorrect then try again
                if self.sub_level_rounds > 0:
                    self.lives -= 1

                else:
                    print(choice(self.wrong_words), "Lets try some easier notes")

                    self.sub_level -= 1
                    self.sub_level_rounds = 3

            # check sub-level status - back to sub-level 1 NOT 0!!!
            if self.sub_level < 1:
                self.sub_level = 1
                # self.lives -= 1

            # check if we are through sub-levels and move to next level
            if self.sub_level > 3:
                print(choice(self.correct_words), "Whoop Whoop - LEVEL UP")

                self.level += 1
                # reset for walkthrogh note list
                self.sub_level = 0
                # get the next level
                self.current_level_list = self.learning_dict.get(self.learning_seq[self.level])

            if self.lives == 0:
                print(choice(self.wrong_words), "Game Over. Have another go.   zLives back up to 3")
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
                self.arrow_help = True
                self.name_help = True
            case 2:
                self.arrow_help = False
                self.name_help = True
            case 3:
                self.arrow_help = False
                self.name_help = False


class Test:
    def __init__(self):
        pass
