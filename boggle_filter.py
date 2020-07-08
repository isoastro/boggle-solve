#!/usr/bin/python3

import string
from BoggleGame import DICE, LETTER_MAP, MIN_WORD_LEN, letters
import argparse


def word_dfs(word, dice_used=set()):
    '''Recursively search through dice to see if a word can be formed'''
    it = iter(word)
    try:
        letter = next(it)
    except StopIteration:
        return dice_used # Base case of recursive call

    try:
        available = LETTER_MAP[letter]
    except KeyError:
        return [] # Can't form the word if the letter isn't in the dice

    # For all dice that contain this letter, see if we can form the rest
    # of the word from the remaining dice    
    for die in available:
        if die in dice_used:
            continue # Can't reuse dice
        # Recursively call word_dfs with the rest of the letters
        res = word_dfs(it, dice_used = dice_used.union([die]))
        if res:
            return res # Found one, end

    # We'll get here if the word can't be formed from the dice already chosen
    return []


def can_word_be_formed(word):
    '''
    Takes an iterable of "letters" and determines if the word can be formed

    "Qu" is a special case and counted as a single letter
    '''
    # Very short words are not allowed
    if len(word) < MIN_WORD_LEN:
        return False

    # Word is non-formable if it is longer than the number of dice
    if len(word) > len(DICE):
        return False

    return word_dfs(word)


def filter_words(words):
    '''Return an iterator over valid Boggle words given a word list'''
    # Strip whitespace, convert "Q"s
    words = (letters(word.strip().upper()) for word in words)
    return filter(can_word_be_formed, words)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input text file of valid words')

    args = parser.parse_args()

    with open(args.input, 'r') as f:
        words = f.readlines()
        possible = filter_words(words)

    for word in possible:
        print(''.join(word))
    
