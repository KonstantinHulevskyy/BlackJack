import Player
from Deck import Deck
from const import MESSAGES, NAMES
import random


class Game:
    max_pl_count = 4

    def __init__(self):
        self.players = []
        self.lost_players = []
        self.player = None
        self.player_pos = None
        self.dealer = Player.Dealer()
        self.all_players_count = 1
        self.deck = Deck()
        self.max_bet, self.min_bet = 101, 0

    @staticmethod
    def _ask_starting(message):
        while True:
            choice = input(message)
            if choice == 'n':
                return False
            elif choice == 'y':
                return True

    def _launching(self):
        while True:
            bots_count = int(input('Hello, write bots count '))
            if bots_count <= self.max_pl_count - 1:
                break
        self.all_players_count = bots_count + 1
        used_names = []
        for _ in range(bots_count):
            name = random.choice(NAMES)
            b = Player.Bot(name)
            while name in used_names:
                name = random.choice(NAMES)
            self.players.append(b)
            used_names.append(name)
            print(b.name, 'Bot is created')
        self.player = Player.Player(input("Type your name: "))
        self.player_pos = random.randint(0, self.all_players_count)
        print('Your position is:', self.player_pos)
        self.players.insert(self.player_pos, self.player)

    def ask_bet(self):
        while self.player.money <= 0:
            no_bank = input(MESSAGES.get("no_bank"))
            if no_bank == "y":
                self.player.money += 100
                print("Giving credit for", (self.player.name + ". New bank equals 100$"))
                self.player.buy_ins += 1
            elif no_bank == "n":
                exit(1)
        for player in self.players:
            player.change_bet(self.max_bet, self.min_bet)

    def first_descr(self):
        for player in self.players:
            for _ in range(2):
                card = self.deck.get_card()
                player.take_card(card)
        card = self.deck.get_card()
        self.dealer.take_card(card)
        self.dealer.print_cards()
        if self.player.full_points == 21:
            self.blackjack(self.player)

    def check_stop(self, player):
        for card in player.cards:
            if player.full_points > 21:
                if card.rank == "A":
                    card.points = 1
                    self.player.change_points()
            else:
                break
        if player.full_points > 21:
            return True
        else:
            return False

    def blackjack(self, player):
        player.print_cards()
        if isinstance(player, Player.Player):
            print('Its Blackjack!')
            self.player.blackjacks += 1
        elif isinstance(player, Player.Bot):
            print(player.name, 'got Blackjack')
        self.player.money += self.player.bet * 3
        blackjack_player = self.players.pop(self.players.index(player))
        self.lost_players.append(blackjack_player)

    def remove_player(self, player):
        player.print_cards()
        if isinstance(player, Player.Player):
            print(f'{self.player.name} lost the game!')
            self.player.loose += 1
        elif isinstance(player, Player.Bot):
            print(player.name, 'have lost!')
        lost_player = self.players.pop(self.players.index(player))
        self.lost_players.append(lost_player)

    def ask_double(self):
        if self.player in self.players:
            ask = input("you want to double your bet? y/n: ")
            if ask == "y":
                self.player.money -= self.player.bet
                self.player.bet *= 2
                card = self.deck.get_card()
                self.player.take_card(card)
                self.check_stop(self.player)
                self.player.change_points()
                self.player.print_cards()
                if self.player.full_points > 21:
                    self.remove_player(self.player)
            elif ask == "n":
                self.player.ask_card()
            else:
                print("Wrong command, try again.")
                self.ask_double()

    def ask_cards(self):
        for player in self.players:
            while player.ask_card():
                card = self.deck.get_card()
                player.take_card(card)
                is_stop = self.check_stop(player)
                if is_stop:
                    if player.full_points > 21 or isinstance(player, Player.Player):
                        self.remove_player(player)
                    break
                if isinstance(player, Player.Player):
                    player.print_cards()
                elif isinstance(player, Player.Bot):
                    player.print_cards()

    def check_winner(self):
        if self.dealer.full_points > 21:
            print('Dealer are fall! All players in game are win!')
            for winner in self.players:
                winner.money += winner.bet * 2
        else:
            for player in self.players:
                if player.full_points == self.dealer.full_points:
                    player.money += player.bet
                    self.player.eq += 1
                    print(MESSAGES.get('eq').format(player=player.name,
                                                    points=player.full_points))
                elif player.full_points > self.dealer.full_points:
                    player.money += player.bet * 2
                    if isinstance(player, Player.Bot):
                        print(MESSAGES.get('win').format(player=player.name))
                    elif isinstance(player, Player.Player):
                        print('You are win!')
                        self.player.win += 1

                elif player.full_points < self.dealer.full_points:
                    if isinstance(player, Player.Bot):
                        print(MESSAGES.get('lose').format(player=player.name))
                    elif isinstance(player, Player.Player):
                        print('You are lose!')
                        self.player.loose += 1

    def play_with_dealer(self):
        while self.dealer.ask_card():
            card = self.deck.get_card()
            self.dealer.take_card(card)
        self.dealer.print_cards()

    def start_game(self):
        for player in self.players:
            player.money += 100
        message = MESSAGES.get('ask_start')
        if not self._ask_starting(message=message):
            exit(1)

        self._launching()

        while True:
            for player in self.players:
                print(player.name, "bank is:", player.money)
            self.ask_bet()
            if len(self.deck.cards) < 30:
                self.deck._generate_deck()

            self.first_descr()

            if self.player in self.players:
                self.player.print_cards()

            if self.player.bet <= self.player.money and isinstance(self.player, Player.Player):
                self.ask_double()
            else:
                self.ask_cards()

            self.play_with_dealer()

            self.check_winner()

            if input("Want to see stats? y/n: ") == "y":
                self.player.get_stats()

            if not self._ask_starting(MESSAGES.get('rerun')):
                break
            else:
                self.player.clear_hand()
                self.dealer.clear_hand()
                self.players.extend(self.lost_players)
                self.lost_players = []

