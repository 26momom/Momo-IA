import random
from operator import index


import pygame
import sys


pygame.init()




# screen parimiters and setup
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Yahtzee Game")


# the fonts
font_name = 'Arial'
font_size = 50
font = pygame.font.SysFont(font_name, font_size, bold=False, italic=False)
fps = 120
clock = pygame.time.Clock()
clock.tick(fps)  #to make it not stutter
scoreboard_font = 26


selected_choice = [False, False, False, False, False, False, False, False, False, False, False, False, False]
possibility = [False, False, False, False, False, False, False, False, False, False, False, False, False]
done = [False, False, False, False, False, False, False, False, False, False, False, False, False]
selected_choice_player_2 = [False, False, False, False, False, False, False, False, False, False, False, False, False]
possibility_player_2 = [False, False, False, False, False, False, False, False, False, False, False, False, False]
done_player_2 = [False, False, False, False, False, False, False, False, False, False, False, False, False]
dice_selected = [False, False, False, False, False]
roll_count = 4
player_1_turn = True
player_2_turn = False







numbers = [0, 0, 0, 0, 0] #to show the dice numbers but it starts black therefore 0
# colors
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GREEN = [0, 200, 0]
RED = [200, 0, 0]
POKER_GREEN = [78, 106, 84]
GOLD = [255, 215, 0]




# Random dice
class Dice:
   def __init__(self, x, y, num, key, selected):
       self.x = x
       self.y = y
       self.num = num
       self.key = key
       self.die = ''
       self.selected = selected


   def create_dice(self):
       self.die = pygame.draw.rect(screen, WHITE, [self.x, self.y, 100, 100], 0, 5)
       if self.num == 1:
           pygame.draw.circle(screen, BLACK, (self.x+ 50, self.y +50), 10)
       if self.num == 2:
           pygame.draw.circle(screen, BLACK, (self.x+ 20, self.y +20), 10)
           pygame.draw.circle(screen, BLACK, (self.x+ 80, self.y +80), 10) #this to draw the dots for number 2 and so on
       if self.num == 3:
           pygame.draw.circle(screen, BLACK, (self.x+ 20, self.y +20), 10)
           pygame.draw.circle(screen, BLACK, (self.x+ 50, self.y +50), 10)
           pygame.draw.circle(screen, BLACK, (self.x+ 80, self.y +80), 10)
       if self.num == 4:
           pygame.draw.circle(screen, BLACK, (self.x + 20, self.y + 20), 10)
           pygame.draw.circle(screen, BLACK, (self.x + 80, self.y + 80), 10)
           pygame.draw.circle(screen, BLACK, (self.x + 20, self.y + 80), 10)
           pygame.draw.circle(screen, BLACK, (self.x + 80, self.y + 20), 10)




       if self.num == 5:
           pygame.draw.circle(screen, BLACK, (self.x + 20, self.y + 20), 10)
           pygame.draw.circle(screen, BLACK, (self.x + 80, self.y + 80), 10)
           pygame.draw.circle(screen, BLACK, (self.x + 20, self.y + 80), 10)
           pygame.draw.circle(screen, BLACK, (self.x + 80, self.y + 20), 10)
           pygame.draw.circle(screen, BLACK, (self.x + 50, self.y + 50), 10)




       if self.num == 6:
           pygame.draw.circle(screen, BLACK, (self.x + 20, self.y + 20), 10)
           pygame.draw.circle(screen, BLACK, (self.x + 20, self.y + 80), 10)
           pygame.draw.circle(screen, BLACK, (self.x + 20, self.y + 50), 10)
           pygame.draw.circle(screen, BLACK, (self.x + 80, self.y + 80), 10)
           pygame.draw.circle(screen, BLACK, (self.x + 80, self.y + 50), 10)
           pygame.draw.circle(screen, BLACK, (self.x + 80, self.y + 20), 10)


       if self.selected:
           lock_font = pygame.font.SysFont(None, 40)
           lock_text = lock_font.render('🔒', True, RED)
           screen.blit(lock_text, (self.x + 70, self.y + 70)) # Makes a cool lock icon




