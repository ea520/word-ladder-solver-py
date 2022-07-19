import json
import argparse
import util


def get_distances(start, end, graph):
    large_dist = len(graph) + 1
    distances = dict((word, large_dist)
                     for word in graph if len(word) == len(start))
    distances[start] = 0
    unvisited = set(distances.keys())
    hammings = dict((el, util.hamming_dist(el, end)) for el in distances)
    while True:
        candidate = min(
            unvisited, key=lambda el: distances[el] + hammings[el])

        if(distances[candidate] == large_dist or candidate == end):
            break

        for neighbour in graph[candidate]:
            if(neighbour in unvisited):
                distances[neighbour] = min(
                    distances[neighbour], distances[candidate] + 1)
        unvisited.remove(candidate)
    return distances


def get_path(node, distances, words):
    my_dist = distances[node]
    large_dist = len(distances) + 1
    if(my_dist == large_dist):
        raise RuntimeError("An unknown error occured")
    elif(my_dist == 0):
        return [node]
    else:
        neighbors = util.get_neighbours(node, words)
        next = None
        for s in neighbors:
            if distances[s] == distances[node] - 1:
                next = s
                break
        if(next == None):
            raise RuntimeError("An unknown error occured")
        out = get_path(next, distances, words)
        out.append(node)
        return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="lime", type=str,
                        help="the initial word")
    parser.add_argument("--end", default="help", type=str,
                        help="the final word")
    parser.add_argument("--graph", default="graph.json", type=str,
                        help="path to the json file for the graph")
    args = parser.parse_args()
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
    dists = get_distances(start, end, graph)
    print(dists[end])
    print(*get_path(end, dists, words), sep="->")
