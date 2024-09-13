# from random import choice
import pandas as pd
from secrets import choice

# from notation import Notation
# from threading import Thread

class Game:
    """
    Class that runs the mecahnics for the learning game.
    If is_game is True, then it will check the realtime input of notes against the game note.
    Each level is different set of notes,
    each level has 4 sub-levels:
        0 = sequence through each note, unlimited goes and full help
        1 = randomly choosen note from list, full help
        2 = randomly choosen note from list, name help only
        3 = randomly choosen note from list, no help, note only

    Sub-level's 1-3 has 3 rounds.
    There are 3 tries per round before life lost
    3 lives overall

    """
    df = pd.read_csv('curriculum.csv', header=None)
    reader = df.values.tolist()

    learning_dict = []
    num_of_levels_from_csv = 0
    for rows in reader:
        num_of_levels_from_csv += 1
        level_notes = []
        for note in rows:
            if note == note:
                level_notes.append(note)
        learning_dict.append(level_notes)

    correct_words = ["Way to go!",
                     "Great job",
                     "Nice going",
                     "You rock",
                     "You rule",
                     "Good",
                     "Job",
                     "Kudos",
                     "Phenomenal",
                     "Bravo/brava",
                     "Shout-out",
                     "Nailed it",
                     "Stellar",
                     "On fire!",
                     "Impressive"
                     ]

    wrong_words = ["Try Again",
                   "You got this",
                   "You can do it",
                   "Nearly",
                   "C'mon, one more",
                   "Close",
                   "We believe in you"
                   ]

    def __init__(self):
        super().__init__()

        # first note of game
        self.first_note = False

        # keeps track of the number of tries per test. 3 tries per test, then loose a live
        self.tries = 3

        # number of lives
        self.lives = 3

        # navigates the learning sequence
        self.level = 0

        # sub-level associated with helpers on screen
        self.sub_level = 0
        self.sub_level_rounds = 3
        self.feedback = ""

        # locks the game loop while dealing with guess
        self.game_lock = False
        self.melody_flag = False

        # define notation helpers
        self.arrow_help = True
        self.name_help = True

        # game params
        self.current_game_note = 0
        self.current_level_list = self.learning_dict[self.level]
        print("current_level_list", self.current_level_list)

        # check if level has a melody flag at [0]
        if self.current_level_list[0] == "m":
            print("MELODY", self.current_level_list)
            self.current_level_list.pop(0)
            self.melody_flag = True
            print("Now", self.current_level_list)

        self.len_current_level_list = len(self.current_level_list)
        self.melody_position = 0

    def reset(self, level=0):
        # first note of game
        self.first_note = False

        # keeps track of the number of tries per test. 3 tries per test, then loose a live
        self.tries = 3

        # number of lives
        self.lives = 3

        # navigates the learning sequence
        self.level = level

        # sub-level associated with helpers on screen
        self.sub_level = 0
        self.sub_level_rounds = 3
        self.feedback = ""

        # locks the game loop while dealing with guess
        self.game_lock = False
        self.melody_flag = False

        # define notation helpers
        self.arrow_help = True
        self.name_help = True

        # game params
        self.current_game_note = 0
        self.current_level_list = self.learning_dict[self.level]

        # check if level has a melody flag at [0]
        if self.current_level_list[0] == "m":
            print("MELODY", self.current_level_list)
            self.current_level_list.pop(0)
            self.melody_flag = True
            print("Now", self.current_level_list)

        self.len_current_level_list = len(self.current_level_list)
        self.melody_position = 0

    def get_random_note(self):
        """
        randomly gets a note from current level list if level, otherwise
        sequence through the melody test
        :return:
        """

        # if sub-level 0 or a melody - sequence through list
        if self.sub_level == 0 or self.melody_flag:
            self.current_game_note = self.current_level_list[self.melody_position]

        # for any other sub-level, choose a random note from the list:
        else:
            self.current_game_note = choice(self.current_level_list)

        print("Current game note = ", self.current_game_note)
        return self.current_game_note

    def make_game_note_notation(self, current_game_note):

        # extract only the note name
        game_note = current_game_note
        match game_note:
            case "c'":
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

        note_filename = game_note + compass
        if self.arrow_help:
            note_filename += "_arrow"
        if self.name_help:
            note_filename += "_name"
        note_filename += ".png"

        return note_filename

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
        #################
        #  level - MELODY line
        #################
        print(f"melody flag {self.melody_flag}, level list {self.current_level_list}, len of lev list {self.len_current_level_list}")

        if self.melody_flag:
            if result:
                self.feedback = f"{choice(self.correct_words)}, CORRECT"
                self.melody_position += 1

                # reached end of melody? now onto next level
                if self.melody_position >= self.len_current_level_list:
                    self.sub_level += 1
                    self.melody_position = 0
            else:
                self.feedback = f"{choice(self.wrong_words)}, Have another go"

        #################
        #  sub-level 0 - training round
        #################

        # sequence through the whole list. unlimited tries
        elif self.sub_level == 0:
            # unlimited goes at sub-level 0
            if result:
                self.feedback = f"{choice(self.correct_words)}, CORRECT"
                self.melody_position += 1
                # reached end of level list? Now onto game
                if self.melody_position >= self.len_current_level_list:
                    self.sub_level += 1
                    self.melody_position = 0
            else:
                self.feedback = f"{choice(self.wrong_words)}, Have another go"

        #################
        # sub-levels 1,2,3 where tries and lives matter
        #################

        else:
            # if correct match (True)
            if result:
                self.feedback = f"{choice(self.correct_words)}, next note"
                # have 3 rounds per sub-level (help indicators)
                self.sub_level_rounds -= 1

                if self.sub_level_rounds <= 0:
                    self.feedback = f"{choice(self.correct_words)}, on to next sub-level - we've reduced the help"
                    # sub-level goes up
                    self.sub_level += 1

                    # reset rounds and tries
                    self.sub_level_rounds = 3
                    self.tries = 3

            else:
                self.feedback = f"{choice(self.wrong_words)}, have another go"
                # if incorrect then try again, loose a try
                self.tries -= 1

                if self.tries <= 0:
                    self.feedback = f"{choice(self.wrong_words)}, Lets try some easier notes"

                    self.sub_level -= 1
                    self.sub_level_rounds = 3
                    self.tries = 3

            # check sub-level status - back to sub-level 1 NOT 0!!!
            if self.sub_level < 1:
                self.sub_level = 1
                # self.lives -= 1

        # check if we are through sub-levels and move to next level
        if self.sub_level > 3:
            self.feedback = f"{choice(self.correct_words)}, Whoop Whoop - LEVEL UP"

            # get the next level
            self.level += 1
            self.current_level_list = self.learning_dict[self.level]

            # check if level has a melody flag at [0]
            if self.current_level_list[0] == "m":
                print("MELODY", self.current_level_list)
                self.current_level_list.pop(0)
                self.melody_flag = True
                print("Now", self.current_level_list)
            else:
                self.melody_flag = False

            # reset for walkthrogh note list
            self.sub_level = 0
            self.len_current_level_list = len(self.current_level_list)

            # reset tries and rounds
            self.sub_level_rounds = 3
            self.tries = 3

        if self.lives == 0:
            self.feedback = f"{choice(self.wrong_words)}, Game Over. Have another go.   Lives back up to 3"
            # reset every thing
            self.lives = 3
            self.tries = 3
            self.sub_level = 0
            self.level = 0
            # check if level has a melody flag at [0]
            if self.current_level_list[0] == "m":
                print("MELODY", self.current_level_list)
                self.current_level_list.pop(0)
                self.melody_flag = True
                print("Now", self.current_level_list)
            else:
                self.melody_flag = False
            self.len_current_level_list = len(self.current_level_list)


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
