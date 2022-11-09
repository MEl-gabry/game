class State():
    def __init__(self, game):
        self.game = game
        self.prev_state = None
        self.speed = 5
        self.done = False
        self.counter = 0
    
    def update(self, actions):
        pass

    def render(self, surface):
        pass

    def type_writer(self, surface, text):
        slice = 0
        if not self.done:
            if self.counter < self.speed * len(text):
                self.counter += 1
                slice = self.counter//self.speed
            else:
                self.done = True
        else:
            slice = len(text)
        self.game.draw_text(surface, text[0:slice], (255,255,255), 7, self.game.GAME_W/2, 3 * self.game.GAME_H/4 + 15)

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()