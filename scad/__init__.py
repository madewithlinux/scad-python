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


def linspace(start, stop, num=50, endpoint=True):
    num = int(num)
    start = start * 1.
    stop = stop * 1.

    if num == 1:
        yield stop
        return
    if endpoint:
        step = (stop - start) / (num - 1)
    else:
        step = (stop - start) / num

    for i in range(num):
        yield start + step * i
