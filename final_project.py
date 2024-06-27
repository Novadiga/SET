import numpy as np 
import random
import pygame
import time

class set_card: # creates a class for setcard objects to represent them logically. 
    def __init__(self, color, symbol, shading, number):
        self.color = color  # can be green, purple or red
        self.symbol = symbol  # can be diamond, oval or squiggle 
        self.shading = shading  # can be empty, filled or shaded
        self.number = number  # can be 1, 2 or 3 
    def compare_cards(self, other): # compares the four attributes of two setcard objects, returns a numpy bolean array with either True or False on every comparison.
        return np.array([
            self.color == other.color,
            self.symbol == other.symbol,
            self.shading == other.shading,
            self.number == other.number])
    def get_image_path(self): # gets the image file name based of atributes of the setcard object.
        return f'kaarten/{self.color}{self.symbol}{self.shading}{self.number}.gif'
    
def is_set(card1, card2, card3): # determines if three setcard objects form a set, and returns True if that is the case.
    comparisons = [
        card1.compare_cards(card2),
        card2.compare_cards(card3),
        card3.compare_cards(card1)] # compares the cards using the compare_cards() function, this will result in three bolean arrays. 
    conditions = [
        all([comparisons[0][i], comparisons[1][i]]) 
        or not any([comparisons[0][i], comparisons[1][i], comparisons[2][i]])
        for i in range(4)] # sets the conditions for the bolean arrays to be a set. 
    return all(conditions) # if all conditions are met, returns True, the cards form a set 

def find_all_sets(collection_of_12_cards): # finds all possible sets in a collection of twelde cards, returns them as a list of lists. 
    sets = []
    for i in range(12):
        for j in range(i + 1, 12):
            for k in range(j + 1, 12):
                if is_set(collection_of_12_cards[i], collection_of_12_cards[j], collection_of_12_cards[k]):
                    sets.append([collection_of_12_cards[i], collection_of_12_cards[j], collection_of_12_cards[k]])
    return sets

def find_random_set(collection_of_12_cards): # chooses one random set from the lists of all possible sets created by find_all_sets().
    all_sets = find_all_sets(collection_of_12_cards)
    return random.choice(all_sets) if all_sets else None

class SetCard: # creates a class for setcard objects to represent them visually in the pygame. 
    def __init__(self, image_path, x, y): 
        self.image_path = image_path
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.selected = False

    def draw(self, surface): # function to draw the card on the screen and highlight it in green when selected. 
        surface.blit(self.image, self.rect.topleft)
        if self.selected:
            pygame.draw.rect(surface, green, self.rect, 3)

    def select(self): # function to select cards, this will switch between True and False when this function is called.
        self.selected = not self.selected

def convert_to_setcards(set_cards, positions): # this function takes a list of  set_card objects and their position tuples as input and returns a list of the corresponding SetCard objects.
    image_paths = [card.get_image_path() for card in set_cards] # used the get_image_path function to obtain the image path 
    setcards = [
        SetCard(image_paths[i], positions[i][0], positions[i][1])
        for i in range(len(set_cards))] 
    return setcards

def initialize_and_deal_cards(): # this function will create the deck of set_card objects and shuffles it, 
    # it defines the positions (x-, y-coordinates) of the cards in the pygame window,
    # it will "deal" twelve cards from the deck by taking the last twelve setcard objects from the deck, 
    # it will convert them to SetCard objects assigning the positions to them,
    # a dictionary is created to map set_card objects to SetCard objects.

    colors = ['green', 'purple', 'red']
    symbols = ['diamond', 'oval', 'squiggle']
    shadings = ['empty', 'filled', 'shaded']
    numbers = ['1', '2', '3']
    
    deck = [
        set_card(color, symbol, shading, number)
        for color in colors 
        for symbol in symbols 
        for shading in shadings 
        for number in numbers ] # Initializes the deck, as a list of all possible unique set_card objects
    
    random.shuffle(deck) # puts the deck in randon order
    
    positions = [(i * 105 + 50, j * 205 + 50) for j in range(3) for i in range(4)] # Generates positions as tuples

    set_card_objects = deck[:12] # takes the top twelve set_card_objects from the deck
    deck[:] = deck[12:] # updates the deck
    cards = convert_to_setcards(set_card_objects, positions) # converts the set_card objects to SetCard objects with the appropriate positions 
    card_map = {cards[i]: set_card_objects[i] for i in range(len(cards))}  # Creates a dictionary to map the SetCard objects to the set_card objects.
    # the dictionary is needed to quickly refer back and forth between instances of set_card objects (used to compare and find sets) and SetCard objects (used for the pygame interface): 
    return cards, card_map, deck

def replace_cards(cards, selected_cards, deck, card_map): # replaces the 3 selected cards with 3 new cards from the deck if they form a set 
    selected_positions = [card.rect.topleft for card in selected_cards] # keeps track of the position of the selected cards

    if len(deck) >= 3: # the deck needs to have at least 3 cards left in order to replace 3 cards 
        for card in selected_cards:
            cards.remove(card) # removes the cards
            del card_map[card]  # Removes the mapping for the selected card
        
        new_card_objects = deck[:3] # takes the top 3 set_card objects from the deck
        deck[:] = deck[3:] # updates the deck
        
        
        new_cards = convert_to_setcards(new_card_objects, selected_positions) # converts the set_card objects to SetCard objects assigning the positions of the selected cards
        
         
        cards.extend(new_cards) # adds new cards to the cards list
        for i in range(len(new_cards)): # updates the dictionary
            card_map[new_cards[i]] = new_card_objects[i]

    return cards, card_map

