# Let's Play Some Thirty-One

## Overview
Knock, knock. Hope you have some good cards because you've only got one turn left.
Have you ever wanted to be a character from the hit motion picture The Matrix playing the card game Thirty-One against other characters from the hit motion picture The Matrix?
Well look no further, this repo has all you need and more for something like that!

And the best part is that your character is randomly selected so you're not ALWAYS stuck playing as Morpheus, you're welcome.

These rule-based AI computer players are ready to knock and leave you high and dry looking for that 3rd king. Don't say I didn't warn you!

## Features
  - Play a fast-paced game of Thirty-One against rule-based AI players
  - Play as one of four characters from the hit motion picture The Matrix
  - Hand based scoring system, just play out a hand
      - relax, don't get too competetive, just have fun and play out a hand of Thirty-One
  - Feel the satisfaction that only winning a hand of the card game Thirty-One can offer

## Gameplay
  - Each player starts with three cards, a turn is defined by drawing the card from the top of the deck, and discarding a card of your choice 
  - The idea is to get cards of the same suit to add up to 31:
      - Face cards are worth 10
      - Aces are worth 11
  - If a player gets two cards worth 10 and an ace of the same suit, it is an immediate win and the hand is over
  - Otherwise, when a player is satisfied with their hand, they can "knock" (knock on the surface of the object the game is being played on)
      -This gives each player one more turn to make the highest number of suited cards
  - Lastly, if a player gets three of the same card (ex. three jacks or three sevens), the score of the hand is 30.5, but the player still must knock

## Getting Started
  - Python 3.x installed on your system

## Installation Steps
  - Clone the repo:
    - git clone https://github.com/PulpCanMoveBaby/Thirty_One.git
  - Run the game:
    - python3 game_v2.py
    - python game_v2.py
   
## Usage
  - Follow the instructions on the screen
  - Cards are numbered in order from top card(1), middle card(2), bottom card in hand(3), the card drawn(4)
