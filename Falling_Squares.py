import pygame
import random
import math
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600
GOLD = (212, 175, 55)
RED = (255,0,0)
BLUE = (0,0,255)
WHITE = (255, 255, 255)
LIGHT_BLUE = (47,141,255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
BACK = (0, 0, 0)
invi_time = 0
size = 40
ENEMIES = 2
enemy_list = []
pos = [WIDTH/2, HEIGHT - 2*size]
chance = random.randint(20, 60)
increase_change = 15
font_XXsmall = pygame.font.Font('freesansbold.ttf', 20)
font_xsmall = pygame.font.Font('freesansbold.ttf', 28)
font_small = pygame.font.Font('freesansbold.ttf', 32)
font_large = pygame.font.Font('freesansbold.ttf', 44)
font_xlarge = pygame.font.Font('freesansbold.ttf', 55)
font_XXlarge = pygame.font.Font('freesansbold.ttf', 70)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
total_score = 0

class Score:

	def __init__(self, value, certified=False):
		self.value = value
		self.certified = certified
		self.nedified = ""
		if certified: self.nedified = "Nedified*"

high_scores = [Score(0), Score(0), Score(0), Score(0), Score(0)]

game_over = False
paused = False

def restart():
	global enemy_list, up, gold_up, score, total_score, increase, game_over, moving_left, moving_right, ENEMIES, invi_count, victory, speed, nedified
	enemy_list.clear()
	up = 0
	gold_up = 0
	score = 0.1
	invi_count = 2
	increase = 60
	game_over = False
	i = 0
	moving_left = False
	moving_right = False
	ENEMIES = 2
	victory = False
	speed = 10
	nedified = True
	while i < 2:
		enemy_list.append(enemy(((random.randint(0, WIDTH-size)), 0), random.randint(5, 9), 40))
		i += 1

def menu():
	go = False
	global total_score
	total_score = math.floor(total_score/10)
	if total_score > high_scores[4].value:
		del high_scores[4]
		if total_score > high_scores[0].value:
				high_scores.insert(0, Score(total_score, nedified))
		else:
			j = 3
			while j >= 0:
				if total_score <= high_scores[j].value:
					high_scores.insert(j+1, Score(total_score, nedified))
					break
				j -= 1
	while not go:
		screen.fill(BACK)
		printwords(font_XXlarge, "Welcome to Ned", BLUE, WIDTH/2, HEIGHT - 200)
		printwords(font_large, "Highscores:", RED, WIDTH/2, 60)
		printwords(font_xsmall, "Press 'SPACE' to use Cloak", PURPLE, WIDTH/2, HEIGHT - 80)
		printwords(font_xsmall, "Press 'UP' to Play / Pause", PURPLE, WIDTH/2, HEIGHT - 120)
		printwords(font_xsmall, "Score 1000 to Win", PURPLE, WIDTH/2, HEIGHT - 40)
		for j in range(len(high_scores)):
			place = f'{j + 1}. {high_scores[j].value}'
			colour = WHITE
			if high_scores[j].value >= 1000: colour = GREEN
			elif high_scores[j].value >= 500: colour = YELLOW
			elif high_scores[j].value >= 200: colour = RED
			elif high_scores[j].value >= 50: colour = PURPLE
			printwords(font_large, place, colour, WIDTH/2, 120 + j*50)
			if high_scores[j].value > 0: printwords(font_XXsmall, high_scores[j].nedified, GOLD, WIDTH/2 + 125, 126 + j*50)
		pygame.display.update() 
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					go = True
	total_score = 0

	

def pause(winner):
	global paused
	global score, victory
	while paused:
		if winner == True:
			printwords(font_xlarge, "You Win Ned!", BLUE, WIDTH/2, HEIGHT/2)
			victory = True
		else:
			printwords(font_small, "Multiplier: " + str(score*10), PURPLE, WIDTH/2, 30)
			printwords(font_small, "Enemies: " + str(ENEMIES), PURPLE, WIDTH/2, 60)
			pygame.draw.rect(screen, PURPLE, (WIDTH/2 + 10, HEIGHT/2 - 20, 20, 50))
			pygame.draw.rect(screen, PURPLE, (WIDTH/2 - 30, HEIGHT/2 - 20, 20, 50))
		pygame.display.update() 
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					paused = False

def printwords(font_size, text, color, center_x, center_y):     
	words = font_size.render(text, False, color)
	text_rect = words.get_rect()
	if center_x != None:
		text_rect.center = (center_x, center_y)
	screen.blit(words, text_rect)

class enemy:
	
	def __init__(self, position, speed, area):
		self.x_pos = position[0]
		self.y_pos = position[1]
		self.speed = speed
		self.area = area

	def fall(self):
		if self.y_pos < HEIGHT:
			self.y_pos += self.speed
			return False
		else:
			self.y_pos = 0
			self.x_pos = random.randint(0, WIDTH-size)
			self.speed = random.randint(3, 7)
			return True

	def show(self):
		pygame.draw.rect(screen, RED, (self.x_pos, self.y_pos, self.area, self.area))

	def collide(self):

		e_x = self.x_pos
		e_y = self.y_pos
		p_x = pos[0]
		p_y = pos[1]		
		if (e_x >= p_x and e_x < (p_x + size)) or (p_x >= e_x and p_x < (e_x + self.area)):
			if (e_y >= p_y and e_y < (p_y + size)) or (p_y >= e_y and p_y < (e_y + self.area)):
				self.reset()

	def reset(self):
		if invi_time == 0:
			global game_over
			game_over = True

class gold(enemy):

	def show(self):
		pygame.draw.rect(screen, GREEN, (self.x_pos, self.y_pos, 25, 25))
		global gold_up
		gold_up = 0

	def reset(self):
		global score
		score += 0.1
		if coin in enemy_list:
			enemy_list.remove(coin)

class boost(enemy):

	def show(self):
		pygame.draw.rect(screen, LIGHT_BLUE, (self.x_pos, self.y_pos, 25, 25))
		global gold_up
		gold_up = 0

	def reset(self):
		global invi_count
		invi_count += 2
		if coin in enemy_list:
			enemy_list.remove(coin)

while True:
	restart()
	menu()
	while not game_over:

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				sys.exit()

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_SPACE and invi_count > 0:
					nedified = False
					invi_count -= 1
					invi_time = 30					
				elif event.key == pygame.K_UP:
					paused = True
					pause(False)

			if event.type == pygame.KEYUP:

				if event.key == pygame.K_LEFT and moving_left:
					moving_left = False
				elif event.key == pygame.K_RIGHT and moving_right:
					moving_right = False

		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]: pos[0] -= speed
		if keys[pygame.K_RIGHT]: pos[0] += speed

		if pos[0] == WIDTH - 10: pos[0] = 20

		if pos[0] == -30: pos[0] = WIDTH - 20

		if invi_time > 0:
			speed = 15
			invi_time -= 1
			tint = LIGHT_BLUE
		else: 
			tint = BLUE
			speed = 10

		total_score += score
		screen.fill(BACK)
		pygame.draw.rect(screen, tint, (pos[0], pos[1], size, size))
		if up == increase:
			enemy_list.append(enemy(((random.randint(0, WIDTH-size)), 0), random.randint(5, 9), 40))
			ENEMIES += 1
			up = 0
		else:
			up += 1
		if gold_up == chance:
			gold_up = 0
			chance = random.randint(20, 60)
			boosted = random.randint(1,4)
			if boosted == 4: coin = boost(((random.randint(0, WIDTH-size)), 0), 10, 25)
			else: coin = gold(((random.randint(0, WIDTH-size)), 0), 10, 25)
			enemy_list.append(coin)
			increase += increase_change
		else:
			gold_up += 1
		for block in enemy_list:
			block.show()
			if block.fall() and (isinstance(block, gold) or isinstance(block, boost)):
				if coin in enemy_list:
					enemy_list.remove(coin)
			block.collide()
		printwords(font_small, str(math.floor(total_score/10)), GREEN, None, None)
		#  printwords(font_small, str(math.floor(score*10)), PURPLE, 9, 40)
		# printwords(font_small, str(ENEMIES), PURPLE, WIDTH - 60, 20)
		printwords(font_small, str(invi_count), LIGHT_BLUE, WIDTH - 20, 20)
		if victory == False and total_score/10 >= 1000:
			paused = True
			pause(True)
		pygame.display.update() 
		clock.tick(35)