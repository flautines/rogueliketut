import libtcodpy as libtcod


#-----------------------------------------------------------------------------
#                           Constants
# ----------------------------------------------------------------------------

# normal (in light) colors
T_WALL_COLOR            = libtcod.Color(210, 180, 140)
T_FLOOR_COLOR           = libtcod.white
T_TREE_COLOR            = libtcod.dark_green
T_STAIRS_DOWN_COLOR     = libtcod.cyan
T_STAIRS_UP_COLOR       = libtcod.light_blue

# dark (in shadow) colors
T_GEN_DARK_COLOR      = libtcod.Color(47, 79, 79)
# for now, set all shadow colors to the same generic color.
# But we can change it later on if we want each tile to have its own
# shadow color
T_WALL_DARK_COLOR     = T_GEN_DARK_COLOR
T_FLOOR_DARK_COLOR    = T_GEN_DARK_COLOR
T_TREE_DARK_COLOR     = T_GEN_DARK_COLOR
T_STAIRS_DOWN_DARK_COLOR    = T_GEN_DARK_COLOR
T_STAIRS_UP_DARK_COLOR      = T_GEN_DARK_COLOR

# tile_info
# key : (char, normal color, dark color, is_passable)
tile_info = {
    "t_floor":  ('.',      T_FLOOR_COLOR,  T_FLOOR_DARK_COLOR,  True),
    "t_wall":   (chr(178), T_WALL_COLOR,   T_WALL_DARK_COLOR,   False),
    "t_tree":   ('T',      T_TREE_COLOR,   T_TREE_DARK_COLOR,   False),
    "t_stairs_down": ('>', T_STAIRS_DOWN_COLOR, T_STAIRS_DOWN_DARK_COLOR,
        True),
    "t_stairs_up": ('<', T_STAIRS_UP_COLOR, T_STAIRS_UP_DARK_COLOR,
        True)
}


#-----------------------------------------------------------------------------
#           Tile class
#-----------------------------------------------------------------------------

# a tile of the map and its properties
class Tile:
    def __init__(self, type, blocks_sight=None):
        """
        A Tile contains info about each cell in the map.
        ;:param type: Tile type, must be a string in the tile_info keys.
        :param blocks_sight: True if the tile doesn't block sight
        """
        self.type = type

        self.blocks_sight = blocks_sight
        # by default, if a tile is blocked, it also blocks sight
        if blocks_sight is None:
            self.blocks_sight = not tile_info[self.type][3]

        # all tiles start unexplored
        self.explored = False

    @property
    def char(self):
        return tile_info[self.type][0]

    @property
    def color(self):
        return tile_info[self.type][1]

    @property
    def dark_color(self):
        return tile_info[self.type][2]

    def is_passable(self):
        return tile_info[self.type][3]