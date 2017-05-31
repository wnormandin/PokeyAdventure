
from .core import GameObject


class Item(GameObject):

    ''' Base class for items, weapons, and Armor '''

    SMALL_ITEM = -1
    NORMAL_ITEM = 0
    LARGE_ITEM = 1

    def __init__(self, pos=None):
        self.pos = None
        self.weight = 0.1
        self.slots = 0      # Slots can hold other items
        self.size = Item.NORMAL_ITEM
        self.equipped = False
        self.equippable = False
        self.consumable = False
        self.usage_verb = 'use'

    def equip(self):
        if self.equippable:
            self.equipped = True
        else:
            self.equipped = False
        return self.equipped

class Torch(Item):
    pass
