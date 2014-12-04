from core import tile
from core.tile import Tile

class Rect:
    def __init__(self, x, y, width, height):
        """
        A rectangle on the map. used to characterize a room

        :param x: Coord x of the top left corner
        :param y: Coord y of the top left corner
        :param width: Width of the rectangle
        :param height: Height of the rectangle
        """
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.dungeon_map = [[]]


class DungeonGenerator(object):
    def __init__(self):
        self.dungeon_map = [[]]

    def create_room(self, room):
        """

        :param room:
        """

        # go through the tiles in the rectangle and make them passable
        # we actually want to leave some walls at the border of the room, so
        # we'll leave out one tile in all directions. (+1 at start, +0 end)
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2 + 1):
                self.dungeon_map[x][y] = Tile('t_floor')

    def make_map(self, width, height):
        """

        :param width:
        :param height:
        """

        # Fill the map with walls
        self.dungeon_map = [[Tile('t_wall')
                            for y in range(height)]
                                for x in range(width)]

        # create two rooms
        room1 = Rect(10, 15, 10, 15)
        room2 = Rect(30, 15, 10, 15)

        self.create_room(room1)
        self.create_room(room2)

        self.dungeon_map[13][18] = Tile('t_tree')

        return self.dungeon_map