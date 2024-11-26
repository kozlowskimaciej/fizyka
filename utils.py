def sign(val: float) -> int:
    if val > 0:
        return 1
    if val < 0:
        return -1
    return 0


def change_abs_value(val: float, change: float) -> float:
    return sign(val) * max((abs(val) + change), 0)
