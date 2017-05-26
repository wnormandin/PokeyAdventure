import operator


class stuple(tuple):
    def __add__(self, other):
        try:
            return self.__class__(map(operator.add, self, other))
        except:
            return ValueError('map operation failed: {}:{}'.format(self, other))


class MapManager:

    ''' Class to manage the viewable area, minimap, and other map functions '''

    # directions in (y, x) format
    NORTH = UP = stuple((-1, 0))
    SOUTH = DOWN = stuple((1, 0))
    EAST = RIGHT = stuple((0, 1))
    WEST = LEFT = stuple((0, -1))
    MAP_DIRS = NORTH, SOUTH, EAST, WEST
    VIEW_DIRS = UP, DOWN, RIGHT, LEFT

    def __init__(self, game_map, view_dim, size=25):
        self.game_map = game_map
        self.tile_size = size
        self.y_dim, self.x_dim = view_dim
        self.map_view_origin = stuple((0, 0))

    @property
    def top_edge(self):
        return 

    @property
    def bottom_edge(self):

    @property
    def left_edge(self):

    @property
    def right_edge(self):

    @property
    def viewable(self):
        return None

    def shift(self, direction=stuple((0, 0))):
        valid = list(self.MAP_DIRS)
        valid.append(stuple((0, 0)))
        assert direction in valid
        self.map_view_origin += direction

    def show_origin(self):
        print(self.map_view_origin)

if __name__ == '__main__':
    mm = MapManager(600, 800)
    mm.shift(mm.SOUTH)
    mm.show_origin()
    mm.shift(mm.EAST)
    mm.show_origin()
    mm.shift(mm.NORTH)
    mm.show_origin()
    mm.shift(mm.WEST)
    mm.show_origin()
