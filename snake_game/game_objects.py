import time

import pygame as pg
from random import randrange

from main import COLORS, FONTS

vec2 = pg.math.Vector2


class Snake:
    def __init__(self, game, color, control_side):
        self.game = game
        self.color = color
        self.score = 0
        self.control_side = control_side
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        self.rect.center = self.get_random_position()
        self.direction = vec2(0, 0)
        self.step_delay = 100  # milliseconds
        self.time = 0
        self.length = 1
        self.segments = []
        self.directionsR = {pg.K_w: 1, pg.K_a: 1, pg.K_d: 1, pg.K_s: 1}
        self.directionsL = {pg.K_UP: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1, pg.K_DOWN: 1}
        # self.opponent = object()

    def get_opponent(self, game):
        if len(game.players) > 1:
            if self.color == COLORS['BLUE']:
                return game.players[0]
            return game.players[1]

    def control(self, event, control_side):
        if event.type == pg.KEYDOWN:
            if control_side == "R":
                if event.key == pg.K_w and self.directionsR[pg.K_w]:
                    self.direction = vec2(0, -self.size)
                    self.directionsR = {pg.K_w: 1, pg.K_a: 1, pg.K_d: 1, pg.K_s: 0}
                if event.key == pg.K_s and self.directionsR[pg.K_s]:
                    self.direction = vec2(0, self.size)
                    self.directionsR = {pg.K_w: 0, pg.K_a: 1, pg.K_d: 1, pg.K_s: 1}
                if event.key == pg.K_a and self.directionsR[pg.K_a]:
                    self.direction = vec2(-self.size, 0)
                    self.directionsR = {pg.K_w: 1, pg.K_a: 1, pg.K_d: 0, pg.K_s: 1}
                if event.key == pg.K_d and self.directionsR[pg.K_d]:
                    self.direction = vec2(self.size, 0)
                    self.directionsR = {pg.K_w: 1, pg.K_a: 0, pg.K_d: 1, pg.K_s: 1}
            else:
                if event.key == pg.K_UP and self.directionsL[pg.K_UP]:
                    self.direction = vec2(0, -self.size)
                    self.directionsL = {pg.K_UP: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1, pg.K_DOWN: 0}
                if event.key == pg.K_DOWN and self.directionsL[pg.K_DOWN]:
                    self.direction = vec2(0, self.size)
                    self.directionsL = {pg.K_UP: 0, pg.K_LEFT: 1, pg.K_RIGHT: 1, pg.K_DOWN: 1}
                if event.key == pg.K_LEFT and self.directionsL[pg.K_LEFT]:
                    self.direction = vec2(-self.size, 0)
                    self.directionsL = {pg.K_UP: 1, pg.K_LEFT: 1, pg.K_RIGHT: 0, pg.K_DOWN: 1}
                if event.key == pg.K_RIGHT and self.directionsL[pg.K_RIGHT]:
                    self.direction = vec2(self.size, 0)
                    self.directionsL = {pg.K_UP: 1, pg.K_LEFT: 0, pg.K_RIGHT: 1, pg.K_DOWN: 1}

    def delta_time(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time > self.step_delay:
            self.time = time_now
            return True
        return False

    def get_random_position(self):
        return [randrange(self.size // 2, self.game.WINDOW_SIZE - self.size // 2, self.size)] * 2

    def check_food(self):
        if self.rect.center == self.game.food.rect.center:
            self.game.food.rect.center = self.get_random_position()
            self.length += 1
            self.score += 1

    def game_over(self):
        if self.game.num_players == 2:
            self.game.message("GAME OVER!", COLORS['GRAY'], 6, FONTS['go_font'], 85)
            self.game.message(
                f'Green player - {self.game.players[0].score} Blue player - {self.game.players[1].score} ',
                COLORS['GRAY'], 4)
            self.game.game_over = True

        else:
            self.game.message("GAME OVER!", COLORS['GRAY'], 6, FONTS['go_font'], 85)
            self.game.message(
                f'Green player score: {self.game.players[0].score} ',
                COLORS['GRAY'], 4)
            self.game.game_over = True



    # maybe without it
    # def check_opponent(self):
    #     if self.game.num_players == 2:
    #         for pl in self.game.players:
    #             if len(pl.opponent.segments) != len(set(segment.center for segment in pl.segments)):
    #                 self.game_over()
    #                 return True

    def check_borders(self):
        if self.rect.left < 0 or self.rect.right > self.game.WINDOW_SIZE:
            self.game_over()
            return True
        if self.rect.top < 0 or self.rect.bottom > self.game.WINDOW_SIZE:
            self.game_over()
            return True

    def check_self_eating(self):
        if len(self.segments) != len(set(segment.center for segment in self.segments)):
            self.game_over()
            return True

    def move(self):
        if self.delta_time():
            self.rect.move_ip(self.direction)
            self.segments.append(self.rect.copy())
            self.segments = self.segments[-self.length:]

    def update(self):
        self.check_food()
        if self.stop_move_event():
            return self.game_over()
        self.move()

    def draw(self):
        [pg.draw.rect(self.game.screen, self.color, segment) for segment in self.segments]

    def stop_move_event(self):
        if self.check_borders():
            print('border crossed')
            return True
        # if self.check_opponent():
        #     print('opponent touched')
        #     return True
        if self.check_self_eating():
            print('self touched')
            return True


class Food:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        for pl in range(self.game.num_players):
            self.rect.center = self.game.players[pl].get_random_position()

    def draw(self):
        pg.draw.rect(self.game.screen, COLORS["RED"], self.rect)
