import libtcodpy as libtcod


# This is the back buffer console
back_buffer = None


# Screen with / height in characters
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50


# This starts libtcod console
def start():
    libtcod.console_set_custom_font('arial10x10.png',
                                    libtcod.FONT_TYPE_GREYSCALE |
                                    libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT,
                              'RogueLike with libtcod', False)

    back_buffer = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)


def get_back_buffer():
    global back_buffer
    return back_buffer


# Clear the screen. This uses the libtcod clear routine
def clear():
    libtcod.console_clear(back_buffer)


# Draw a character at X,Y. Includes boundary checking
def draw(x, y, char, color=libtcod.white):
    libtcod.console_put_char_ex(back_buffer, x, y, char,
                                fore=color, back=libtcod.BKGND_NONE)


