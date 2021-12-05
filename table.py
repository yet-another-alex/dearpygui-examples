# Dear PyGui basic table example
# table creation and cell editing
# no import or export functionality

import dearpygui.dearpygui as dpg

# create context
dpg.create_context()

# increase font size for better visibility
dpg.set_global_font_scale(1.4)

# create viewport
dpg.create_viewport(title='Dear PyGui table example', width=1280, height=720)


def show_status_update(statusmessage, color=(255, 255, 255, 255)):
    """Utility function to display status messages with a color to the label "status_text".

    Args:
        statusmessage (str): the status message to display. Prefix "current status: " will always be added.
        color ((float, float, float, float), optional): Color the text should appear in. Defaults to (255, 255, 255, 255).
    """
    dpg.configure_item("status_text", color=color)
    dpg.set_value("status_text", f"current status: {statusmessage}")

def add_row():
    """Function for adding rows to the table "maintable". Also adds the click handler to the label 
    for each cell. Number of columns is pulled via global variable columns. Global variable 
    rows gets updated after the row is added.
    """
    global rows
    with dpg.table_row(parent="maintable"):
        for i in range(0, columns):
            # add text field to table
            dpg.add_text(f"row{rows} column{i}", tag=f"cell_{rows}{i}")
            # add click handler to text field / cell
            with dpg.item_handler_registry(tag=f"cell_handler_{rows}{i}") as handler:
                dpg.add_item_clicked_handler(callback=cell_edit)
            dpg.bind_item_handler_registry(f"cell_{rows}{i}", f"cell_handler_{rows}{i}")
    rows += 1

def delete_table():
    """Function to delete the table "maintable".
    Resets global variables rows and columns to 0.
    Since DearPyGui sometimes does not remove an alias upon deletion, the function 
    includes deletion of all aliases starting with "row_", "col_" or "cell_".
    """
    # delete main table
    dpg.delete_item("maintable")
    # reset counters
    global rows
    global columns
    rows = 0
    columns = 0

    # sometimes some aliases will not be removed upon item deletion
    # I found no intended way to deal with this, so all prefixes must be deleted manually
    to_delete = []
    for alias in dpg.get_aliases():
        # rows / columns / cells
        if alias.startswith("row_") or alias.startswith("col_") or alias.startswith("cell_"):
            to_delete.append(alias)
    # delete marked aliases
    for alias in to_delete:
        dpg.remove_alias(alias)

def create_table(colcount=3, rowcount=3):
    """Function to create a table with a specified row and column count.
    Header-columns get automatically added, labelled with "column" and an incrementing number.
    After the creation, show_status_update() is invoked with information for the user.

    Global variables columns and rows will be reset and adjusted.

    Table will be added to "mainwindow" and have the tag "maintable".

    Note: maximum columns accepted by DearPyGui are 50. This is validated in GUI only in this example.

    Args:
        colcount (int, optional): Number of columns for the table. Defaults to 3.
        rowcount (int, optional): Number of rows for the table. Defaults to 3.
    """
    # remember variables if needed
    global columns
    global rows
    columns = colcount  # columns can always stay the same for now
    rows = 0            # rows start at 0 and will be counted up by add_row()
    # create table
    with dpg.table(parent="mainwindow", header_row=True, resizable=True, policy=dpg.mvTable_SizingStretchProp,
                   borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True,
                   tag="maintable", row_background=True):

        # add header columns
        for i in range(0, colcount):
            dpg.add_table_column(tag=f"col_{i}", label=f"column {i}")

        # add rows and cells
        for i in range(0, rowcount):
            add_row()
    
    # update for user
    show_status_update(f"table with {colcount} columns and {rowcount} rows created!")


def create_table_btn():
    """Click-handler for the create table button.
    Retrieves current row and column count from the GUI using "rowcount" and "columncount" widgets.
    Deletes the table and creates a new one in its place.
    sender/app_data is not included since its unused.
    """
    # get row and column count
    rowc = dpg.get_value("rowcount")
    colc = dpg.get_value("columncount")

    # delete and create table
    delete_table()
    create_table(colcount=colc, rowcount=rowc)

def cell_edit(sender, app_data):
    """Click-handler. Function to enable editing in a table cell.
    The function shows a status update to the user including tag and content of the clicked cell.
    To achieve editing, the label within the table cell is removed and a text input widget is 
    placed at the same position and updated with the same tag and content.

    Args:
        sender (obj): callback-sender
        app_data ([obj]): app_data
    """
    # remember current cell for later
    global current_cell
    current_cell = app_data[1]
    # show clicked info to user
    show_status_update(f"clicked on cell tag {app_data[1]}, content {dpg.get_value(app_data[1])}")
    # store cell contents for later
    cell_content = dpg.get_value(app_data[1])

    # save current parent
    parent = dpg.get_item_parent(current_cell)
    # iterate cells in current row and save the position
    cell_position = None
    cell_before = None
    for child in dpg.get_item_children(parent)[1]:
        # if we saved a cell position, we can save the next one for the before-parameter
        if cell_position:
            cell_before = dpg.get_item_alias(child)
            # escape to not overwrite any saved items
            break
        if dpg.get_item_alias(child) == current_cell:
            cell_position = dpg.get_item_alias(child)
    # delete current cell (meaning the label)
    dpg.delete_item(current_cell)
    # remove the alias if not already happened
    if dpg.does_alias_exist(current_cell):
        dpg.remove_alias(current_cell)
    
    # add an input text widget instead of the label one
    # if we saved a "before"-position, attach it before that position
    if cell_before:
        dpg.add_input_text(tag=current_cell, parent=parent, before=cell_before)
    else:
        dpg.add_input_text(tag=current_cell, parent=parent)
    dpg.set_value(current_cell, cell_content)


# create mainwindow
with dpg.window(tag="mainwindow"):
    # intro text box
    dpg.add_text("Dear PyGui basic table example. Click the text within a cell to edit it.")
    dpg.add_spacer()
    # text box for status updates
    dpg.add_text("current status: ", tag="status_text")

    # controls for table creation
    # integer input field for column count between 1 and 50
    dpg.add_input_int(tag="columncount", label="number of columns", max_value=50, max_clamped=True,
                        min_value=1, min_clamped=True, default_value=3)
    # integer input field for row count between 1 and infinite
    dpg.add_input_int(tag="rowcount", label="number of rows", min_value=1, min_clamped=True, default_value=10)
    # button to create a new table
    dpg.add_button(tag="create_table_button", label="create new table", callback=create_table_btn)

    # buttons for table interaction / user_data is column count
    dpg.add_button(tag="add_row_button", label="add row", callback=add_row)

    # create an example table with header
    create_table(4, 15)

# finish the setup, show viewport, set primary window - maybe maximize
dpg.setup_dearpygui()
dpg.show_viewport()
# maximize the window
#dpg.maximize_viewport()
# set primary window to mainwindow
dpg.set_primary_window("mainwindow", True)
dpg.start_dearpygui()
dpg.destroy_context()
