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