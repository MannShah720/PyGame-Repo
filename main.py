import pygame as pg
import random
import sqlite3

# Define decision
decision = ""

# Create sqlite database
def create_table():
    with sqlite3.connect("Details.db") as db:
        cursor = db.cursor()
        sql = """ CREATE TABLE IF NOT EXISTS tblScoreDetails
                  (Word TEXT Primary Key,
                  Score INTEGER,
                  Decision TEXT) """
        cursor.execute(sql)

# Add data to table
def add_data():
    with sqlite3.connect("Details.db") as db:
        cursor = db.cursor()
        sql = """ INSERT OR IGNORE INTO tblScoreDetails
                   (Word, Score, Decision)
                   VALUES ("{}", {}, "{}")""".format(rand_word, score, decision)
        cursor.execute(sql)

# Initialise Pygame
pg.init()
window = pg.display.set_mode((1100, 675))
clock = pg.time.Clock()


# Music & Sound Effects
music = pg.mixer.music.load("Sounds/Music.mp3")
music = pg.mixer.music.set_volume(0.2)
music = pg.mixer.music.play(-1)
lost_sound = pg.mixer.Sound("Sounds/GameOver.wav")
play_lost_sound = True


# Font
font_type = "Typographica.ttf"
font = pg.font.Font(font_type, 40)


# Game Assets
game_bg = pg.image.load("Assets/GameBG.png")
pg.display.set_icon(pg.image.load("Assets/AtomBG.png"))
score = 0
FPS = 60
mouse_pos = pg.mouse.get_pos() 


# Brain (Player)
class player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 4


# Creating player object
brain = player(225, 345, 90, 90)
brain_surface = pg.transform.scale(pg.image.load("Assets/Brain.png"),(brain.width, brain.height))
brain_rect = brain_surface.get_rect(center = (brain.x, brain.y))


# Physics Words list
word_lst = [["Velocity", 0],    ["Acceleration", 1], ["Drag", 2],          ["Weight", 3],      ["Friction", 4], ["Ohm's Law", 5],
            ["Lenz", 6],        ["Tension", 7],      ["Upthrust", 8],      ["Moment", 9],      ["Quark", 10],  ["Reflection", 11],
            ["Density", 12],    ["Pressure", 13],    ["Power", 14],        ["Extension", 15],  ["Stress", 16],  ["Strain", 17],
            ["Momentum", 18],   ["Impulse", 19],     ["Current", 20],      ["Isotope", 21],    ["Lepton", 22],      ["EMF", 23],
            ["Resistance", 24], ["Resistivity", 25], ["Longitudinal", 26], ["Transverse", 27], ["Faraday", 28],
            ["Amplitude", 29],  ["Wavelength", 30],  ["Frequency", 31],    ["Period", 32],     ["Superposition", 33],
            ["Refraction", 34], ["Diffraction", 35], ["Polarisation", 36], ["Intensity ", 37], ["Interference", 38],
            ["Coherence", 39],  ["SHC", 40],         ["SLH", 41],          ["Mole", 42],       ["SHM", 43],     ["Resonance", 44],
            ["Damping", 45],    ["Work", 46],        ["Antiparticle", 47], ["Boltzmann", 48],  ["Capacitance", 49],
            ["B-Field", 50],    ["G-Field", 51],     ["G-Potential", 52],  ["E-Field", 53],    ["E-Potential", 54]]


# Physics Words class
class physics_words():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 12
        self.font = pg.font.Font(font_type,50)


# 1st physics word
rand_pos = random.randint(10,640)
word = physics_words(1100, rand_pos)
rand_word = word_lst[random.randint(0,len(word_lst) - 1)][0]
physicsTxt = word.font.render(f"{rand_word}", True, "black")
physicsTxt_rect = physicsTxt.get_rect()
physicsTxt_rect.x = 1100


# 2nd physics word
rand_pos2 = random.randint(10,640)
word2 = physics_words(1200, rand_pos2)
rand_word2 = word_lst[random.randint(0,len(word_lst) - 1)][0]
physicsTxt2 = word2.font.render(f"{rand_word2}", True, "black")
physicsTxt_rect2 = physicsTxt2.get_rect()
physicsTxt_rect2.x = 1100

# Load Button Images
unsure_img = pg.image.load("Assets/Unsure.png")
right_img = pg.image.load("Assets/Right.png")

# Button class
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def draw(self):

        action = False

        # Get position of mouse
        pos = pg.mouse.get_pos()

        # Checks if the button is pressed by the mouse
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            if pg.mouse.get_pressed()[0] == 0:
                self.clicked = False

        window.blit(self.image, (self.rect.x, self.rect.y))

        return action

# Create button instances
unsure_button = Button(350, 525, unsure_img)
right_button = Button(600, 525, right_img)

# Menu
start_game = False
menu = pg.image.load("Assets/MenuBG.png")

