from enums import PosTrait
from enums import NegTrait
from enums import Interests

class Dupe:
    def __init__(self):
        self.postrait = PosTrait.UNKNOWN
        self.negtrait = NegTrait.UNKNOWN
        self.interestt = Interests.NONE
        self.interestm = Interests.NONE
        self.interestb = Interests.NONE
        self.skip = False
