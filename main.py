import sys
import time

from pricefetch import Stock

import pygame
from random import randint, random, seed
from threading import Thread

pygame.init()

W, H = 1280, 720

FULL_SCREEN = False

surface = pygame.display.set_mode((W, H))
screen = pygame.Surface((W, H))

pygame.display.set_caption('Stonk Snake')

clock = pygame.time.Clock()
FPS = 60

FIRST_TIME_PLAYED = False

SCORE = 0

# WALL RECTS
up_wall = pygame.Rect(0, -10, W, 10)
down_wall = pygame.Rect(0, H, W, 10)
left_wall = pygame.Rect(-10, 0, 10, H)
right_wall = pygame.Rect(W, 0, 10, H)

companies = {}


def clamp(value, _min, _max):
    if value < _min:
        return _min
    if value > _max:
        return _max
    return value


def word_count(sentence):
    return len(sentence.split(' '))


def load_all_companies(d):
    with open('companies.txt', 'r') as f:
        data = f.read().split('\n')
        for row in data:
            if row:
                # name = row.split('\t')[0]
                d[row.split('\t')[0]] = row.split('\t')[1]


def random_pos(offset=100):
    x = randint(offset, W - offset)
    y = randint(offset, H - offset)
    return x, y


class Apple:
    def __init__(self, _type='positive', _text='ABCD'):
        self.type = _type
        self.size = 30
        self.r = 0
        self.text_msg = _text.upper()
        size = 25 if len(_text) <= 3 else 20
        self.font = pygame.font.SysFont('consolas', size, bold=True)
        self.text = self.font.render(self.text_msg, True, 'black')
        self.pos = pygame.Vector2(*random_pos(offset=self.size))
        self.mode = 'spawn'
        self.r_rate = 1
        self.timer = time.time()
        seed(self.text_msg)
        self.time_duration = randint(2, 3) + random()

    def update(self):
        if self.mode == 'spawn':
            self.r += self.r_rate
        elif self.mode == 'de-spawn':
            self.r -= self.r_rate
        self.r = clamp(self.r, 0, self.size)
        if self.r == self.size and self.mode != 'none':
            self.mode = 'none'
            self.timer = time.time()
        if self.r == 0:
            self.mode = 'spawn'
            self.pos = pygame.Vector2(*random_pos(offset=self.size))
        if self.mode == 'none' and time.time() - self.timer > self.time_duration:
            self.mode = 'de-spawn'

    @property
    def negative(self):
        return self.type == 'negative'

    def check_collision(self, pos):
        if self.r == self.size or self.type == 'positive':
            return self.pos.distance_to(pos) <= self.r + 10
        else:
            return False

    def draw(self, surf: pygame.Surface):
        pygame.draw.circle(surf, 'green' if self.type == 'positive' else 'red', self.pos, self.r)
        pygame.draw.circle(surf, 'white', self.pos, self.r, 2)
        surf.blit(self.text, self.text.get_rect(center=self.pos))


class Snake:
    def __init__(self):
        self.x = W // 2
        self.y = H // 2
        self.body = [(self.x, self.y) for _ in range(10)]
        self.size = 25
        self.dir = pygame.Vector2(0, 0)
        self.speed = 5
        self.stopped = False
        self.UP_KEYS = [pygame.K_UP, pygame.K_w]
        self.DOWN_KEYS = [pygame.K_DOWN, pygame.K_s]
        self.LEFT_KEYS = [pygame.K_LEFT, pygame.K_a]
        self.RIGHT_KEYS = [pygame.K_RIGHT, pygame.K_d]
        self.flag = False

    @property
    def pos(self):
        return self.x, self.y

    def update(self, events: list[pygame.event.Event]):
        flag = False
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key in self.UP_KEYS and self.dir.y != 1:
                    self.dir.y = -1
                    self.dir.x = 0
                    flag = True
                if e.key in self.DOWN_KEYS and self.dir.y != -1:
                    self.dir.y = 1
                    self.dir.x = 0
                    flag = True
                if e.key in self.LEFT_KEYS and self.dir.x != 1:
                    self.dir.x = -1
                    self.dir.y = 0
                    flag = True
                if e.key in self.RIGHT_KEYS and self.dir.x != -1:
                    self.dir.x = 1
                    self.dir.y = 0
                    flag = True

        self.flag = flag if not self.flag else True

        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        if up_wall.colliderect(rect) or down_wall.colliderect(rect) or left_wall.colliderect(rect) or right_wall.colliderect(rect):
            self.stopped = True

        if not self.stopped:
            self.x += self.dir.x * self.speed
            self.y += self.dir.y * self.speed
            for i in range(len(self.body) - 1, -1, -1):
                self.body[i] = self.body[i - 1]
            self.body[0] = (self.x, self.y)

    def draw(self, surf: pygame.Surface):
        s = self.size // 2
        for i in self.body:
            pygame.draw.rect(surf, 'grey', (i[0] - s, i[1] - s, 2 * s, 2 * s))
        pygame.draw.rect(surf, 'blue', (self.x - s, self.y - s, s * 2, s * 2))
        pygame.draw.rect(surf, 'white', (self.x - s, self.y - s, s * 2, s * 2), 2)