# function to make the text fit
def shrink_to_fit(text, max_width, starting_size=72, min_size=10):
   for size in range(starting_size, min_size - 1, -1):  # go down by 1
       font = pygame.font.SysFont(None, size)
       if font.size(text)[0] <= max_width:
           return font
   return pygame.font.SysFont(None, min_size)


# function to create a button
def create_button(text, x, y, width, height, base_font, mouse_pos, button_color, hovering_color):
   rect = pygame.Rect(x, y, width, height)
   color = hovering_color if rect.collidepoint(mouse_pos) else button_color
   pygame.draw.rect(screen, color, rect, border_radius=10)
   fitting_font = shrink_to_fit(text, width - 10, base_font.get_height(), 10)
   text_surface = fitting_font.render(text, True, WHITE)
   text_x = x + (width - text_surface.get_width()) // 2
   text_y = y + (height - text_surface.get_height()) // 2
   screen.blit(text_surface, (text_x, text_y))
   return rect


category_names = [
   'Ones', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes',
   'Three of a Kind', 'Four of a Kind', 'Full House',
   'Small Straight', 'Large Straight', 'YAHTZEEEEEE!', 'Chance'
]




#scoreboard of the yahtzee
scoreboard_player_1 = {
   "Ones": {"score": None, "selected": False, "possible": False},
   "Twos": {"score": None, "selected": False, "possible": False},
   "Threes": {"score": None, "selected": False, "possible": False},
   "Fours": {"score": None, "selected": False, "possible": False},
   "Fives": {"score": None, "selected": False, "possible": False},
   "Sixes": {"score": None, "selected": False, "possible": False},
   "Total": {"score": 0, "selected": True, "possible": False},


   "Three of a Kind": {"score": None, "selected": False, "possible": False},
   "Four of a Kind": {"score": None, "selected": False, "possible": False},
   "Full House": {"score": None, "selected": False, "possible": False},
   "Small Straight": {"score": None, "selected": False, "possible": False},
   "Large Straight": {"score": None, "selected": False, "possible": False},
   "YAHTZEEEEEE!": {"score": None, "selected": False, "possible": False},
   "Chance": {"score": None, "selected": False, "possible": False},
   "Total Score": {"score": 0, "selected": True, "possible": False},
}


scoreboard_player_2 = {
   "Ones": {"score": None, "selected": False, "possible": False},
   "Twos": {"score": None, "selected": False, "possible": False},
   "Threes": {"score": None, "selected": False, "possible": False},
   "Fours": {"score": None, "selected": False, "possible": False},
   "Fives": {"score": None, "selected": False, "possible": False},
   "Sixes": {"score": None, "selected": False, "possible": False},
   "Total": {"score": 0, "selected": True, "possible": False},


   "Three of a Kind": {"score": None, "selected": False, "possible": False},
   "Four of a Kind": {"score": None, "selected": False, "possible": False},
   "Full House": {"score": None, "selected": False, "possible": False},
   "Small Straight": {"score": None, "selected": False, "possible": False},
   "Large Straight": {"score": None, "selected": False, "possible": False},
   "YAHTZEEEEEE!": {"score": None, "selected": False, "possible": False},
   "Chance": {"score": None, "selected": False, "possible": False},
   "Total Score": {"score": 0, "selected": True, "possible": False},
}






