import pygame, os
from .state import State
from .events import simple_events
from math import ceil

class DefaultTextEvent(State):
    def __init__(self, game, event_num):
        State.__init__(self, game)
        self.event = simple_events[event_num]
        self.keys = list(self.event["options"].keys())
        self.cursor_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "cursor.png"))
        self.cursor = self.cursor_img.get_rect()
        self.pos = 0
        self.fcol_x = self.game.GAME_W/4
        self.scol_x = 3 * self.game.GAME_W/4
        self.start_y = 7 * self.game.GAME_H/8
        self.cursor.x, self.cursor.y = self.fcol_x - 100, self.start_y - 3
        self.increment = self.game.GAME_H/16

    def update(self, actions):
        self.update_cursor(actions)
        if actions["action2"]:
            self.exit_state()
        self.game.reset_keys()

    def render(self, display):
        self.prev_state.render(display)
        try:
            display.blit(self.event["image"], self.event["coords"])
        except KeyError:
            pass

        self.type_writer(display, self.event["text"])
        if self.done:
            y = self.start_y
            
            for i in range(ceil(len(self.event["options"])/2)):
                self.game.draw_text(display, self.keys[i], (255,255,255), 7, self.fcol_x, y)
                y += self.increment
            
            self.scol_x = 3 * self.game.GAME_W/4
            y = self.start_y

            for i in range(ceil(len(self.event["options"])/2), len(self.event["options"])):
                self.game.draw_text(display, self.keys[i], (255,255,255), 7, self.scol_x, y)
                y += self.increment

            display.blit(self.cursor_img, self.cursor)

    def update_cursor(self, actions):
        if actions["down"]:
            self.pos = (self.pos + 1) % len(self.event["options"])
        elif actions["up"]:
            self.pos = (self.pos - 1) % len(self.event["options"])
        
        if actions["start"] and not self.done:
            self.done = True
        elif actions["start"]:
            self.trigger_event()
        
        y_offset = 0

        if self.pos < ceil(len(self.event["options"])/2):
            self.cursor.x = self.fcol_x - 100
        else:
            self.cursor.x = self.scol_x - 100
            y_offset = -ceil(len(self.event["options"])/2)
        self.cursor.y = (self.start_y - 3) + (self.pos + y_offset) * self.increment

    def trigger_event(self):
        self.exit_state()
        event = self.event["options"][self.keys[self.pos]](self.game)
        event.enter_state()