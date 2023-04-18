import os
import sys
import math
import argparse
import pygame

N = 50
BLOCK_SIZE = 10

getBit = lambda i, n: i >> n & 1
neighbors = lambda x: [
    x - 1,
    x + 1,
    x - N,
    x + N,
    x - N - 1,
    x - N + 1,
    x + N - 1,
    x + N + 1,
]
count = lambda i, x: sum(map(lambda z: getBit(i, z) if z > -1 else 0, neighbors(x)))


def bits(n):
    while n:
        b = n & (~n + 1)
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
        index = int(math.log(b, 2))

        n = count(i, index)
        if n < 2 or n > 3:
            j = setBit(j, index, 0)

        for neighbor in neighbors(index):
            if (
                neighbor > -1
                and (neighbor // N) < N
                and (neighbor % N != 0)
                and count(i, neighbor) == 3
            ):
                j = setBit(j, neighbor, 1)

    return j


def get_coords(i):
    for b in bits(i):
        index = int(math.log(b, 2))
        x, y = index % N, index // N
        yield x, y


def parse(s):
    s = s.replace(" ", "")
    s = s.replace(".", "0")
    s = s.replace("O", "1")

    p = N - s.index("\n")
    if p > 0:
        s = s.replace("\n", "0" * p)
    else:
        s = s.replace("\n", "")

    s = s[::-1]
    return s


def main(args):
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

        f = open(path, mode="r")
        s = parse(f.read())
        f.close()
        s = "0" * 10 * N + s

    i = int(s, 2)

    # pygame setup
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)

    pygame.init()
    fps = pygame.time.Clock()
    pygame.display.set_caption('Conway\'s Game of Life - Press "q" to quit.')

    window_x, window_y = 512, 512
    game_window = pygame.display.set_mode((window_x, window_y))
    game_window.fill(black)

    gen = 0
    while True:
        # handling key events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        # draw
        game_window.fill(black)
        for x, y in get_coords(i):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(game_window, white, rect)
        pygame.display.update()
        fps.tick(args.speed)

        # step
        i = step(i)
        gen += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument("-s", "--seed", help="path to seed")
    parser.add_argument("--speed", help="game speed", default=10, type=int)
    args = parser.parse_args()
    try:
        main(args)
    except KeyboardInterrupt:
        sys.stderr.write("\nExiting by user request.\n")
        sys.exit(0)
