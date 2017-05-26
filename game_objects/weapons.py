
from .core import CHA_SKILLS
from .items import Item

class Weapon(Item):

    FAST_SPEED = 1
    NORMAL_SPEED = 0
    SLOW_SPEED = -1

    ''' Base class for Weapon objects '''

    def __init__(self):
        super().__init__()
        self.level = 1  # <= player level to use
        self.dmg = 2    # bonus to damage
        self.skills = []    # required skills to use weapon
        self.equippable = True
        self.speed = Weapon.NORMAL_SPEED

class Sword(Weapon):

    ''' Slashing weapon '''

    def __init__(self):
        super().__init__()
        self.skills.append('slashing')

class Mace(Weapon):

    ''' Blunt weapon '''

    def __init__(self):
        super().__init__()
        self.skills.append('blunt')
        self.dmg = 3
        self.speed = Weapon.SLOW_SPEED

class Dagger(Weapon):

    ''' Piercing Weapon '''

    def __init__(self):
        super().__init__()
        self.skills.append('piercing')
        self.dmg = 1
        self.speed = Weapon.FAST_SPEED


class Staff(Weapon):

    ''' Magic user's weapon '''

    def __init__(self):
        super().__init__()
        self.skills.append('blunt')
        self.skills.append('spells')
        self.speed = Weapon.SLOW_SPEED
