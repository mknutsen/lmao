# Example file showing a circle moving on screen
import pygame
from pygame import midi
from enum import Enum, auto
from time import time
from pygame.color import THECOLORS
from pygame import font

from random import choice
# pygame setup
pygame.init()
if not midi.get_init():
    midi.init()

jumps = 0
font.init()
py_midi_in = midi.Input(0)
gravity = 9.5
pygame.quit()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
SECONDS_PER_MINUTE = 60
PULSES_PER_SIXTEENTH_NOTE = 6 * 4
JUMP_VELOCITY = -5
DEBUG = False
MOVE_SPEED = 400
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
import math

def debug_print(*string):
    if DEBUG:
        print(string)

class Character():
    def __init__(self, rect) -> None:
        self.rect = rect
        self.y_velocity = 0
    def reset_y(self):
        global JUMP_ACTIVE
        JUMP_ACTIVE = False
        self.y_velocity = 0
        self.rect.move_ip(0, -screen.get_height())

    def move(self, x, dt):
        self.rect.move_ip(x, self.y_velocity)
        self.y_velocity = dt * gravity + self.y_velocity
        debug_print("move velocity", self.y_velocity)
    def jump(self):
        global JUMP_ACTIVE
        if self.rect.collidelist(rectangles) and not JUMP_ACTIVE:
            self.y_velocity = JUMP_VELOCITY
            debug_print("jump", self.y_velocity)
            JUMP_ACTIVE = True

class MidiClock():
    def __init__(self) -> None:
        self.times = list()
    def tap(self):
        self.times.append(time())
        if len(self.times) >= 2000:
            debug_print("resetting")
            self.times = self.times[-100:]
    def get_seconds_per_quarter_note(self):
        self.get_beat() / 60
    def get_beat(self):
        start = 0 if len(self.times) < 20 else -20
        sub_arr = self.times[start:]
        diffs = []
        for i in range(0, len(sub_arr) - 1):
            diffs.append(sub_arr[i + 1] - sub_arr[i])
        if not diffs:
            debug_print("no clock!")
            return 1
        average_seconds_between_tics = sum(diffs) / len(diffs)
        # beats_per_minute = SECONDS_PER_MINUTE / average_seconds_between_tics / PULSES_PER_SIXTEENTH_NOTE
        return average_seconds_between_tics


class MidiNote():
    def __init__(self, note_status, keynum, velocity, unused):
        self.note_status = note_status
        self.keynum = keynum
        self.velocity = velocity
        self.unused = unused
        self.status = parse_midi_status(note_status)
        debug_print(self.status)
    
class MidiStatus(Enum):
    NOTE_OFF = auto()
    NOTE_ON = auto()
    AFTERTOUCH = auto()
    CONTROLLER = auto()
    PROGRAM_CHANGE = auto()
    CHANNEL_PRESSURE = auto()
    PITCH_WHEEL = auto()
    SYSEX = auto()
    TIME_CODE_QUARTER_FRAME = auto()
    SONG_POSITION_POINTER = auto()
    SONG_SELECT = auto()
    TUNE_REQUEST = auto()
    MIDI_CLOCK = auto()
    MIDI_START = auto()
    MIDI_CONTINUE = auto()
    MIDI_STOP = auto()
    ACTIVE = auto()
    RESET = auto()


class MidiException(Exception):
    """Midi exception"""

def randomcolor():
    return choice([color for color in list(THECOLORS.keys()) if color != "black"])

