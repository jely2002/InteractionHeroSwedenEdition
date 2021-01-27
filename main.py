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
    song = song_library.example_song_short  # Short random song for debugging
    #song = song_library.example_song_long  # Ode To Joy
    #song = song_library.du_gamla_du_fria

    # Create game_state instance, this holds all required game info
    game_state = GameState(allsprites, song)

    # Checks if the program is running on a Raspberry Pi
    is_running_on_rpi = utils.is_running_on_rpi()
    if is_running_on_rpi:
        # Below are some pin input numbers, feel free to change them. However,
        # !!! ALWAYS READ THE PIN DOCUMENTATION CAREFULLY !!!
        # Pay special attention to the difference between GPIO pin numbers and BOARD pin numbers
        # For example GPIO17 is addressed 17 rather than 11 (See pin numbering diagram.)
        # https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering
        gpio_pin_numbers = [22, 23, 24, 27]  # Max 4 pins
        gpio_buttons = init_rpi_buttons(gpio_pin_numbers)
        game_state.add_gpio_pins(gpio_pin_numbers)

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
                    for button in gpio_buttons:
                        # When a buttons is pressed in this loop and wasn't pressed in the last loop
                        if button.is_pressed() and button.gpio_key is hitbox.gpio_event_key and button.is_available():
                            button.use()  # Set the button as unavailable for the next loop
                            game_state.check_for_hit(hitbox)
                        # When a button was not pressed in this loop
                        elif not button.is_pressed():
                            button.wake()  # Set the button as available again
                            hitbox.unpunch()

        # This calls the update() function on all sprites
        allsprites.update()

        # Draw Everything
        screen.blit(game_state.get_background(), (0, 0))  # First draw a new background
        allsprites.draw(screen)  # Next draw all updated sprites
        pygame.display.update()  # Finally render everything to the display


def init_rpi_buttons(gpio_pin_numbers):
    # Initialize Raspberry Pi input pins

    gpio_buttons = []

    from gpiozero import Button
    from classes.GpioButton import GpioButton

    # Here you can configure which pins you use on your Raspberry Pi
    gpio_pins = gpio_pin_numbers  # Max 4 pins 
    bounce_time_in_sec = 0.1

    gpio_buttons.append(GpioButton(Button(gpio_pins[0], bounce_time=bounce_time_in_sec)))
    gpio_buttons.append(GpioButton(Button(gpio_pins[1], bounce_time=bounce_time_in_sec)))
    gpio_buttons.append(GpioButton(Button(gpio_pins[2], bounce_time=bounce_time_in_sec)))
    gpio_buttons.append(GpioButton(Button(gpio_pins[3], bounce_time=bounce_time_in_sec)))

    print('The following pins are configured as (gpio) button inputs:', gpio_pins)

    return gpio_buttons


if __name__ == "__main__":
    main()
