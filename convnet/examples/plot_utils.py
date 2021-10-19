import matplotlib
import matplotlib.pyplot as plot
import itertools

NICE_BLUE = '#66b3ff'
NICE_RED = '#ff9999'
NICE_GREEN = '#99ff99'
NICE_ORANGE = '#ffcc99'
NICE_PURPLE = 'mediumpurple'

nice_color = itertools.cycle((NICE_BLUE, NICE_RED, NICE_GREEN, NICE_ORANGE))
nice2_color = itertools.cycle((NICE_BLUE, NICE_RED, NICE_GREEN, NICE_ORANGE, 'olive', 'purple'))
dark_color = itertools.cycle(('green', 'purple', 'blue', 'magenta', 'purple', 'gray', 'brown', 'turquoise', 'gold', 'olive', 'silver', 'rosybrown', 'plum', 'goldenrod', 'lightsteelblue', 'lightpink', 'orange', 'darkgray', 'orangered'))
light_color = itertools.cycle(('silver', 'rosybrown', 'plum', 'lightsteelblue', 'lightpink', 'orange', 'turquoise'))
linestyle_cycle = itertools.cycle(('-', '--', '-.', ':'))
marker_cycle = itertools.cycle(('x', '+', 'v', '^', 'p', 'd', '<', '>', '1' , '2', '3', '4'))
skinny_marker_l = ['x', '+', '1', '2', '3', '4']

mew, ms = 1, 2 # 3, 5

def prettify(ax):
  ax.patch.set_alpha(0.2)
  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)
