import pygame, os
from .state import State
from .pause_menu import PauseMenu
from .text_event import TextEvent

class Game_World(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.space_img = pygame.transform.scale(pygame.image.load(os.path.join(self.game.assets_dir, "map", "space.png")), (self.game.GAME_W, self.game.GAME_H))
        self.text_box = pygame.transform.scale(pygame.image.load(os.path.join(self.game.assets_dir, "map", "box.png")), (self.game.GAME_W, self.game.GAME_H/4))

    def update(self, delta_time, actions):
        if actions["start"]:
            new_state = PauseMenu(self.game)
            new_state.enter_state()

    def render(self, display):
        display.blit(self.space_img, (0,0))
        display.blit(self.text_box, (0, 3 * self.game.GAME_H/4))
        self.trigger_event()

    def trigger_event(self):
        event = TextEvent(self.game)
        event.enter_state()