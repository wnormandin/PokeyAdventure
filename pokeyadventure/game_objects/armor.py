
from .core import CHA_SKILLS
from .items import Item

class Armor(Item):

    ''' Base class for Armor objects '''

    def __init__(self):
        super().__init__()
        self.level = 1  # <= player level to use
        self.ac = 1     # default bonus to ac
        self.equippable = True
        self.skills = []

class LeatherArmor(Armor):

    ''' Light leather armor '''

    def __init__(self):
        super().__init__()
        self.ac = 2
        self.skills.append('light_armor')

class IronArmor(Armor):

    ''' Heavy Iron Armor '''

    def __init__(self):
        super().__init__()
        self.ac = 3
        self.skills.append('heavy_armor')

class ClothArmor(Armor):

    ''' Cloth armor for caster types '''

    def __init__(self):
        super().__init__()
        self.skills.append('spells')