def parse_midi_status(input):
    if input >= 0x80 and input <= 0x8F:
        return MidiStatus.NOTE_OFF
    if input >= 0x90 and input <= 0x9F:
        return MidiStatus.NOTE_ON
    if input >= 0xA0 and input <= 0xAF:
        return MidiStatus.AFTERTOUCH
    if input >= 0xB0 and input <= 0xBF:
        return MidiStatus.CONTROLLER
    if input >= 0xC0 and input <= 0xCF:
        return MidiStatus.PROGRAM_CHANGE
    if input >= 0xD0 and input <= 0xDF:
        return MidiStatus.CHANNEL_PRESSURE
    if input >= 0xE0 and input <= 0xEF:
        return MidiStatus.PITCH_WHEEL
    if input == 0xF0:
        return MidiStatus.SYSEX
    if input == 0xF1:
        return MidiStatus.TIME_CODE_QUARTER_FRAME
    if input == 0xF2:
        return MidiStatus.SONG_POSITION_POINTER
    if input == 0xF3:
        return MidiStatus.SONG_SELECT
    if input == 0xF6:
        return MidiStatus.TUNE_REQUEST
    if input == 0xF8:
        return MidiStatus.MIDI_CLOCK
    if input == 0xFA:
        return MidiStatus.MIDI_START
    if input == 0xFB:
        return MidiStatus.MIDI_CONTINUE
    if input == 0xFC:
        return MidiStatus.MIDI_STOP
    if input == 0xFE:
        return MidiStatus.ACTIVE
    if input == 0xFF:
        return MidiStatus.RES

    raise MidiException(input)

JUMP_ACTIVE = False
def process_character_press(keys):
    global jump
    global player_pos
    if keys[pygame.K_UP]:
        PLAYER_CHARACTER.jump()
    if keys[pygame.K_DOWN]:
        player_pos.y += 300 * dt
    if keys[pygame.K_LEFT]:
        PLAYER_CHARACTER.move(-MOVE_SPEED * dt, 0)
    if keys[pygame.K_RIGHT]:
        PLAYER_CHARACTER.move(MOVE_SPEED * dt, 0)

def _SECONDS_TO_MILLISECONDS(time_sec):
    return time_sec * 1000

UPPER_VALUE = 9
COLORS = [randomcolor() for i in range(0, UPPER_VALUE)]
SECONDS_PER_NOTE = 1
HEIGHT = screen.get_height() /  UPPER_VALUE
WIDTH = screen.get_width()
CLOCK = MidiClock()

def land(character_place):
    global COLORS, jumps, JUMP_ACTIVE
    JUMP_ACTIVE = False
    if COLORS[character_place] != "black":
        COLORS[character_place] = "black"
        jumps += 1

player_rect = pygame.Rect(WIDTH/2, 0, 20, 20)
PLAYER_CHARACTER = Character(player_rect)
rectangles = [pygame.Rect(0, i * HEIGHT, WIDTH / 4, 75) for i in range(0, UPPER_VALUE)]
class GameState:
    def __init__(self):
        self.slots = [0 for i in range(0, UPPER_VALUE)]
    
    def tag(self, slot):
        global COLORS
        if slot < UPPER_VALUE and slot >= 0:
            rectangles[slot].left = WIDTH
            COLORS[slot] = randomcolor()
    
    def process(self, rate, dt):
        global rectangles
        for i in range (0, UPPER_VALUE):
            rectangles[i].left -= rate * dt

def process_midi():
    global CLOCK
    input_val = py_midi_in.read(1)
    if input_val:
        midi_note, timestamp = input_val[0]
        note = MidiNote(*midi_note)
        if note.status == MidiStatus.MIDI_CLOCK:
            CLOCK.tap()
        if note.status == MidiStatus.NOTE_ON:
            offset = 33
            real_note = note.keynum - offset
            game.tag(real_note)

game = GameState()
font.init()
all_fonts = font.get_fonts()
debug_print(all_fonts)
font_object = font.Font(None, 24)
while running:
    num_cells = WIDTH
    beat = CLOCK.get_beat() * 10

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    game.process(num_cells / beat, dt)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    while py_midi_in.poll():
        process_midi()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple" if JUMP_ACTIVE else "red")


    for i in range(0, UPPER_VALUE):
        pygame.draw.rect(screen, COLORS[i], rectangles[i])

    keys = pygame.key.get_pressed()
    process_character_press(keys)
    pygame.draw.rect(screen, "black", player_rect)
    character_place = player_rect.collidelist(rectangles)
    if character_place < 0:
        PLAYER_CHARACTER.move(0, dt)
        pass
    else:
        land(character_place)

    if player_rect.bottom >= screen.get_height():
        jumps = 0
        PLAYER_CHARACTER.reset_y()
    
    img = font_object.render(f'{jumps}', True, randomcolor())
    screen.blit(img, (20, 20))


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick() / 1000

pygame.quit()