# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4 filetype=python:

####################################################################################################
# Dependencies
####################################################################################################

import sys
sys.path.append('/home/minecraft/config/overviewer/')
from functools import partial

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
    'markers': [],
}

# Surface Night
renders['randomhost_night'] = {
    'world': 'Random World',
    'title': 'Nacht',
    'rendermode': [Base(), EdgeLines(), SmoothLighting(night=True, strength=0.9)],
    'markers': [],
}

# Cave
renders['randomhost_cave'] = {
    'world': 'Random World',
    'title': 'Untergrund',
    'rendermode': [Base(), EdgeLines(), Cave(only_lit=True)],
    'markers': [],
}

####################################################################################################
# Overlay Renders
####################################################################################################

renders['ramdomhost_spawnoverlay'] = {
    'world': 'Random World',
    'rendermode': [ClearBase(), SpawnOverlay()],
    'title': "Monster-Spawn",
    'overlay': ['randomhost_day','randomhost_night'],
    'markers': [],
}

renders['ramdomhost_biomeoverlay'] = {
    'world': 'Random World',
    'rendermode': [ClearBase(), BiomeOverlay()],
    'title': "Biome",
    'overlay': ['randomhost_day','randomhost_night'],
    'markers': [],
}

renders['ramdomhost_depthoverlay'] = {
    'world': 'Random World',
    'rendermode': [Base(), EdgeLines(), Cave(only_lit=True), DepthTinting()],
    'title': "Tiefe",
    'overlay': ['randomhost_cave'],
    'markers': [],
}

####################################################################################################
# Apply world based Markers Partials
####################################################################################################

for key in renders:
    world = renders[key]['world']
    worldPath = worlds[world]
    renders[key]['markers'].append(
        dict(
            name='Spieler',
            filterFunction=partial(playerFilter, worldPath),
            icon='icons/marker_comment.png',
            checked=False
        )
    )