def main_game(_apples):
    global SCORE
    SCORE = 0
    snake = Snake()

    font = pygame.font.SysFont('consolas', 25)
    font1 = pygame.font.SysFont('impact', 50)
    image = pygame.image.load('bg1.png').convert()

    while True:
        events = pygame.event.get()
        handle_full_screen_event(events)
        for e in events:
            if e.type == pygame.QUIT:
                sys.exit(0)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sys.exit(0)
                # if e.key == pygame.K_r:
                #     init()
        screen.fill(0)
        screen.blit(image, (0, 0))
        for i in apples:
            i.update()
            i.draw(screen)
            if i.check_collision(snake.pos):
                if i.negative and snake.dir:
                    snake.stopped = True
                else:
                    i.pos = pygame.Vector2(*random_pos(offset=i.size))
                    SCORE += 1
        snake.update(events)
        snake.draw(screen)
        if not snake.flag:
            text = font.render('Press Arrow Keys or WASD to move', True, 'white')
            screen.blit(text, text.get_rect(center=(W / 2, H / 2 + 150)))
        else:
            text = font1.render(f'Score = {SCORE}', True, 'white')
            screen.blit(text, (10, 10))
        if snake.stopped:
            return
        if FULL_SCREEN:
            pygame.transform.smoothscale(screen, (1920, 1080), surface)
        else:
            surface.blit(screen, (0, 0))
        pygame.display.update()
        clock.tick(FPS)
        # print(clock.get_fps())


def end_screen():
    image = pygame.image.load('image.png')
    font = pygame.font.SysFont('consolas', 50)
    font1 = pygame.font.SysFont('impact', 100)
    text1 = font.render('Press Enter to Go Back', True, 'white', 'black')
    text2 = font1.render(f' SCORE = {SCORE} ', True, 'white', 'black')
    while True:
        events = pygame.event.get()
        handle_full_screen_event(events)
        for e in events:
            if e.type == pygame.QUIT:
                sys.exit(0)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sys.exit(0)
                if e.key == pygame.K_RETURN:
                    return
                # if e.key == pygame.K_r:
                #     init()
        screen.fill(0)
        screen.blit(image, (0, 0))
        screen.blit(text1, text1.get_rect(center=(W / 2, H / 2 + 250)))
        screen.blit(text2, text2.get_rect(center=(875, H / 2 + 40)))
        if FULL_SCREEN:
            pygame.transform.smoothscale(screen, (1920, 1080), surface)
        else:
            surface.blit(screen, (0, 0))
        pygame.display.update()
        clock.tick(FPS)


def help_screen():
    image = pygame.image.load('help_page.png')
    font = pygame.font.SysFont('consolas', 25)
    text_list = [
        'This game helps us visualize real-time stock data',
        'for a few companies',
        '',
        'You play as a Snake',
        'Use WASD or Arrow Keys to move the snake',
        '',
        'The Red balls are the companies with decrease in stock price',
        'The Green balls are the companies with decrease in stock price',
        '',
        'Take more green balls to increase scores',
        'If you hit a Red Ball, you need to replay the game',
        '', '', '',
        'Press Enter to go back to Home Page'
    ]
    while True:
        events = pygame.event.get()
        handle_full_screen_event(events)
        for e in events:
            if e.type == pygame.QUIT:
                sys.exit(0)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sys.exit(0)
                if e.key == pygame.K_RETURN:
                    return
                # if e.key == pygame.K_r:
                #     init()
        screen.fill(0)
        screen.blit(image, (0, 0))

        y = H / 2 - 150
        for i in text_list:
            y += 25
            text = font.render(i, True, 'white')
            screen.blit(text, text.get_rect(center=(W / 2, y)))

        if FULL_SCREEN:
            pygame.transform.smoothscale(screen, (1920, 1080), surface)
        else:
            surface.blit(screen, (0, 0))
        pygame.display.update()
        clock.tick(FPS)


