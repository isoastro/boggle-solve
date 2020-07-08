# boggle-solve

## Filtering
boggle_filter.py takes a newline-separated file of words, and filters out those words that are impossible to be found in valid game of Boggle.

See enable1.txt and enable1_filtered.txt for an example.

## Solving
boggle_solve.py will continuously solve games of Boggle, using enable1_filtered.txt as a word list.

It builds a trie from the word list, and then recursively searches through the valid moves in the board to see if the path is worth continuing down. It'll print the best game, as measured by total game score every time a new best is found.

On my machine, solves at about 200 games/second.
