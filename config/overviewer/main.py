# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4 filetype=python:

####################################################################################################
# Dependencies
####################################################################################################

import sys
sys.path.append('/home/minecraft/config/overviewer/')

####################################################################################################
# General Options
####################################################################################################

outputdir = '/home/minecraft/overviewer'
texturepath = '/home/minecraft/resourcepacks/chromahills'

####################################################################################################
# Default Render Settings
####################################################################################################

dimension = 'overworld'
northdirection = 'upper-right'
defaultzoom = 5
showlocationmarker = False
showspawn = False
processes  = 3

from manualpois import *
from filters import *
from markers import *

####################################################################################################
# Worlds
####################################################################################################

worlds['Random World'] = '/home/minecraft/vanilla/randomhost'

####################################################################################################
# Normal Renders
####################################################################################################

# Surface Day
renders['randomhost_day'] = {
    'world': 'Random World',
    'title': 'Tag',
    'rendermode': smooth_lighting,
}

# Surface Night
renders['randomhost_night'] = {
    'world': 'Random World',
    'title': 'Nacht',
    'rendermode': [Base(), EdgeLines(), SmoothLighting(night=True, strength=0.9)],
}

# Cave
renders['randomhost_cave'] = {
    'world': 'Random World',
    'title': 'Untergrund',
    'rendermode': [Base(), EdgeLines(), Cave(only_lit=True)],
}

####################################################################################################
# Overlay Renders
####################################################################################################

renders['ramdomhost_spawnoverlay'] = {
    'world': 'Random World',
    'rendermode': [ClearBase(), SpawnOverlay()],
    'title': "Monster-Spawn",
    'overlay': ['randomhost_day','randomhost_night']
}

renders['ramdomhost_biomeoverlay'] = {
    'world': 'Random World',
    'rendermode': [ClearBase(), BiomeOverlay()],
    'title': "Biome",
    'overlay': ['randomhost_day','randomhost_night']
}

renders['ramdomhost_depthoverlay'] = {
    'world': 'Random World',
    'rendermode': [Base(), EdgeLines(), Cave(only_lit=True), DepthTinting()],
    'title': "Tiefe",
    'overlay': ['randomhost_cave']
}
