import pygame
from pygame import mixer 
import math
import random 


# Initializing pygame 
pygame.init()

# Creating a screen 
screen = pygame.display.set_mode((800,600)) 

# Title and Logo 
pygame.display.set_caption("SpaceInvaders.Inc") 
icon = pygame.image.load("spaceship.png") 
pygame.display.set_icon(icon)  

# Background 
background = pygame.image.load("background.png") 

#Background music 
mixer.music.load('background.wav') 
mixer.music.play(-1) 

# Player 
player_img = pygame.image.load("player.png")
playerX = 370
playerY =  480 
player_delX = 0 
player_delY = 0

def player(X,Y) :
	screen.blit(player_img,(X,Y))  

# Enemies 
num = 5
monster_img = [] 
monsterX = [] 
monsterY = [] 
monster_delX = []
monster_delY = []
for i in range(num) : 
	monster_img.append(pygame.image.load("monster1.png"))
	monsterX.append(random.randint(0,736)) 
	monsterY.append(random.randint(50,175))
	monster_delX.append(2) 
	monster_delY.append(35) 

def monster(img,X,Y) :
	screen.blit(img,(X,Y))


# Bullet 
bullet_img = pygame.image.load("bullet.png") 
bulletX = 0 
bulletY = 480 
bullet_delY = -10 
bullet_state = "ready"

def fire_bullet(X,Y) :  
	global bullet_state 
	bullet_state = "fire" 
	screen.blit(bullet_img,(X+15,Y+16)) 


# Function to check collision 
def collision(x1,y1,x2,y2) :
	dist = math.sqrt(math.pow(x1-x2,2) + math.pow(y1-y2,2)) 
	if dist <= 27 : 
		return True 
	return False 


# Player Score 
player_score = 0
font1 = pygame.font.Font('freesansbold.ttf',32)

def show_score() : 
	score = font1.render("Score : "+str(player_score),True,(255,255,255)) 
	screen.blit(score,(10,10))

font2 = pygame.font.Font('freesansbold.ttf',64)
def game_over() :
	text1 = font2.render("GAME OVER",True,(255,255,255))
	text2 = font1.render("Your final score: "+str(player_score),True,(255,255,255))
	screen.blit(text1,(200,250)) 
	screen.blit(text2,(250,310)) 


# Game loop 
running  = True 

while running  : 
	
	screen.fill((0,0,0)) 
	screen.blit(background,(0,0)) 
	
	for event in pygame.event.get() : 
		if event.type == pygame.QUIT : 
			running = False 
		
		if event.type == pygame.KEYDOWN :
			if event.key == pygame.K_LEFT :
				player_delX = -3
			if event.key == pygame.K_RIGHT :
				player_delX = 3
			if event.key == pygame.K_SPACE :
				if bullet_state == "ready" : 
					fire_sound = mixer.Sound('fire.wav') 
					fire_sound.play()
					bulletX = playerX
					fire_bullet(bulletX,bulletY)

		if event.type == pygame.KEYUP : 
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT : 
				player_delX = 0

	# Player Movement
	playerX += player_delX
	if playerX <= 0 :
		playerX = 0
	elif playerX >= 736 :
		playerX = 736

	# Monster movement
	for i in range(num) :
		if monsterY[i] >= 440 :
			for j in range(num) : 
				monsterY[j] = 1000
			game_over()
			break

		monsterX[i] += monster_delX[i]; 
		if monsterX[i] <= 0 : 
			monsterX[i] = 0 
			monster_delX[i] = 2
			monsterY[i] += monster_delY[i]
		elif monsterX[i] >= 736 : 
			monsterX[i] = 736 
			monster_delX[i] = -2
			monsterY[i] += monster_delY[i]

	# Bullet Movement
	if(bulletY <= 0) :
		bullet_state = "ready" 
		bulletY = 480 	
		bulletX = 0
	if bullet_state == "fire" : 
		fire_bullet(bulletX,bulletY)
		bulletY += bullet_delY 

	# Check Collision
	for i in range(num) :
		if collision(monsterX[i],monsterY[i],bulletX,bulletY) :
			explosion_sound = mixer.Sound('explosion.wav') 
			explosion_sound.play()
			bullet_state = "ready" 
			bulletY = 480
			bulletX = 0
			player_score += 1
			monsterX[i] = random.randint(0,736)
			monsterY[i] = random.randint(50,175)

	player(playerX,playerY)
	for i in range(num) :
		monster(monster_img[i],monsterX[i],monsterY[i])
	show_score()
	pygame.display.update()