def replace_right_most_cards(cards, deck, card_map): # when no set is found by the computer, the three right most cards are replaced with new ones.
    right_most_positions = [(470, i * 205 + 50) for i in range(3)]
    

    if len(deck) >= 3: # the deck needs to have at least 3 cards left in order to replace 3 cards
        for pos in right_most_positions:
            for card in cards:
                if card.rect.topleft == pos:
                    cards.remove(card) # removes the cards
                    del card_map[card] # removes the mapping from the dictionary 

        window.fill(black)
        for card in cards:
            card.draw(window)
        draw_ui(window, player_score, computer_score, remaining_time, remaining_deck = len(deck))
        pygame.display.flip() 
        pygame.time.wait(1000)  

        new_card_objects = deck[:3] # takes the top 3 set_card objects from the deck
        deck[:] = deck[3:] # updates the deck
        
         
        new_cards = convert_to_setcards(new_card_objects, right_most_positions) # converts the set_card objects to SetCard objects assigning the positions right most positions
        
        cards.extend(new_cards) # adds new cards to the main cards list 
        for i in range(len(new_cards)): # updates the dictionary
            card_map[new_cards[i]] = new_card_objects[i]

    
    return cards, card_map

def draw_ui(window, player_score, computer_score, remaining_time, remaining_deck): # draws user interface 
    # displays the player's score at the bottom left
    score_text = font.render(f"Player Score: {player_score}", True, white)
    window.blit(score_text, (10, height - 60))
    
    # displays the computer's score above the player's score
    comp_score_text = font.render(f"Computer Score: {computer_score}", True, white)
    window.blit(comp_score_text, (10, height - 30))

    # displays the remaining time at the bottom right
    timer_text = font.render(f"Time Left: {int(remaining_time)}", True, white)
    window.blit(timer_text, (width - 150, height - 30))

    # displays the remaining deck above the timer
    deck_text = font.render(f"Deck: {remaining_deck}", True, white)
    window.blit(deck_text, (width - 150, height - 60))


cards, card_map, deck = initialize_and_deal_cards() # initialises and deals card by setting the cards, card_map and deck

selected_cards = [] # keeps track of selected cards
player_score = 0  # player's score
computer_score = 0  # computer's score
start_time = time.time()
time_limit = 30  # time limit in seconds

pygame.init() # initialises pygame

width, height = 520, 800
window = pygame.display.set_mode((width, height)) # sets the windwow

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0) # defines the colors 

clock = pygame.time.Clock()
fps = 30 # defines the framerate 

font = pygame.font.Font(None, 36) # sets the font of the displayed text

running = True
while running:
    elapsed_time = time.time() - start_time
    remaining_time = max(0, time_limit - elapsed_time)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for card in cards:
                if card.rect.collidepoint(pos):
                    card.select()    
                    if card not in selected_cards:
                        selected_cards.append(card)
                    else:
                        selected_cards.remove(card)
    
    if len(selected_cards) == 3: # this code runs when the player selects three cards
        
        selected_card_objects = [card_map[card] for card in selected_cards]
        if is_set(*selected_card_objects):
            
            player_score += 1
            
            cards, card_map = replace_cards(cards, selected_cards, deck, card_map)
            selected_cards = []
            start_time = time.time()  # resets timer after a successful set
        else:
            for card in selected_cards:
                card.select()
            selected_cards = []
    
        # if time is up, let the computer select a set
    
    if remaining_time == 0:
        comp_set = find_random_set([card_map[card] for card in cards])
        if comp_set:
            comp_set_cards = [card for card in cards if card_map[card] in comp_set]
            for card in comp_set_cards:
                card.select()  # ensures the computer's set is selected
            
            # redraw the window to show the highlighted cards
            window.fill(black)
            for card in cards:
                card.draw(window)
            draw_ui(window, player_score, computer_score, remaining_time, remaining_deck = len(deck))
            pygame.display.flip()       
            pygame.time.wait(1000)  # wait to show the highlighted set in green
            computer_score += 1         
            cards, card_map = replace_cards(cards, comp_set_cards, deck, card_map)
        else:
            # if no set is found, replace the three right-most cards
            cards, card_map = replace_right_most_cards(cards, deck, card_map)
        start_time = time.time()  # resets timer after computer's turn

    if len(deck) == 0:
        window.fill(black)
        if player_score > computer_score:
            end_text = font.render("YOU WIN!", True, white)
        else:
            end_text = font.render("YOU LOSE", True, white)
        window.blit(end_text, (width // 2 - 50, height // 2))
        pygame.display.flip()
        pygame.time.wait(3000)  # wait for 3 seconds to display the message
        running = False

    window.fill(black)

    for card in cards:
        card.draw(window)

    draw_ui(window, player_score, computer_score, remaining_time, remaining_deck= len(deck))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()

