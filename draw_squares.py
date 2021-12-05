# Dear PyGui basic drawing squares example
# draws randomly colored squares on a 

import dearpygui.dearpygui as dpg
import random

# create context
dpg.create_context()

# create viewport - width/height irrelevant since window will be maximized later
dpg.create_viewport(title="drawing squares example")

def random_color():
    """helper function to generate a random color

    Returns:
        (int, int, int, int): tuple with random values between 0 and 255 for the first three values and always 255 for the last
    """
    # generate random color values using random module
    cola = random.randrange(0, 255)
    colb = random.randrange(0, 255)
    colc = random.randrange(0, 255)
    # return the random color with full alpha
    return (cola, colb, colc, 255)

# create main window
with dpg.window(tag="mainwindow"):

    # create a drawing list and add to it, large width/height to make it scrollable
    with dpg.drawlist(width=3000, height=3000):
        # iterate the "grid"
        for x in range(0, 30):
            for y in range(0, 30):
                # define a multiplier
                multi = 100
                # calculate the points of the rectangle
                p1 = (x*multi, y*multi)                 # upper left corner
                p2 = (x*multi+multi, y*multi+multi)     # lower right corner
                # get a random color
                randcol = random_color()
                # draw and fill the rectangle
                dpg.draw_rectangle(p1, p2, color=randcol, fill=randcol)


# finish the setup, show viewport, set primary window, maximize
dpg.setup_dearpygui()
dpg.show_viewport()
# maximize the window
dpg.maximize_viewport()
# set primary window to fill the entire application with mainwindow
dpg.set_primary_window("mainwindow", True)
dpg.start_dearpygui()
dpg.destroy_context()
