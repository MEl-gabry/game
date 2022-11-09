import os, pygame
from states.title import Title

class Game():
    def __init__(self):
        pygame.init()
        self.GAME_W, self.GAME_H = 480, 270
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 960, 540
        self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.running, self.playing = True, True
        self.actions = {"left": False, "right": False, "up" : False, "down" : False, "action1" : False, "action2" : False, "start" : False}
        self.state_stack = []
        self.distance = 0
        self.money = 0
        self.fuel = 100
        self.fuel_per_distance = 0.2
        self.fps = 60
        self.supplies = 3
        self.damage_events = 0
        self.prev_event_distance = 0
        self.prev_station_distance = 0
        self.artifacts = {}
        self.dmg_accept = False
        self.clock = pygame.time.Clock()
        self.load_assets()
        self.load_states()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == pygame.K_UP:
                    self.actions['up'] = True
                if event.key == pygame.K_DOWN:
                    self.actions['down'] = True
                if event.key == pygame.K_p:
                    self.actions['action1'] = True
                if event.key == pygame.K_o:
                    self.actions['action2'] = True    
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = True  

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.actions['up'] = False
                if event.key == pygame.K_DOWN:
                    self.actions['down'] = False
                if event.key == pygame.K_p:
                    self.actions['action1'] = False
                if event.key == pygame.K_o:
                    self.actions['action2'] = False
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = False  

    def game_loop(self):
        while self.playing:
            self.clock.tick(self.fps)
            self.get_events()
            self.update()
            self.render()
    
    def update(self):
        self.state_stack[-1].update(self.actions)

    def render(self):
        self.state_stack[-1].render(self.game_canvas)
        self.screen.blit(pygame.transform.scale(self.game_canvas, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
        pygame.display.flip()
    
    def draw_text(self, surface, text, color, size, x, y):
        font = pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), size)
        text_surface = font.render(text, True, color)
        # text_surface.set_colorkey((0, 0 ,0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)
    
    def move(self, distance):
        self.fuel -= round(distance * self.fuel_per_distance)
        self.distance += distance - self.damage_events * 5

    def load_assets(self):
        self.assets_dir = os.path.join("assets")
        self.sprite_dir = os.path.join(self.assets_dir, "sprites")
        self.font_dir = os.path.join(self.assets_dir, "font")

    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()