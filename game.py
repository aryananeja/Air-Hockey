# This code is written to output a game commonly known as Air Hockey. 
# It has a two player feature and mystery feature wherin you have a random 
# size for the puck and the striker
# Written by Aryan Aneja

import simplegui
import random
import math
import time 

# Width and height for the frame. 
WIDTH = 800
HEIGHT = 450

# Size of button on canvas
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 50

# Game stages and their assigned numeric values
MAIN_MENU = 0
SECONDARY_MENU = 1
PLAYING = 2
PLAYING_2 = 3
END_MENU = 4

# Background images
PLAYING_IMG = simplegui.load_image("https://cdn.discordapp.com/attachments/810792775578288168/902724312514035753/Presentation1.png")
MAIN_MENU_IMAGE = simplegui.load_image("https://cdn.discordapp.com/attachments/810792775578288168/912776611873566750/main_menu.png")
SECONDARY_MENU_IMG = simplegui.load_image("https://cdn.discordapp.com/attachments/810792775578288168/930155034166063196/Presentation5.png")
END_MENU_IMG = simplegui.load_image("https://cdn.discordapp.com/attachments/810792775578288168/918632695171543062/endscreen.png")

# Game objects
STRIKER_1_IMG = simplegui.load_image("https://cdn.discordapp.com/attachments/810792775578288168/902728579924779038/il9XAhh.png")
STRIKER_2_IMG = simplegui.load_image("https://cdn.discordapp.com/attachments/810792775578288168/902728596618096640/odeqada.png")
PUCK_IMG = simplegui.load_image("https://assets.thdstatic.com/mobile-apps/2d/images/301036883_301036883.png")

# Game sounds
GAME_END_SOUND = simplegui.load_sound("https://cdn.discordapp.com/attachments/810792775578288168/933470113292771348/mixkit-medieval-show-fanfare-announcement-226.wav")
GAME_SOUND = simplegui.load_sound("https://cdn.discordapp.com/attachments/810792775578288168/933463968318652446/mixkit-game-level-music-689.wav")
COLLIDE_SOUND = simplegui.load_sound("https://cdn.discordapp.com/attachments/810792775578288168/933462355550015548/mixkit-quick-win-video-game-notification-269-AudioTrimmer.com2.wav")
GOAL_SOUND = simplegui.load_sound("https://cdn.discordapp.com/attachments/810792775578288168/935219987075973150/mixkit-game-bonus-reached-20651-AudioTrimmer.com.wav")

# Dictionaries for all the image sizes and centers.
IMG_SIZES = {
             PLAYING_IMG:[1280,720],
             MAIN_MENU_IMAGE:[1280,720],
             SECONDARY_MENU_IMG:[1280,720],
             END_MENU_IMG:[1280,720],
             STRIKER_1_IMG:[960,540], 
             STRIKER_2_IMG:[960,540], 
             PUCK_IMG:[600,600]
            }


IMG_CENTERS = {
               PLAYING_IMG:[1280/2,720/2], 
               MAIN_MENU_IMAGE:[1280/2,720/2],
               SECONDARY_MENU_IMG:[1280/2,720/2],
               END_MENU_IMG:[1280/2,720/2],
               STRIKER_1_IMG:[960/2,540/2], 
               STRIKER_2_IMG:[960/2,540/2], 
               PUCK_IMG:[600/2,600/2]
              }

game_state = MAIN_MENU
countdown = 0
game_over = False 
time1 = time.time()
GAME_SOUND.play()


# Global objects in the game
def new_game():
    global player1
    global player2
    global puck1
    global goal1
    global goal2
    global timer1
    global button1
    global button2
    player1 = Striker(STRIKER_1_IMG, [200, 225])
    player2 = Striker(STRIKER_2_IMG, [600,225])
    puck1 = Puck(PUCK_IMG)
    goal1 = Goal([0,225])
    goal2 = Goal([800,225])
    timer1 = Timer([400,50])
    button1 = Button((220,275), BUTTON_WIDTH, BUTTON_HEIGHT)
    button2 = Button((590,275), BUTTON_WIDTH, BUTTON_HEIGHT)

    
