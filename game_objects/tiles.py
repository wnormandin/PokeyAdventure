import pygame
import os
import random
import operator


class stuple(tuple):
    def __add__(self, other):
        try:
            return self.__class__(map(operator.add, self, other))
        except:
            return ValueError('add operation failed: {}::{}'.format(self, other))


class MapGrid:

    NORTH = UP = stuple((-1, 0))
    SOUTH = DOWN = stuple((1, 0))
    EAST = RIGHT = stuple((0, 1))
    WEST = LEFT = stuple((0, -1))
    MAP_DIRS = NORTH, SOUTH, EAST, WEST
    VIEW_DIRS = UP, DOWN, RIGHT, LEFT

    def __init__(self, map_size, tile_size, start_pos=stuple((0, 0))):
        self.h_cells, self.v_cells = map_size
        self.view_h = int(self.h_cells * 0.75)
        self.view_v = int(self.v_cells * 0.75)
        self.tile_size = tile_size
        self.map = self.gen_matrix()
        self.map_view_origin = start_pos

    @property
    def view_center(self):
        ''' Returns the approximate center visible cell '''
        top = self.view_h_orig
        bottom = self.view_h_edge
        left = self.view_v_orig
        right = self.view_v_edge
        return top + int(self.view_h / 2), left + int(self.view_v / 2)

    @property
    def view_h_orig(self):
        ''' Returns the viewable left-most column '''
        return self.map_view_origin[0]

    @property
    def view_v_orig(self):
        ''' Returns the viewable top-most row '''
        return self.map_view_origin[1]

    @property
    def view_h_edge(self):
        ''' Returns the viewable right-most column '''
        return self.map_view_origin[0] + self.view_h

    @property
    def view_v_edge(self):
        ''' Returns the viewable bottom row '''
        return self.map_view_origin[1] + self.view_v

    @property
    def viewable(self):
        ''' Returns a dictionary containing the visible map '''
        out_dict = {}
        for y in range(self.view_h_orig, self.view_h_edge):
            for x in range(self.view_v_orig, self.view_v_edge):
                key = stuple((y - self.view_h_orig, x - self.view_v_orig))
                out_dict[key] = self.map(y, x)
                # Add values representing min/max pixels
                out_dict[key]['y_min'] = key[0] * self.tile_size
                out_dict[key]['x_min'] = key[1] * self.tile_size
                out_dict[key]['y_max'] = (key[0] * self.tile_size) + self.tile_size
                out_dict[key]['x_max'] = (key[1] * self.tile_size) + self.tile_size
        return out_dict

    @property
    def valid_shift(self):
        return [d for d in self.MAP_DIRS if (self.map_view_origin + d) in self.map]

    def shift(self, direction=stuple((0, 0))):
        valid = self.valid_shift
        valid.append(stuple((0, 0)))
        if direction in valid:
            self.map_view_origin += direction

    def gen_matrix(self):
        return {stuple((y, x)): {
                'tile': None,
                'player': None,
                'items': {},
                'npcs': {}
                } for y in range(self.v_cells) for x in range(self.h_cells)}

    def fill_matrix(self, test=False):
        if test:
            for tile in self.map:
                obj = Tile()
                obj._load_image()
                self.map[tile]['tile'] = obj
        else:
            pass    # Not yet implemented

    def get(self, pos, item=None):
        y, x = pos
        if item is not None:
            return self.map[y, x][item]
        return self.map[y, x]

    def random(self, get=False):
        # Return a random map position, or tile if get is True
        choice = random.choice(list(self.map))
        if get:
            return self.get(choice)
        return choice


class Tile:

    def __init__(self):
        self.passable = True    # Determines whether char can pass through tile
        self.locked = False
        self.image_base_path = 'resources/textures'
        self.image_filename = 'black_wood_wall_25px.png'
        self.traps = []
        self.metachar = '#'

    def _load_image(self):
        file_path = os.path.join(os.getcwd(), self.image_base_path)
        file_path = os.path.join(file_path, self.image_filename)
        self.image = pygame.image.load(file_path)


class Floor:

    def __init__(self):
        self.damage = 0 # Assign for DPS
        self.false = False # Indicate whether this is a false door
        self.false_image = ''


class Door:

    def _toggle_lock(self):
        self.locked = not self.locked
        self.passable = not self.locked


class Wall:

    def __init__(self):
        self.passable = False


class MossyFloor(Tile, Floor):

    def __init__(self):
        super().__init__()
        self.image_filename = 'mossy_floor_25px.png'
        self._load_image()
        self.metachar = 'm'


class BarnDoor(Tile, Door):

    def __init__(self):
        super().__init__()
        self.image_filename = 'barn_door_25px.png'
        self._load_image()
        self.metachar = 'D'


class LavaFloor(Tile, Floor):

    def __init__(self):
        super().__init__()
        self.image_filename = 'fire_ground_25px.png'
        self._load_image()
        self.metachar = 'L'
        self.damage = 1


class WoodWall(Tile, Wall):

    def __init__(self):
        super().__init__()
        self.image_filename = 'interior_wood_wall_25px.png'
        self._load_image()
        self.metachar = 'W'


class SnowFloor(Tile, Floor):

    def __init__(self):
        super().__init__()
        self.image_filename = 'snowy_path_25px.png'
        self._load_image()
        self.metachar = 'S'


class BrickWall(Tile, Wall):

    def __init__(self):
        super().__init__()
        self.image_filename = 'red_brick_25px.png'
        self._load_image()
        self.metachar = 'w'


class WoodDoor(Tile, Door):

    def __init__(self):
        super().__init__()
        self.image_filename = 'wooden_door_25px.png'
        self._load_image()
        self._toggle_lock() # Start locked
        self.metachar = 'd'


class Curtain(Tile):

    RED = 0
    BLUE = 1

    def __init__(self, color=0):
        super().__init__()
        template = 'curtain_{}_25px.png'
        if color == Curtain.RED:
            template.format('red')
        elif color == Curtain.BLUE:
            template.format('blue')
        else:
            raise ValueError("Color {} not found".format(color))
        self._load_image()
        self.metachar = 'C'


class TudorWall(Tile, Wall):

    def __init__(self):
        super().__init__()
        self.image_filename = 'interior_wood_wall_25px.png'
        self._load_image()
        self.metachar = 'T'


class BrickFloor(Tile):

    def __init__(self):
        super().__init__()
        self.image_filename = 'gray_brick_25px.png'
        self._load_image()
        self.metachar = 'B'