#creationg scoreboard class
class Scoreboard:
   def __init__(self, x, y, text, selected, possible, done, score, scoreboardp1, scoreboardp2):
       self.x = x
       self.y = y
       self.text = text
       self.selected = selected
       self.possible = possible
       self.done = done
       self.score = score
       self.scoreboardp1 = scoreboardp1
       self.scoreboardp2 = scoreboardp2
       global selected_choice
       global current_scoreboard

   def create_scoreboard(self):
       row_width = 350 #225
       row_height = 30
       spacing = 5
       category_x = 30
       p1_x = 200
       p2_x = 300

       category_font = shrink_to_fit(self.text, 200, starting_size=26, min_size=10)
       category_text = category_font.render(self.text, True, BLACK)


       #lines for row
       pygame.draw.line(screen, BLACK, (self.x, self.y), (self.x + row_width, self.y), 2)
       pygame.draw.line(screen, BLACK, (self.x, self.y + row_height), (self.x + row_width, self.y + row_height), 2)



       # horizontal line under headers
       pygame.draw.line(screen, BLACK, (category_x, 195), (category_x + row_width, 195), 2)

       fitting_font = shrink_to_fit(self.text, row_width - 2 * spacing, starting_size=26, min_size=10)




       if self.done:
           color = BLACK
       elif self.possible:
           color = GREEN
       else:
           color = BLACK




       scoreboard_text = fitting_font.render(self.text, True, color)
       text_x = self.x + spacing
       text_y = self.y + (row_height - scoreboard_text.get_height()) // 2
       separator_x = (p1_x + p2_x) // 2  # vertica, line
       pygame.draw.line(screen, BLACK, (separator_x, self.y), (separator_x, self.y + row_height), 1)

       screen.blit(scoreboard_text, (text_x, text_y))

       score_font = pygame.font.SysFont(None, 22)

       # Player 1 score
       if self.scoreboardp1[self.score]["score"] is not None:
           p1_score_text = score_font.render(str(self.scoreboardp1[self.score]["score"]), True, BLACK)
           screen.blit(p1_score_text, (p1_x, self.y))

       # Player 2 score
       if self.scoreboardp2[self.score]["score"] is not None:
           p2_score_text = score_font.render(str(self.scoreboardp2[self.score]["score"]), True, BLACK)
           screen.blit(p2_score_text, (p2_x, self.y))


def check_possibility(possibility, numbers):
   counts = [numbers.count(i) for i in range(1, 7)]  # how many of each number 1–6
   unique = sorted(set(numbers))  # to help with checking straights


   # these are always possible
   possibility[0] = True
   possibility[1] = True
   possibility[2] = True
   possibility[3] = True
   possibility[4] = True
   possibility[5] = True
   possibility[12] = True  # This is for the chance option


   # check how many of the same number exist
   max_count = max(counts)


   # check for 3 of a kind
   possibility[6] = max_count >= 3


   # check for 4 of a kind
   possibility[7] = max_count >= 4


   # check for full house 3 of one + 2 of another
   possibility[8] = (3 in counts and 2 in counts)


   # check for small straight — any 4 in a row
   small_straights = [
       {1, 2, 3, 4},
       {2, 3, 4, 5},
       {3, 4, 5, 6}
   ]
   possibility[9] = False
   for straights in small_straights:
       if straights.issubset(unique):
           possibility[9] = True
           break  #checks that if any elements of one set is in another set, thats what subset does.


   # check for large straight must be exact 5 in a row so only 2 options
   possibility[10] = unique == [1, 2, 3, 4, 5] or unique == [2, 3, 4, 5, 6]


   # check for yahtzee 5 of a kind
   possibility[11] = max_count == 5


   return possibility



















# used as constrains to make game run
game_running = True
game_state = "start"
roll = False


