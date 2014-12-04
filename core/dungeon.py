

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


class DungeonGenerator(object):
    def __init__(self):
        self.dungeon_map = [[]]

    def create_room(self, room):
        """

        :param room:
        """

        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1, room.x2 + 1):
            for y in range(room.y1, room.y2 + 1):
                self.dungeon_map[x][y]