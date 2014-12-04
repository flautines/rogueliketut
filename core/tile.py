import libtcodpy as libtcod

# tile_info
# key : (char, color, is_passable)
tile_info = {
    "t_floor": ('.', libtcod.white, True),
    "t_wall": (chr(178), libtcod.light_sepia, False),
    "t_tree": ('T', libtcod.dark_green, False)
}


# a tile of the map and its properties
class Tile:
    def __init__(self, type, blocks_sight=None):
        """
        A Tile contains info about each cell in the map.

        :param blocks_sight: True if the tile doesn't block sight
        """
        self.type = type

        # by default, if a tile is blocked, it also blocks sight
        if blocks_sight is None:
            self.blocks_sight = not tile_info[self.type][2]

    @property
    def char(self):
        return tile_info[self.type][0]

    @property
    def color(self):
        return tile_info[self.type][1]

    def is_passable(self):
        return tile_info[self.type][2]