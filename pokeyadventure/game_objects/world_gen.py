
import random

# Parent Classes (For generic/test maps)
from .tiles import MossyFloor
from .tiles import BarnDoor
from .tiles import LavaFloor
from .tiles import WoodWall
from .tiles import SnowFloor
from .tiles import BrickWall
from .tiles import BrickFloor
from .tiles import WoodDoor
from .tiles import TudorWall
from .tiles import ScreenFloor


class LevelGenerator:

    # Defaults
    DEF_WALL = BrickWall
    DEF_FLOOR = ScreenFloor
    DEF_DOOR = WoodDoor

    def __init__(self, canvas, bounds, test=False):
        self.max_y, self.max_x = bounds
        self.canvas = canvas
        self.test = test
        self.prepped = False

    def prep(self):
        if self.test:
            self.wall = self.DEF_WALL
            self.floor = self.DEF_FLOOR
            self.door = self.DEF_DOOR
        else:
            pass    # Not implemented
        self.prepped = True

    def generate(self):
        self._fill_walls()
        self.start_point = self._start_point()
        self.end_point = self._end_point()
        self._connect_points(self.start_point, self.end_point, self.floor)
        self._instantiate_canvas()

    # Private methods
    def _instantiate_canvas(self):
        # Lazy instantiation of map objects
        for tile in self.canvas:
            tile_obj = self.canvas[tile]['tile']
            self.canvas[tile]['tile'] = tile_obj(tile)

    def _fill_walls(self):
        assert self.prepped
        for tile in self.canvas:
            self.canvas[tile]['tile'] = self.wall

    def _random_point(self):
        valid = [(y, x) for y in range(3, self.max_y -3)
                        for x in range(3, self.max_x - 3)]
        return random.choice(valid)

    def _start_point(self):
        while True:
            test_pt = self._random_point()
            self.canvas[test_pt]['tile'] = self.door
            return test_pt

    def _connect_points(self, p1, p2, tile=None):
        if tile is None:
            tile = self.DEF_FLOOR
        y_dist, x_dist = p1[0] - p2[0], p1[1] - p2[1]
        loop_max_y = min(self.max_y -1, p1[0] + y_dist)
        loop_max_x = min(self.max_x -1, p1[1] + x_dist)
        for y in range(p1[0], loop_max_y):
            for x in range(p1[1], loop_max_x):
                self.canvas[y, x]['tile'] = tile

    def _point_distance(self, p1, p2):
        y_dist = abs(p1[0] - p2[0])
        x_dist = abs(p1[1] - p2[1])
        return y_dist, x_dist

    def _end_point(self):
        while True:
            test_pt = self._random_point()
            start_distance = self._point_distance(self.start_point, test_pt)
            if start_distance[0] > 10 and start_distance[1] > 10:
                self.canvas[test_pt]['tile'] = self.door
                return test_pt
