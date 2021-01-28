import pygame
from utils import load_font


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, function, type, font_filename, allsprites, game_state):
        pygame.sprite.Sprite.__init__(self, allsprites)
        self.game_state = game_state
        self.allsprites = allsprites
        self.x = x
        self.y = y
        self.enabled = True
        self.width = width
        self.height = height
        self.type = type
        self.onclick_function = function
        self.color_text = (255,255,255)
        self.dark_bg_rgb = (4,2,3, 170)
        self.light_bg_rgb = (4,2,3, 170)
        self.font = load_font(font_filename, 30)

        self.text = self.font.render(text, True, self.color_text)

        dark_button = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        dark_button = dark_button.convert_alpha()
        dark_button.fill(self.dark_bg_rgb)
        dark_button.blit(self.text, (22, -2))
        self.dark_button = dark_button

        light_button = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        light_button = light_button.convert_alpha()
        light_button.fill(self.light_bg_rgb)
        light_button.blit(self.text, (21, -1))
        self.light_button = light_button

        self.image = self.dark_button
        self.pos = (self.x, self.y)
        self.rect = (self.pos, (self.width, self.height))
    
    def update(self):
        if self.game_state.state == 'prestart':
            if self.type != "menu":
                self.hide()
            else:
                self.show()
                if self._mouse_hover():
                    self.image = self.light_button
                else:
                    self.image = self.dark_button
        elif self.game_state.state == 'playing':
            self.hide()
        elif self.game_state.state == 'score':
            if self.type != "score":
                self.hide()
            else:
                self.show()

    def hide(self):
        if self.enabled:
            self.rect = ((-500, -500), (self.width, self.height))
            self.enabled = False

    def show(self):
        if not self.enabled:
            self.rect = (self.pos, (self.width, self.height))
            self.enabled = True

    def _mouse_hover(self):
        mouse = pygame.mouse.get_pos()
        return (mouse[0] >= self.x and mouse[0] <= self.x + self.width and mouse[1] >= self.y and mouse[1] <= self.y + self.height)

    def check_click(self):
        if self._mouse_hover():
            self.onclick_function()
