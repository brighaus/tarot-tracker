__author__ = 'brighamhausman'



from models.card import Card
import datetime

class Daily_TT():
    __date = None
    __card = None

    def __init__(self, date = datetime.date.today(), card = Card()):
        self.__date = date
        self.__card = card

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        if not isinstance(date, datetime.date):
            raise ValueError('expected datetime.date() got {}'.format(str(date)))
        self.__date = date

    @property
    def card(self):
        return self.__card

    @card.setter
    def card(self, card):
        self.__card = card


if __name__ == '__main__':
    # create a Daily_TT
    dtt = Daily_TT()
    assert isinstance(dtt, Daily_TT), "Daily_TT did not instantiate!"
    print('Daily_TT object exists')
    card = Card()
    print(str(card))
