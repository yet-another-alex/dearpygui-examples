# Dear PyGui basic arrow drawing example
# drawing arrows on click and every frame

import dearpygui.dearpygui as dpg
import random

# create context
dpg.create_context()

# create the viewport - width/height is irrelevant - window will be maximized later
dpg.create_viewport(title="drawing arrows example")

# mouse marking variable setup
mouse_mark_pos = (0, 0)
mouse_mark = False
mouse_mark_circle = None

# calculate mouse coordinates
def get_mouse_coords():
    """helper function to get the mouse position and calculate 
    offset of the scrolling within the main window

    Returns:
        (float, float): tuple with mousex and mousey
    """
    # get mouse position from dearpygui
    mousex = dpg.get_mouse_pos(local=False)[0]
    mousey = dpg.get_mouse_pos(local=False)[1]
    # add scroll offset to get actual mouse coordinates on screen
    mousex += dpg.get_x_scroll("mainwindow")
    mousey += dpg.get_y_scroll("mainwindow")
    # return the mouse position
    return (mousex, mousey)

def click_handler():
    """handler for click events
    Marks a position when clicked and draws an arrow when clicked again.
    """
    global mouse_mark_pos       # position (float, float) of the mouse when first clicked
    global mouse_mark           # flag (bool) wether a mark is set or not
    global mouse_mark_circle    # UUID (int) of the dpg-circle that is drawn when first clicked

    # if the mouse has already been clicked before and there is a circle currently
    if mouse_mark:
        # draw an arrow from the previously marked position to the current position in a random color
        dpg.draw_arrow(get_mouse_coords(), mouse_mark_pos, thickness=4, color=random_color(), parent="mainwindow")
        # set the mouse flag to not clicked
        mouse_mark = False
        # remove marking circle by deleting the dpg-item
        dpg.delete_item(mouse_mark_circle)
    else:
        # this is the first click performed
        # remember the mouse coordinates
        mouse_mark_pos = get_mouse_coords()
        # set the mouse flag to clicked
        mouse_mark = True
        # draw a circle at the marked position
        mouse_mark_circle = dpg.draw_circle(mouse_mark_pos, 10, color=(255, 0, 0, 255), fill=(255, 0, 0, 255), parent="mainwindow")

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

# create the main window for our example
with dpg.window(tag="mainwindow"):

    # add a drawlist with a certain width and height to enable scrolling
    with dpg.drawlist(width=3000, height=3000):
        pass

# register the mouse click handler
with dpg.handler_registry():
    dpg.add_mouse_click_handler(callback=click_handler)


# final setup required by dpg
dpg.setup_dearpygui()
dpg.show_viewport()
# maximize the window
dpg.maximize_viewport()
# set mainwindow as the primary window
dpg.set_primary_window("mainwindow", True)

# instead of running start_dearpygui(), we will execute the frame render manually
while dpg.is_dearpygui_running():
    # setup markmouse variable to remember the arrow moving with the mouse
    global markmouse
    markmouse = None
    # if there was a click and the marking circle is currently on screen, we will draw a moving arrow pointing to the mouse
    if mouse_mark:
        # note: the color is random and will be reevaluated every frame
        markmouse = dpg.draw_arrow(get_mouse_coords(), mouse_mark_pos, thickness=4, color=random_color(), parent="mainwindow")
    # render the frame
    dpg.render_dearpygui_frame()
    # after the frame was rendered, check again to see if a second click was made
    if mouse_mark and markmouse != None:
        # delete the moving arrow
        dpg.delete_item(markmouse)
    
dpg.destroy_context()
