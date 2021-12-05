# Dear PyGui basic plotting example to visualize sorting algorithms

from functools import partial
import dearpygui.dearpygui as dpg
from enum import Enum
import random
import time

# set up sorting enum
class SortingAlgorithm (str, Enum):
    BUBBLE = "Bubble Sort",
    INSERTION = "Insertion Sort",
    QUICK = "Quick Sort",           # note: recursion and generators make this visualization interesting but not accurate
    STALIN = "Stalin Sort"          # note: this is obviously a joke algorithm

# create context
dpg.create_context()

# increase font size for better visibility
dpg.set_global_font_scale(1.6)

# create viewport
dpg.create_viewport(title='Dear PyGui plotting sorting algorithm visualizer', width=1600, height=900)

def sort_bubble(listx, listy, delay=0):
    """Standard bubble sort implementation, adjusted to update Dear PyGui.

    Args:
        listx ([type]): list of x values for the plot
        listy ([type]): list of y values for the plot
        delay (int, optional): Delay in seconds between each UI update. Defaults to 0.

    Returns:
        list: sorted list of y values for the plot
    """
    # start time
    stime = time.time()
    # get the length of the list for y values (x is just for updating purposes)
    list_length = len(listy)

    # look at each item in the list
    for i in range(list_length):
        # define sorted flag for keeping track
        sorted_flag = True

        # check remaining list elements
        for j in range(list_length - i - 1):
            # compare list elements
            if listy[j] > listy[j + 1]:
                # if the current item is bigger than the next one, swap them
                listy[j], listy[j + 1] = listy[j + 1], listy[j]

                # sorted flag needs to be False for the algorithm to keep going - only of we swapped two elements though
                sorted_flag = False
            # update the plot for each value to visualize progress
            update_ui(listx, listy, delay, time.time() - stime)

        # if no sorting took place, the array is sorted
        if sorted_flag:
            break
    # return the sorted list - unused in this example
    return list

def sort_insertion(listx, listy, delay=0):
    """Standard insertion sort implementation, adjusted to update Dear PyGui.

    Args:
        listx ([type]): list of x values for the plot
        listy ([type]): list of y values for the plot
        delay (int, optional): Delay in seconds between each UI update. Defaults to 0.

    Returns:
        list: sorted list of y values for the plot
    """
    # start time
    stime = time.time()
    # start at the second element and look through all other items
    for i in range(1, len(listy)):
        # get current item to be sorted
        current_item = listy[i]
        # index variable to find correct sorting slot
        index = i - 1

        # check the left side of the array
        while index >= 0 and listy[index] > current_item:
            # push one to the left
            listy[index + 1] = listy[index]
            index -= 1
        # finish up by placing current item
        listy[index + 1] = current_item
        # update the plot for each value to visualize progress
        update_ui(listx, listy, delay, time.time() - stime)

    return listy

def sort_quick(listx, listy, delay=0):
    """Basic Quicksort implementation, adjusted to update Dear PyGui.
    This implementation uses the helper-function quicksort() to do the recursion via a generator.
    This isn't quite efficient or the way to visualize quicksort, but I found the results interesting,
    so I left it in.

    Args:
        listx ([type]): list of x values for the plot
        listy ([type]): list of y values for the plot
        delay (int, optional): Delay in seconds between each UI update. Defaults to 0.
    """
    time_start = time.time()

    # get a generator of the quicksort method
    listgen = quicksort(listy, listy, listx)
    framenumber = idx = 0
    # walk through the frames and update the ui
    # note: because of how this works, the visualization looks very un-quicksort-like
    for frame in listgen:
        if(len(frame) > 0):
            for item in frame:
                listy[idx] = item
                update_ui(listx, listy, delay, time.time() - time_start)
                idx += 1
            framenumber += 1

def quicksort(list, listy, listx):
    """Helper-function for the Quicksort implementation sort_quick().
    Yields a generator. Note: some of the contents of the generator are empty and need to be
    accounted for.

    Args:
        list ([type]): the list to sort in this current execution
        listy ([type]): list with the original y values
        listx ([type]): list with the original x values

    Yields:
        generator: A python generator with each step of the sorting algorithm.
    """
    # if theres only one element remaining, we're done
    if len(list) < 2:
        yield list
        return list

    low, same, high = [], [], []

    # select a random comparison element
    compare = list[random.randint(0, len(list) - 1)]

    # iterate the list
    for element in list:
        # sort the element into the corresponding new list
        if element < compare:
            low.append(element)
        elif element == compare:
            same.append(element)
        elif element > compare:
            high.append(element)

    # finally return low, same and high
    yield from quicksort(list=low, listx=listx, listy=listy)
    yield same
    yield from quicksort(list=high, listx=listx, listy=listy)

def sort_stalin(listy, delay=0):
    """A made up Stalin sort implementation, which is also a made up joke algorithm.
    Adjusted to update DearPyGui, even though it doesn't look half as interesting.

    Args:
        listy ([type]): list of y values for the plot
        delay (int, optional): Delay in seconds between each UI update. Defaults to 0.
    """

    # Note: This is a joke algorithm.
    stime = time.time()
    
    listlength = len(listy)
    element = listy[0]
    sortedlist = []

    # iterate the list once, every element that is not sorted, does not belong to the list
    for i in range(0, listlength):
        if listy[i] >= element:
            sortedlist.append(listy[i])
            element = listy[i]
            # update the ui but with only the sorted list
        update_ui(sortedlist, sortedlist, delay, time.time() - stime)


