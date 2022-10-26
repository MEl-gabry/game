import pygame, os
from states.state import State

class TextEvent(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)

    def update(self, delta_time, actions):
        if actions["action2"]:
            self.exit_state()
        self.game.reset_keys()

    def render(self, display):
        self.prev_state.render(display)
        self.game.draw_text(display, "Hello World!", (255,255,255), 10, self.game.GAME_W/2, 7 * self.game.GAME_H/8)