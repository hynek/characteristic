"""
A quick way to asses the impact of certain changes.
"""

from __future__ import absolute_import, division, print_function

from characteristic import attributes


class Artisanal(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


@attributes(["a", "b", "c"])
class NoDefaults(object):
    pass


@attributes(["a", "b", "c"], defaults={"c": 42})
class Defaults(object):
    pass


def bench_artisanal():
    Artisanal(a=1, b=2, c=3)


def bench_no_defaults():
    NoDefaults(a=1, b=2, c=3)


def bench_defaults():
    Defaults(a=1, b=2)


def bench_both():
    NoDefaults(a=1, b=2, c=3)
    Defaults(a=1, b=2)


if __name__ == "__main__":
    import timeit

    for func in ["bench_no_defaults", "bench_defaults", "bench_both",
                 "bench_artisanal"]:
        print(
            func + ": ",
            timeit.timeit(func + "()",
                          setup="from __main__ import {}".format(func))
        )
