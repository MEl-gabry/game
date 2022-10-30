import pygame, os
from .state import State
from .events import events

class TextEvent(State):
    def __init__(self, game, event_num):
        self.game = game
        self.event = events[event_num]
        self.cursor_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "cursor.png"))
        self.cursor = self.cursor_img.get_rect()
        self.pos = 0
        self.fcol_x = self.game.GAME_W/4
        self.scol_x = 3 * self.game.GAME_W/4
        self.start_y = 7 * self.game.GAME_H/8
        self.cursor.x, self.cursor.y = self.fcol_x - 50, self.start_y - 3
        self.increment = self.game.GAME_H/16
        self.speed = 5
        self.done = False
        self.counter = 0
        State.__init__(self, game)

    def update(self, delta_time, actions):
        self.update_cursor(actions)
        if actions["action2"]:
            self.exit_state()
        self.game.reset_keys()

    def render(self, display):
        self.prev_state.render(display)
        slice = 0
        if not self.done:
            if self.counter < self.speed * len(self.event["text"]):
                self.counter += 1
                slice = self.counter//self.speed
            else:
                self.done = True
        else:
            slice = len(self.event["text"])
        self.game.draw_text(display, self.event["text"][0:slice], (255,255,255), 7, self.game.GAME_W/2, 3 * self.game.GAME_H/4 + 15)
        if self.done:
            y = self.start_y
            
            for i in range(len(self.event["options"])//2):
                self.game.draw_text(display, self.event["options"][i], (255,255,255), 7, self.fcol_x, y)
                y += self.increment
            
            self.scol_x = 3 * self.game.GAME_W/4
            y = self.start_y

            for i in range(len(self.event["options"])//2, len(self.event["options"])):
                self.game.draw_text(display, self.event["options"][i], (255,255,255), 7, self.scol_x, y)
                y += self.increment

            display.blit(self.cursor_img, self.cursor)

    def update_cursor(self, actions):
        if actions["down"]:
            self.pos = (self.pos + 1) % len(self.event["options"])
        elif actions["up"]:
            self.pos = (self.pos - 1) % len(self.event["options"])
        
        if actions["start"] and not self.done:
            self.done = True
        
        y_offset = 0

        if self.pos < len(self.event["options"])//2:
            self.cursor.x = self.fcol_x - 50
        else:
            self.cursor.x = self.scol_x - 50
            y_offset = -len(self.event["options"])//2
        self.cursor.y = (self.start_y - 3) + (self.pos + y_offset) * self.increment