def sort(sender, app_data):
    """Callback for the Sort-Button.
    Gets current values for x and y from the plot, the delay and determines the algorithm 
    for the sorting.

    Args:
        sender (obj): Dear PyGui sender object for the callback
        app_data (obj): App Data
    """
    # get sorting algorithm
    algo = dpg.get_value("combo_sorting")
    # get data to sort
    scatterx = dpg.get_value("scatter_plot")[0]
    scattery = dpg.get_value("scatter_plot")[1]

    # get the delay
    delay = dpg.get_value("input_delay")

    # Python 3.10+ can use matching patterns instead
    if(algo == SortingAlgorithm.BUBBLE):
        sort_bubble(scatterx, scattery, delay)
    elif(algo == SortingAlgorithm.INSERTION):
        sort_insertion(scatterx, scattery, delay)
    elif(algo == SortingAlgorithm.QUICK):
        sort_quick(scatterx, scattery, delay)
    elif(algo == SortingAlgorithm.STALIN):
        sort_stalin(scatterx, scattery, delay)

def update_ui(listx, listy, delay, time_running):
    """Function to update the plot "scatter_plot" and the time running text "text_time".
    This function also sleeps for the appropriate delay.

    Args:
        listx ([type]): list of x values for the plot
        listy ([type]): list of y values for the plot
        delay (int): delay to sleep in seconds
        time_running (float): time the algorithm is running
    """
    # update the plot for each value to visualize progress
    dpg.set_value("scatter_plot", [listx, listy])
    # sleep for a delay if wanted
    if delay > 0:
        time.sleep(delay)
    # update elapsed time
    dpg.set_value("text_time", f"Time Running: {time_running}")

def plot(sender, app_data):
    """Function to plot values using Dear PyGui plots.
    Values used are taken from Inputs "input_min", "input_max" and "input_values".
    Generates "input_values" amount of random numbers between "input_min" and "input_max" to plot a
    more or less random plot.
    Adds a scatter series with the random values and a line series with the random values but sorted.
    Plot will be added to "mainwindow".

    Args:
        sender (obj): Dear PyGui sender
        app_data (obj): App Data
    """
    # if "plot" is clicked and a plot is present, default to reset
    if dpg.does_alias_exist("plot"):
        reset(sender, app_data)
        return
    
    # create the plot and add it to parent "mainwindow"
    plot_values=[]
    min_size = dpg.get_value("input_min")
    max_size = dpg.get_value("input_max")
    max_value = dpg.get_value("input_values")
    # generate random numbers
    for i in range(max_value):
        val = random.randint(min_size, max_size)
        plot_values.append(val)

    # create the plot
    with dpg.plot(label="Sorting Plot", tag="plot", parent="mainwindow", height=600, width=1200):
        # add plot legend
        dpg.add_plot_legend()
        # add both axis
        dpg.add_plot_axis(dpg.mvXAxis, label="x axis")
        dpg.add_plot_axis(dpg.mvYAxis, label="y axis")
        # x axis list
        xlist = list(range(len(plot_values)))
        # y axis list with sorted values (tim sort)
        ylist = sorted(plot_values)
        # add scatter series for random values
        dpg.add_scatter_series(label="values to sort", tag="scatter_plot", x=xlist, y=plot_values, parent=dpg.last_item())
        # add another axis and line series with increasing values
        dpg.add_plot_axis(dpg.mvYAxis, label="y axis")
        dpg.add_line_series(label="sorted values line", tag="line_plot", x=xlist, y=ylist, parent=dpg.last_item())

def reset(sender, app_data):
    """Function to reset the plot. Instead of providing new values, all Dear PyGui elements and 
    aliases are deleted and created again via plot().

    Args:
        sender (obj): Dear PyGui sender
        app_data (obj): App Data
    """
    # delete all items
    dpg.delete_item("scatter_plot")
    dpg.delete_item("line_plot")
    dpg.delete_item("plot")
    # delete all aliases if necessary - dpg sometimes does not remove an alias when deleting
    if dpg.does_alias_exist("scatter_plot"):
        dpg.remove_alias("scatter_plot")
    if dpg.does_alias_exist("line_plot"):
        dpg.remove_alias("line_plot")
    if dpg.does_alias_exist("plot"):
        dpg.remove_alias("plot")
    # plot a graph again
    plot(sender, app_data)
    # reset the timer
    dpg.set_value("text_time", "Time Running ...")

# create mainwindow
with dpg.window(tag="mainwindow"):
    # width for all controls
    def_width = 350
    # minimum value
    dpg.add_input_int(tag="input_min", label="minimum value", default_value=0, width=def_width)
    # maximum value
    dpg.add_input_int(tag="input_max", label="maximum value", default_value=100, width=def_width)
    # amount of values to generate
    dpg.add_input_int(tag="input_values", label="number of values to be generated", default_value=1000, width=def_width)
    # input for delay
    dpg.add_input_float(tag="input_delay", label="Sorting delay for each point in seconds", default_value=0,
                        min_value=0, min_clamped=True, width=def_width)
    # button for plotting
    dpg.add_button(tag="button_plot", label="Plot", callback=plot, width=def_width)
    # reset
    dpg.add_button(tag="button_reset", label="Reset", callback=reset, width=def_width)
    # combobox for chosing sorting algorithm
    sa = []
    for algo in SortingAlgorithm:
        sa.append(algo)
    dpg.add_combo(tag="combo_sorting", label="Sorting algorithm", items=sa, width=def_width, default_value=sa[0])
    # label for elapsed time
    dpg.add_text(tag="text_time", default_value="Time Running ... ")
    # button for sorting
    dpg.add_button(tag="button_sort", label="Sort", callback=sort, width=def_width)

# finish the setup, show viewport, set primary window - maybe maximize
dpg.setup_dearpygui()
dpg.show_viewport()
# maximize the window
dpg.maximize_viewport()
# set primary window to mainwindow
dpg.set_primary_window("mainwindow", True)
dpg.start_dearpygui()
dpg.destroy_context()
