__author__ = 'brighamhausman'


class Cardmeta:
    RANK_TYPE_MAJOR = 'major'
    RANK_TYPE_MINOR = 'minor'

    SUIT_TYPE_SWORDS = 'swords'
    SUIT_TYPE_WANDS = 'wands'
    SUIT_TYPE_PENTACLES = 'pentacles'
    SUIT_TYPE_CUPS = 'cups'
    SUIT_TYPE_TRUMPS = 'trumps'

    SUITS = [
        SUIT_TYPE_CUPS,
        SUIT_TYPE_PENTACLES,
        SUIT_TYPE_SWORDS,
        SUIT_TYPE_WANDS,
        SUIT_TYPE_TRUMPS
    ]

    RANKS = {RANK_TYPE_MINOR: {
        1: 'ace',
        2: '2',
        3: '3',
        4: '4',
        5: '5',
        6: '6',
        7: '7',
        8: '8',
        9: '9',
        10: '10',
        11: 'page',
        12: 'knight',
        13: 'queen',
        14: 'king'
    },
        RANK_TYPE_MAJOR: {
            0: 'the fool ',
            1: 'the magician ',
            2: 'the high priestess',
            3: 'the empress',
            4: 'the emperor',
            5: 'the heirophant',
            6: 'the lovers',
            7: 'the chariot',
            8: 'strength',
            9: 'the hermit',
            10: 'wheel of fortune',
            11: 'justice',
            12: 'the hanged man',
            13: 'death',
            14: 'temperance',
            15: 'the devil',
            16: 'the tower',
            17: 'the star',
            18: 'the moon',
            19: 'the sun',
            20: 'judgement',
            21: 'the world'
        }}


class Card:
    __suit = ''
    __rank = 0
    __cardmeta = Cardmeta()

    @property
    def suit(self):
        return self.__suit

    @suit.setter
    def suit(self, suit):

        if suit in self.__cardmeta.SUITS:
            self.__suit = suit

    @property
    def rank(self):
        return self.__rank

    @rank.setter
    def rank(self, rank):
        if not isinstance(rank, int):
            raise ValueError('rank must be int: {}'.format(rank))
        self.__rank = rank

    @property
    def meta(self):
        return self.__cardmeta

###TODO: tests,  should be imported...

def test_create_card():
    test_card = Card()
    assert(isinstance(test_card, Card))
    return test_card

def test_set_suit(card, new_suit):
    start_val = card.suit
    card.suit = new_suit
    end_val = card.suit
    return start_val != end_val




def run_tests():
    print('testing create')
    tc = test_create_card()
    print('card {}'.format(str(tc)))
    print('testing set suit success: {}'.format(test_set_suit(tc, tc.meta.SUIT_TYPE_CUPS)))

if __name__ == '__main__':
    run_tests()
