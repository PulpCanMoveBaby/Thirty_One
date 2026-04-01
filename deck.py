import random

class Deck:
    # suits = ['S', 'C', 'H', 'D']
    suits = ['\u2660', '\u2663', '\u2665', '\u2666']
    number = list(range(2,15))
    faces = {11:'J', 12: 'Q', 13: 'K', 14:'A'}

    def __init__(self):
        self.reset_deck()
        
    def reset_deck(self):
        self.deck = []
        self.discard_pile = []
        for suit in Deck.suits:
            for num in Deck.number:
                if num > 10:
                    num = Deck.faces[num]                
                self.deck.append(str(num)+str(suit))

    def shuffle(self):
        shuffled = []
        original_deck = self.deck
        while self.deck:
            card = random.choice(self.deck)
            self.deck.remove(card)
            shuffled.append(card)        
        self.deck = shuffled

    def deal(self, players):
        for i in range(3):
            for player in players:
                card = self.deck[0]
                self.deck = self.deck[1:]
                player.hand.append(card)
