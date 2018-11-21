def frange(x, y, jump):
    while x < y:
        yield x
        x += jump


def sgn(x: float) -> float:
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0
