import pygame
import sys, string, os

pygame.init()

#화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

#배경 이미지 불러오기
main_background = pygame.image.load("C:\\Users\\Hyerim\\Desktop\\광운\\1-2\\컴퓨팅사고\\팀플\\Python workplace\\main\\main.png")

running = True

while running:
    
    for event in pygame.event.get():#동작 체킹을 위한 부분
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:#Esc 눌렀을 때 종료
                running = False

    keys = pygame.key.get_pressed()
    #1번을 눌렀을 때 테트리스 실행
    if (keys[pygame.K_1]):
        os.chdir('C:\\Users\\Hyerim\\Desktop\\광운\\1-2\\컴퓨팅사고\\팀플\\Python workplace\\Tetris')
        os.system('"C:\\Users\\Hyerim\\Desktop\\광운\\1-2\\컴퓨팅사고\\팀플\\Python workplace\\Tetris\\Tetris.py"') 
    #2번을 눌렀을 때 슈팅게임 실행
    elif (keys[pygame.K_2]):
        os.chdir('C:\\Users\\Hyerim\\Desktop\\광운\\1-2\\컴퓨팅사고\\팀플\\Python workplace\\shootting game')
        os.system('"C:\\Users\\Hyerim\\Desktop\\광운\\1-2\\컴퓨팅사고\\팀플\\Python workplace\\shootting game\\shotting game.py"')

    screen.blit(main_background, (0,0))#게임 배경 드로잉
    pygame.display.update()#게임 화면 다시 그림

pygame.quit()