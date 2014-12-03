import libtcodpy as libtcod
import sys
import traceback


# Screen with / height in characters
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50


# A Game represents a single instance of a game, including its maps,
# data, and everything else.

class Game(object):
    def __init__(self):
        pass

    def step(self):
        x, y = 5, 5
        while not libtcod.console_is_window_closed():

            # render the screen
            libtcod.console_clear(0)
            libtcod.console_put_char(0, x, y, "@")
            libtcod.console_flush()

            # handle keys and exit game
            key = libtcod.console_wait_for_keypress(True)
            if key.vk == libtcod.KEY_ESCAPE:
                return True

            # toggle full screen Alt+Enter
            if key.vk == libtcod.KEY_ENTER and key.lalt:
                libtcod.console_set_fullscreen(not libtcod.
                                               console_is_fullscreen())

            # handle movement
            if libtcod.console_is_key_pressed(libtcod.KEY_UP): y -= 1
            if libtcod.console_is_key_pressed(libtcod.KEY_DOWN): y += 1
            if libtcod.console_is_key_pressed(libtcod.KEY_LEFT): x -= 1
            if libtcod.console_is_key_pressed(libtcod.KEY_RIGHT): x += 1


    # Runs an interactive session of our game with the player
    def play(self):
        libtcod.console_set_custom_font('arial10x10.png',
                                        libtcod.FONT_TYPE_GREYSCALE |
                                        libtcod.FONT_LAYOUT_TCOD)

        libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT,
                                  'RogueLike with libtcod', False)

        try:
            self.step()
        except:
            print (traceback.format_exc())
            sys.exit(-1)
        