
import random

class Card:
    def __init__(self, value, color) -> None:
        self.value = value
        self.color = color
        val = int(value) if value not in FIGURES else 11 # else Ace
        if val == 11:
            for i in range(4):
                if value == FIGURES[i]:
                    val = 11 + i
        self.rank = val + ord(color) * 15

    def filename(self) -> str:
        file = str(self.value) + "_of_"
        color = ""
        if self.color == "C":
            color = "clubs"
        elif self.color == "D":
            color = "diamonds"
        elif self.color == "H":
            color = "hearts"
        else: 
            color = "spades"
        dir = "Playing Cards/PNG-cards-1.3/"
        return dir+file+color+".png"
    def __repr__(self) -> str:
        return f"{self.value}{self.color}"
    def __lt__(self, other):
        return self.rank - other.rank < 0

COLORS = ['C', 'D', 'H', 'S']
FIGURES = ['J', 'Q', 'K', 'A']
CARDS_FOR_PLAYER = 13

def shuffle(deck: list) -> list:
    random.shuffle(deck)
    return deck

def compare_cards(card: Card):
    print(card.value, card.value in FIGURES)
    if card.value not in FIGURES:
        return int(card.value) + ord(card.color)
    return 

def sort_by_color(hands: list[list]) -> list:
    for hand in hands:
        hand.sort()
    return hands

def deal_cards(deck: list) -> list:
    '''
    player_cards = [[], [], [], []] #empty list of cards for each hand
    for card in deck:
        while True:
            player_no = random.randint(0,4)
            if player_cards[player_no].count() <= 13: # maximum number for each player
                player_cards[player_no].append(card)
                break
    return player_cards
    '''
    deck = shuffle(deck)
    cards = []
    for i in range(4):
        cards.append(deck[(CARDS_FOR_PLAYER)*i:CARDS_FOR_PLAYER*(i+1)])
    cards = sort_by_color(cards)
    return cards


def generate_deck() -> list:
    deck = []
    for color in COLORS:
        for i in range(2,10):
            deck.append(Card(chr(i+48), color))
        deck.append(Card('10', color))
        for fig in FIGURES:
            deck.append(Card(fig, color))
    return deck

if __name__ == "__main__":
    deck = generate_deck()
    dealt_hands = deal_cards(deck)
    print(dealt_hands)