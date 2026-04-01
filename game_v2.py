from deck import Deck
from players import Human, Computer
import random
import sys
import time

players = []
names = ['Neo', 'Morpheus', 'Trinity', 'Agent Smith']
class Game:
    def __init__(self):
        self.deck = Deck()
        self.names_used = []
        self.immediate_win = False
        self.simulation = False
        self.winner = []
        self.winner_list = {}
        self.get_players()
        
    def get_players(self):    
        while True:
            try:
                num_players = int(input('How many human players? '))
                num_cpu = int(input('How many computer players? '))
                if num_players + num_cpu <= 4:
                    break
            except:
                print('Invalid input...')
            
        for i in range(num_players):
            while True:
                name = random.choice(names)
                if name not in self.names_used:
                    self.names_used.append(name)
                    players.append(Human(name))
                    break

        for i in range(num_cpu):
            while True:
                name = random.choice(names)
                if name not in self.names_used:
                    self.names_used.append(name)
                    players.append(Computer(name))
                    break

        for player in players:
            self.winner_list[player.name] = 0         

    def player_turn(self, player):
        player.reset_score()
        player.draw(self.deck)
        player.discard(self)
        self.immediate_win, self.winner_immediate = player.evaluate_hand(self.knock)
        if player.__class__ == Human:
            print(player.score)
        else:
            time.sleep(2)

    def play(self):
        self.knock = False
        immediate_win = False
        for i in range(25):
            self.deck.shuffle()
        self.deck.deal(players)

        while not self.knock: 
            for player in players:
                if self.knock == True:
                    continue              
                self.player_turn(player)
                if self.immediate_win == True:
                    self.game_over()
                    self.knock = True
                self.knock, self.knocker = player.knock(self)
        
        if not self.immediate_win:
            knocker_index = [idx for idx, obj in enumerate(players) if obj == self.knocker]
            post_knock_player_order = players[knocker_index[0]:] + players[:knocker_index[0]]
            for player in post_knock_player_order:
                if player == self.knocker:
                    continue
                self.player_turn(player)
            self.find_winner()

        if not self.simulation:
            again = input('Play again? (y) for yes, enter for no. ')
            if again == 'y':
                self.reset_game()
                self.play()
    
    def find_winner(self):
        #get a dictionary of every player's max score
        final_score = {player.name:max(player.score.values()) for player in players}
        
        #find the winner and show the rest of the players' scores
        sorted_scores = set(final_score.values())
        sorted_scores = sorted(sorted_scores, reverse = True)
        
        self.winners = [player.name for player in players if final_score[player.name] == sorted_scores[0]]
        if len(self.winners) > 1:
            winners_str = ''
            for i in range(len(self.winners)):
                if winners_str:
                    winners_str = winners_str + ',' + self.winners[i]
                else:
                    winners_str = i
            print(f'\nThe winners are {winners_str}!!!!!!')
        else:
            print(f'\nThe winner is {self.winners[0]}!!!!')

        print('\n')
        for i in sorted_scores:
            for key in final_score:
                if final_score[key] == i:
                    print(f'{key:<15}----> {i}')

    def game_over(self):
        print(f'\n\nThe winner is {self.winner_immediate.name} with a score of 31 !!!')  
        self.winners = [self.winner_immediate.name]
     
        if not self.simulation:
            input('Press enter...')
            sys.exit()

    def reset_game(self):
        for player in players:
            player.reset_score()
            player.reset_hand()
        self.deck.reset_deck()
        # self.winner_list += self.winner
        self.winner = []

class Simulation(Game):
    def __init__(self):
        super().__init__()
        self.total_wins = []
        self.games = []
        self.simulation = True
    
    def get_players(self):    
        while True:
            try:
                num_cpu = int(input('How many computer players? '))
                if num_cpu <= 4:
                    break
            except:
                print('Invalid input...')
            
        for i in range(num_cpu):
            while True:
                name = random.choice(names)
                if name not in self.names_used:
                    self.names_used.append(name)
                    players.append(Computer(name))
                    break

        for player in players:
            self.winner_list[player.name] = 0
            
    def run(self):
        num_games = int(input('How many games? '))
        for i in range(num_games):
            self.reset_game()
            self.play()
            self.get_stats()

    def get_stats(self):
        ties = []
        score = {}
        outcome = {player.name:max(player.score.values()) for player in players}
        self.games.append(outcome)
        for i in self.winners:
            self.winner_list[i] +=1
        print(self.winner_list)

if __name__ == '__main__':
    choice = input("Game (1) or simulation (2)? ")

    if choice == '1':
        game = Game()
        game.play()

    elif choice == '2':
        sim = Simulation()
        sim.run()
        