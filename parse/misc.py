# helpers and similar
import math


def check_int(interval):
    assert len(interval) == 2, "Intervals are not two-valued?"
    assert interval[0] < interval[1] or interval[0] == math.inf == interval[1], "Intervals are not correctly ordered?"


def intersect(int1, int2):
    check_int(int1)
    check_int(int2)

    a1, b1 = int1[0], int1[1]
    a2, b2 = int2[0], int2[1]

    if b1 < a2 or b2 < a1:
        return None
    else:
        return (max(a1, a2), min(b1, b2))


def length(interval):
    check_int(interval)

    return interval[1] - interval[0]


def interval_convolution(int1, int2):
    check_int(int1)
    check_int(int2)

    a1, b1 = int1[0], int1[1]
    a2, b2 = int2[0], int2[1]
    l1, l2 = length(int1), length(int2)

    if l1 == l2:
        # in this case one of the intervals would be a singleton, so we just need to consider the two intervals with
        # interior points.
        l = l1
        return [(a1 + a2, a1 + a2 + l),
                (a1 + a2 + l, b1 + b2)]

    else:
        return [(a1 + a2, a1 + a2 + min(l1, l2)),
                (a1 + a2 + min(l1, l2), a1 + a2 + max(l1, l2)),
                (a1 + a2 + max(l1, l2), b1 + b2)]


def multiset_interval_convolution(intervals1: list, intervals2: list):
    # takes to interval lists and returns all the intervals from the convolution of the two

    out = []

    for int1 in intervals1:
        for int2 in intervals2:
            out += interval_convolution(int1, int2)

    return out
