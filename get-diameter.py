import json
import util
import numpy as np
filename = "word-list.txt"
words = [line.strip().upper() for line in open(
    filename, "r").read().splitlines() if len(line.strip()) == 2]
print(len(words))
graph = np.zeros(shape=(len(words), len(words)), dtype=np.int32)
LARGE = len(words)
cache = json.load(open("graph.json", "r"))
for i, source in enumerate(words):
    for j, destination in enumerate(words[i + 1:]):
        j += i+1
        if destination in cache[source]:
            graph[i, j] = graph[j, i] = 1
        else:
            graph[i, j] = graph[j, i] = LARGE
    progress = 100 * i // LARGE
    print(f"\r [{'#' * progress}] {progress}%", end="")
print(f"\r [{'#' * 100}] {100}%")

print(graph)
dist = graph.copy()
for k in range(LARGE):
    for i in range(LARGE):
        for j in range(LARGE):
            dist[i, j] = min(dist[i, j], dist[i, k] + dist[k, j])
    progress = 100 * k // LARGE
    print(f"\r [{'#' * progress}] {progress}%", end="")
print(f"\r [{'#' * 100}] {100}%")
dist[dist == LARGE] = 0
print(dist)
print(np.max(dist))
coords = np.unravel_index(np.argmax(dist), dist.shape)
print(words[coords[0]], "->", words[coords[1]])
