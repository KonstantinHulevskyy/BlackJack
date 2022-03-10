import abc
import random
from const import MESSAGES


class AbstractPlayer(abc.ABC):
    def __init__(self):
        self.cards = []
        self.bet = 0
        self.full_points = 0
        self.money = 100

    def change_points(self):
        self.full_points = sum([card.points for card in self.cards])

    def take_card(self, card):
        self.cards.append(card)
        self.change_points()

    def clear_hand(self):
        self.cards = []

    @abc.abstractmethod
    def change_bet(self, max_bet, min_bet):
        pass

    def print_cards(self):
        print("")
        print(self.name, "turn")
        for card in self.cards:
            print(card)
        print('Full points:', self.full_points)


class Player(AbstractPlayer):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.win = 0
        self.loose = 0
        self.blackjacks = 0
        self.buy_ins = 1
        self.eq = 0

    def change_bet(self, max_bet, min_bet):
        while True:
            value = int(input('Make your bet: '))
            if min_bet < value < max_bet:
                self.bet = value
                if self.money - self.bet >= 0:
                    self.money -= self.bet
                    break
                else:
                    print("You cant bet more than your bank:", self.money)
                    continue
        print('Your bet is:', self.bet)

    def ask_card(self):
        while True:
            choice = input(MESSAGES.get('ask_card'))
            if choice == 'y':
                return True
            elif choice == "n":
                return False
            else:
                continue

    def get_stats(self):
        print(self.name, f"stats: win = {self.win}\nloose = {self.loose}\n"
                         f"blackjacks = {self.blackjacks}\nbuy in = {self.buy_ins}\n"
                         f"equals = {self.eq}\ncurrent bank = {self.money}")


class Bot(AbstractPlayer):
    def __init__(self, name):
        self.name = name
        super().__init__()
        self.max_points = random.randint(17, 21)

    def change_bet(self, max_bet, min_bet):
        self.bet = random.randint(min_bet, self.money)
        self.money -= self.bet
        print(self.name, 'give:', self.bet)

    def ask_card(self):
        if self.full_points < self.max_points:
            return True
        else:
            return False


class Dealer(AbstractPlayer):
    max_points = 17

    def __init__(self):
        super().__init__()
        self.name = "Dealer"

    def change_bet(self, max_bet, min_bet):
        """
        NOTE: This type is Dealer so it has no bets
        """""
        raise Exception('This type is dealer so it has no bets')

    def ask_card(self):
        if self.full_points < self.max_points:
            return True
        else:
            return False