# Used to obtain the distance betwenn two colliding objects
def distance(pos1,pos2):
    a = pos2[0] - pos1[0]
    b = pos2[1] - pos1[1]
    d = math.sqrt(a**2 + b**2)
    return d


# Generate random sizes for the puck and strikers in the mystery game mode
def random_sizes():
    player1.size = [random.randrange(0,100),random.randrange(0,200)]
    player1.rad = player1.size[0]/2
    player2.size = [random.randrange(0,100),random.randrange(0,200)]
    player2.rad = player2.size[1]/2
    puck1.size = [random.randrange(0,100),random.randrange(0,100)]
    puck1.rad = puck1.size[0]/2

 
# Striker class
class Striker:
    def __init__(self, img, pos):
        self.img = img
        self.pos = pos
        self.vel = [0,0]
        self.speed = 7.5
        self.size = [160,90]
        self.rad = 40
        self.score = 0
        self.name = ""

    # Drawing the strikers on the gamecanvas
    def draw(self,canvas):
        center = IMG_CENTERS[self.img]
        size = IMG_SIZES[self.img]
        canvas.draw_image(self.img,
                         center,
                         size,
                         self.pos,
                         self.size)
        
    # Defining the boundaries for the strikers and update the positions
    # for the strikers
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        if self.pos[0] < self.rad:
            self.pos[0] = self.rad
        
        if self.pos[0] > WIDTH - self.rad:
            self.pos[0] = WIDTH - self.rad
        
        if self.pos[1] < self.rad:
            self.pos[1] = self.rad
            
        if self.pos[1] > HEIGHT - self.rad:
            self.pos[1] = HEIGHT - self.rad 
         
        
# Puck class        
class Puck:
    def __init__(self,img):
        self.img = img
        self.pos = [WIDTH/2,HEIGHT/2]
        self.size = [50,50]
        self.vel = [0,5]
        self.rad = 30
        
    # Drawing the puck on the game canvas       
    def draw(self,canvas):
        center = IMG_CENTERS[self.img]
        size = IMG_SIZES[self.img]
        canvas.draw_image(self.img, 
                          center,
                          size,
                          self.pos,
                          self.size) 
        
    # Carries out the movements for the puck
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        # Setting velocity limits on puck
        if self.vel[0] >= 15:
            self.vel[0] = 15
            
        if self.vel[1] >= 15:
            self.vel[1] = 15
        
        # Left side of the screen
        if self.pos[0] <= self.rad:
            self.pos[0] = self.rad
            if self.vel[0] < 0:
                self.vel[0] += 1
                self.vel[0] *= -1
            elif self.vel[0] > 0:
                self.vel[0] -= 1
                self.vel[0] *= -1
                
        # Right side of the screen
        if self.pos[0] >= WIDTH - self.rad:
            self.pos[0] = WIDTH - self.rad
            if self.vel[0] < 0:
                self.vel[0] += 1
                self.vel[0] *= -1
            elif self.vel[0] > 0:
                self.vel[0] -= 1
                self.vel[0] *= -1 
                
        # Top of the screen  
        if self.pos[1] <= self.rad :
            self.pos[1] = self.rad 
            if self.vel[1] < 0:
                self.vel[1] += 1
                self.vel[1] *= -1
            elif self.vel[1] > 0:
                self.vel[1] -= 1
                self.vel[1] *= -1
                
        # Bottom of the screen       
        if self.pos[1] >= HEIGHT - self.rad:    
            self.pos[1] = HEIGHT - self.rad
            if self.vel[1] < 0:
                self.vel[1] += 1
                self.vel[1] *= -1
            elif self.vel[1] > 0:
                self.vel[1] -= 1
                self.vel[1] *= -1
    
    # To check and return the distance if they collide
    def has_collided(self, other):
        dist = distance(self.pos, other.pos)
        return dist <= self.rad + other.rad
    

