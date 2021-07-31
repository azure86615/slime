import numpy as np
import cv2
import pygame, sys, random, time
from pygame.locals import *

#遊戲視窗
display_width = 743
#display_width = 640
display_height = 480

windowSurface = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Slime')

#偵測色彩範圍,hsv格式 (範圍越小的話偵測到的顏色越精準)
lower_H = np.array([50,60,60],dtype=np.uint8)
upper_H = np.array([95,255,255],dtype=np.uint8)

#opencv，攝影視窗
cap0 = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)

#圖片
startImage = pygame.image.load('start_screen.png')
startImage = pygame.transform.scale(startImage,(display_width,display_height))
playImage = pygame.image.load('grass3.jpg')
playImage = pygame.transform.scale(playImage,(display_width,display_height))
slime_dark = pygame.image.load('dark.png')
slime_fire = pygame.image.load('fire.png')
slime_flash = pygame.image.load('flash.png')
slime_leaf = pygame.image.load('leaf.png')
slime_water = pygame.image.load('water.png')
slime_handsome = pygame.image.load('handsome.png')
slime_normal = pygame.image.load('normal.png')
slime_pudding = pygame.image.load('pudding.png')
select_slime = [slime_fire, slime_water, slime_dark, slime_flash, slime_leaf, slime_normal, slime_handsome, slime_pudding]

#統一選角圖片大小
selectsize = 120						#角色顯示圖的長寬一致
for i in range(len(select_slime)):
	select_slime[i] = pygame.transform.scale(select_slime[i],(selectsize,selectsize))

#初始化
pygame.init()
mainClock = pygame.time.Clock()

#變數宣告
global Screen
Screen = 0								#0:開始畫面，1:選角畫面，2:遊戲畫面
FPS = 40								#每秒畫面刷新次數
player1 = 0								#玩家1所選史萊姆編號
player2 = 3								#玩家2所選史萊姆編號
scoreboard = 50
global player1_score, player2_score
player1_score = 20
player2_score = 20
global player1_image, player2_image, player1_y, player2_y
player1_image = select_slime[player1]	#對應玩家所選史萊姆圖片
player2_image = select_slime[player2]
player1_y = display_height/2
player2_y = display_height/2
playersize = 90							#遊戲畫面的角色大小(正方形)
global shootflag_p1, shootflag_p2, bullet_p1, bullet_p2
shootflag_p1 = False
shootflag_p2 = False
bullet_p1 = []
bullet_p2 = []
bulletsize = int(playersize/2)
RED = (255,0,0)
BLUE = (0,0,255)
GRAY = (110,110,110)
WHITE = (0,0,0)
PURPLE = (200,50,255)
hit = pygame.image.load('hit.png')
hit = pygame.transform.scale(hit,(bulletsize, bulletsize))
sad = pygame.image.load('sad.png')
sad = pygame.transform.scale(sad,(bulletsize, bulletsize))
global winner_str,color,winner_slime
winner_str = ''
color = PURPLE
winner_slime = slime_dark

#退出
def terminate():
	cv2.destroyAllWindows()
	pygame.quit()
	sys.exit()
	
#開始畫面
def startscreen():
	windowSurface.blit(startImage,(0,0))
	
#選角畫面
def selectscreen():
	windowSurface.fill(GRAY)
	#畫玩家選擇框(挑選史萊姆)
	if player1 < 3:
		pygame.draw.rect(windowSurface, RED, [15+(selectsize+20)*player1,15,selectsize+10,selectsize+10])
		pygame.draw.rect(windowSurface, GRAY, [20+(selectsize+20)*player1,20,selectsize,selectsize])
	elif player1 <6:
		pygame.draw.rect(windowSurface, RED, [15+(selectsize+20)*(player1-3),35+selectsize,selectsize+10,selectsize+10])
		pygame.draw.rect(windowSurface, GRAY, [20+(selectsize+20)*(player1-3),40+selectsize,selectsize,selectsize])
	else:
		pygame.draw.rect(windowSurface, RED, [15+(selectsize+20)*(player1-6),55+selectsize*2,selectsize+10,selectsize+10])
		pygame.draw.rect(windowSurface, GRAY, [20+(selectsize+20)*(player1-6),60+selectsize*2,selectsize,selectsize])
	if player2 < 3:
		pygame.draw.rect(windowSurface, BLUE, [15+(selectsize+20)*player2,15,selectsize+5,selectsize+5])
		pygame.draw.rect(windowSurface, GRAY, [20+(selectsize+20)*player2,20,selectsize-5,selectsize-5])
	elif player2 < 6:
		pygame.draw.rect(windowSurface, BLUE, [15+(selectsize+20)*(player2-3),35+selectsize,selectsize+5,selectsize+5])
		pygame.draw.rect(windowSurface, GRAY, [20+(selectsize+20)*(player2-3),40+selectsize,selectsize-5,selectsize-5])
	else:
		pygame.draw.rect(windowSurface, BLUE, [15+(selectsize+20)*(player2-6),55+selectsize*2,selectsize+5,selectsize+5])
		pygame.draw.rect(windowSurface, GRAY, [20+(selectsize+20)*(player2-6),60+selectsize*2,selectsize-5,selectsize-5])

	for i in range(len(select_slime)):
		if i<3:
			windowSurface.blit(select_slime[i],(20+(selectsize+20)*i,20))
		elif i<6:
			windowSurface.blit(select_slime[i],(20+(selectsize+20)*(i-3),40+selectsize))
		else:
			windowSurface.blit(select_slime[i],(20+(selectsize+20)*(i-6),60+selectsize*2))
	
