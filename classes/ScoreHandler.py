from pygame import sprite, font
from utils import load_font
from classes.Label import Label


class ScoreHandler(sprite.Sprite):
    def __init__(self, allsprites, game_state, song, background_handler):
        sprite.Sprite.__init__(self, allsprites)
        self.game_state = game_state
        self.background_handler = background_handler
        self.font = load_font(song.get_font_filename(), 36)

        self.score = 0
        self.show_highscore = False

        self.enabled = True

        # Feel free to play around with these variables
        # Currently they are not used anywhere in the code
        self.score_streak = 0
        self.score_multiplier = 1

        # Required to make sure the first note hits correctly
        self.played_once = False

        # Flag to see when a score should be saved after an update
        self.score_is_saved = True

        self.image = self.font.render('Score: ' + str(self.score), 1, (255, 255, 255))
        self.pos = (1050, 650)  # Set the location of the text
        self.score_text = None
        self.rect = (self.pos, self.image.get_size())

        self.streak_label = Label("", 1050, 600, False, 36, song.get_font_filename(), (255, 255, 255),
                                  "playing", allsprites, game_state)

    def restart(self):
        self.score = 0
        self.score_streak = 0
        self.score_is_saved = False

    # This is called every frame
    def update(self):
        if self.game_state.state == 'playing':
            self.streak_label.text = f"Streak: {str(self.score_streak)}"
            self.image = self.get_score_text_to_blit()
            self.show()
        elif self.game_state.state == 'prestart':
            self.streak_label.text = ""
            self.hide()
        elif self.game_state.state == 'difficulty':
            self.streak_label.text = ""
            self.hide()
        elif self.game_state.state == 'score':
            self.streak_label.text = ""
            self.score_streak = 0
            self.image = self.font.render("Last score: " + str(self.score), 1, (255, 255, 255))
            self.hide()
            self.show((self.background_handler.background.get_width() / 2 - self.image.get_width() / 2, 270))
        if not self.game_state.state == 'playing' and not self.score_is_saved:
            self.save_score()

    def get_score_text_to_blit(self):
        self.score_text = self.font.render('Score: ' + str(self.score), 1, (255, 255, 255))
        return self.score_text

    def change_score(self, score_difference):
        if (score_difference < 0):
            self.score_streak = 0
        elif score_difference > 0:
            self.score_streak += 1
        self.score += score_difference

    def get_high_score(self):
        played_song = self.game_state.song.get_notes_filename()
        best_score = None
        with open('scores.txt', 'r') as f:
            scores = f.read().splitlines(False)
            for score in scores:
                songdata = score.split(' ')
                songname = songdata[0]
                songscore = int(songdata[1])
                if songname == played_song and (best_score == None or songscore > best_score):
                    best_score = songscore

        return str(best_score)

    def get_last_score(self):
        with open('scores.txt', 'r') as f:
            lines = f.read().splitlines()
            last_line = lines[-1]
            return last_line.split(" ")[1]

    def save_score(self):
        self.score_is_saved = True
        self.played_once = True
        with open('scores.txt', 'a') as f:
            text = self.game_state.song.get_notes_filename() + ' ' + str(self.score) + '\n'
            f.write(text)
        print('The highscore is', self.get_high_score(), '- See ScoreHandler.py for new implementation')
        print('Your score is', self.score, '- See ScoreHandler.py for new implementation')

    def hide(self):
        if self.enabled:
            self.rect = ((-500, -500), self.image.get_size())
            self.enabled = False

    def show(self, pos=None):
        if pos is None:
            pos = self.pos
        if not self.enabled:
            self.rect = (pos, self.image.get_size())
            self.enabled = True