# Goal class    
class Goal:
    def __init__(self,pos):
        self.pos = pos
        self.height = 150
        self.rad = 70
        
    # Draws the goal lines and goal restrictions on both ends of the screen
    def draw(self, canvas):
        canvas.draw_line((self.pos[0],self.pos[1]-self.height/2), 
                          (self.pos[0],self.pos[1]+self.height/2),
                            5, "black")
        
        canvas.draw_circle([self.pos[0],self.pos[1]], self.rad, 
                           2, "white")
        
    # To check and see if stiker and the goal in_crease line colldes             
    def in_crease(self, striker):    
        dist = distance(self.pos, striker.pos)
        return dist <= self.rad + striker.rad
         
    def has_collided(self, puck):
        cond1 = abs(self.pos[0] - puck.pos[0]) <= puck.rad
        cond2 = puck.pos[1] >=self.pos[1]-self.height/2
        cond3 = puck.pos[1] <= self.pos[1] + self.height/2
        if cond1 and cond2 and cond3:
            return True
        else:
            return False
        
        
# This is the timer class and we are defining the various functions under it.            
class Timer:
    def __init__(self,pos):
        self.pos = pos
        self.width = 200
        self.height = 60
    
    # Draws the box for the timer at the top of screen
    def draw(self, canvas):
        canvas.draw_polygon([[self.pos[0]-self.width/2,self.pos[1]-self.height/2],
                             [self.pos[0]+self.width/2,self.pos[1]-self.height/2],
                             [self.pos[0]+self.width/2,self.pos[1]+self.height/2],
                             [self.pos[0]-self.width/2,self.pos[1]+self.height/2]], 
                            2,"white", 
                            "grey")
        
        # Draw player's socre and offset it acording to the score's width
        offset1 = frame.get_canvas_textwidth(str(player1.score), 50)/2
        canvas.draw_text(str(player1.score), 
                         (self.pos[0]- self.width/4 - offset1 ,self.pos[1] + 18), 
                         50, 'Red')
      
        offset2 = frame.get_canvas_textwidth(str(player2.score), 50)/2
        canvas.draw_text(str(player2.score), 
                         (self.pos[0]+ self.width/4 - offset2 ,self.pos[1] + 18), 
                         50, 'Red')
        
        
# Button class
class Button:
    def __init__(self, location, width, height):
        self.pos = location
        self.width = width
        self.height = height
        self.left = self.pos[0] - self.width/2
        self.right = self.pos[0] + self.width/2
        self.top = self.pos[1] - self.height/2
        self.bottom = self.pos[1] + self.height/2
        
    # Selection method for buttons
    def is_selected(self, click_pos):
        if click_pos[0] >= self.left and click_pos[0] <= self.right:
            if click_pos[1] >= self.top and click_pos[1] <= self.bottom:
                return True
        return False
    
                  
