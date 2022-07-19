# word-ladder-solver-py
## use the provided dictionary (scrabble)
Unzip the graph file to get graph.json

```bash
python get-paths.py --start hello --end world --graph /path/to/graph.json
```

Example output

```
HELLO -> WORLD
6
HELLO -> HELLS -> HEALS -> HEALD -> WEALD -> WOALD -> WORLD
```

## Custom graph
Make a new line separated file of words in the dictionary (case insensitive)
python .\save-graph.py --out foo.json --words words.txt

if words.json was 
```
hello
hells
world

hell
tell
fell
sell
hill
```
foo.json would be
```json
{
    "HELLO": [
        "HELLS"
    ],
    "HELLS": [
        "HELLO"
    ],
    "WORLD": [],
    "HELL": [
        "TELL",
        "FELL",
        "SELL",
        "HILL"
    ],
    "TELL": [
        "HELL",
        "FELL",
        "SELL"
    ],
    "FELL": [
        "HELL",
        "TELL",
        "SELL"
    ],
    "SELL": [
        "HELL",
        "TELL",
        "FELL"
    ],
    "HILL": [
        "HELL"
    ]
}
```

Note the ~300,000 word scrabble dictionary took several hours to form the graph
