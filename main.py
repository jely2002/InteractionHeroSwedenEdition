# General imports
import pygame, utils
from classes.GameState import GameState
from classes.Button import Button
import song_library
from classes.Label import Label


def main():
    # Initialize pygame
    pygame.init()
    # Set screen size. Don't change this unless you know what you are doing!
    screen = pygame.display.set_mode((1280, 720))
    # Set the window title
    pygame.display.set_caption("Sweden - Interaction Hero")

    # Keeps track of all sprites to be updated every frame
    allsprites = pygame.sprite.Group()

    # Song to be used in game. Only one can be used.
    #song = song_library.example_song_short  # Short random song for debugging
    #song = song_library.example_song_long  # Ode To Joy
    song = song_library.du_gamla_du_fria

    # Checks if the program is running on a Raspberry Pi
    is_running_on_rpi = utils.is_running_on_rpi()

    # Create game_state instance, this holds all required game info
    game_state = GameState(allsprites, song, is_running_on_rpi)


    if is_running_on_rpi:
        from classes.TouchButtons import TouchButtons
        touch_pin_numbers = [1, 2, 3, 4]  # Max 4 pins
        touchButtons = TouchButtons(1, 0x57)
        game_state.add_touch_pins(touch_pin_numbers)

    # Prepare game objects
    clock = pygame.time.Clock()
    startButton = Button(570, 200, 140, 40, ' Börja', game_state.restart, "menu", song.get_font_filename(), allsprites, game_state)
    quitButton = Button(570, 300, 140, 40, ' Sluta', quit, "menu", song.get_font_filename(), allsprites, game_state)
    scoreButton = Button(570, 250, 140, 40, ' Score', game_state.open_score_menu, "menu", song.get_font_filename(), allsprites, game_state)
    scoreBackButton = Button(570, 350, 140, 40, ' Bakåt', game_state.open_menu, "score", song.get_font_filename(), allsprites, game_state)
    highscoreLabel = Label("", 100, 220, True, 36, song.get_font_filename(), (255,255,255), "score", allsprites, game_state)

    # Main loop
    going = True
    while going:

        # Update the clock, argument is max fps
        clock.tick(60)

        # Every 'tick' or programcycle the gamestate update() is called
        game_state.update()

        # Get all events from the last cycle and store them as variable
        # This is stored as a variable because pygame.even.get() empties this list
        eventlist = pygame.event.get()

        # Check if there are any global quit events
        for event in eventlist:
            # If yes, the game loop won't start again
            if event.type == pygame.QUIT:
                going = False
            elif event.type == pygame.KEYDOWN and event.unicode == pygame.K_ESCAPE:
                going = False

        # This runs before the user starts the game
        if game_state.state == 'prestart':
            for event in eventlist:
                # Checks if a mouse is clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    startButton.check_click()
                    quitButton.check_click()
                    scoreButton.check_click()

        elif game_state.state == 'score':
            highscoreLabel.text = "Highscore: " + str(game_state.scoreHandler.get_high_score())
            for event in eventlist:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    scoreBackButton.check_click()


        # This runs when the users starts a game
        elif game_state.state == 'playing':
            # Loop through all potential hitboxes
            for hitbox in game_state.hitboxes:
                # Every hitbox needs to check all events
                for event in eventlist:
                    if event.type == pygame.KEYDOWN and event.unicode == hitbox.event_key:
                        game_state.check_for_hit(hitbox)
                    elif event.type == pygame.KEYUP:
                        hitbox.unpunch()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        game_state.state = 'prestart'
                        hitbox.destroy_all_notes()

                # When on RPi also check for GPIO input
                if is_running_on_rpi:
                    for button in touch_pin_numbers:
                        if touchButtons.is_pressed(button) and button == hitbox.touch_event_key and touchButtons.is_available():
                            touchButtons.use()
                            if not touchButtons.is_cooldown(button):
                                touchButtons.set_cooldown(True, button)
                                game_state.check_for_hit(hitbox)
                        elif not touchButtons.is_pressed(button):
                            if touchButtons.is_cooldown(button):
                                hitbox.unpunch()
                            touchButtons.wake()    

        # This calls the update() function on all sprites
        allsprites.update()

        # Draw Everything
        screen.blit(game_state.get_background(), (0, 0))  # First draw a new background
        allsprites.draw(screen)  # Next draw all updated sprites
        pygame.display.update()  # Finally render everything to the display


if __name__ == "__main__":
    main()
