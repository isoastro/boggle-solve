from random import sample, seed
import string
from collections import Counter


DICE = (('A', 'A', 'C', 'I', 'O', 'T'),
        ('A', 'B', 'I', 'L', 'T', 'Y'),
        ('A', 'B', 'J', 'M', 'O', 'QU'),
        ('A', 'C', 'D', 'E', 'M', 'P'),
        ('A', 'C', 'E', 'L', 'R', 'S'),
        ('A', 'D', 'E', 'N', 'V', 'Z'),
        ('A', 'D', 'H', 'M', 'R', 'S'),
        ('B', 'F', 'I', 'O', 'R', 'X'),
        ('D', 'E', 'N', 'O', 'S', 'W'),
        ('D', 'K', 'N', 'O', 'T', 'U'),
        ('E', 'E', 'F', 'H', 'I', 'Y'),
        ('E', 'G', 'I', 'N', 'T', 'V'),
        ('E', 'G', 'K', 'L', 'U', 'Y'),
        ('E', 'H', 'I', 'N', 'P', 'S'),
        ('E', 'L', 'P', 'S', 'T', 'U'),
        ('G', 'I', 'L', 'R', 'U', 'W'))

BOARD_SIZE = 4

MIN_WORD_LEN = 3

# All possible moves in 1D and 2D
MOVES_2D = ((0, +1), (-1, +1), (-1, 0), (-1, -1), (0, -1), (+1, -1), (+1, 0), (+1, +1))
MOVES_1D = tuple(y * BOARD_SIZE + x for y, x in MOVES_2D)

# The 'Q' tile is special and contains 'QU' to make the game a little easier
LETTERS = list(string.ascii_uppercase)
LETTERS[LETTERS.index('Q')] = 'QU'

def dice_containing_letter(letter):
    return (i for i, die in enumerate(DICE) if letter in die)

# Lookup from letter to dice
LETTER_MAP = {letter: list(dice_containing_letter(letter)) for letter in LETTERS}

# Statistics for commonness of letters
LETTER_COUNTS = Counter({letter: len(dice) for letter, dice in LETTER_MAP.items()})


def letters(word):
    '''Returns a tuple of letters but replaces {"Q", *} with {"Q*"}'''
    it = (letter.upper() for letter in word)
    try:
        return [i + next(it) if i == 'Q' else i for i in it]
    except StopIteration: # Dumb words that end in "Q"
        return list(it)

class BoggleGame:
    def __init__(self):
        '''Create an instance of a single game of Boggle'''
        self.shake_board()


    def copy(self):
        '''
        Create a new instance of the game, populate and return

        If you just do new_game = old_game, updating old_game's board state will
        modify new_game as well
        '''
        bg = BoggleGame()
        bg._board = self._board.copy()
        return bg


    def shake_board(self):
        '''Randomize board'''
        self._board = [sample(d, 1)[0] for d in sample(DICE, len(DICE))]


    @staticmethod
    def score_word(word):
        '''Score an individual word'''
        word_len = len(word)
        if word_len < MIN_WORD_LEN:
            return 0
        if word_len <= 4:
           return 1
        if word_len == 5:
           return 2
        if word_len == 6:
           return 3
        if word_len == 7:
           return 5
        return 11


    def __str__(self):
        '''Create string representation of board'''
        res = ''
        row_delim = '---'.join('+' * (BOARD_SIZE + 1))
        row_delim = '\n' + row_delim + '\n'

        def get_rows():
            for i in range(BOARD_SIZE):
                yield '|' + '|'.join(['{:^3}'.format(l) for l in self[i]]) + '|'

        return row_delim + row_delim.join(get_rows()) + row_delim


    def __getitem__(self, i):
        '''Index into board by row'''
        return self._board[i * BOARD_SIZE:(i + 1) * BOARD_SIZE]


    @staticmethod
    def valid_moves(i, j):
        '''Return an iterable that yields valid moves from current location'''
        for di, dj in MOVES_2D:
            newi = i + di
            newj = j + dj
            if 0 <= newi < BOARD_SIZE and 0 <= newj < BOARD_SIZE:
                yield newi, newj
