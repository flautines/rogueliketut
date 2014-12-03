from core.gfx import SCREEN_WIDTH
import libtcodpy as libtcod
import sys
import traceback
import gfx


# A Game represents a single instance of a game, including its maps,
# data, and everything else.

class Game(object):
    def __init__(self):
        pass

    def step(self):
        x, y = 5, 5

        # get reference to the back buffer
        scr = gfx.get_back_buffer()
        while not libtcod.console_is_window_closed():

            # render the screen to the back buffer
            libtcod.console_clear(scr)
            libtcod.console_put_char(scr, x, y, "@")

            # blit contents from back buffer to root window
            libtcod.console_blit(gfx.get_back_buffer(), 0, 0,
                                 gfx.SCREEN_WIDTH, gfx.SCREEN_HEIGHT,
                                 0, 0, 0)

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
        gfx.start()

        try:
            self.step()
        except:
            print (traceback.format_exc())
            sys.exit(-1)

