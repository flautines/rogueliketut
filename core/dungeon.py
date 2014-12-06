from core import tile, entity
from core.tile import Tile
import libtcodpy as libtcod


#--------------------------------------------------------------------------
# Constants
#--------------------------------------------------------------------------
# Room dimensions
ROOM_MIN_SIZE = 6
ROOM_MAX_SIZE = 10
MAX_ROOMS = 30

# Dungeon generator algorithms
DG_TRIAL_ERROR  = 0


class Rect:
    def __init__(self, x, y, width, height):
        """
        A rectangle on the map. used to characterize a room

        :param x: Coord x of the top left corner
        :param y: Coord y of the top left corner
        :param width: Width of the rectangle
        :param height: Height of the rectangle
        """

        # Top left coordinates
        self.x1 = x
        self.y1 = y

        # Bottom right coordinates
        self.x2 = x + width
        self.y2 = y + height

        # Center coordinates
        self._center_x = (self.x1 + self.x2) / 2
        self._center_y = (self.y1 + self.y2) / 2

    def intersects(self, other):
        """Returns true if this Rectangle overlaps the "other" Rectangle

        :param other: Rectangle to check for intersection
        """
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    @property
    def center(self):
        """Returns the center of this Rectangle as a tuple


        :return: Tuple: (center_x, center_y)
        """
        return (self._center_x, self._center_y)


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

    def create_v_tunnel(self, y1, y2, x):
        """'Carves' a vertical tunnel between two rooms


        :param y1: Coord. y of the first room
        :param y2: Coord. y of the second room
        ;param x: Coord. x of the first room
        """
        #creative use of min,max avoids an if/else to determine
        #wether we must carve from up to down or down to bottom
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.dungeon_map[x][y] = Tile('t_floor')

    def create_h_tunnel(self, x1, x2, y):
        """'Carves' a horizontal tunnel between two rooms

        :param x1: Coord. x of first room
        :param x2: Coord. y of second room
        :param y: Coord. y of first room
        """
        #creative use of min,max avoids an if/else to determine
        #wether we must carve from left to right or rigt to left
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.dungeon_map[x][y] = Tile('t_floor')

    def make_test_map(self, width, height):
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

        # just for testing add a Tree tile
        self.dungeon_map[13][18] = Tile('t_tree')

        # connect the two rooms with a horizontal tunnel
        self.create_h_tunnel(15, 35, 23)

        return self.dungeon_map

    def make_map(self, width, height, player, entities,
                 dg_algorithm=DG_TRIAL_ERROR):

        # fill the map with "wall" tiles
        """

        :param width: Map width
        :param height: Map height
        :param player: Player entity
        :param entities: List of entities (monsters, potions, player, etc.)
                         in the map
        :param dg_algorithm:
        :return:
        """
        self.dungeon_map = [[Tile('t_wall')
            for y in range(height)]
                for x in range(width)]

        # Trial and error method used by default
        if dg_algorithm == DG_TRIAL_ERROR:
            rooms = []
            num_rooms = 0

            for room in range(MAX_ROOMS):
                # random room dimensions
                room_width = libtcod.random_get_int(0,
                        ROOM_MIN_SIZE, ROOM_MAX_SIZE)

                room_height = libtcod.random_get_int(0,
                        ROOM_MIN_SIZE, ROOM_MAX_SIZE)

                # random room position inside boundaries of the map
                room_x = libtcod.random_get_int(0,
                        1, width-1 - room_width - 1)

                room_y = libtcod.random_get_int(0,
                        1, height-1 - room_height - 1)

                # new room with dimensions and position from above
                new_room = Rect(room_x, room_y, room_width, room_height)

                # run through the other rooms and see if they intersect with
                # this one
                intersects = False
                for other_room in rooms:
                    intersects = new_room.intersects(other_room)
                    if intersects:
                        break

                # If the new room didn't intersect other rooms, then
                # the new room is valid and we can add it to the map
                if not intersects:
                    self.create_room(new_room)

                    # center coordinates of this new room
                    (new_x, new_y) = new_room.center

                    # debug, print room letters
                    room_no = entity.Entity(chr(65+num_rooms), new_x, new_y,
                                chr(65+num_rooms), libtcod.white)
                    entities.insert(0, room_no)

                    # place the player at the first room (center)
                    if num_rooms == 0:
                        player.x = new_x
                        player.y = new_y

                    else:
                        # all rooms after the first:
                        # connect it to the previous room with a tunnel

                        # center coordinates of the previous room
                        (prev_x, prev_y) = rooms[num_rooms-1].center

                        # create a vertical tunnel from the previous room to
                        # the new room and then repeat with a horizontal
                        # tunnel, creating n a L shape connection
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)

                    # finally, append the new room to the list
                    rooms.append(new_room)
                    num_rooms += 1

            return self.dungeon_map