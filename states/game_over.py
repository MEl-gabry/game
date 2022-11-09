from .state import State

class GameOver(State):
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, actions):
        if actions["start"]:
            self.game.playing = False
            self.game.running = False

    def render(self, display):
        display.fill((255, 255, 255))
        self.game.draw_text(display, "Game Over", (0,0,0), 20, self.game.GAME_W/2, self.game.GAME_H/2)