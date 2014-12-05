import libtcodpy as libtcod
from core import gfx
from core import entity
from core import tile
from core.tile import Tile
from core import dungeon

class World(object):
    def __init__(self):
        self.width = 100         # Level width
        self.height = 100        # level height
        self.view_width = 50    # displayed level window width
        self.view_height = 45   # displayed level window height
        self.player = entity.Entity("Player", 15, 22, "@", libtcod.yellow)

        # The world keeps track of all the entities (monsters, player, etc.)
        self.entities = []

    # Draws the world
    def draw(self):

        # get reference to the back buffer
        scr = gfx.get_back_buffer()

        # clear the screen contents
        gfx.clear()

        view_center_x = self.player.x - self.view_width / 2
        view_center_y = self.player.y - self.view_height / 2

        if view_center_x < 1:
            view_center_x = 1
        if view_center_y < 1:
            view_center_y = 1

        if view_center_x + self.view_width > self.width:
            view_center_x = self.width - self.view_width

        if view_center_y + self.view_height > self.height:
            view_center_y = self.height - self.view_height

        # draw the map tiles
        for y in range(self.view_height):
            for x in range(self.view_width):

                tile_empty = True
                # For each tile, determine what entities will be drawn there
                for entity in self.entities:
                    if (entity.x - view_center_x, entity.y - view_center_y) \
                            == (x, y):

                        gfx.draw(x,y, entity.char, entity.color)
                        tile_empty = False

                        # If tile is empty (no entities), draw wall or floor
                if tile_empty:
                    tile = self.map[x + view_center_x][y + view_center_y]
                    gfx.draw(x, y, char=tile.char, color=tile.color)

                    # else:
                    # gfx.draw(x, y, ".")

        # Draw the player
        draw_player_x = self.player.x - view_center_x
        draw_player_y = self.player.y - view_center_y
        gfx.draw(draw_player_x, draw_player_y,
                 self.player.char, self.player.color)

        # blit contents from back buffer to root window
        libtcod.console_blit(gfx.get_back_buffer(), 0, 0,
                             gfx.SCREEN_WIDTH, gfx.SCREEN_HEIGHT,
                             0, 0, 0)
        libtcod.console_flush()

    def handle_keys(self):
        # handle keys and exit game
        key = libtcod.console_wait_for_keypress(True)
        if key.vk == libtcod.KEY_ESCAPE:
            return True

        # toggle full screen Alt+Enter
        if key.vk == libtcod.KEY_ENTER and key.lalt:
            libtcod.console_set_fullscreen(not libtcod.
                                           console_is_fullscreen())

        dx = 0
        dy = 0
        # handle movement
        if libtcod.console_is_key_pressed(libtcod.KEY_UP):
            dx = 0
            dy = -1

        if libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
            dx = 0
            dy = 1

        if libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
            dx = -1
            dy = 0

        if libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
            dx = 1
            dy = 0

        if self.is_passable(self.player.x + dx, self.player.y + dy):
            self.player.x += dx
            self.player.y += dy

        return False

    def make_map(self):
        # fill the map with "unblocked" tiles
        dungeon_gen = dungeon.DungeonGenerator()
        self.map = dungeon_gen.make_map(
            self.width, self.height, self.player, self.entities)

    # returns True if tile at x, y position is walkable
    def is_passable(self, x, y):
        # return true if it's passable
        in_h_bounds = 0 <= x < self.width
        in_v_bounds = 0 <= y < self.height

        in_bounds = in_h_bounds and in_v_bounds

        if not in_bounds:
            return False
        else:
            tile = self.map[x][y]
            return tile.is_passable()