# Handler to draw on canvas
def draw(canvas):
    global countdown
    global countdown_music
    global game_state
    global winner
    global time1
    global time2
    global game_sound
    
    center1 = IMG_CENTERS[MAIN_MENU_IMAGE]
    size1 = IMG_SIZES[MAIN_MENU_IMAGE]
    
    center2 = IMG_CENTERS[PLAYING_IMG]
    size2 = IMG_SIZES[PLAYING_IMG]  
    
    center3 = IMG_CENTERS[SECONDARY_MENU_IMG]
    size3 = IMG_SIZES[SECONDARY_MENU_IMG] 
    
    center4 = IMG_CENTERS[END_MENU_IMG]
    size4 = IMG_SIZES[END_MENU_IMG] 
     
    if game_state == MAIN_MENU:
        canvas.draw_image(MAIN_MENU_IMAGE,
                          center1,
                          size1,
                          [WIDTH/2,HEIGHT/2],
                         [ WIDTH,HEIGHT])
        
        # Draw player's inputted name and offset it acording to the name's text width
        offset1 = frame.get_canvas_textwidth(player1.name, 40)/2
        canvas.draw_text(player1.name, [217 - offset1,360], 40, "White")
        
        offset2 = frame.get_canvas_textwidth(player2.name, 40)/2
        canvas.draw_text(player2.name, [587 - offset2,360], 40, "White")
        
        time2 = time.time()
        # Loop for the game sound
        if time2 - time1 >= 8:
            time1 = 0
            GAME_SOUND.play()
        
       # Countdown used to change game state to PLAYING after a certain time
        if player1.name != '' and player2.name != '' and countdown < 100:
            countdown += 1
        elif player1.name != '' and player2.name != '' and countdown == 100:
            game_state = SECONDARY_MENU
            countdown=0
            
    elif game_state == SECONDARY_MENU:
        canvas.draw_image(SECONDARY_MENU_IMG,
                          center3,
                          size3,
                          [WIDTH/2,HEIGHT/2],
                          [WIDTH,HEIGHT])
        
    elif game_state == PLAYING:
        canvas.draw_image(PLAYING_IMG,
                          center1,
                          size1,
                          [WIDTH/2,HEIGHT/2],
                          [WIDTH,HEIGHT])
        
        # Changes to puck position and velocity when collided with player1
        if puck1.has_collided(player1):
            puck1.pos[0] -= puck1.vel[0]
            puck1.pos[1] -= puck1.vel[1]
            puck1.vel[0] *= -1
            puck1.vel[0] += player1.vel[0]
            puck1.vel[1] += player1.vel[1]  
            puck1.pos[0] += puck1.vel[0]
            puck1.pos[1] += puck1.vel[1]
            COLLIDE_SOUND.play()
        
        # Changes to puck position and velocity when collided with player2
        if puck1.has_collided(player2):
            puck1.pos[0] -= puck1.vel[0]
            puck1.pos[1] -= puck1.vel[1]
            puck1.vel[0] *= -1
            puck1.vel[0] += player2.vel[0] 
            puck1.vel[1] += player2.vel[1]
            puck1.pos[0] += puck1.vel[0]
            puck1.pos[1] += puck1.vel[1]
            COLLIDE_SOUND.play() 
        
        # Changes to puck position and velocity & player's position and score
        # when collided with goal1
        if goal1.has_collided(puck1):            
            player2.score += 1
            puck1.pos[0] = 500
            puck1.pos[1] = 225
            puck1.vel = [0,0]
            player1.pos[0] = 200
            player1.pos[1] = 225
            player2.pos[0] = 600            
            player2.pos[1] = 225
            GOAL_SOUND.play() 
                
        # Changes to puck position and velocity & player's position and score 
        # when collided with goal2               
        if goal2.has_collided(puck1):            
            player1.score += 1            
            puck1.pos[0] = 300
            puck1.pos[1] = 225
            puck1.vel = [0,0]          
            player1.pos[0] = 200
            player1.pos[1] = 225            
            player2.pos[0] = 600
            player2.pos[1] = 225
            GOAL_SOUND.play()
                                  
        if player1.pos[0] > WIDTH/2 - player1.rad:
            player1.pos[0] = WIDTH/2 - player1.rad
            
        if player2.pos[0] < WIDTH/2 + player1.rad:
            player2.pos[0] = WIDTH/2 + player1.rad
            
        player1.draw(canvas)
        player2.draw(canvas)
        player1.update()  
        player2.update()
        puck1.draw(canvas)
        puck1.update()
        goal1.draw(canvas)
        goal2.draw(canvas)
        timer1.draw(canvas)
        
        # Negative velcoity to not let it enter whens striker collides
        if goal1.in_crease(player1):
            player1.pos[0] -= player1.vel[0] 
            player1.pos[1] -= player1.vel[1] 
            
        if goal2.in_crease(player2):
            player2.pos[0] -= player2.vel[0] 
            player2.pos[1] -= player2.vel[1]
        
        # Display END_MENU state if the score of any player reaches 10
        if player1.score >= 10:
            game_state = END_MENU
            winner = player1.name
            GAME_END_SOUND.play()
        
        if player2.score >= 10: 
            game_state = END_MENU
            winner = player2.name
            GAME_END_SOUND.play()
                         
    elif game_state == END_MENU:
        canvas.draw_image(PLAYING_IMG,
                          center1,
                          size1,
                          [WIDTH/2,HEIGHT/2],
                          [WIDTH,HEIGHT])
        
        canvas.draw_image(END_MENU_IMG,
                          center2,
                          size2,
                          [WIDTH/2,HEIGHT/2],
                          [0.8*WIDTH,0.8*HEIGHT])
        
        # Get the the winners text width and display it
        offset3 = frame.get_canvas_textwidth(winner +"wins", 40)/2
        
        canvas.draw_text(winner+" wins", 
                         [WIDTH/2-offset3,225],
                         40,
                         "WHITE" )
        
        GAME_SOUND.pause()    
        
   
