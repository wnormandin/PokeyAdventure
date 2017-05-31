
from .core import CHA_ATTRIBUTES
from .core import CHA_FACTIONS
from .core import CHA_STATUS_EFFECTS
from .core import CHA_SKILLS
from .core import CHA_SIZES
from .core import CHA_LANGUAGES
from .core import GameObject
from .core import stuple
from .items import Torch

# Player and NPC Race classes
# Race: parent class
# <Race Subclass>: subclass to contain each race's specific properties

class Race:

    ''' Parent class for character and NPC races '''

    def __init__(self):
        self.size = None
        self.speed = 30
        self.vision = 50
        self._subrace = False   # sub-race indicator

        # Race type indicators
        # For faction responses
        self._magical = False # fay, elf, dragonborn
        self._small = False   # dwarf, halfling, gnome
        self._beast = False   # orc, katman
        self._human = False   # highlander, human

        # Initialize attribute, bonus, skill, faction dicts
        self.advantages = []
        self.inventory = {'Torch': Torch()}
        self.languages = {lang: False for lang in CHA_LANGUAGES}
        self.bonuses = {attr: 0 for attr in CHA_ATTRIBUTES}
        self.factions = {faction: 0 for faction in CHA_FACTIONS}
        self.skills = {
            'darkvision': False
            }
        self.skills = {skill: False for skill in CHA_SKILLS}

        # Racial flags
        self.can_charm = True       # if true, race can be charmed/confused
        self.can_sleep = True       # if true, can be put to sleep
        self.can_paralyze = True    # if true, can be paralyzed
        self.languages['common'] = True

    def _post_init(self):
        self._default_factions()

    def _apply_faction(self, faction, amt):
        self.factions[faction] += amt

    def _default_factions(self):

        def apply_faction(vals):
            for key in vals:
                self._apply_faction(key, vals[key])

        # After assigning faction, run Race()._default_faction() to init
        if self._magical:
            values = {'magical': 5, 'small': -10, 'beast': 5}
            apply_faction(values)
        if self._small:
            values = {'magical': -10, 'small': 5, 'human': 5}
            apply_faction(values)
        if self._beast:
            values = {'magical': 5, 'human': -5}
            apply_faction(values)
        if self._human:
            values = {'beast': -5, 'small': 5}
            apply_faction(values)

class Dwarf(Race):

    ''' Sturdy mountain-folk with a penchant for fighting '''

    def __init__(self):
        super().__init__()
        self.size = CHA_SIZES['small']
        self.speed = 25
        self.vision = 45
        self._small = True
        self.bonuses['stamina'] = 2
        self.languages['mountain'] = True
        self.skills['sneak'] = True
        self._post_init()
        self.advantages.extend(['stamina', 'wisdom'])

class Elf(Race):

    ''' Magical long-living forest dwellers '''

    def __init__(self):
        super().__init__()
        self.size = CHA_SIZES['medium']
        self.speed = 35
        self.vision = 60
        self._magical = True
        self.bonuses['dexterity'] = 2
        self.languages['elvish'] = True
        self.skills['darkvision'] = True
        self._post_init()
        self.advantages.extend(['intelligence', 'wisdom'])

class Human(Race):

    ''' Your average guy, a good all-around character '''

    def __init__(self):
        super().__init__()
        # using default speed
        # using default vision range
        # only speaks common by default
        self.size = CHA_SIZES['medium']
        self._human = True
        self.bonuses = {attr: 1 for attr in CHA_ATTRIBUTES}
        self._post_init()
        self.advantages.extend(['charisma', 'stamina'])

RACE_LIST = Human, Dwarf, Elf
