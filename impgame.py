import pygame
import random
import sys

pygame.init()

width=1000
height=700
red=(255,0,0)
blue=(0,0,255)
score_color=(0,0,0)
background_colour=(255,255,255)

player_size=50
player_pos=[width/2,height-2*player_size]

enemy_size=50
enemy_pos=[random.randint(0,width-enemy_size),0]
enemy_list=[enemy_pos]

screen = pygame.display.set_mode((width,height))

score=0
speed=10
rate=0.1
game_over=False

clock=pygame.time.Clock()
my_font=pygame.font.SysFont("monospace",35)

def set_level(score,speed):
	if score<20:
		speed=5
		#rate=0.05
	elif score<40:
		speed=7
		#rate=0.08
	elif score<60:
		speed = 9
		#rate= 0.1
	else:
		speed = 10
		#rate=0.2 
	return speed
def drop_enemies(enemy_list):
	delay=random.random()

	if len(enemy_list)<10 and delay<rate:
		x_pos=random.randint(0,width-enemy_size)
		y_pos=0
		enemy_list.append([x_pos,y_pos])

def draw_enemies(enemy_list):
	for enemy_pos in enemy_list:
		pygame.draw.rect(screen,blue,(enemy_pos[0],enemy_pos[1],enemy_size,enemy_size))

def update_enemy_pos(enemy_list,score):
	for i, enemy_pos in enumerate(enemy_list):

		if enemy_pos[1]>=0 and enemy_pos[1]<height:
			enemy_pos[1]=enemy_pos[1]+speed
		else: 
			enemy_list.pop(i)
			score=score+1
	return score

def collion_check(enemy_list, player_pos):
	for enemy_pos in enemy_list:
		if detect_collision(enemy_pos,player_pos):
			return True
	return False

def detect_collision(player_pos,enemy_pos):
	p_x=player_pos[0]
	p_y=player_pos[1]

	e_x=enemy_pos[0]
	e_y=enemy_pos[1]

	if (e_x>=p_x and e_x<(p_x+player_size)) or (p_x>=e_x and p_x<(e_x+enemy_size)):
		if(e_y>=p_y and e_y<(p_y+player_size)) or (p_y>=e_y and p_y<(e_y+enemy_size)):
			return True
	return False

while not game_over:
	
	for event in pygame.event.get():
		
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type==pygame.KEYDOWN:
			
			x=player_pos[0]
			y=player_pos[1]
			if event.key==pygame.K_LEFT:
				x-=player_size
			elif event.key==pygame.K_RIGHT:
				x+=player_size
			player_pos=[x,y]	
	screen.fill(background_colour)
	

	drop_enemies(enemy_list)
	score=update_enemy_pos(enemy_list,score)

	speed = set_level(score,speed)

	text = "Score: " + str(score)
	label=my_font.render(text, 1,score_color)
	screen.blit(label, (width-250,height-40))
	
	if collion_check(enemy_list,player_pos):
		game_over=True
		break

	draw_enemies(enemy_list)
	
	pygame.draw.rect(screen,red,(player_pos[0],player_pos[1],player_size,player_size))
	clock.tick(30)
	pygame.display.update()
