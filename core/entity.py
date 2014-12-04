import libtcodpy as libtcod

# An entity is anything that exists in the world.
class Entity(object):
    def __init__(self, name, x, y, char=None, color=libtcod.white):
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.char = name[0] if char is None else char

        self.target = None

    # Attempt to move 1 tile in a direction
    def move(self, (dx, dy)):
        self.x += dx
        self.y += dy