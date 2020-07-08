#!/usr/bin/python3

from Trie import Trie
from BoggleGame import BoggleGame, letters, BOARD_SIZE, MIN_WORD_LEN
from operator import itemgetter


# Format specifier for the scoreboard
FMT = '{:<20}{:>5}'


def get_words_prefix(current_position, game, trie, visited=(), current_word=()):
    '''Recursively yield words that can be found from the current position'''
    die = game[current_position[0]][current_position[1]]

    # Build word, see if it exists so far
    visited += (current_position,)
    current_word += (die,)
    prefix = trie.find_prefix(current_word)
    if prefix is None:
        return

    # A word can be a prefix and a valid word so check the "end" flag
    if prefix.end:
        yield current_word, visited

    # Try all other words from the current position
    for move in game.valid_moves(*current_position):
        if move in visited:
            continue
        yield from get_words_prefix(move, game, trie, visited, current_word)


def solve_board(game, trie):
    '''Solve a board, given a word list-loaded trie'''
    words = set()
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            for word, path in get_words_prefix((i, j), game, trie):
                # "quote" counts as 5 letters even though it's 4 dice
                score = game.score_word(''.join(word))
                words.add((word, score))
    return words


def top_words(words, n=10):
    '''Return the top words, sorted by score, length, and alphabetically'''
    words = sorted(words, key=itemgetter(0)) # Alphabetically
    words = sorted(words, key=lambda x: len(x[0]), reverse=True) # By word len
    words = sorted(words, key=itemgetter(1), reverse=True) # By score
    for i in range(n):
        try:
            yield words[i]
        except IndexError:
            break


if __name__ == '__main__':
    trie = Trie()
    
    valid_words_file = 'enable1_filtered.txt'
    with open(valid_words_file, 'r') as f:
        for count, word in enumerate(f, 1):
            trie.add_iterable(letters(word.strip()))
        print('Loaded {} words into trie'.format(count))
    
    bg = BoggleGame()

    best_game = None
    best_score = 0

    games_solved = 0
    while True:
        words = solve_board(bg, trie)
        total_score = sum([score for word, score in words])

        # Report best
        if total_score > best_score:
            best_game = bg.copy()
            best_score = total_score

            print('Best so far:')
            print(bg)
            print(FMT.format('Words found', len(words)))
            print(FMT.format('Total score', total_score))
            print('Top 10:')
            print(FMT.format('Word', 'Score'))
            print(FMT.format('-' * 17, '-' * 5))
            for word, score in top_words(words):
                print(FMT.format(''.join(word), score))
            print()

        bg.shake_board()

        games_solved += 1
        if games_solved % 1000 == 0:
            print('Solved {} games'.format(games_solved))
