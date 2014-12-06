import libtcodpy as libtcod
from core import gfx
from core import entity
from core import tile
from core.tile import Tile
from core import dungeon


# FOV constants
FOV_ALGO = libtcod.FOV_BASIC
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 5

#-----------------------------------------------------------------------------
#           World class
#-----------------------------------------------------------------------------

class World(object):
    def __init__(self):
        self.width = 100        # Level width
        self.height = 100        # level height
        self.view_width = 50    # displayed level window width
        self.view_height = 45   # displayed level window height
        self.player = entity.Entity("Player", 15, 22, "@", libtcod.yellow)

        # The world keeps track of all the entities (monsters, player, etc.)
        self.entities = []

        # keeps track when the FOV needs to be recomputed
        self.fov_recompute = True


    def _create_fov_map(self):
        """


        """
        self.fov_map = libtcod.map_new(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                libtcod.map_set_properties(
                    self.fov_map, x, y,
                    not self.map[x][y].blocks_sight,
                    self.map[x][y].is_passable())

    def _recompute_fov_if_needed(self):
        """


        """
        # If FOV needs to be recomputed, flag it as no longer needed
        # and do the FOV computations
        if self.fov_recompute:
            self.fov_recompute = False
            libtcod.map_compute_fov(self.fov_map,
                self.player.x, self.player.y, TORCH_RADIUS,
                FOV_LIGHT_WALLS, FOV_ALGO)

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

        # recompute FOV if needed (player moved or something)
        self._recompute_fov_if_needed()

        # draw the map tiles
        for y in range(self.view_height):
            for x in range(self.view_width):

                visible = libtcod.map_is_in_fov(self.fov_map,
                                x + view_center_x, y + view_center_y)
                tile = self.map[x + view_center_x][y + view_center_y]

                if visible:
                    gfx.draw(x, y, char=tile.char, color=tile.color)

                    #since it's visible, flag it as explored
                    self.map[x + view_center_x][y + view_center_y].explored = True

                elif self.map[x + view_center_x][y + view_center_y].explored:
                    gfx.draw(x, y, char=tile.char, color=tile.dark_color)

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
            # if the player can move to the new position, flag that FOV
            # needs to be recomputed and update the player's coordinates
            self.fov_recompute = True
            self.player.x += dx
            self.player.y += dy

        return False

    def make_map(self):
        # use the DungeonGenerator class to create the map level
        dungeon_gen = dungeon.DungeonGenerator()
        self.map = dungeon_gen.make_map(
            self.width, self.height, self.player, self.entities)

        # create the FOV map
        self._create_fov_map()


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