# Assigning the striker movements when certain keys are pressed   
def key_press(key):
    if key==simplegui.KEY_MAP['A']:
        player1.vel[0]=-player1.speed
        
    if key==simplegui.KEY_MAP['D']:
        player1.vel[0]=player1.speed
        
    if key==simplegui.KEY_MAP['W']:
        player1.vel[1]=-player1.speed
        
    if key==simplegui.KEY_MAP['S']:
        player1.vel[1]=player1.speed
        
    if key==simplegui.KEY_MAP['left']:
        player2.vel[0]=-player2.speed
        
    if key==simplegui.KEY_MAP['right']:
        player2.vel[0]=player2.speed
        
    if key==simplegui.KEY_MAP['up']:
        player2.vel[1]=-player2.speed
        
    if key==simplegui.KEY_MAP['down']:
        player2.vel[1]=player2.speed
        
        
# Assigning the striker movements when certain keys are released     
def key_release(key):
    if key==simplegui.KEY_MAP['A']:
        player1.vel[0] =0
        
    if key==simplegui.KEY_MAP['D']:
        player1.vel[0] =0
        
    if key==simplegui.KEY_MAP['W']:
        player1.vel[1]=0
        
    if key==simplegui.KEY_MAP['S']:
        player1.vel[1]=0
        
    if key==simplegui.KEY_MAP['left']:
        player2.vel[0] =0
        
    if key==simplegui.KEY_MAP['right']:
        player2.vel[0] =0
        
    if key==simplegui.KEY_MAP['up']:
        player2.vel[1]=0
        
    if key==simplegui.KEY_MAP['down']:
        player2.vel[1]=0
     
    
def mouse_click(mouse_position):
    global game_state
    if button1.is_selected(mouse_position):
        game_state = PLAYING
        
    if button2.is_selected(mouse_position):
        random_sizes()
        game_state = PLAYING
        
        
# Defining the text input labels         
def player1_name(text_input):
    global player1
    player1.name = text_input
   

def player2_name(text_input):
    global player2
    player2.name = text_input

     
# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home",WIDTH,HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_press)
frame.set_keyup_handler(key_release)
frame.set_mouseclick_handler(mouse_click)
frame.add_input("PLAYER_1", player1_name, 50)
frame.add_input("PLAYER_2", player2_name, 50)
label1 = frame.add_label('')
label1 = frame.add_label('Game Instructions',200)
label1 = frame.add_label('')
label2 = frame.add_label('Attention Player 1 ',100)
label2 = frame.add_label('Use WASD keys to move your striker in the game',150)
label1 = frame.add_label('')
label1 = frame.add_label('')
label3 = frame.add_label('Attention Player 2 ',100)
label3 = frame.add_label('Use Arrow keys to move your striker in the game',150)

# Start the frame animation
new_game()
frame.start()

