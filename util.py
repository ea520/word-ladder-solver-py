def hamming_dist(a, b):
    assert(len(a) == len(b))
    return sum(c1 != c2 for c1, c2 in zip(a, b))


def get_neighbours(word, words):
    return tuple(candidate for candidate in words if hamming_dist(candidate, word) == 1)
