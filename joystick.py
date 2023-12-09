"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
http://programarcadegames.com/python_examples/f.php?file=joystick_calls.py
Show everything we can pull off the joystick
"""
import pygame
from mingus.containers import Note, NoteContainer, Bar, Track
from mingus.midi import fluidsynth

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

class Joystick:
    def __init__(self):
        self.running = None
        self.compass = ""

    # def init(self):
        pygame.init()

        # Set the width and height of the screen [width,height]
        size = [500, 700]
        self.screen = pygame.display.set_mode(size)

        pygame.display.set_caption("Mach AI Inst")

        # Loop until the user clicks the close button.
        self.running = True

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

        # Initialize the joysticks
        pygame.joystick.init()
        self.joystick_active_range = 0.7

        # Get ready to print
        self.textPrint = TextPrint()

        # init midi synth
        fluidsynth.init("GeneralUserGSv1.471.sf2")
        self.fs_is_playing = False

        # midi vars
        self.octave = 4
        self.dynamic = 70
        self.add_accidental = 0

    def mainloop(self):
        # -------- Main Program Loop -----------
        while self.running:
            # EVENT PROCESSING STEP
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN
                # JOYBUTTONUP JOYHATMOTION
                if event.type == pygame.JOYBUTTONDOWN:
                    print("Joystick button pressed.")
                if event.type == pygame.JOYBUTTONUP:
                    print("Joystick button released.")

            # DRAWING STEP
            # First, clear the screen to white. Don't put other drawing commands
            # above this, or they will be erased with this command.
            self.screen.fill(WHITE)
            self.textPrint.reset()

            # Get count of joysticks
            joystick_count = pygame.joystick.get_count()

            self.textPrint.print(self.screen, "Number of joysticks: {}".format(joystick_count))
            self.textPrint.indent()

            # For each joystick:
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                self.compass = ""

                self.textPrint.print(self.screen, "Joystick {}".format(i))
                self.textPrint.indent()

                # Get the name from the OS for the controller/joystick
                name = joystick.get_name()
                self.textPrint.print(self.screen, "Joystick name: {}".format(name))

                # Calc # or b using buttons 4 & 5
                buttons = joystick.get_numbuttons()
                self.textPrint.print(self.screen, "Number of buttons: {}".format(buttons))
                self.textPrint.indent()

                for i in range(buttons):
                    button = joystick.get_button(i)
                    self.textPrint.print(self.screen, "Button {:>2} value: {}".format(i, button))
                    # reset accidental
                    self.add_accidental = 0

                    match buttons:
                        case 4:
                            self.add_accidental += 1
                        case 5:
                            self.add_accidental -= 1
                self.textPrint.unindent()

                # Usually axis run in pairs, up/down for one, and left/right for
                # the other.
                axes = joystick.get_numaxes()
                self.textPrint.print(self.screen, "Number of axes: {}".format(axes))
                self.textPrint.indent()

                for i in range(axes):
                    axis = joystick.get_axis(i)
                    self.textPrint.print(self.screen, "Axis {} value: {:>6.3f}".format(i, axis))

                    # Calculate note joystick position for notes
                    if i == 2 and axis < -self.joystick_active_range:
                        self.compass += "N"
                    elif i == 2 and axis >= self.joystick_active_range:
                        self.compass += "S"

                    if i == 3 and axis < -self.joystick_active_range:
                        self.compass += "W"
                    elif i == 3 and axis >= self.joystick_active_range:
                        self.compass += "E"

                    # Calculate dynamic joystick for dynamics
                    if i == 1:
                        round(axis, 2)
                        # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
                        self.dynamic = (((axis - -1) * (20 - 120)) / (1 - -1)) + 120
                        # print(self.dynamic)

                    # Calculate octvave shift
                    if i == 0:
                        if axis > self.joystick_active_range:
                            self.octave = 5
                        elif axis < -self.joystick_active_range:
                            self.octave = 3
                        else:
                            self.octave = 4
                        # print(self.octave)

                self.textPrint.print(self.screen, f"Compass: {self.compass}")

                # make a sound
                # if self.compass:
                if self.compass == "":
                    self.fs_is_playing = False
                    self.textPrint.print(self.screen, f"Note: ")
                else:
                    # set monophonic to on
                    self.fs_is_playing = True

                    # get current octave
                    octave = self.octave

                    # match compass to notes
                    match self.compass:
                        case 'N':
                            note = 'C'
                        case 'NE':
                            note = 'E'
                        case 'E':
                            note = 'G'
                        case 'SE':
                            note = 'B'
                        case 'S':
                            note = 'C'
                            octave = self.octave+1
                        case 'SW':
                            note = 'A'
                        case 'W':
                            note = 'F'
                        case 'NW':
                            note = 'D'

                    # adjust note for enharmonic shift
                    if self.add_accidental != 0:
                        match self.add_accidental:
                            case 1:
                                note = f"{note}#"
                            case -1:
                                note = f"{note}b"

                    self.make_sound(note,
                                    octave,
                                    self.dynamic
                                    )

                    self.textPrint.print(self.screen, f"Note: {note}-{octave}")
                self.textPrint.unindent()

                # Hat switch. All or nothing for direction, not like joysticks.
                # Value comes back in an array.
                hats = joystick.get_numhats()
                self.textPrint.print(self.screen, "Number of hats: {}".format(hats))
                self.textPrint.indent()

                for i in range(hats):
                    hat = joystick.get_hat(i)
                    self.textPrint.print(self.screen, "Hat {} value: {}".format(i, str(hat)))
                self.textPrint.unindent()

                self.textPrint.unindent()

            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # Limit to 60 frames per second
            self.clock.tick(60)

    def make_sound(self,
                   new_note,
                   octave = 5,
                   dynamic = 70
                   ):
        # if new_note != playing_note:
        #     playing_note = new_note
        # if not self.fs_is_playing:

        # fs_note_to_play = f"{new_note}-{self.octave}"
        fluidsynth.play_Note(Note(new_note,
                                  octave=octave,
                                  velocity=dynamic
                                  )
                             )

    def terminate(self):
        # Close the window and quit.
        pygame.quit()

if __name__ == "__main__":
    js = Joystick()
    js.mainloop()