# main loop
while game_running == True:

   screen.fill(POKER_GREEN)
   user_position = pygame.mouse.get_pos()
   # events so that the game can actualy function properly
   for event in pygame.event.get():
       if event.type == pygame.QUIT:  # to quit using the X
           game_running = False



       elif event.type == pygame.MOUSEBUTTONDOWN:
           if game_state == "start":
               if start_game_button.collidepoint(user_position):  # changes the gamestate
                   game_state = "gamemode_selection"
               elif quit_game_button.collidepoint(user_position):
                   game_running = False


           elif game_state == "gamemode_selection":
               if regular_yahtzee.collidepoint(user_position):
                   game_state = "choose_opponent"
               elif simplified_version.collidepoint(user_position):
                   game_state = "choose_opponent"
               elif locking_version.collidepoint(user_position):
                   game_state = "choose_opponent"
               elif chronological_order.collidepoint(user_position):
                   game_state = "choose_opponent"
               elif go_back_button.collidepoint(user_position):
                   game_state = "start"


           elif game_state == "choose_opponent":
               if human.collidepoint(user_position):
                   print("Mode: Human vs Human")
                   game_state = "game_start"
               elif robot.collidepoint(user_position):
                   print("Mode: Human vs AI")
                   game_state = "AI_option"
               elif go_back_button_gamemode.collidepoint(user_position):
                   game_state = "gamemode_selection"


           elif game_state == "AI_option":
               if easy_mode.collidepoint(user_position):  # easy AI selected
                   game_state = 'game_start'
               elif normal_mode.collidepoint(user_position):  # normal AI selected
                   game_state = 'game_start'
               elif impossiible_mode.collidepoint(user_position):  # impossible AI selected
                   game_state = 'game_start'
               elif go_back_button_gamemode.collidepoint(user_position):
                   game_state = "gamemode_selection"




           elif game_state == 'game_start' and event.type == pygame.MOUSEBUTTONDOWN:



               if roll_button.collidepoint(user_position) and roll_count > 0:
                   roll = True
                   roll_count = roll_count - 1
               elif go_back_button_gamemode.collidepoint(user_position):
                   game_state = "gamemode_selection"
               elif dice_1.die.collidepoint(event.pos):
                   dice_selected[0] = not dice_selected[0]
               elif dice_2.die.collidepoint(event.pos):
                   dice_selected[1] = not dice_selected[1]
               elif dice_3.die.collidepoint(event.pos):
                   dice_selected[2] = not dice_selected[2]
               elif dice_4.die.collidepoint(event.pos):
                   dice_selected[3] = not dice_selected[3]
               elif dice_5.die.collidepoint(event.pos):
                   dice_selected[4] = not dice_selected[4]
               else:
                   if player_1_turn == True:
                       current_scoreboard = scoreboard_player_1
                       for category, rect in scoreboard_slots.items():  # loops through ones, twos etc
                           if rect.collidepoint(user_position):
                               index = category_names.index(category)
                               if possibility[index] and not scoreboard_player_1[category]['selected']:

                                   if category == 'Ones':
                                       target = 1
                                   elif category == 'Twos':
                                       target = 2
                                   elif category == 'Threes':
                                       target = 3
                                   elif category == 'Fours':
                                       target = 4
                                   elif category == 'Fives':
                                       target = 5
                                   elif category == 'Sixes':
                                       target = 6

                                   elif category == 'Three of a Kind':
                                       if possibility[6] == True:
                                           target = sum(numbers)
                                   elif category == 'Four of a Kind':
                                       if possibility[7] == True:
                                           target = sum(numbers)

                                   elif category == 'Full House':
                                       target = 25
                                   elif category == 'Small Straight':
                                       target = 30
                                   elif category == 'Large Straight':
                                       target = 40
                                   elif category == 'YAHTZEEEEEE!':
                                       target = 50
                                   elif category == 'Chance':
                                       target = sum(numbers)

                                   if category in ['Ones', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes']:
                                       counter = 0
                                       for i in range(len(numbers)):  # iterate through the list
                                           if numbers[i] == target:
                                               counter = counter + target

                                       scoreboard_player_1[category]['score'] = counter
                                       scoreboard_player_1[category]['selected'] = True

                                       selected_choice[index] = True
                                       done[index] = True
                                       possibility[index] = False
                                       dice_selected = [False, False, False, False, False]  # to reset dice
                                       roll_count = 4
                                       player_1_turn = False
                                       player_2_turn = True



                                   elif category == 'Three of a Kind':
                                       if possibility[6] == True:
                                           scoreboard_player_1[category]['score'] = sum(numbers)
                                           scoreboard_player_1[category]['selected'] = True

                                       selected_choice[index] = True
                                       done[index] = True
                                       possibility[index] = False
                                       dice_selected = [False, False, False, False, False]  # to reset dice
                                       roll_count = 4
                                       player_1_turn = False
                                       player_2_turn = True


                                   elif category == 'Four of a Kind':
                                       if possibility[7] == True:
                                           scoreboard_player_1[category]['score'] = sum(numbers)
                                           scoreboard_player_1[category]['selected'] = True

                                       selected_choice[index] = True
                                       done[index] = True
                                       possibility[index] = False
                                       dice_selected = [False, False, False, False, False]  # to reset dice
                                       roll_count = 4
                                       player_1_turn = False
                                       player_2_turn = True


                                   elif category in ['Full House', 'Small Straight', 'Large Straight', 'YAHTZEEEEEE!',
                                                     'Chance']:
                                       scoreboard_player_1[category]['score'] = target
                                       scoreboard_player_1[category]['selected'] = True

                                   selected_choice[index] = True
                                   done[index] = True
                                   possibility[index] = False
                                   dice_selected = [False, False, False, False, False]  # to reset dice
                                   roll_count = 4
                                   player_1_turn = False
                                   player_2_turn = True

                   elif player_2_turn == True:
                       current_scoreboard = scoreboard_player_2
                       for category, rect in scoreboard_slots.items():
                           if rect.collidepoint(user_position):
                               index = category_names.index(category)
                               if possibility_player_2[index] and not scoreboard_player_2[category]['selected']:

                                   if category == 'Ones':
                                       target = 1
                                   elif category == 'Twos':
                                       target = 2
                                   elif category == 'Threes':
                                       target = 3
                                   elif category == 'Fours':
                                       target = 4
                                   elif category == 'Fives':
                                       target = 5
                                   elif category == 'Sixes':
                                       target = 6
                                   elif category == 'Full House':
                                       target = 25
                                   elif category == 'Small Straight':
                                       target = 30
                                   elif category == 'Large Straight':
                                       target = 40
                                   elif category == 'YAHTZEEEEEE!':
                                       target = 50
                                   elif category == 'Chance':
                                       target = sum(numbers)

                                   if category in ['Ones', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes']:
                                       counter = 0
                                       for i in range(len(numbers)):
                                           if numbers[i] == target:
                                               counter += target
                                       scoreboard_player_2[category]['score'] = counter
                                       scoreboard_player_2[category]['selected'] = True

                                   elif category == 'Three of a Kind':
                                       if possibility_player_2[6]:
                                           scoreboard_player_2[category]['score'] = sum(numbers)
                                           scoreboard_player_2[category]['selected'] = True

                                   elif category == 'Four of a Kind':
                                       if possibility_player_2[7]:
                                           scoreboard_player_2[category]['score'] = sum(numbers)
                                           scoreboard_player_2[category]['selected'] = True

                                   elif category in ['Full House', 'Small Straight', 'Large Straight', 'YAHTZEEEEEE!',
                                                     'Chance']:
                                       scoreboard_player_2[category]['score'] = target
                                       scoreboard_player_2[category]['selected'] = True

                                   # Final state update
                                   selected_choice_player_2[index] = True
                                   done_player_2[index] = True
                                   possibility_player_2[index] = False
                                   dice_selected = [False, False, False, False, False]
                                   roll_count = 4
                                   player_1_turn = True
                                   player_2_turn = False

   if game_state == "start":  # so that I can section it easier and change the screen
       welcome_font = shrink_to_fit("Welcome to Yahtzee! Click Start To Play", 800)
       text_surface = welcome_font.render("Welcome to Yahtzee! Click Start To Play", True, BLACK)  # renders on screen
       screen.blit(text_surface, (100, 50))  # that it actually appears




       start_game_button = create_button('Start', 175, 650, 300, 70, font, user_position, RED, GOLD)
       quit_game_button = create_button('Quit', 525, 650, 300, 70, font, user_position, RED, GOLD)
       pygame.display.flip()


   elif game_state == "gamemode_selection":
       gamemode_font = shrink_to_fit("Select Which Gamemode You Would Like to Play", 800)
       text_surface = gamemode_font.render("Select Which Gamemode You Would Like to Play", True, BLACK)
       screen.blit(text_surface, (100, 50))


       regular_yahtzee = create_button('Regular', 350, 180, 300, 70, font, user_position, RED, GOLD)
       simplified_version = create_button('Simplified Yahtzee', 350, 270, 300, 70, font, user_position, RED, GOLD)
       locking_version = create_button('Dice Locking', 350, 360, 300, 70, font, user_position, RED, GOLD)
       chronological_order = create_button('Chronological', 350, 450, 300, 70, font, user_position, RED, GOLD)
       go_back_button = create_button('Back', 20, 730, 150, 50, font, user_position, RED, GOLD)
       pygame.display.flip()


   elif game_state == 'AI_option':
       a = shrink_to_fit("Select Difficulty level of your Opponent", 800)  # FIX THIS TMR BY ADDING AI TEXT
       text_surface = a.render("Select AI Difficulty", True, BLACK)
       screen.blit(text_surface, (100, 100))


       easy_mode = create_button('Easy', 350, 200, 300, 70, font, user_position, RED, GOLD)
       normal_mode = create_button('Normal', 350, 300, 300, 70, font, user_position, RED, GOLD)
       impossiible_mode = create_button('Impossible', 350, 400, 300, 70, font, user_position, RED, GOLD)
       go_back_button_gamemode = create_button('Back', 20, 730, 150, 50, font, user_position, RED, GOLD)
       pygame.display.flip()  # this is used so that the screen actually shows and it's not black for some reason


   elif game_state == 'choose_opponent':
       human_or_AI = shrink_to_fit('Against Human or AI?', 800) #this Defines
       text_surface = human_or_AI.render('Against Human or AI?', True, BLACK) #this calls
       screen.blit(text_surface, (100, 100))
       human = create_button('1v1', 350, 300, 300, 70, font, user_position, RED, GOLD)
       robot = create_button('AI Opponent', 350, 400, 300, 70, font, user_position, RED, GOLD)
       go_back_button_gamemode = create_button('Back', 20, 730, 150, 50, font, user_position, RED, GOLD)
       pygame.display.flip()




   elif game_state == 'game_start':
       if player_1_turn == True:
           current_scoreboard = scoreboard_player_1
       else:
           current_scoreboard = scoreboard_player_2
       current_scoreboard = scoreboard_player_1 if player_1_turn else scoreboard_player_2
       category_x = 30
       p1_x = 200
       p2_x = 300
       spacing = 5
       row_width = 350

       header_font = pygame.font.SysFont(None, 24, bold=True)
       screen.blit(header_font.render("Category", True, BLACK), (category_x + spacing, 160))
       screen.blit(header_font.render("P1", True, BLACK), (p1_x + spacing, 160))
       screen.blit(header_font.render("P2", True, BLACK), (p2_x + spacing, 160))
       pygame.draw.line(screen, BLACK, (category_x, 185), (category_x + row_width, 185))


       scoreboard_slots = {
           'Ones': pygame.Rect(0, 190, 225, 35),
           'Twos': pygame.Rect(0, 225, 225, 35),
           'Threes': pygame.Rect(0, 260, 225, 35),
           'Fours': pygame.Rect(0, 295, 225, 35),
           'Fives': pygame.Rect(0, 330, 225, 35),
           'Sixes': pygame.Rect(0, 365, 225, 35),
           'Total': pygame.Rect(0, 400, 225, 35),
           'Three of a Kind': pygame.Rect(0, 435, 225, 35),
           'Four of a Kind': pygame.Rect(0, 470, 225, 35),
           'Full House': pygame.Rect(0, 505, 225, 35),
           'Small Straight': pygame.Rect(0, 540, 225, 35),
           'Large Straight': pygame.Rect(0, 575, 225, 35),
           'YAHTZEEEEEE!': pygame.Rect(0, 610, 225, 35),
           'Chance': pygame.Rect(0, 645, 225, 35),
           'Total Score': pygame.Rect(0, 680, 225, 35),
       }

       b = shrink_to_fit('Player 1 Turn', 800)
       text_surface = b.render('Player 1 Turn', True, BLACK) #antialias means so that the font will be smooth and not chunky/blocky
       screen.blit(text_surface, (100,100))
       go_back_button = create_button('Back', 20, 730, 150, 50, font, user_position, RED, GOLD)
       rolls_left = shrink_to_fit((f'You have: {roll_count} left'), 200)
       rolls_left_surface = rolls_left.render(f'You have {roll_count} left', 300, BLACK)
       screen.blit(rolls_left_surface, (550 ,550))
       #FIX THIS


       dice_1 = Dice(330, 600, numbers[0], 0, dice_selected[0])
       dice_2 = Dice(450, 600, numbers[1], 1, dice_selected[1])
       dice_3 = Dice(570, 600, numbers[2], 2, dice_selected[2])
       dice_4 = Dice(690, 600, numbers[3], 3, dice_selected[3])
       dice_5 = Dice(810, 600, numbers[4], 4, dice_selected[4])


       roll_button = create_button('Click to Roll', 200, 700,300, 70, font, user_position, RED, GOLD)
       if player_1_turn == True:
           ones = Scoreboard(0, 190, 'Ones', selected_choice[0], possibility[0], done[0], 'Ones', scoreboard_player_1, scoreboard_player_2) #FIX DIMENSIONS FOR ALL
           twos = Scoreboard(0, 225, 'Twos', selected_choice[1], possibility[1], done[1] ,'Twos', scoreboard_player_1, scoreboard_player_2)
           threes = Scoreboard(0, 260, 'Threes', selected_choice[2], possibility[2], done[2], 'Threes', scoreboard_player_1, scoreboard_player_2)
           fours = Scoreboard(0, 295, 'Fours', selected_choice[3], possibility[3], done[3], 'Fours', scoreboard_player_1, scoreboard_player_2)
           fives = Scoreboard(0, 330, 'Fives', selected_choice[4], possibility[4], done[4], 'Fives', scoreboard_player_1, scoreboard_player_2)
           sixes = Scoreboard(0, 365, 'Sixes', selected_choice[5], possibility[5], done[5], 'Sixes', scoreboard_player_1, scoreboard_player_2)
           total_1 = Scoreboard(0, 400, 'Total', False, False, True, 'Total' , scoreboard_player_1, scoreboard_player_2)
           three_of_a_kind = Scoreboard(0, 435, 'Three of a Kind', selected_choice[6], possibility[6], done[6],'Three of a Kind', scoreboard_player_1, scoreboard_player_2)
           four_of_a_kind = Scoreboard(0, 470, 'Four of a Kind', selected_choice[7], possibility[7], done[7], 'Four of a Kind', scoreboard_player_1, scoreboard_player_2)
           full_house = Scoreboard(0, 505, 'Full House', selected_choice[8], possibility[8], done[8], 'Full House', scoreboard_player_1, scoreboard_player_2)
           small_straight = Scoreboard(0, 540, 'Small Straight', selected_choice[9], possibility[9], done[9], 'Small Straight', scoreboard_player_1, scoreboard_player_2)
           large_straight = Scoreboard(0, 575, 'Large Straight', selected_choice[10], possibility[10], done[10], 'Large Straight', scoreboard_player_1, scoreboard_player_2)
           yahtzee = Scoreboard(0, 610, 'YAHTZEEEEEE!', selected_choice[11], possibility[11], done[11], 'YAHTZEEEEEE!', scoreboard_player_1, scoreboard_player_2)
           chance = Scoreboard(0, 645, 'Chance', selected_choice[12], possibility[12], done[12], 'Chance', scoreboard_player_1, scoreboard_player_2)
           total_2 = Scoreboard(0, 680, 'Total Score', False, False, True, 'Total Score', scoreboard_player_1, scoreboard_player_2)
           ones.create_scoreboard()
           twos.create_scoreboard()
           threes.create_scoreboard()
           fours.create_scoreboard()
           fives.create_scoreboard()
           sixes.create_scoreboard()
           total_1.create_scoreboard()
           three_of_a_kind.create_scoreboard()
           four_of_a_kind.create_scoreboard()
           full_house.create_scoreboard()
           small_straight.create_scoreboard()
           large_straight.create_scoreboard()
           yahtzee.create_scoreboard()
           chance.create_scoreboard()
           total_2.create_scoreboard()
       elif player_2_turn == True:
           ones = Scoreboard(0, 190, 'Ones', selected_choice_player_2[0], possibility_player_2[0], done_player_2[0], 'Ones', scoreboard_player_1, scoreboard_player_2)  # FIX DIMENSIONS FOR ALL
           twos = Scoreboard(0, 225, 'Twos', selected_choice_player_2[1], possibility_player_2[1], done_player_2[1], 'Twos', scoreboard_player_1,  scoreboard_player_2)
           threes = Scoreboard(0, 260, 'Threes', selected_choice_player_2[2], possibility_player_2[2], done_player_2[2], 'Threes', scoreboard_player_1, scoreboard_player_2)
           fours = Scoreboard(0, 295, 'Fours', selected_choice_player_2[3], possibility_player_2[3], done_player_2[3], 'Fours', scoreboard_player_1, scoreboard_player_2)
           fives = Scoreboard(0, 330, 'Fives', selected_choice_player_2[4], possibility_player_2[4], done_player_2[4], 'Fives', scoreboard_player_1, scoreboard_player_2)
           sixes = Scoreboard(0, 365, 'Sixes', selected_choice_player_2[5], possibility_player_2[5], done_player_2[5], 'Sixes', scoreboard_player_1, scoreboard_player_2)
           total_1 = Scoreboard(0, 400, 'Total', False, False, True, 'Total', scoreboard_player_1, scoreboard_player_2)
           three_of_a_kind = Scoreboard(0, 435, 'Three of a Kind', selected_choice_player_2[6], possibility_player_2[6], done_player_2[6], 'Three of a Kind', scoreboard_player_1, scoreboard_player_2)
           four_of_a_kind = Scoreboard(0, 470, 'Four of a Kind', selected_choice_player_2[7], possibility_player_2[7], done_player_2[7], 'Four of a Kind', scoreboard_player_1, scoreboard_player_2)
           full_house = Scoreboard(0, 505, 'Full House', selected_choice_player_2[8], possibility_player_2[8], done_player_2[8], 'Full House', scoreboard_player_1, scoreboard_player_2)
           small_straight = Scoreboard(0, 540, 'Small Straight', selected_choice_player_2[9], possibility_player_2[9], done_player_2[9], 'Small Straight', scoreboard_player_1, scoreboard_player_2)
           large_straight = Scoreboard(0, 575, 'Large Straight', selected_choice_player_2[10], possibility_player_2[10], done_player_2[10], 'Large Straight', scoreboard_player_1, scoreboard_player_2)
           yahtzee = Scoreboard(0, 610, 'YAHTZEEEEEE!', selected_choice_player_2[11], possibility_player_2[11], done_player_2[11], 'YAHTZEEEEEE!', scoreboard_player_1, scoreboard_player_2)
           chance = Scoreboard(0, 645, 'Chance', selected_choice_player_2[12], possibility_player_2[12], done_player_2[12], 'Chance', scoreboard_player_1, scoreboard_player_2)
           total_2 = Scoreboard(0, 680, 'Total Score', False, False, True, 'Total Score', scoreboard_player_1, scoreboard_player_2)
           ones.create_scoreboard()
           twos.create_scoreboard()
           threes.create_scoreboard()
           fours.create_scoreboard()
           fives.create_scoreboard()
           sixes.create_scoreboard()
           total_1.create_scoreboard()
           three_of_a_kind.create_scoreboard()
           four_of_a_kind.create_scoreboard()
           full_house.create_scoreboard()
           small_straight.create_scoreboard()
           large_straight.create_scoreboard()
           yahtzee.create_scoreboard()
           chance.create_scoreboard()
           total_2.create_scoreboard()

       if player_1_turn:
           possibility = check_possibility(possibility, numbers)
       else:
           possibility_player_2 = check_possibility(possibility_player_2, numbers)

       dice_1.create_dice()
       dice_2.create_dice()
       dice_3.create_dice()
       dice_4.create_dice()
       dice_5.create_dice()



       # Roll dice if button was clicked
       if roll:
           for i in range(len(numbers)):
               if not dice_selected[i]:  # only reroll if die isnt locked
                   numbers[i] = random.randint(1, 6)
           roll = False #resets the flag


       pygame.display.flip()




pygame.quit()

#gamemode 1 Regular
'''play_button = int(input("Click This button to play")) #replaced by number 0 for now
select_gamemode = int(input("Click Which Gamemode")) #swap to a different screen asking the user for the gamemode they want to play


regular = 1 #place stander for button


if regular == '1' or ' 1':
   #ask user against human or AI
   #ask for AI difficulty
   #swap to gamestart with scoreboard


#gamemode 2 = simplified


simplified = select_gamemode


if simplified == '2' or ' 2':
   #ask user against human or ai
   #if ai ask for ai difficulty
   #swap to screen with scoreboard


if select_gamemode == '3' or ' 3': #for chronological
   #ask user against human
   # if not then against which difficulty of AI easy, medium or hard,
if select_gamemode == '4' or ' 4': #this is for dice locking
   #ask user afainst human
   #if not ask against which difficulty of AI'''

