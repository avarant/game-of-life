import os
import sys
import math
import argparse
import pygame
import logging

logging.basicConfig(
    format="%(message)s",
    level=logging.DEBUG,
)
log = logging.getLogger(__name__)


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

BG_COLOR = pygame.Color(0, 0, 0)
BLOCK_COLOR = pygame.Color(255, 255, 255)


class GameOfLife:
    def __init__(self, seed=None, render=False, speed=10):
        # default seed is glider gun
        if seed is None:
            self.seed = GLIDER_GUN[1:]
        else:
            self.seed = seed
        # current state represented as a binary integer
        self._state = GameOfLife._parse(self.seed)
        self._gen = 0  # generation (step)

        self._render = render
        self._speed = speed

        # pygame setup
        if render:
            pygame.init()
            pygame.display.set_caption('Conway\'s Game of Life - Press "q" to quit.')
            window_x, window_y = N * BLOCK_SIZE, N * BLOCK_SIZE
            self._canvas = pygame.display.set_mode((window_x, window_y))
            self.render()

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

        if self._render:
            self.render()

        return j

    def get_state(self):
        """
        Returns the current state of the game as generator of (x, y) coordinates.
        """
        for b in GameOfLife._bits(self._state):
            index = int(math.log(b, 2))
            x, y = index % N, index // N
            yield x, y

    def render(self):
        self._canvas.fill(BG_COLOR)
        for x, y in self.get_state():
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(self._canvas, BLOCK_COLOR, rect)
        pygame.display.update()
        pygame.time.Clock().tick(self._speed)


def main(args):
    path_to_seed = args.seed
    seed = None
    if path_to_seed is not None:
        if not os.path.isfile(path_to_seed):
            log.error("Error: %s not found" % path_to_seed)
            sys.exit()

        with open(path_to_seed, "r") as f:
            seed = f.read()

    env = GameOfLife(seed=seed, render=True, speed=args.speed)

    while True:
        # handle key events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

                elif args.debug and event.key == pygame.K_RIGHT:
                    env.step()

        if args.debug:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                env.step()
        else:
            env.step()


def parse_args():
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument(
        "-s", "--seed", default=None, help="path to seed (defaults to glide gun)"
    )
    parser.add_argument("--speed", help="game speed", default=10, type=int)
    parser.add_argument("--debug", help="debug mode", action="store_true")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    try:
        args = parse_args()
        main(args)
    except KeyboardInterrupt:
        sys.stderr.write("\nExiting by user request.\n")
        sys.exit(0)
