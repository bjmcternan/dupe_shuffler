from enum import Enum

class PosTrait(Enum):
    UNKNOWN = 0
    BUFF = 1
    CAREGIVER = 2
    DIVERS_LUNGS = 3
    EARLY_BIRD = 4
    GERM_RESIST = 5
    GOURMET = 6
    GREASE_MONKEY = 7
    DECORATOR = 8
    IRON_GUT = 9
    MOLE = 10
    OWL = 11
    LEARNER = 12
    SIMPLE_TASTES = 13
    TWINKLE = 14
    UNCULTURED = 15


class NegTrait(Enum):
    UNKNOWN = 0
    ALLERGIES = 1
    ANEMIC = 2
    BIO = 3
    BOTTOMLESS = 4
    FLATULENT = 5
    GASTROPHOBIA = 6
    IBS = 7
    LOUD = 8
    MOUTH = 9
    NARCO = 10
    NOODLE = 11
    PACIFIST = 12
    SLOW = 13
    BLADDER = 14
    SQUEAMISH = 15
    YOKEL = 16


class Interests(Enum):
    NONE = 0
    ART = 1
    BUILD = 2
    CARE = 3
    COOK = 4
    DIG = 5
    FARM = 6
    OPERATE = 7
    RANCH = 8
    RESEARCH = 9
    SUIT = 10
    SUPPLY = 11
    TIDY = 12
