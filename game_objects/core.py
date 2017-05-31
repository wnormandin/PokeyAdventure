
import operator
import random
import pygame


# Globals and utility functions/classes

# !! Put these in __init__.py
INITIAL_STAT_SUM = 18

# Default core attributes
CHA_ATTRIBUTES = (
    'strength',
    'stamina',
    'dexterity',
    'wisdom',
    'intelligence',
    'charisma'
    )

# Default Languages
CHA_LANGUAGES = {
    'common',
    'mountain',
    'elvish',
    'beast',
    'dragon',
    'celestial'
    }

# Character sizes
CHA_SIZES = {
    'small': -1,
    'medium': 0,
    'large': 1
    }

# Default factions
CHA_FACTIONS = (
    'magical',
    'small',
    'beast',
    'human',
    'guards',
    'thieves',
    'mages',
    'merchant'
    )

# Default status effects
CHA_STATUS_EFFECTS = (
    'blind',
    'paralyzed',
    'slowed',
    'silenced'
    )

# Character base skill list
CHA_SKILLS = (
    'darkvision',
    'spells',
    'slashing',
    'piercing',
    'sneak',
    'blunt',
    'heavy_armor',
    'light_armor'
    )


class stuple(tuple):

    ''' Special tuple, allows addition '''

    def __add__(self, other):
        try:
            return self.__class__(map(operator.add, self, other))
        except:
            raise ValueError('add operation failed: {}::{}'.format(
                                self, other))


class MapGrid:

    ''' Primary game grid containing all game objects '''

    def __init__(self, map_size, view_dims, start_pos=stuple((0, 0)), default=None):
        self.y_cells, self.x_cells = map_size
        self.y_px, self.x_px = view_dims
        self.tile_size = GameObject.CELL_SIZE
        self.set_visible_size()
        self.visible_cells(start_pos) # Not capturing returned vals for now
        self.map = self.gen_matrix()
        self.default_tile = default
        self.map_surface()

    def set_visible_size(self):
        self.y_view = 20    # Test values, dynamic later, perhaps?
        self.x_view = 25

    def map_surface(self):
        # Create a surface for the main map
        self.map_s = pygame.Surface((self.x_px, self.y_px))

    def visible_cells(self, player_position):
        # Return visible cells based on player position
        # return: ((y, x), (y1, x1),..), (y0, x0) where
        #   (y, x), (y1, x1),.. are valid coordinates &
        #   (y0, x0) is the view origin
        y, x = player_position
        y_offset = int(self.y_view / 2)
        x_offset = int(self.x_view / 2)

        # Create test y0, x0, then set based on valid range
        # MapGrid.valid tests a point part and ensures it does
        # not exceed the map boundaries
        test_y, test_x = y - y_offset, x - x_offset
        off_y = self.valid(test_y + self.y_view, True)
        off_x = self.valid(test_x + self.x_view)
        y0 = self.valid(off_y - self.y_view, True)
        x0 = self.valid(off_x - self.x_view)

        # Set the view origin and return
        self.view_origin = y0, x0
        return (stuple((y_val, x_val))
                for y_val in range(y0, y0 + self.y_view)
                for x_val in range(x0, x0 + self.x_view)), (y0, x0)

    def valid(self, val, is_y=False):
        if is_y:
            limit = self.y_cells
        else:
            limit = self.x_cells

        if val < 0:
            return 0
        elif val > limit:
            return limit
        else:
            return val

    def gen_matrix(self):
        return {stuple((y, x)): {
            'tile': None,
            'player': None,
            'items': {},
            'npcs': {}
            } for y in range(self.y_cells) for x in range(self.x_cells)}

    def fill_matrix(self, gen, test=False):
        if test:
            lvl_gen = gen(self.map, (self.y_cells, self.x_cells), test)
            lvl_gen.prep()
            lvl_gen.generate()
            self.start_point = lvl_gen.start_point
            self.end_point = lvl_gen.end_point
            # for tile in self.map:
            #    if def_tile is not None:
            #        obj = def_tile(tile)
            #        obj._load_image()
            #    else:
            #        obj = def_tile
            #    self.map[tile]['tile'] = obj
        else:
            pass    # Not yet implemented

    def get(self, pos, item=None):
        y, x = pos
        if item is not None:
            return self.map[x, y][item]
        return self.map[y, x]

    def random(self, get=False):
        # Return random position (or tile if get)
        choice = random.choice(list(self.map))
        if get:
            return self.get(choice, 'tile')
        else:
            return choice


class GameObject:

    ''' Superclass for in-game objects '''

    CELL_SIZE = 25
    NORTH = UP = stuple((-1, 0))
    SOUTH = DOWN = stuple((1, 0))
    EAST = RIGHT = stuple((0, 1))
    WEST = LEFT = stuple((0, -1))
    MAP_DIRS = NORTH, SOUTH, EAST, WEST
    VIEW_DIRS = UP, DOWN, RIGHT, LEFT

    def __init__(self, pos=None):
        self.position = pos
        self.active = False

    def move(self, direction=stuple((0, 0))):
        self.position += direction

    def _pt_distance(self, pt):
        x, y = self.position
        return abs(pt[1] - y), abs(pt[0] - x)

    @property
    def dist_to_obj(self, obj):
        return self._pt_distance(obj.position)

    @property
    def x_min(self):
        # Absolute min, not visible (must be offset)
        if self.position is not None:
            try:
                return self.position[1] * self.CELL_SIZE
            except AttributeError:
                raise AttributeError('GameObject.position not set')

    @property
    def y_min(self):
        # Absolute min, not visible (must be offset)
        if self.position is not None:
            try:
                return self.position[0] * self.CELL_SIZE
            except AttributeError:
                raise AttributeError('GameObject.position not set')

