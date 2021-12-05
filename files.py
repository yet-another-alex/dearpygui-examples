# Dear PyGui file dialog example
# choose a directory, populate a listbox with items
# when selected, display some file info

import dearpygui.dearpygui as dpg
from os import listdir, path
import time

# create context
dpg.create_context()

# increase font size for better visibility
dpg.set_global_font_scale(1.6)

# create viewport
dpg.create_viewport(title='Dear PyGui file dialog example', width=1280, height=720)

def select_directory(sender, app_data):
    """Function to build a file dialog and select a directory.
    Callback upon completion is process_directory().

    Args:
        sender (obj): Dear PyGui sender widget
        app_data (None): None in this case
    """
    with dpg.file_dialog(directory_selector=True, show=True, callback=process_directory):
        dpg.add_file_extension(".*")

def process_directory(sender, app_data):
    """Function to get all files and directories within the selected directory.
    Will populate the listbox "files_listbox" with the items.

    Args:
        sender (obj): Dear PyGui sender widget
        app_data ([obj]): information from the file dialog: file_path_name, file_name, current_path, current_filter, selections[]
    """
    # retrieve file path
    directory = app_data["file_path_name"]
    # get all files and directories from path
    files = listdir(directory)
    # add files to the listbox
    dpg.configure_item("files_listbox", items=files)
    # update the UI to confirm selected directory
    dpg.set_value("file_text", directory)

def select_file(sender, app_data):
    """Function to update the GUI when a file in the listbox is selected.
    Retrieves some information on the selected files and displays them in the GUI.

    Args:
        sender (obj): Dear PyGui sender widget
        app_data (str): selected listbox entry
    """
    # get selected file
    selected_file = app_data
    # get current path
    cwd = dpg.get_value("file_text")
    # add path to file/dir
    selected_file = cwd + "/" + selected_file

    # get some basic file info and display it via gui
    dpg.set_value("file_info_n", "file          :" + selected_file)
    dpg.set_value("file_info_1", "last accessed :" + time.ctime(path.getatime(selected_file)))
    dpg.set_value("file_info_2", "last modified :" + time.ctime(path.getmtime(selected_file)))
    dpg.set_value("file_info_3", "last changed  :" + time.ctime(path.getctime(selected_file)))
    dpg.set_value("file_info_4", "file size     :" + path.getsize(selected_file))


# create mainwindow
with dpg.window(tag="mainwindow"):
    # intro text
    dpg.add_text("Choose a directory and get a listing of all files in the listbox.")
    dpg.add_text("Select a file in the listbox to display information about that file.")
    dpg.add_spacer()

    # file input information
    dpg.add_text(tag="file_text")
    dpg.add_button(label="choose directory", callback=select_directory)

    # list box for files in directory
    dpg.add_listbox(tag="files_listbox", label="files in directory", callback=select_file, num_items=12)

    # label for file information
    dpg.add_text(tag="file_info_n")
    dpg.add_text(tag="file_info_1")
    dpg.add_text(tag="file_info_2")
    dpg.add_text(tag="file_info_3")
    dpg.add_text(tag="file_info_4")

# finish the setup, show viewport, set primary window - maybe maximize
dpg.setup_dearpygui()
dpg.show_viewport()
# maximize the window
#dpg.maximize_viewport()
# set primary window to mainwindow
dpg.set_primary_window("mainwindow", True)
dpg.start_dearpygui()
dpg.destroy_context()
