
from .core import CHA_ATTRIBUTES
from .core import CHA_FACTIONS
from .core import CHA_STATUS_EFFECTS
from .core import CHA_SKILLS
from .core import CHA_SIZES
from .core import CHA_LANGUAGES
from .weapons import Sword, Mace, Dagger, Staff
from .armor import LeatherArmor, ClothArmor, IronArmor

class Background:

    ''' Parent class for player background objects '''

    def __init__(self):
        self.bonuses = {attr: 0 for attr in CHA_ATTRIBUTES}
        self.factions = {fact: 0 for fact in CHA_FACTIONS}
        self.skills = {skill: False for skill in CHA_SKILLS}
        self.languages = {lang: False for lang in CHA_LANGUAGES}
        self.advantages = []
        self.inventory = {}

class Soldier(Background):

    ''' War is your background, for better or worse '''

    def __init__(self):
        super().__init__()
        self.factions['guards'] += 5
        self.factions['thieves'] -= 5
        self.skills['light_armor'] = True
        self.advantages.extend(['stamina', 'strength'])
        self.inventory['Leather Armor'] = LeatherArmor()

class Urchin(Background):

    ''' You grew up on the streets and learned well from them '''

    def __init__(self):
        super().__init__()
        self.factions['thieves'] += 5
        self.factions['merchants'] -= 5
        self.skills['sneak'] = True
        self.advantages.extend(['dexterity', 'charisma'])

class Acolyte(Background):

    ''' You have apprenticed with a mage of some power '''

    def __init__(self):
        super().__init__()
        self.factions['mages'] += 5
        self.skills['spells'] = True
        self.languages['dragon'] = True
        self.advantages.extend(['wisdom', 'intelligence'])

class Charlatan(Background):

    ''' You specialize in confidence games to make a living '''

    def __init__(self):
        super().__init__()
        self.factions['guards'] -= 5
        self.factions['thieves'] += 5
        self.skills['sneak'] = True
        self.advantages.extend(['intelligence', 'dexterity'])

BG_LIST = Soldier, Urchin, Acolyte, Charlatan
