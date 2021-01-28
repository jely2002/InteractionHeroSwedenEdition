import pygame
from utils import load_font


class Label(pygame.sprite.Sprite):
    def __init__(self, text, x, y, center, font_size, font_name, color, type, allsprites, game_state):
        pygame.sprite.Sprite.__init__(self, allsprites)
        self.game_state = game_state
        self.allsprites = allsprites

        self.background_handler = game_state.background_handler
        self.center = center
        self.x = x
        self.y = y
        self.type = type
        self.enabled = False
        self.type = type
        self.color = color
        self.text = text

        self.font = load_font(font_name, font_size)
        self.image = self.font.render('', 1, color)
        if center:
            self.pos = (self.background_handler.background.get_width() / 2 - self.image.get_width() / 2, self.y)
        else:
            self.pos = (x, y)
        self.rect = (self.pos, self.image.get_size())
        self.hide()

    def update(self):
        self.image = self.font.render(self.text, 1, self.color)
        #print(self.text)
        self.check_pos()
        if self.game_state.state == 'prestart':
            self.hide()
        elif self.game_state.state == 'playing':
            if self.type == "playing":
                self.show()
            else:
                self.hide()
        elif self.game_state.state == 'difficulty':
            self.hide()
        elif self.game_state.state == 'score':
            if self.type == 'score':
                self.show()
            else:
                self.hide()

    def check_pos(self):
        if self.enabled:
            if self.center:
                self.rect = ((self.background_handler.background.get_width() / 2 - self.image.get_width() / 2, self.y),self.image.get_size())
            else:
                self.rect = (self.pos, self.image.get_size())

    def hide(self):
        if self.enabled:
            self.rect = ((-500, -500), self.image.get_size())
            self.enabled = False

    def show(self):

        if not self.enabled:
            self.check_pos()
            self.enabled = True