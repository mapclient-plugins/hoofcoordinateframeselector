
'''
MAP Client Plugin
'''

__version__ = '0.1.0'
__author__ = 'Hugh Sorby'
__stepname__ = 'Coordinate Frame Selector'
__location__ = ''

# import class that derives itself from the step mountpoint.
from mapclientplugins.coordinateframeselectorstep import step

# Import the resource file when the module is loaded,
# this enables the framework to use the step icon.
import resources_rc