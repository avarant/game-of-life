import os
import argparse
from math import log
from time import sleep
from tcanvas import TCanvas 

N = 50
STEPS = 1000
DELAY = .05

getBit = lambda i, n: i >> n & 1
neighbors = lambda x: [x-1, x+1, x-N, x+N, x-N-1,x-N+1, x+N-1, x+N+1]
count = lambda i, x: sum(map(lambda z: getBit(i,z) if z > -1 else 0, neighbors(x)))

def bits(n):
    while n:
        b = n & (~n+1)
        yield b
        n ^= b

def setBit(num, ind, val):
    mask = 1 << ind
    num &= ~mask
    if val:
        num |= mask
    return num
        
def step(i):
    j = i

    for b in bits(i):
        index = int(log(b,2))

        n = count(i, index)
        if n < 2 or n > 3:
            j = setBit(j, index, 0)

        for neighbor in neighbors(index):
            if neighbor > -1 and (neighbor // N) < N and (neighbor % N != 0) and count(i, neighbor) == 3:
                j = setBit(j, neighbor, 1)
        
    return j



def draw(canvas, i):
    canvas.clear()
    for b in bits(i):
        index = int(log(b,2))
        x, y = index % N, index // N
        canvas.fill(x, y)
    return canvas.refresh()


def parse(s):
    s = s.replace(' ','')
    s = s.replace('.', '0')
    s = s.replace('O', '1')
 
    p = N - s.index('\n')
    if p > 0:
        s = s.replace('\n', '0'*p)
    else:
        s = s.replace('\n', '')

    s = s[::-1]
    return s

    
def main():

    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument("-s", "--seed", help="path to seed")
    args = parser.parse_args()

    glider_gun = """
    ........................O...........
    ......................O.O...........
    ............OO......OO............OO
    ...........O...O....OO............OO
    OO........O.....O...OO..............
    OO........O...O.OO....O.O...........
    ..........O.....O.......O...........
    ...........O...O....................
    ............OO......................
    """
    glider_gun = glider_gun[1:]

    path = args.seed
    if not path:
        s = parse(glider_gun)
    else:
        if not os.path.isfile(path):
            print("Error: %s not found" % path)
            sys.exit()

        f = open(path, mode='r')
        s = parse(f.read())
        f.close()
        s = '0' * 10 * N + s

    i = int(s, 2)

    canvas = None
    try:
        canvas = TCanvas(N, N)
        gen = 0
        inp = None
        while gen < STEPS and inp != ord('q'):
            inp = draw(canvas, i)
            i = step(i)
            sleep(DELAY)
            gen += 1
    except:
        raise
    finally:
        if canvas:
            canvas.exit()

if __name__ == "__main__":
    main() 


