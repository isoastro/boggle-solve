# boggle-solve

## Filtering
boggle_filter.py takes a newline-separated file of words, and filters out those words that are impossible to be found in valid game of Boggle.

See enable1.txt and enable1_filtered.txt for an example.

## Solving
boggle_solve.py will continuously solve games of Boggle, using enable1_filtered.txt as a word list.

It builds a trie from the word list, and then recursively searches through the valid moves in the board to see if the path is worth continuing down. It'll print the best game, as measured by total game score every time a new best is found.

On my machine, solves at about 200 games/second.

### Example Output

```
+---+---+---+---+
| T | D | E | N |
+---+---+---+---+
| P | S | I | T |
+---+---+---+---+
| E | S | E | R |
+---+---+---+---+
| O | R | A | G |
+---+---+---+---+

Words found           389
Total score          1039
Top 10:
Word                Score
-----------------   -----
PEREGRINES             11
DISPERSER              11
DISSENTER              11
GREASIEST              11
PEREGRINE              11
ARTINESS               11
ASSENTER               11
ASSERTED               11
DESIRERS               11
DISPERSE               11
```

### Aside
It's really a shame that Boggle caps the score at 11 points for a word. `PEREGRINES` should really be more valuable than `ERASER` (both found in the board above)
