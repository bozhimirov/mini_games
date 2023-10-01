import sys
import time

import pygame as pg

from game_objects import *

COLORS = {
    'GRAY': (128, 128, 128),
    'YELLOW': (255, 255, 102),
    'BLACK': (0, 0, 0),
    'RED': (213, 50, 80),
    'GREEN': (0, 255, 0),
    'BLUE': (50, 153, 213),
}

FONTS = {
    'font_style': ("bahnschrift"),
    'go_font': ('arial')
}


class ChooseGame:
    def __init__(self):
        pg.init()
        self.WINDOW_SIZE = 630
        self.TILE_SIZE = 30
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        pg.display.set_caption('Snake game by Bozhimirov')
        self.clock = pg.time.Clock()
        self.num_players = self.get_num_players()

    def get_num_players(self):
        self.message("Type number of players (1 or 2)", COLORS['GRAY'])
        number_of_players = 0
        while number_of_players == 0:
            pl = int(self.choose_game())
            number_of_players = pl

        return number_of_players

    @staticmethod
    def choose_game():
        ev = ''
        while len(ev) == 0:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        ev = '1'
                    elif event.key == pg.K_2:
                        ev = '2'
        return ev

    def message(self, msg, color, font_attr=FONTS['font_style'], size=25):

        dis_width = self.WINDOW_SIZE
        dis_height = self.WINDOW_SIZE
        font = pg.font.SysFont(font_attr, size)
        mesg = font.render(msg, True, color)
        self.screen.blit(mesg, [dis_width / 6, dis_height / 3])
        pg.display.flip()


class Game:
    def __init__(self, num_players):
        self.game_over = False
        pg.init()
        self.WINDOW_SIZE = 630
        self.TILE_SIZE = 30
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        pg.display.set_caption('Snake game by Bozhimirov')
        self.clock = pg.time.Clock()
        self.players = []
        self.num_players = num_players
        if self.num_players == 1:
            [self.snake, self.food] = self.new_game()
        elif self.num_players == 2:
            [self.snake_l, self.snake_r, self.food] = self.new_game()

    def draw_grid(self):
        [pg.draw.line(self.screen, [self.TILE_SIZE] * 3, (x, 0), (x, self.WINDOW_SIZE))
         for x in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]
        [pg.draw.line(self.screen, [self.TILE_SIZE] * 3, (0, y), (self.WINDOW_SIZE, y))
         for y in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]

    def new_game(self):
        if self.num_players == 1:
            snake = Snake(self, COLORS['GREEN'], 'L')
            self.players.append(snake)
            food = Food(self)
            return snake, food
        else:
            snake_l = Snake(self, COLORS["GREEN"], 'L')
            self.players.append(snake_l)
            snake_r = Snake(self, COLORS["BLUE"], "R")
            self.players.append(snake_r)
            food = Food(self)
            return snake_l, snake_r, food

    def update(self):
        for snake in range(self.num_players):
            self.players[snake].update()
        pg.display.flip()
        self.clock.tick(60)

    def draw(self):
        self.screen.fill(COLORS['BLACK'])
        self.draw_grid()

        if not self.game_over:
            self.food.draw()
            for snake in self.players:
                self.check_event()
                snake.draw()

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # Snake control
            else:
                if self.num_players == 1:
                    self.snake.control(event, self.snake.control_side)
                else:
                    self.snake_l.control(event, self.snake_l.control_side)
                    self.snake_r.control(event, self.snake_r.control_side)

    def run(self):
        self.draw()
        while not self.game_over:
            if self.num_players > 1:
                for pl in range(self.num_players):
                    self.players[pl].opponent = self.players[pl].get_opponent(game)
            self.check_event()
            self.update()
            self.draw()
        time.sleep(10)

    def message(self, msg, color, var=6, font_attr=FONTS['font_style'], size=25):
        font = pg.font.SysFont(font_attr, size)
        dis_width = self.WINDOW_SIZE
        dis_height = self.WINDOW_SIZE

        mesg = font.render(msg, True, color)
        self.screen.blit(mesg, [dis_width / var, dis_height / (var / 2)])
        pg.display.flip()


if __name__ == '__main__':
    players = ChooseGame().num_players
    game = Game(players)
    game.run()
