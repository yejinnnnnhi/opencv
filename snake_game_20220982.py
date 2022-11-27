import pygame
import os
import sys
import random
from time import sleep

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

WHITE = (255, 255, 255)
ORANGE = (250, 150, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
GREEN = (0, 155, 0)

# 뱀 객체
class Snake(object):
    def __init__(self):
        self.create()

    # 뱀 생성
    def create(self):
        self.length = 3
        self.positions = [(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    # 뱀 방향 조정
    def control(self, xy):
        if (xy[0] * -1, xy[1] * -1) == self.direction:
            return
        else:
            self.direction = xy

    # 뱀 이동
    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        new = (cur[0] + (x * GRID_SIZE)), (cur[1] + (y * GRID_SIZE))

        # 뱀이 자기 몸통에 닿았을 경우 뱀 처음부터 다시 생성
        if new in self.positions[2:]:
            sleep(1)
            self.create()
        # 뱀이 게임화면을 넘어갈 경우 뱀 처음부터 다시 생성
        elif new[0] < 0 or new[0] >= SCREEN_WIDTH or \
                new[1] < 0 or new[1] >= SCREEN_HEIGHT:
            sleep(1)
            self.create()
        # 뱀이 정상적으로 이동하는 경우
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    # 뱀이 먹이를 먹을 때 호출
    def eat(self):
        self.length += 1
        pygame.mixer.music.load("pong.wav")
        pygame.mixer.music.play()

    #뱀이 랜덤박스 만날 때
    def track(self, num):
        if num == 0:
            self.length=self.length-1
            if len(self.positions) > self.length:
                self.positions.pop()
            pygame.mixer.music.load("die2.mp3")
            pygame.mixer.music.play()
        else:
            self.length=self.length+1
            pygame.mixer.music.load("pluz.mp3")
            pygame.mixer.music.play()

    # 뱀 그리기
    def draw(self, screen, s):
        if s == 'g':    
            red, green, blue = 50 / (self.length), 150, 150 / (self.length)
            for i, p in enumerate(self.positions):
                color = (100 + red * i, green, blue * i)
                rect = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, color, rect)
        elif s == 'b':
            red, green, blue = 50 / (self.length), 150 / (self.length), 200
            for i, p in enumerate(self.positions):
                color = (red * i, green * i, blue)
                rect = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, color, rect)

           


# 먹이 객체
class Feed(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = ORANGE
        self.create()

    # 먹이 생성
    def create(self):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        self.position = x * GRID_SIZE, y * GRID_SIZE

    # 먹이 그리기
    def draw(self, screen):
        rect = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, rect)

#랜덤박스
class Track(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (255,0,0)
        self.create()

    def create(self):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        self.position = x * GRID_SIZE, y * GRID_SIZE
    
    def draw(self, screen):
        a, b = self.position[0], self.position[1]
        rect = pygame.Rect((a, b), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.polygon(screen, self.color, [[a, b], [a+GRID_SIZE//2, b-GRID_SIZE//2], [a+GRID_SIZE-1, b]])


#장애물
class Makekdie(object):
    def __init__(self):
        self.position = (0, 0)
        self.create()

    def create(self):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(10, GRID_HEIGHT - 10)
        self.position = x * GRID_SIZE, y * GRID_SIZE
    
    def draw(self, screen):
        yellow = (255,255,0)
        red = (255,0,0)
        a, b = self.position[0], self.position[1]
        rect = pygame.Rect((a, b), (GRID_SIZE*2, GRID_SIZE*2))
        pygame.draw.rect(screen, yellow, rect)
        pygame.draw.polygon(screen, red, [[a, b], [a+GRID_SIZE//2, b-GRID_SIZE], [a+GRID_SIZE-1, b]])
        pygame.draw.polygon(screen, red, [[a+GRID_SIZE, b], [a+GRID_SIZE*(3/2), b-GRID_SIZE], [a+2*GRID_SIZE-1, b]])

# 게임 객체
class Game(object):
    def __init__(self):
        self.snake = Snake()
        self.feed = Feed()
        self.speed = 20
        self.track = Track()
        self.snake2 = Snake()
        self.Makedie = Makekdie()

    # 게임 이벤트 처리 및 조작
    def process_events(self):
        #list1 = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        #list2 = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.control(UP)
                if event.key == pygame.K_DOWN:
                    self.snake.control(DOWN)
                if event.key == pygame.K_LEFT:
                    self.snake.control(LEFT)
                if event.key == pygame.K_RIGHT:
                    self.snake.control(RIGHT)
                if event.key == pygame.K_w:
                    self.snake2.control(UP)
                if event.key == pygame.K_s:
                    self.snake2.control(DOWN)
                if event.key == pygame.K_a:
                    self.snake2.control(LEFT)
                if event.key == pygame.K_d:
                    self.snake2.control(RIGHT)

        return False

    # 게임 로직 수행
    def run_logic(self):
        self.snake.move()
        self.snake2.move()
        self.check_eat(self.snake, self.feed)
        self.check_track(self.snake, self.track)
        self.check_eat(self.snake2, self.feed)
        self.check_track(self.snake2, self.track)
        self.speed = (20 + self.snake.length) / 4
        self.check_die(self.snake, self.Makedie)
        self.check_die(self.snake2, self.Makedie)

    # 뱀이 먹이를 먹었는지 체크
    def check_eat(self, snake, feed):
        if snake.positions[0] == feed.position:
            snake.eat()
            feed.create()

    #뱀이 랜덤박스 만날 때 랜덤으로 채택
    def check_track(self, snake, track):
        if snake.positions[0] == track.position:
            num = random.randint(0,1)
            snake.track(num)
            track.create()

    #뱀이 장애물 만날 때
    def check_die(self, snake, Make_die):
        x, y = Make_die.position[0], Make_die.position[1]
        if snake.positions[0] == (x, y) or snake.positions[0] == (x+GRID_SIZE, y):
            self.create()
        elif snake.positions[0] == (x, y+GRID_SIZE) or snake.positions[0] == (x+GRID_SIZE, y+GRID_SIZE):
            self.snake.create()
    
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # 게임 정보 출력
    def draw_info(self, length, speed, screen, x, color):
        info = "Length: " + str(length) + "    " + "Speed: " + str(round(speed, 2))
        font_path = resource_path("assets/NanumGothicCoding-Bold.ttf")
        font = pygame.font.Font(font_path, 26)
        text_obj = font.render(info, 1, color)
        text_rect = text_obj.get_rect()
        text_rect.x, text_rect.y = x, 10
        screen.blit(text_obj, text_rect)

    # 게임 프레임 처리
    def display_frame(self, screen):
        screen.fill(WHITE)
        self.draw_info(self.snake.length, self.speed, screen, 475, GREEN)
        self.draw_info(self.snake2.length, self.speed, screen, 10, BLUE)
        self.snake.draw(screen, 'g')
        self.snake2.draw(screen, 'b')
        self.feed.draw(screen)
        screen.blit(screen, (0, 0))
        self.track.draw(screen)
        self.Makedie.draw(screen)


# 리소스 경로 설정
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def main():
    # 게임 초기화 및 환경 설정
    pygame.init()
    pygame.display.set_caption('Snake Game')

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Game()

    done = False
    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen)
        pygame.display.flip()
        clock.tick(game.speed)

    pygame.quit()


if __name__ == '__main__':
    main()
