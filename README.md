# SET
The code for the final assignment of the python course

Rules of the SET card game
Twelve cards will be dealt from the deck and the goal is to identify a "set". A set being a collection of three cards where each attribute (colour, shape, shading and number) is either the same across all three cards or different across all three cards. The three cards forming a "set" will then be replaced by three new ones from the deck. When no set is found the three upper cards (in this program, most right ones) are replaced with three new cards. When the deck is finished, the player who found the most sets wins the game. 

Instructions how to play this game

### IMPORTANT ### Make sure the to open the kaarten.zip and place the folder in the same folder containing the .py file.

Goal: beat the computer, by getting the most points before the deck finishes. 

When running the python script, the game window pops up displaying 12 SET-cards from the deck. The player has a predetermined time (as default 30 sec, can be changed in file at line 174) to successfully select 3 cards forming a set. When a player selects a card, the card is highlighted in green. If the three cards selected form a set, the cards will be replaced, and the player gets a point. If the three cards selected do not form a set, the cards will be deselected. When the time is up, the computer will select a set, these cards will be replaced, and the computer gets a point. If the computer doesn't find a set, the three right most cards will be replaced. The game ends when the deck is finished. On the bottom of the window the scores, time and remaining deck cards are displayed. 

![image](https://github.com/Novadiga/SET/assets/174059150/b5e3bc11-e436-4b2d-b824-51edd1f12be2)