#遊戲畫面
def playscreen():
	windowSurface.blit(playImage,(0,0))
	pygame.draw.line(windowSurface, RED, (display_width/2,0),(display_width/2,display_height))	#畫中場線
	
	scoreText = pygame.font.Font('LucidaBrightDemiBold.ttf', 50)
	global player1_score, player2_score
	TextSurf = scoreText.render(str(player1_score)+'    '+str(player2_score), True, PURPLE)
	TextRect = TextSurf.get_rect()
	TextRect.center = (display_width / 2, 30)
	windowSurface.blit(TextSurf, TextRect)
	
	global player1_image,player2_image
	player1_image = pygame.transform.scale(player1_image,(playersize,playersize))
	player2_image = pygame.transform.scale(player2_image,(playersize,playersize))
	player1_image = pygame.transform.flip(player1_image,1,0)
	player2_image = pygame.transform.flip(player2_image,1,0)
	
	global player1_y,player2_y
	player1_y = detecting_y0(cap0)
	player2_y = detecting_y1(cap1)
	#print('player1:' +str(player1_y) + '\t\tplayer2:'+str(player2_y))
	windowSurface.blit(player1_image,(0,player1_y))
	windowSurface.blit(player2_image,(display_width-playersize,player2_y))
	
	shoot_p1 = detecting_x0(cap0)
	shoot_p2 = detecting_x1(cap1)
	if shoot_p1 == True:
		bullet_p1.append([player1_y,playersize,False])
	for bullet in bullet_p1:
		bullet[1] += 10
		if (bullet[1] > display_width):
			del bullet
			continue
		windowSurface.blit(sad,(bullet[1],bullet[0]))
		iscrash = crash(bullet[1],bullet[0],bulletsize, display_width - playersize,player2_y, playersize)
		if iscrash == True and bullet[2]==False:
			player2_score = player2_score-1
			bullet[2] = True
	if shoot_p2 == True:
		bullet_p2.append([player2_y,display_width - playersize-bulletsize, False])
	for bullet in bullet_p2:
		bullet[1] -= 10
		if (bullet[1] < 0-playersize):
			del bullet
			continue
		windowSurface.blit(hit,(bullet[1],bullet[0]))
		iscrash = crash(bullet[1],bullet[0],bulletsize, 0,player1_y, playersize)
		if iscrash == True and bullet[2]==False:
			player1_score = player1_score-1
			bullet[2] = True
	global Screen,winner_str,color,winner_slime
	if player1_score <= 0 and Screen != 3:
		winner_str = 'Player2 is Winner!'
		color = BLUE
		winner_slime = select_slime[player2]
		Screen = 3
	elif player2_score <=0 and Screen != 3:
		winner_str = 'Player1 is Winner!'
		color = RED
		winner_slime = select_slime[player1]
		Screen = 3
	#print('player1:' +str(shoot_p1) + '\t\tplayer2:'+str(shoot_p2))

	
#結束畫面
def endscreen():
	windowSurface.blit(playImage,(0,0))
	scoreText = pygame.font.Font('LucidaBrightDemiBold.ttf', 50)
	TextSurf = scoreText.render(winner_str, True, color)
	TextRect = TextSurf.get_rect()
	TextRect.center = (display_width / 2, display_height/2)
	windowSurface.blit(TextSurf, TextRect)
	windowSurface.blit(winner_slime, (display_width/2-playersize, display_height/2+75))
	
#opencv處理
def detecting_y0(cap):
	ret, frame = cap.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lower_H, upper_H)
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
	mask = cv2.erode(mask, kernel, iterations = 2)
	mask = cv2.dilate(mask, kernel, iterations = 2)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	y_position = 50
	
	if len(cnts) > 0:					#若未連接在一起元素數量不為零個
		c = max(cnts, key=cv2.contourArea)		#依照contour面積找最大的點集合
		((x, y), radius) = cv2.minEnclosingCircle(c)	#找最接近的圓，儲存中心點跟半徑
		#下面兩行，取得中心點 (細節不懂)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# 當所抓到的圓半徑超過某值之後才執行
		if radius > 10:
			cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			y_position = int(M["m01"] / M["m00"])
			
	res = cv2.bitwise_and(frame,frame, mask= mask)
	cv2.imshow('frame_y0',frame)
	if y_position > scoreboard:
		return y_position
	else:
		return scoreboard

