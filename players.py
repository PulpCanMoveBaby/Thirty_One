import random
import sys
import time

class Human:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = {'\u2660':0, '\u2663':0, '\u2665':0, '\u2666':0, 'etc':0}
        self.facecard ={'J':10, 'Q':10, 'K':10, 'A':11}

    def reset_score(self):
        self.score = {'\u2660':0, '\u2663':0, '\u2665':0, '\u2666':0, 'etc':0}
    
    def reset_hand(self):
        self.hand = []

    def draw(self, Deck):
        print('\n'*5)
        print(f'--------{self.name}\'s TURN-----------')
        if Deck.deck:
            self.hand.append(Deck.deck[0])
            Deck.deck = Deck.deck[1:]
        else:
            self.hand.append(Deck.discard_pile[0])
            Deck.discard_pile = Deck.discard_pile[1:]
        
    def evaluate_hand(self, Game):
        for card in self.hand:
            if card[0:2] == '10':
                self.score[card[2]] = self.score[card[2]] + int(card[0:2])
            elif card[0] not in self.facecard.keys():
                self.score[card[1]] = self.score[card[1]] + int(card[0])
            else:
                self.score[card[1]] = self.score[card[1]] + self.facecard[card[0]]
            
        if self.hand[0][:2] == '10':
            if self.hand[1][:2] == '10' and self.hand[2][:2] == '10':
                self.score['etc'] = 30.5

        if self.hand[0][0] == self.hand[1][0] == self.hand[2][0]:
            self.score['etc'] = 30.5

        if max(self.score.values()) == 31:
            return True, self
        else:
            return False, None

    def discard(self, game):

        print(f'\nYour Hand------------')
        for idx, i in enumerate(self.hand[:3]):
            print(i, '\t\t', f'({idx+1})')
        # print(*self.hand[:3], sep = '\n')
        print(f"\nThe card drawn---------------")
        print(self.hand[3], '\t\t', '(4)\n')
        while True:
            try:
                choice = input('Pick a card to discard...(1-4): ')
                choice = int(choice)
                if choice >= 1 and choice <= 4:
                    break

            except KeyboardInterrupt:
                sys.exit()
            
            except Exception as e:
                print('Pick a number between 1 (top card in hand) and 4 (card drawn). ')

        self.hand.pop(choice-1)
        game.deck.discard_pile.append(choice-1)
        print(f'\n\n{self.name}\'s hand is: ')
        print(*self.hand, sep = '\n')
    
    def knock(self, Game):
        choice = input('\nDo you want you knock? "y" for yes, "enter" for no: ')
        if choice == 'y':
            Game.knock = True
            return Game.knock, self
        else:
            return Game.knock, None