def loading_screen(_apples):
    loading_done = []
    price = {}

    def init(apple_list, loaded, _price):
        load_all_companies(companies)
        _names = companies.keys()
        for x in sorted(companies.keys()):
            try:
                print(x)
                _price[x] = Stock(x).change
            except Exception as exc:
                print(exc)
        # _price = {'AAPL': -2.3100128, 'ABBV': 0.0500031, 'ABT': -0.389999, 'ACN': -2.34, 'AMZN': -3.5299988, 'ASML': -4.899994,
        #           'AVGO': -8.929993, 'AZN': -1.7299995, 'BABA': -1.91, 'BAC': -0.77,
        #           'COST': -20.77002, 'CSCO': -0.49000168, 'CVX': -10.12, 'DHR': -1.16, 'DIS': -2.66,
        #           'GOOG': -1.4000015, 'GOOGL': -1.4000015, 'HD': 1.79999, 'JNJ': 0.540009, 'JPM': -2.07, 'KO': -0.66,
        #           'LLY': 0.589996, 'MA': -4.78, 'MCD': -1.99001, 'META': -2.4100037,
        #           'MRK': -0.730003, 'MSFT': -3.0599976, 'NEE': -1.02, 'NVDA': -0.44999695, 'NVO': -0.379997, 'NVS': -1.13,
        #           'ORCL': -1.48, 'PEP': -0.08000183, 'PFE': -0.489998, 'PG': -0.630005, 'SHEL': -4.23,
        #           'TM': -1.7700043, 'TMO': 0.5, 'TMUS': -2.7200012, 'TSLA': -13.26001, 'TSM': -1.7599945,
        #           'UNH': -3.8500366, 'V': -1.8299866, 'VZ': -0.40999985, 'WFC': -1.1100006, 'WMT': -3.3300018, 'XOM': -4.8199997}
        _price = {x: _price[x] for x in list(_price.keys())[0:25]}
        # apple_list.extend([Apple('negative' if _price[_].change < 0 else 'positive', _text=_) for _ in _price])
        apple_list.extend([Apple('negative' if _price[_] < 0 else 'positive', _text=_) for _ in _price])
        loaded.append(1)
        return

    if not _apples:
        thread = Thread(target=init, args=(_apples, loading_done, price))
        thread.daemon = True
        thread.start()
    else:
        loading_done = True

    font = pygame.font.SysFont('consolas', 25)
    font1 = pygame.font.SysFont('consolas', 105, bold=True)
    c = 0
    timer = time.time()

    image = pygame.image.load('loading.png').convert()

    while True:
        events = pygame.event.get()
        handle_full_screen_event(events)
        for e in events:
            if e.type == pygame.QUIT:
                sys.exit(0)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sys.exit(0)
                if e.key == pygame.K_RETURN:
                    return
                if e.key == pygame.K_h:
                    help_screen()
        screen.fill(0)
        screen.blit(image, (0, 0))
        if not loading_done:
            text = font.render('Loading' + '.' * (c + 1), True, 'white')
            if time.time() - timer > 0.5:
                timer = time.time()
                c += 1
                c %= 3
            screen.blit(text, text.get_rect(center=(W / 2, H / 2 + 100)))
            _list = list(price.keys())
            if _list:
                text = font.render(f'STOCK - {_list[-1]}', True, 'white')
                screen.blit(text, text.get_rect(center=(W / 2, H / 2 + 150)))
        else:
            text = font.render('Press Enter to Play', True, 'white')
            screen.blit(text, text.get_rect(center=(W / 2, H / 2 + 100)))
            text = font.render('Press H for Help', True, 'white')
            screen.blit(text, text.get_rect(center=(W / 2, H / 2 + 130)))
        text = font1.render('Stonk Snake', True, 'white')
        screen.blit(text, text.get_rect(center=(W / 2, H / 2)))
        if FULL_SCREEN:
            pygame.transform.smoothscale(screen, (1920, 1080), surface)
        else:
            surface.blit(screen, (0, 0))
        pygame.display.update()
        clock.tick(FPS)


def handle_full_screen_event(events):
    global FULL_SCREEN, surface
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                FULL_SCREEN = not FULL_SCREEN
                if FULL_SCREEN:
                    surface = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)
                else:
                    surface = pygame.display.set_mode((W, H))


# end_screen()
apples: list[Apple] = []
while True:
    for apple in apples:
        apple.__init__(apple.type, apple.text_msg)
    loading_screen(apples)
    main_game(apples)
    end_screen()
