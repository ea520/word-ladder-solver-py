from enum import Enum, auto
from queue import Queue
import json
import argparse
import util


class ALGORITHM(Enum):
    DIJKSTRA = auto()
    ASTAR = auto()
    BFS = auto()


def get_distances_potentially_weighted(start, end, graph, algorithm):
    large_dist = len(graph) + 1
    distances = dict((word, large_dist)
                     for word in graph if len(word) == len(start))
    distances[start] = 0
    unvisited = set(distances.keys())
    hammings = None
    metric = None
    if(algorithm == ALGORITHM.ASTAR):
        hammings = dict((el, util.hamming_dist(el, end)) for el in distances)
        def metric(el): return distances[el] + hammings[el]
    else:
        assert(algorithm == ALGORITHM.DIJKSTRA)
        def metric(el): return distances[el]
    while True:
        candidate = min(unvisited, key=metric)

        if(distances[candidate] == large_dist or candidate == end):
            break

        for neighbour in graph[candidate]:
            if(neighbour in unvisited):
                distances[neighbour] = min(
                    distances[neighbour], distances[candidate] + 1)
        unvisited.remove(candidate)
    for key in distances:
        if distances[key] == large_dist:
            distances[key] = -1

    return distances


def get_distances_bfs(start, end, graph: dict, words):
    large_dist = len(words) + 1
    distances = dict((word, len(words) + 1)
                     for word in graph if len(word) == len(start))
    visited = set()
    pending = Queue()
    distances[start] = 0
    pending.put(start)
    while True:
        node = pending.get()
        neighbours = set(graph[node])
        unvisited_neighbours = neighbours - visited
        for un in unvisited_neighbours:
            distances[un] = min(distances[node] + 1, distances[un])
            pending.put(un)
        visited.add(node)
        if(node == end):
            break

    for key in distances:
        if distances[key] == large_dist:
            distances[key] = -1
    return distances


def get_distances(start, end, graph, words, algorithm):
    if algorithm == ALGORITHM.BFS:
        return get_distances_bfs(start, end, graph, words)
    else:
        return get_distances_potentially_weighted(start, end, graph, algorithm)


def get_path(node, distances, words, graph):
    my_dist = distances[node]
    large_dist = len(distances) + 1
    if(my_dist == large_dist):
        raise RuntimeError("An unknown error occured")
    elif(my_dist == 0):
        return [node]
    else:
        neighbors = graph[node]
        next = None
        for s in neighbors:
            if distances[s] == distances[node] - 1:
                next = s
                break
        if(next == None):
            raise RuntimeError("An unknown error occured")
        out = get_path(next, distances, words, graph)
        out.append(node)
        return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", "-s", default="lime", type=str,
                        help="the initial word")
    parser.add_argument("--end", "-e", default="help", type=str,
                        help="the final word")
    parser.add_argument("--graph", "-g", default="graph.json", type=str,
                        help="path to the json file for the graph")
    parser.add_argument("--dijkstra", action="store_true",
                        help="Whether to use dijkstra")
    parser.add_argument("--astar", action="store_true",
                        help="Whether to use A*")
    parser.add_argument("--bfs", action="store_true",
                        help="Whether to use BFS")
    args = parser.parse_args()

    algorithm = None
    # check only 1 algorithm is set
    assert(args.astar ^ args.dijkstra ^ args.bfs)
    if args.astar:
        algorithm = ALGORITHM.ASTAR
    elif args.dijkstra:
        algorithm = ALGORITHM.DIJKSTRA
    else:
        algorithm = ALGORITHM.BFS

    if(len(args.start) != len(args.end)):
        raise ValueError("The start and end words must have the same length")

    start = args.start.upper()
    end = args.end.upper()
    graph = json.load(open(args.graph, "r"))

    if(start not in graph):
        raise ValueError(
            f"The starting word ({start}) wasn't found in the graph ({args.graph})")
    if(end not in graph):
        raise ValueError(
            f"The ending word ({end}) wasn't found in the graph ({args.graph})")
    print(start, "->", end)
    words = tuple(word for word in graph if len(word) == len(start))
    dists = get_distances(start, end, graph, words, algorithm)
    i = 0
    for key in dists:
        if(dists[key] != -1):
            i += 1
    print("Optimal path length:", dists[end])
    print("#Nodes inspected:", i)
    print(*get_path(end, dists, words, graph), sep=" -> ")
