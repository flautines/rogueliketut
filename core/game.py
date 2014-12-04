from core.gfx import SCREEN_WIDTH
import libtcodpy as libtcod
import sys
import traceback

import gfx
import world



# A Game represents a single instance of a game, including its maps,
# data, and everything else.

class Game(object):
    def __init__(self):
        self.world = world.World()

    # Runs an interactive session of our game with the player
    def play(self):
        gfx.start()

        try:
            running = True
            self.world.make_map()
            while running:

                # render world
                self.world.draw()
                exit_code = self.world.handle_keys()
                if exit_code:
                    running = False
        except:
            print (traceback.format_exc())
            sys.exit(-1)