def draw_menu():
    window.blit(menu,(0,0))
    pg.display.update()


# Displaying the game
def draw_game():
    window.blit(game_bg,(0,0))
    window.blit(brain_surface, brain_rect)
    window.blit(physicsTxt, physicsTxt_rect)
     
    if score >= 5:
        window.blit(physicsTxt2, physicsTxt_rect2)
    scoreTxt = font.render(f"{score}", True, "black")
    window.blit(scoreTxt,(548,20))
    pg.display.update()
    

# Game Loop
running = True
while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Title & FPS
    clock.tick(FPS) 
    pg.display.set_caption(f"Mind Your Physics! ({clock.get_fps() :.1f} FPS)")

    # Key press
    keys = pg.key.get_pressed()

    if keys[pg.K_q]:
        running = False

    if keys[pg.K_SPACE]:
        start_game = True

    if start_game == True:
        lost = False

        # Check if brain collides with the word
        if pg.Rect.colliderect(brain_rect, physicsTxt_rect):
            lost = True
        if pg.Rect.colliderect(brain_rect, physicsTxt_rect2):
            lost = True
        
        if lost == False:
            # Player movement
            if keys[pg.K_d] and brain_rect.x < 1000:
                brain_rect.x += brain.velocity
            elif keys[pg.K_a] and brain_rect.x > 0:
                brain_rect.x -= brain.velocity
            elif keys[pg.K_w] and brain_rect.y > 0:
                brain_rect.y -= brain.velocity
            elif keys[pg.K_s] and brain_rect.y < 580:
                brain_rect.y += brain.velocity

            # Physics Word movement
            if physicsTxt_rect.x <= 1100 and physicsTxt_rect.x >= -200:
                physicsTxt_rect.x -= word.velocity
            if physicsTxt_rect2.x <= 1100 and physicsTxt_rect2.x >= -200:
                physicsTxt_rect2.x -= word2.velocity

                # Generate new word after dodging
            elif physicsTxt_rect.x < -200:
                rand_word = word_lst[random.randint(0,len(word_lst) - 1)][0]
                physicsTxt = word.font.render(f"{rand_word}", True, "black")
                physicsTxt_rect = physicsTxt.get_rect()
                physicsTxt_rect.x = 1100
                physicsTxt_rect.y = random.randint(10,640)

                # Increment score after dodging 1st word
                score += 1

            elif score >= 5 and physicsTxt_rect2.x < -200:
                rand_word2 = word_lst[random.randint(0,len(word_lst) - 1)][0]
                physicsTxt2 = word.font.render(f"{rand_word2}", True, "black")
                physicsTxt_rect2 = physicsTxt2.get_rect()
                physicsTxt_rect2.x = 1100
                physicsTxt_rect2.y = random.randint(10,640)

                # Increment score after dodging 2nd word
                score += 1
                scoreTxt = font.render(f"{score}", True, "black")

                # Difficulty increase
                # Words move faster as you gain a higher score
                for i in range(5,65,5):
                    if score == i:
                        word.velocity += 2
                    if score == i + 15:
                        word2.velocity +=2

            draw_game()
        
        # When the player loses the game
        elif lost == True:
            if play_lost_sound:
                play_lost_sound = False
                lost_sound.play()

            # Stops the music
            music = pg.mixer.music.pause()

            # Loads definition

            # For loop that goes through the word list
            for x in word_lst:

                # If score is less than 5, it checks for only the 1st word generated
                if score < 5:
                    if x[0] == rand_word:
                        lost_bg = pg.image.load(f"Definitions/Word {x[1]}.png")

                # If score is greater than 5, it checks for either the 1st or 2nd word depending on the collision
                elif score >= 5:
                    if pg.Rect.colliderect(brain_rect, physicsTxt_rect):
                        if x[0] == rand_word:
                            lost_bg = pg.image.load(f"Definitions/Word {x[1]}.png")
                    if pg.Rect.colliderect(brain_rect, physicsTxt_rect2):
                        if x[0] == rand_word2:
                            lost_bg = pg.image.load(f"Definitions/Word {x[1]}.png")

            # Blits the definition onto the screen                
            window.blit(lost_bg, (0,0))
            
            if unsure_button.draw():
                decision = "Unsure"
                print("Unsure")
                
            
            if right_button.draw():
                decision = "Right"
                print("Right")

            # Updates database
            add_data()
            pg.display.update()

            # Restart the game
            if keys[pg.K_r]:
                start_game = False

                # Reset word velocity
                word.velocity = 12
                word2.velocity = 12

                # Reset word position
                brain_rect.x = 190
                brain_rect.y = 400
                physicsTxt_rect.x = 1100

                # Reset score
                score = 0
                music = pg.mixer.music.unpause()
                play_lost_sound = True
    
    # Continues drawing if not hit by a word
    else:
        draw_menu()
        

pg.quit()