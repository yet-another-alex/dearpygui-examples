# Dear PyGui basic bare window example
# no content, one main window, different default font size

import dearpygui.dearpygui as dpg

# create context
dpg.create_context()

# increase font size for better visibility
dpg.set_global_font_scale(1.6)

# create viewport
dpg.create_viewport(title='very basic Dear PyGui window', width=1280, height=720)

# create mainwindow
with dpg.window(tag="mainwindow"):
    # this is where to start with more ui components
    # e.g. Hello World in (mostly) the center of the viewport
    dpg.add_text("Hello World!", pos=(dpg.get_viewport_width()/2, dpg.get_viewport_height()/2))

# finish the setup, show viewport, set primary window - maybe maximize
dpg.setup_dearpygui()
dpg.show_viewport()
# maximize the window
#dpg.maximize_viewport()
# set primary window to mainwindow
dpg.set_primary_window("mainwindow", True)
dpg.start_dearpygui()
dpg.destroy_context()
