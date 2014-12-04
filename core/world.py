import libtcodpy as libtcod
from core import gfx
from core import entity


# tile_info
# key : (char, color, is_passable)
tile_info = {
    "t_floor": ('.', libtcod.white, True),
    "t_wall": ('#', libtcod.light_sepia, False),
    "t_tree": ('T', libtcod.dark_green, True)
}


# a tile of the map and its properties
class Tile:
    def __init__(self, is_passable, type, blocks_sight=None):
        """
        A Tile contains info about each cell in the map.

        :param is_passable: True if the tile doesn't block movement
        :param blocks_sight: True if the tile doesn't block sight
        """
        self.is_passable = is_passable

        # by default, if a tile is blocked, it also blocks sight
        if blocks_sight is None:
            self.blocks_sight = not is_passable

        self.type = type


class World(object):
    def __init__(self):
        self.width = 40
        self.height = 25
        self.player = entity.Entity("Player", 4, 4, "@", libtcod.yellow)

        # The world keeps track of all the entities (monsters, player, etc.)
        self.entities = [self.player]

    # Draws the world
    def draw(self):

        # get reference to the back buffer
        scr = gfx.get_back_buffer()

        # clear the screen contents
        gfx.clear()

        # draw the map tiles
        for y in range(self.height):
            for x in range(self.width):

                tile_empty = True
                # For each tile, determine what entities will be drawn there
                for e in self.entities:
                    if (e.x, e.y) == (x, y):
                        gfx.draw(x, y, e.char, e.color)
                        tile_empty = False

                        # If tile is empty (no entities), draw wall or floor
                if tile_empty:
                    tile = self.map[x][y]
                    gfx.draw(x, y, tile_info[tile.type][0],
                             color=tile_info[tile.type][1])

                    # else:
                    # gfx.draw(x, y, ".")

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
        self.map = [[Tile(True, 't_floor')
                     for y in range(self.height)]
                    for x in range(self.width)]

        self.map[30][22] = Tile(False, 't_wall')
        self.map[39][22] = Tile(False, 't_wall')
        self.map[23][12] = Tile(False, 't_tree')

    # returns True if tile at x, y position is walkable
    def is_passable(self, x, y):
        # return true if it's passable
        in_h_bounds = 0 <= x < self.width
        in_v_bounds = 0 <= y < self.height

        in_bounds = in_h_bounds and in_v_bounds

        if not in_bounds:
            return False
        else:
            return tile_info[self.map[x][y].type][2]
