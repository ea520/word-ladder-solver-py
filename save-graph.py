from ctypes import util
from datetime import timedelta
import json
import argparse
from time import time
import util


def get_words_by_size(words):
    words_by_size = dict()
    for word in words:
        if len(word) not in words_by_size:
            words_by_size[len(word)] = [word]
        else:
            words_by_size[len(word)].append(word)
    return words_by_size


def get_graph(filename):
    graph = dict()
    words = [line.strip().upper() for line in open(
        filename, "r").read().splitlines() if len(line.strip()) > 0]
    words_by_size = get_words_by_size(words)
    n = len(words)
    i = 0
    t0 = time()
    for key in words_by_size:
        words = words_by_size[key]
        for word in words:
            graph[word] = util.get_neighbours(word, words)
            progress = i * 100 // n
            i += 1
            elapsed = time() - t0
            remaining = (elapsed / i) * (n - i)
            dt = timedelta(seconds=int(remaining))
            dt.resolution
            print(
                f"\r [{'#' * progress}] {progress}% {dt} s remaining", end="")

    return graph


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--words", default="word-list.txt", type=str,
                        help="a path to the newline separated list of words")
    args = parser.parse_args()
    json.dump(get_graph(args.words), fp=open("graph.json", "w"), indent=4)
