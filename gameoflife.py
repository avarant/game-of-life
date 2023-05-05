import os
import sys
import math
import argparse
import pygame


GLIDER_GUN = """
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

N = 50
BLOCK_SIZE = 10  # pygame window block size


class GameOfLife:
    def __init__(self, seed=None):
        # default seed is glider gun
        if seed is None:
            self.seed = GLIDER_GUN[1:]
        else:
            self.seed = seed
        self._state = GameOfLife._parse(
            self.seed
        )  # current state represented as a binary integer
        self._gen = 0  # generation (step)

    @staticmethod
    def _parse(s):
        s = s.replace(" ", "")
        s = s.replace(".", "0")
        s = s.replace("O", "1")

        p = N - s.index("\n")
        if p > 0:
            s = s.replace("\n", "0" * p)
        else:
            s = s.replace("\n", "")

        s = s[::-1]
        return int(s, 2)

    @staticmethod
    def _get_bit(i, n):
        return i >> n & 1

    @staticmethod
    def _get_neighbors(x):
        return [
            x - 1,
            x + 1,
            x - N,
            x + N,
            x - N - 1,
            x - N + 1,
            x + N - 1,
            x + N + 1,
        ]

    @staticmethod
    def _count_neighbors(i, x):
        f = lambda z: GameOfLife._get_bit(i, z) if z > -1 else 0
        return sum(map(f, GameOfLife._get_neighbors(x)))

    @staticmethod
    def _bits(n):
        while n:
            b = n & (~n + 1)
            yield b
            n ^= b

    @staticmethod
    def _set_bit(num, ind, val):
        mask = 1 << ind
        num &= ~mask
        if val:
            num |= mask
        return num

    def step(self):
        j = self._state

        for b in GameOfLife._bits(self._state):
            index = int(math.log(b, 2))

            n = GameOfLife._count_neighbors(self._state, index)
            if n < 2 or n > 3:
                j = GameOfLife._set_bit(j, index, 0)

            for neighbor in GameOfLife._get_neighbors(index):
                if (
                    neighbor > -1
                    and (neighbor // N) < N
                    and (neighbor % N != 0)
                    and GameOfLife._count_neighbors(self._state, neighbor) == 3
                ):
                    j = GameOfLife._set_bit(j, neighbor, 1)

        self._state = j
        return j

    def get_state(self):
        """
        Returns the current state of the game as generator of (x, y) coordinates.
        """
        for b in GameOfLife._bits(self._state):
            index = int(math.log(b, 2))
            x, y = index % N, index // N
            yield x, y


def main(args):
    path_to_seed = args.seed

    seed = None
    if path_to_seed is not None:
        if not os.path.isfile(path_to_seed):
            print("Error: %s not found" % path_to_seed)
            sys.exit()

        with open(path_to_seed, "r") as f:
            seed = f.read()

    env = GameOfLife(seed)

    # pygame setup
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)

    pygame.init()
    fps = pygame.time.Clock()
    pygame.display.set_caption('Conway\'s Game of Life - Press "q" to quit.')

    window_x, window_y = N * BLOCK_SIZE, N * BLOCK_SIZE
    game_window = pygame.display.set_mode((window_x, window_y))
    game_window.fill(black)

    while True:
        # handle key events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        # draw
        game_window.fill(black)
        for x, y in env.get_state():
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(game_window, white, rect)
        pygame.display.update()
        fps.tick(args.speed)

        env.step()


def parse_args():
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument(
        "-s", "--seed", default=None, help="path to seed (defaults to glide gun)"
    )
    parser.add_argument("--speed", help="game speed", default=10, type=int)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    try:
        args = parse_args()
        main(args)
    except KeyboardInterrupt:
        sys.stderr.write("\nExiting by user request.\n")
        sys.exit(0)
