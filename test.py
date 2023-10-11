import math
def round_up(n, decimals=0):
    multiplier = 10**decimals
    return math.ceil(n * multiplier) / multiplier
print(round_up(45298438473294,-6)/1e6)