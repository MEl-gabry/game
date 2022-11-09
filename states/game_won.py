from .state import State

class GameWon(State):
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, actions):
        if actions["start"]:
            self.game.playing = False
            self.game.running = False

    def render(self, display):
        display.fill((255, 255, 255))
        self.game.draw_text(display, "You escape to the planet Gondon!", (0,0,0), 12, self.game.GAME_W/2, self.game.GAME_H/2)