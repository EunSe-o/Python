# Game.py (메인화면)
import pygame
import sys, string, os

pygame.init()

#화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

#배경 이미지 불러오기
main_background = pygame.image.load("C:\\Users\\박은서\\Desktop\\python\\Tetris\\main\\main.png")

running = True

while running:
    
    for event in pygame.event.get(): #동작 체킹을 위한 부분
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: #Esc 눌렀을 때 종료
                running = False

    keys = pygame.key.get_pressed()
    #1번을 눌렀을 때 테트리스 실행
    if (keys[pygame.K_1]):
        os.chdir("C:\\Users\\박은서\\Desktop\\python\\Tetris\\main")
        os.system('"C:\\Users\\박은서\\Desktop\\python\\Tetris\\Tetris"') 
    #2번을 눌렀을 때 슈팅게임 실행
    elif (keys[pygame.K_2]):
        os.chdir("C:\\Users\\박은서\\Desktop\\python\\Tetris\\main")
        os.system('"C:\\Users\\박은서\\Desktop\\python\\Tetris\\shootting game"')

    screen.blit(main_background, (0,0)) #게임 배경 드로잉
    pygame.display.update() #게임 화면 다시 그림

pygame.quit()

# Tetris.py (테트리스 게임)
# 조작키
#       Down - Drop block faster
# Left/Right - Move block
#         Up - Rotate block clockwise
#     Escape - Quit game
#          P - Pause game
#     Return - Instant drop

from random import randrange as rand
import pygame, sys

pygame.mixer.init()

#배경음악 재생
pygame.mixer.music.load("C:\\Users\\박은서\\Desktop\\python\\Tetris\\Tetris\\Tetris_background.wav")
pygame.mixer.music.play(-1)

game_over_sound=pygame.mixer.Sound('C:\\Users\\박은서\\Desktop\\python\\Tetris\\Tetris\\gameoversound.wav')

# 기본 설정
cell_size = 30   # 크기
width =     10   # 가로
string =    22   # 세로
maxfps =    30
 
colors = [
( 0,  0,  0 ), 
(255, 113, 113), # 빨 - ㅜ
(110, 227, 247), # 하늘 - s
(250, 237, 125), # 노랑 - z 
(255, 178, 217), # 연분홍 - ㄴ
(103, 153, 255), # 파랑 - ㄴ(반대)
(188, 229, 92 ), # 연두 - 막대기
(183, 120, 255), # 연보라 - ㅁ
(53,  53,  53)   # 배경 
]

tetris_shapes = [ # 모양
    [[1, 1, 1],   # ㅜ
     [0, 1, 0]],
 
    [[0, 2, 2],   # s
     [2, 2, 0]],
 
    [[3, 3, 0],   # z
     [0, 3, 3]],
 
    [[4, 0, 0],   # ㄴ
     [4, 4, 4]],
 
    [[0, 0, 5],   # ㄴ(반대)
     [5, 5, 5]],
 
    [[6, 6, 6, 6]],  # 막대기
 
    [[7, 7],      # ㅁ
     [7, 7]] 
]
 
 
# 오른쪽으로 회전
def rotate_shape_right(shape):  
    return [
        [ shape[y][x] for y in range(len(shape)) ]
        for x in range(len(shape[0]) - 1, -1, -1)
    ]
 
# 블록이 벽이나 땅에(혹은 가장 위에있는 블록) 부딪히는 경우
def check_overlapped(board, shape, offset):
    x_offset, y_offset = offset
    for cy, row in enumerate(shape): 
        for cx, cell in enumerate(row):
            try:
                if cell and board[ cy + y_offset ][ cx + x_offset ]:
                    return True  # 충돌
            except IndexError:
                return True
    return False
 
# 한 줄이 모두 채워질 시 해당 줄을 지움
def erase_line(board, line):
    del board[line]
    return [[0 for i in range(width)]] + board
 
