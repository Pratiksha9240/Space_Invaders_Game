import pygame
from pygame import mixer
import random
import math

pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Space Invaders")

player_image = pygame.image.load("spaceship.png")
alien_image = pygame.image.load("alien.png")

alienImage = []
alienx = []
alieny = []
alienx_change = []
alieny_change = []
no_of_aliens = 15

for i in range(no_of_aliens):
    alienImage.append(alien_image)
    alienx.append(random.randint(10,750))
    alieny.append(random.randint(10,150))
    alienx_change.append(4)
    alieny_change.append(10)


# Bullet
# rest - bullet is not moving
# fire - bullet is moving
bulletImage = pygame.image.load('bullet.png')
bullet_X = 0
bullet_Y = 500
bullet_Xchange = 0
bullet_Ychange = 3
bullet_state = "rest"

def bullet(x, y):
	global bullet_state
	screen.blit(bulletImage, (x, y))
	bullet_state = "fire"


player_x = 370
player_y = 525
playerx_change = 0

def show_player(x,y):
    screen.blit(player_image,(x,y))


def show_alien(x,y,i):
    screen.blit(alienImage[i],(x,y))


# Collision Concept
def isCollision(x1, x2, y1, y2):
	distance = math.sqrt((math.pow(x1 - x2,2)) +
						(math.pow(y1 - y2,2)))
	if distance <= 50:
		return True
	else:
		return False


score = 0

score_font = pygame.font.Font('freesansbold.ttf',32)

def show_score(score):
    score_text = score_font.render("Score : "+str(score),True,(255,255,255))
    screen.blit(score_text,(10,10))
     

running = True

while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerx_change = 1.5
            if event.key == pygame.K_LEFT:
                playerx_change = -1.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "rest":
                    bullet_sound = mixer.Sound('bullet.wav')
                    bullet_sound.play()
                    bullet_X = player_x
                    bullet(bullet_X, bullet_Y)                 
        if event.type == pygame.KEYUP:
            playerx_change = 0

    if player_x < 0:
        player_x = 16
    elif player_x > width:
        player_x = 750

    # bullet movement
    if bullet_Y <= 0:
        bullet_Y = 600
        bullet_state = "rest"
    if bullet_state == "fire":
        bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Ychange



    player_x += playerx_change

    for i in range(no_of_aliens):
        alienx[i] += alienx_change[i]
        if alienx[i] < 0:
            alienx_change[i] = 4
            alieny[i] += alieny_change[i]
        elif alienx[i] > width:
            alienx_change[i] = -4
            alieny[i] += alieny_change[i]
        collision = isCollision(alienx[i],bullet_X,alieny[i],bullet_Y)
        if collision:
             score = score + 1
             explosion_sound = mixer.Sound('explosion.wav')
             explosion_sound.play()
             alienx[i] = random.randint(10,750)
             alieny[i] = random.randint(10,150)
        show_alien(alienx[i],alieny[i],i)

    show_score(score)
    show_player(player_x,player_y)
    pygame.display.update()

pygame.quit()