class Computer(Human):
    def __init__(self, name):
        super().__init__(name)
        self.go_for_three = False

    def discard(self, game):
        #evaluate hand and return immediate win if cpu score is 31
        self.evaluate_hand(game)
        if game.simulation:
            print('Before Discard')
            print(self.hand)
            print('\n')
            print(self.score)
            print('\n')
        
        #get the highest suit score and lowest suit score from evaluation
        highest = max(self.score.values())
        non_zero = [i for i in self.score.values() if i != 0]
        lowest = min(non_zero)
        num_suits = {}
        same_value = {}


        #get the suit the cpu should try to collect based on highest score
        try_for_suit = [i[0] for i in self.score.items() if i[1] == highest]
        

        #iterate through hand to gather info
        for idx1, card1 in enumerate(self.hand):
            
            #get the number of cards per suit
            if card1[-1] not in num_suits:
                num_suits[card1[-1]] = 1
            else:
                num_suits[card1[-1]] += 1

            #see if you have two or three of the same number (ex. two sevens or three jacks)
            for idx2, card2 in enumerate(self.hand):
                if idx2 <= idx1:
                    continue
                if card1[:-1] == card2[:-1]:
                    if card1[:-1] in same_value.keys():
                        same_value[card1[:-1]] += 1
                    else:
                        same_value[card1[:-1]] = 1

        
        #if there are multiple suit with the same score
        if len(try_for_suit) > 1:
            
            #find the suit with the highest score and LEAST amount of cards
            #num_suits holds how many cards of each suit is in hand
            suit_to_try = {key:value for key,value in num_suits.items() if key in try_for_suit}
            #code design example. === cpu has 10 of hearts, 6 and 4 of spades, keep the ten, get rid of a spade
            suit_to_try = [i for i in suit_to_try.keys() if suit_to_try[i] == min(suit_to_try.values())]
            
            #if there are still multiple suits, pick randomly
            if len(suit_to_try) > 1:
                try_for_suit = [random.choice(suit_to_try)]
            else:
                try_for_suit = [suit_to_try[0]]

        #if you have two sets of doubles (draw card is in hand here)
        #same_value ---> dict where keys = repeated card value (2, 5, 'J', etc.), value = how many of that card
        #same_value ---> value of 1 = two of same card, value of 2 = three of same card
        two_of_same_card = [i for i in same_value.keys() if same_value[i] == 1]
        
        if len(two_of_same_card)>1:
            try_for_number = random.choice(two_of_same_card)
        
        elif two_of_same_card:
            try_for_number = two_of_same_card[0]
        
        else:
            try_for_number = False

        if try_for_number and highest < 21:
            self.go_for_three = True
        else:
            self.go_for_three = False

        #set flag for if you have three of the same number (ex. three kings)
        triple_and_knock = [i for i in same_value.keys() if same_value[i] > 1]

        #discard the one that is not a repeated card value
        if triple_and_knock:
            card = [i for i in self.hand if i[:-1] != triple_and_knock[0]]
            
            #the edge case where you have all four cards of a card value (ex. all four Aces)
            if not card:
                card = random.choice(self.hand)
        
        #check to see if cpu is trying to get three of the same card, and get discard potentials
        elif self.go_for_three == False:
            
            #find the suit with the lowest value and MOST cards (ex. if 9 hearts, 5 and 4 spades--> get rid of a spade)
            suit_to_discard = {key:value for key,value in num_suits.items() if self.score[key] == lowest}

            #discard suit that has the lowest score AND the highest number of cards
            suit_to_discard = [i for i in suit_to_discard.keys() if suit_to_discard[i] == max(suit_to_discard.values())]
            
            #if there are still multiples, choose random
            if len(suit_to_discard) > 1:
                suit_to_discard = [random.choice(suit_to_discard)]

            #first try to hold on to multiple numbers while going for a high score
            potential_discards = [i for i in self.hand if i[-1] == suit_to_discard[0] and i[:-1] != try_for_number]
            #then
            if not potential_discards:
                potential_discards = [i for i in self.hand if i[-1] == suit_to_discard[0]]

        else:
            #first try to hold on to card that still gives a higher score for non multiples
            potential_discards = [i for i in self.hand if i[:-1] != try_for_number and i[-1] != try_for_suit]
            #then
            if not potential_discards:
                potential_discards = [i for i in self.hand if i[:-1] != try_for_number]

        if not triple_and_knock:
            #discard the lowest card of the chosen suit
            potential_nonface = []
            for card in potential_discards:
                if card[:-1] not in self.facecard.keys():
                    potential_nonface.append(int(card[:-1]))
            if potential_nonface:
                card = [i for i in potential_discards if i[:-1] == str(min(potential_nonface))]
            else:
                potential_faces = [i for i in potential_discards if i[:-1] != 'A']
                if potential_faces:
                    card = [random.choice(potential_faces)]
                else:
                    card = [random.choice(potential_discards)]
        
        #remove card and reset to re-evaluate
        self.hand.remove(card[0])
        if game.simulation:
            print(f'{self.name} has chosen to discard {card[0]}\n')
        game.deck.discard_pile.append(card[0])
        if game.simulation:
            print('After discard')
            print(self.hand)
            print('\n')
        self.reset_score()

    def knock(self, Game):
        if Game.knock == True:
            return Game.knock, None
        if max(self.score.values()) >= 24:
            Game.knock = True

            if not Game.immediate_win:
                print('\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                print(f"Computer {self.name} has knocked")
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n')
                time.sleep(2)

            return Game.knock, self
        else:
            return Game.knock, None

