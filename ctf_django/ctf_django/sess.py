import random

def randomword():
    rand = "%032x" % random.getrandbits(128)
    if rand[:13] == 'administrator':
        return randomword()
    return rand[:13]