# 블록이 가장 아래블록에 닿을 경우 
def update(mat1, mat2, mat2_off):
    x_offset, y_offset = mat2_off
    for cy, string in enumerate(mat2):
        for cx, val in enumerate(string):
            mat1[cy+y_offset-1][cx+x_offset] += val
    return mat1
 
# 벽과 겹쳐진 블록의 상태를 유지해줌
def make_newboard():
    board = [
        [ 0 for x in range(width) ]
        for y in range(string)
    ]
    board += [[ 1 for x in range(width)]]
    return board
 
# 게임 실행
class TetrisApp(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250,25)
        # 게임 창의 너비
        self.width = cell_size*(width+6)
        self.rlim = cell_size*width
        # 게임 창의 높이
        self.height = cell_size*string
        # 배경의 격자무늬
        self.bground_grid = [[ 8 if x%2==y%2 else 0 for x in range(width)] for y in range(string)]
        # 게임화면 옆의 글씨 크기
        self.default_font =  pygame.font.Font(
            pygame.font.get_default_font(), 17)  
 
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION) # 마우스의 움직임을 필요로하지 않기 때문에 이를 막음
        # 다음에 나올 블록을 보여줌
        self.next_block = tetris_shapes[rand(len(tetris_shapes))]
        self.init_game()
 
    # 새 블록을 소환
    def call_newblock(self):
        # 다음에 나올 예정이었던 블록을 현재 블록으로 옮김
        self.block = self.next_block[:]
        # 다음에 나올 블록을 새로 보여줌
        self.next_block = tetris_shapes[rand(len(tetris_shapes))]
        self.block_x = int(width / 2 - len(self.block[0])/2)
        self.block_y = 0
 
        # 벽과의 충돌을 확인
        if check_overlapped(self.board,
                           self.block,
                           (self.block_x, self.block_y)):
            self.gameover = True   # 부딪힐 시 게임 종료
 
    # 게임을 실행할 때 초기 설정(게임 시작)을 위해 불러오는 함수
    def init_game(self):
        self.board = make_newboard() 
        self.call_newblock()
        self.level = 1
        self.score = 0
        self.lines = 0
        pygame.time.set_timer(pygame.USEREVENT+1, 1000)
 
    # 실행화면 오른쪽에 메세지 출력
    def print_message(self, message, top_left):
        x,y = top_left
        for line in message.splitlines():
            self.screen.blit(
                self.default_font.render(
                    line,
                    False,
                    (255,255,255),
                    (0,0,0)),
                (x,y))
            y+=14
    
    # 가운데에 메세지 출력
    def print_message_at_center(self, message):
        for i, line in enumerate(message.splitlines()):
            message_image =  self.default_font.render(line, False,
                (255,255,255), (0,0,0))
 
            msgim_center_x, msgim_center_y = message_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2
 
            self.screen.blit(message_image, (
              self.width // 2-msgim_center_x,
              self.height // 2-msgim_center_y+i*22))
 
    # 블록을 그림
    def draw(self, matrix, offset):
        x_offset, y_offset  = offset
        # 블록 데이터는 1차원이므로 for문을 이용해 0~배열의길이까지 반복
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    # 색상은 colors[val]이고, pygame.Rect(1,2,3,4)에서 
                    # 1, 2를 왼쪽으로 하는 (3,4)영역에 그려짐
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(
                            (x_offset+x) *
                              cell_size,
                            (y_offset+y) *
                              cell_size,
                            cell_size,
                            cell_size),0)

    # 라인을 지울 시 레벨과 점수를 올림
    def if_clear(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += linescores[n] * self.level
        if self.lines >= self.level*6:
            self.level += 1
            newdelay = 1000-50*(self.level-1)
            newdelay = 100 if newdelay < 100 else newdelay
            pygame.time.set_timer(pygame.USEREVENT+1, newdelay)
 
    # 블록을 움직임
    def move_block(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.block_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > width - len(self.block[0]):
                new_x = width - len(self.block[0])
            # 키를 조작했을 때 겹치지 않을 때 
            if not check_overlapped(self.board,
                                   self.block,
                                   (new_x, self.block_y)):
                self.block_x = new_x  # 키 조작을 유효로 함

    # 게임을 종료할 시
    def exit(self):
        self.print_message_at_center("Exiting...")
        pygame.mixer.music.stop()
        pygame.display.update()
        pygame.quit()
        sys.exit()
 
    # 블록을 떨어뜨릴 때 
    def drop_block(self, manual):
        if not self.gameover and not self.paused:
            self.score += 1 if manual else 0
            self.block_y += 1
            # 바닥(가장 위에 있는 블록)에 닿았을 때
            if check_overlapped(self.board,
                               self.block,
                               (self.block_x, self.block_y)):
                self.board = update(
                  self.board,
                  self.block,
                  (self.block_x, self.block_y))
                self.call_newblock()
                clear_line = 0
                while True:
                    # 한 줄이 모두 채워지면 해당 줄을 지움
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = erase_line(
                              self.board, i)
                            clear_line += 1
                            break
                    else:
                        break
                self.if_clear(clear_line)
                return True
        return False
 
    def insta_drop(self):
        if not self.gameover and not self.paused:
            while(not self.drop_block(True)):
                pass
 
    # 블록을 회전시킴
    def rotate_block(self):
        if not self.gameover and not self.paused:
            new_block = rotate_shape_right(self.block)
            # 블록을 회전시켰을 때 벽과 부딪히지 않는다면 실행
            if not check_overlapped(self.board,
                                   new_block,
                                   (self.block_x, self.block_y)):
                self.block = new_block
 
    # 게임을 멈췄을 시
    def pause(self):
        self.paused = not self.paused
 
    def game_start(self):
        if self.gameover:
            self.init_game()
            pygame.mixer.music.play(-1)
            self.gameover = False
 
    # 게임 실행
    def run_game(self):
        # 조작키
        key_actions = {
            'ESCAPE':   self.exit,
            'LEFT':     lambda:self.move_block(-1),
            'RIGHT':    lambda:self.move_block(+1),
            'DOWN':     lambda:self.drop_block(True),
            'UP':       self.rotate_block,
            'p':        self.pause,
            'SPACE':    self.game_start,
            'RETURN':   self.insta_drop
        }
 
        self.gameover = False
        self.paused = False
 
        dont_burn_my_cpu = pygame.time.Clock()
        while 1:
            self.screen.fill((0, 0, 0))
            
            # 게임 오버될 시 출력되는 문구
            if self.gameover:
                self.print_message_at_center("""Game Over!\nYour score: %d\nPress space to continue""" % self.score)
                pygame.mixer.music.stop()
                game_over_sound.play(1)

            else:
                # 게임 중지할 시 출력되는 문구
                if self.paused:
                    self.print_message_at_center("Paused")
                else:
                    pygame.draw.line(self.screen,
                        (255,255,255),
                        (self.rlim+1, 0),
                        (self.rlim+1, self.height-1))
                    # 다음 블록을 알려주는 문구
                    self.print_message("Next:", (
                        self.rlim+cell_size,
                        2))
                    # 게임 실행 화면 오른쪽에 출력되는 문구
                    self.print_message("Score: %d\n\nLevel: %d\
                        \nLines: %d" % (self.score, self.level, self.lines),
                        (self.rlim+cell_size, cell_size*5))
                    self.draw(self.bground_grid, (0,0))
                    self.draw(self.board, (0,0))
                    self.draw(self.block,
                        (self.block_x, self.block_y))
                    self.draw(self.next_block,
                        (width+1,2))
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT+1:
                    self.drop_block(False)
                elif event.type == pygame.QUIT:
                    self.exit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_"
                        +key):
                            key_actions[key]()
 
            dont_burn_my_cpu.tick(maxfps)            
 
if __name__ == '__main__':
    App = TetrisApp()
    App.run_game()

# shooting game.py (슈팅게임)
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