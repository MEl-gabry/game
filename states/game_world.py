import pygame, os
from .state import State
from .pause_menu import PauseMenu
from .default_text_event import DefaultTextEvent
from random import randrange
from .events import simple_events
from .game_over import GameOver
from .game_won import GameWon

class Game_World(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.space_img = pygame.transform.scale(pygame.image.load(os.path.join(self.game.assets_dir, "map", "space.png")), (self.game.GAME_W, self.game.GAME_H))
        self.text_box = pygame.transform.scale(pygame.image.load(os.path.join(self.game.assets_dir, "map", "box.png")), (self.game.GAME_W, self.game.GAME_H/4))
        self.spaceship = pygame.transform.scale(pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "spaceship.png")), (self.game.GAME_W/4, self.game.GAME_H/4))
        self.events_created = 0

    def update(self, actions):
        if actions["start"]:
            new_state = PauseMenu(self.game)
            new_state.enter_state()

    def render(self, display):
        if self.game.damage_events >= 3:
            event = GameOver(self.game)
            event.enter_state()
            return
        elif self.game.distance >= 10000:
            event = GameWon(self.game)
            event.enter_state()
            return

        display.blit(self.space_img, (0,0))
        display.blit(self.text_box, (0, 3 * self.game.GAME_H/4))
        display.blit(self.spaceship, (self.game.GAME_H/4, self.game.GAME_W/6))
        self.game.draw_text(display, f"Distance: {self.game.distance}m", (255,255,255), 9, 68, 10)
        self.game.draw_text(display, f"Fuel: {self.game.fuel}", (255,255,255), 9, 50, 20)
        self.game.draw_text(display, f"Money: {self.game.money}", (255,255,255), 9, 50, 30)
        if self.events_created != 0:
            return

        if self.game.damage_events > 0 and not self.game.dmg_accept:
            self.trigger_event(5)
        elif self.game.fuel == 0:
            self.trigger_event(3)
        elif self.game.distance >= self.game.prev_station_distance + 1000:
            self.game.prev_station_distance = self.game.distance
            self.trigger_event(4)
        elif self.game.distance >= self.game.prev_event_distance + 500 and randrange(0, 4) == 0:
            self.game.prev_event_distance = self.game.distance
            self.trigger_event(randrange(5, len(simple_events)))
        else:
            self.trigger_event(0)
        self.events_created += 1

    def trigger_event(self, num):
        event = DefaultTextEvent(self.game, num)
        event.enter_state()