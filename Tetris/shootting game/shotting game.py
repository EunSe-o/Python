import pygame
import pygame.mixer
import random
import time
import sys

pygame.init()#초기화


#화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

#set title
pygame.display.set_caption("PROJECT GAME")

#FPS
clock = pygame.time.Clock()

#배경 이미지 불러오기
background = pygame.image.load("background.png")

#캐릭터 불러오기
character =  pygame.image.load("character.png")
character_size = character.get_rect().size #이미지 크기를 구함
character_width = character_size[0] #캐릭터 가로 크기
character_height  = character_size[1]#캐릭터 세로 크기
character_x_pos = (screen_width / 2)-(character_width /2) #화면 가로의 절반 크기에 해당하는 곳(가로)
character_y_pos = screen_height-character_height #화면 세로 크기 가장 아래에 해당하는 곳(세로)
characterXY = []

#이동할 좌표
to_x = 0
to_y = 0

#캐릭터 이동속도
character_spd = 0.5

#boom
boom = pygame.image.load("boom.png")

# 적
emyImage =  ["waterball.png"]
emy = pygame.image.load(random.choice(emyImage))
emy_size = emy.get_rect().size #이미지 크기를 구함
emy_width = emy_size[0] #적 가로 크기
emy_height = emy_size[1]#적 세로 크기
emy_x_pos = random.randrange(0, screen_width - emy_width)
emy_y_pos = 0
emy_spd = 2

#적을 맞췄을 때 사운드
explosion_sound = pygame.mixer.Sound("explosion.wav")

# 화살
arrow = pygame.image.load("arrow.png")
arrow_size = arrow.get_rect().size
arrow_width = arrow_size[0]
arrow_height = arrow_size[1]
arrowXY = []
arrow_sound = pygame.mixer.Sound("arrow.wav")

#게임 종료시
gameover = pygame.image.load("gameover.png")
gameover_size = gameover.get_rect().size
gameover_width = gameover_size[0]
gameover_height = gameover_size[1]
gameover_x_pos = (screen_width / 2) - (gameover_width / 2)
gameover_y_pos = (screen_height / 2) - (gameover_height / 2)
gameover_sound = pygame.mixer.Sound("gameover.wav")

#배경음악 재생
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)


isShot = False#적을 맞춘 상태
shotCount = 0#맞춘 적
emyPassed = 0#지나간 적

#loop event
running = True

while running:
    dt = clock.tick(60) # 게임화면 프레임수 설정
    
    for event in pygame.event.get(): #동작 체킹을 위한 부분 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False #게임 수행중이 아님

        if event.type == pygame.KEYDOWN: #키의 반응 확인
            if event.key == pygame.K_LEFT:#왼쪽이동
                to_x -= character_spd 
            elif event.key == pygame.K_RIGHT:#오른쪽이동
                to_x += character_spd 
            elif event.key == pygame.K_SPACE:#무기 발사
                arrow_x_pos = character_x_pos + (character_width / 2) - (arrow_width / 2)#캐릭터의 위치 가운데에 해당하는 곳(가로)
                arrow_y_pos = character_y_pos - (character_height / 2)#캐릭터의 위치 바로 위에 해당하는 곳(세로)
                arrowXY.append([arrow_x_pos, arrow_y_pos])
                arrow_sound.play()#무기 발사 소리
            
        if event.type == pygame.KEYUP:#키보드를 떼면 멈춤
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x =0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                 to_y=0

    character_x_pos += to_x*dt#이동속도 고정을 위해 프레임 곱
    character_y_pos += to_y*dt#마찬가지

    #가로 캐릭터 탈출불가
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
         character_x_pos = screen_width - character_width
    #세로 캐릭터 탈출불가
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height-character_height:
        character_y_pos = screen_height-character_height

    #캐릭터 적과 충돌
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    emy_rect = emy.get_rect()
    emy_rect.left = emy_x_pos
    emy_rect.top = emy_y_pos

    #충돌 확인과 게임 오버
    if character_rect.colliderect(emy_rect):                    
        screen.blit(gameover, (gameover_x_pos, gameover_y_pos))
        pygame.display.update()
        pygame.mixer.music.stop()
        gameover_sound.play()#게임오버 사운드
        time.sleep(2)
        pygame.mixer.music.play(-1)
        running = False

    #screen.fill((0,25,23))RGB색으로 채우는것도 가능
    screen.blit(background, (0,0))#게임 배경
    
    screen.blit(character, (character_x_pos, character_y_pos))#게임에 등장하는 캐릭터 드로잉

    if len(arrowXY) != 0:
        for i, bxy in enumerate(arrowXY):
            #화살 요소 반복
            bxy[1] -= 10#화살의 y좌표 위로 10씩 이동
            arrowXY[i][1] = bxy[1]
            

            #화살이 적을 맞췄을 때
            if bxy[1] < emy_y_pos:
                if bxy[0] > emy_x_pos and bxy[0] < emy_x_pos + emy_width:
                    arrowXY.remove(bxy)
                    isShot = True
                    shotCount += 1
                    screen.blit(boom, (bx, by))


            #화살이 화면 밖을 벗어나면
            if bxy[1] <= 0:
                try:
                    arrowXY.remove(bxy)#화살 제거
                except:
                    pass

    if len(arrowXY) != 0:
        for bx, by in arrowXY:
            screen.blit(arrow, (bx, by))#화살 드로잉

    #맞춘 적의 수 표시
    font = pygame.font.SysFont("hy중고딕", 20, True)
    text = font.render("맞춘 공의 수: "+str(shotCount), True, (255,255,255))
    screen.blit(text, (10,0))

    #적이 아래로 떨어짐
    emy_y_pos += emy_spd

    #적이 끝까지 떨어진 경우
    if emy_y_pos > screen_height:
        #새로운 적(랜덤)
        emy = pygame.image.load(random.choice(emyImage))
        emy_size = emy.get_rect().size
        emy_width = emy_size[0]
        emy_height = emy_size[1]
        emy_x_pos = random.randrange(0, screen_width - emy_width)
        emy_y_pos = 0
        emyPassed += 1

    #적 3개 놓치면 게임오버
    if emyPassed == 3:
        screen.blit(gameover, (gameover_x_pos, gameover_y_pos))
        pygame.display.update()
        pygame.mixer.music.stop()
        gameover_sound.play()#게임 오버 사운드
        time.sleep(2)
        pygame.mixer.music.play(-1)
        running == False

    #놓친 적의 수 표시
    font = pygame.font.SysFont("hy중고딕", 20, True)
    text = font.render("놓친 공: "+str(emyPassed), True, (255,255,255))
    screen.blit(text, (360,0))

    
      
    if isShot:
        #적을 맞췄을 때 사운드 재생
        explosion_sound.play()
        #새로운 적(랜덤)
        emy = pygame.image.load(random.choice(emyImage))
        emy_size = emy.get_rect().size
        emy_width = emy_size[0]
        emy_height = emy_size[1]
        emy_x_pos = random.randrange(0, screen_width - emy_width)
        emy_y_pos = 0
        isShot = False

        #적을 맞췄을 때 속도 증가
        emy_spd += 0.1
        if emy_spd >= 10:
            emy_spd = 10

    screen.blit(emy, (emy_x_pos, emy_y_pos))#적 드로잉
  
    pygame.display.update()#게임화면 다시 그림

pygame.quit()