# BlackJack game with Python
## About

Short guide about the game:
First of all game asks you about starting the game. After player`s consent game asks how many bots to add to play with maximum of 3 bots. You cant play against them, its just an option not to feel lonely. You can also choos your name ant here`s the game start.

First of all you choos bet from 1 to 100. After the first bet you take your cards and, if there is no Blackjack(21 points on 2 girst cardds), here comes the first option: to double your bet and take only one aditional card, or skip it.
If you choose not to double bet, now game asks you about taking another card. You can take any number of cards, but game will stop you if haand will be bigger than 21 points. This way you loose this round and can play in next one.
After player deside not to take more cards, so Play with dealer part starts. At the start of the game dealer opens only one card, and now dealer take cards untill he can win someone on board. If dealers points equals players points bets are back and noone wins. If dealer have greather points but not more than 21 - dealer wins. Also if dealer has more than 21 points - every player in game winst no matter how many points they have.
After round player can check his round stats: losse/win/blackjack/equals etc...
If player is out of money he can ask game about onother "buy-in".
After each round game asks player if he wants to quit, or continue playing. Programm shutting down after player choose to quit. 


## Install 

1. clone project and cd to project dir


## Run it

1. cd to `blackjack` directory
1. run
    ```zsh
    #linux/mac
    python3 main.py
    ```
    ```bash
    #win cmd
    python main.py
    ```