def detecting_y1(cap):
	ret, frame = cap.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lower_H, upper_H)
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
	mask = cv2.erode(mask, kernel, iterations = 2)
	mask = cv2.dilate(mask, kernel, iterations = 2)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	y_position = 50
	
	if len(cnts) > 0:					#若未連接在一起元素數量不為零個
		c = max(cnts, key=cv2.contourArea)		#依照contour面積找最大的點集合
		((x, y), radius) = cv2.minEnclosingCircle(c)	#找最接近的圓，儲存中心點跟半徑
		#下面兩行，取得中心點 (細節不懂)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# 當所抓到的圓半徑超過某值之後才執行
		if radius > 10:
			cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			y_position = int(M["m01"] / M["m00"])
			
			
	res = cv2.bitwise_and(frame,frame, mask= mask)
	cv2.imshow('frame_y1',frame)
	if y_position > scoreboard:
		return y_position
	else:
		return scoreboard

def detecting_x0(cap):
	ret, frame = cap.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lower_H, upper_H)
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
	mask = cv2.erode(mask, kernel, iterations = 2)
	mask = cv2.dilate(mask, kernel, iterations = 2)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	x_position = 0
	
	if len(cnts) > 0:					#若未連接在一起元素數量不為零個
		c = max(cnts, key=cv2.contourArea)		#依照contour面積找最大的點集合
		((x, y), radius) = cv2.minEnclosingCircle(c)	#找最接近的圓，儲存中心點跟半徑
		#下面兩行，取得中心點 (細節不懂)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# 當所抓到的圓半徑超過某值之後才執行
		if radius > 10:
			cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			x_position = int(M["m10"] / M["m00"])
			
	res = cv2.bitwise_and(frame,frame, mask= mask)
	#cv2.imshow('frame_x0',frame)
	
	global shootflag_p1
	if x_position < frame.shape[1]/2 and shootflag_p1 == False:
		shootflag_p1 = True
		return True
	elif x_position > frame.shape[1]/2 and shootflag_p1 == True:
		shootflag_p1 = False
		return False


	
def detecting_x1(cap):
	ret, frame = cap.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lower_H, upper_H)
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
	mask = cv2.erode(mask, kernel, iterations = 2)
	mask = cv2.dilate(mask, kernel, iterations = 2)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	x_position = 0
	
	if len(cnts) > 0:					#若未連接在一起元素數量不為零個
		c = max(cnts, key=cv2.contourArea)		#依照contour面積找最大的點集合
		((x, y), radius) = cv2.minEnclosingCircle(c)	#找最接近的圓，儲存中心點跟半徑
		#下面兩行，取得中心點 (細節不懂)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# 當所抓到的圓半徑超過某值之後才執行
		if radius > 10:
			cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			x_position = int(M["m10"] / M["m00"])
			
	res = cv2.bitwise_and(frame,frame, mask= mask)
	#cv2.imshow('frame_x1',frame)
	global shootflag_p2
	if x_position > frame.shape[1]/2 and shootflag_p2 == False:
		shootflag_p2 = True
		return True
	elif x_position < frame.shape[1]/2 and shootflag_p2 == True:
		shootflag_p2 = False
		return False

#碰撞
def crash(object1_x,object1_y,object1_size, object2_x,object2_y,object2_size):
	if object1_x >= object2_x and object1_x <= object2_x+object2_size:
		if object1_y >= object2_y and object1_y <= object2_y+object2_size:
			return True
		elif object1_y+object1_size >= object2_y and object1_y+object1_size <= object2_y+object2_size:
			return True
	elif object1_x+object1_size >= object2_x and object1_x+object1_size <= object2_x+object2_size:
		if object1_y >= object2_y and object1_y <= object2_y+object2_size:
			return True
		elif object1_y+object1_size >= object2_y and object1_y+object1_size <= object2_y+object2_size:
			return True
	return False
	
#遊戲主程式
while(1):
	for event in pygame.event.get():
		if event.type == QUIT:
			terminate()
		if Screen == 0:
			if event.type == KEYDOWN and event.key == 13:		#按下enter，從開始畫面換到選角畫面
				Screen = 1
		elif Screen == 1:
			if event.type == KEYDOWN:
				if event.unicode == 'a':						#玩家1選角，a左移d右移
					player1 = (player1-1)%8
				elif event.unicode == 'd':
					player1 = (player1+1)%8
				if event.unicode == 'j':						#玩家2選角，j左移l右移
					player2 = (player2-1)%8
				elif event.unicode == 'l':
					player2 = (player2+1)%8
				if event.key == 13:								#按下enter，選角完畢，換到遊戲畫面
					player1_image = select_slime[player1]
					player2_image = select_slime[player2]
					Screen = 2
					
	windowSurface.fill(WHITE)									#畫面刷白
	
	if Screen == 0:
		startscreen()
	elif Screen == 1:
		selectscreen()
	elif Screen == 2:
		playscreen()
	else:
		endscreen()

	pygame.display.update()
	mainClock.tick(FPS)