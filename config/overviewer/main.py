# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4 filetype=python:

####################################################################################################
# Dependencies
####################################################################################################

import sys
sys.path.append('/home/minecraft/config/overviewer/')
from .observer import JSObserver

####################################################################################################
# General Options
####################################################################################################

outputdir = '/var/www/sites/tv.random-host.minecraft/src/www/overviewer'
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
center = [0, 64, 0]

from manualpois import *
from filters import *
from markers import *

####################################################################################################
# Worlds
####################################################################################################

worlds['Random World'] = '/home/minecraft/cache/overviewer/worldstorage/randomhost'

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

####################################################################################################
# Overlay Renders
####################################################################################################

renders['ramdomhost_spawnoverlay'] = {
    'world': 'Random World',
    'title': 'Monster-Spawn',
    'rendermode': [ClearBase(), SpawnOverlay()],
    'overlay': ['randomhost_day','randomhost_night']
}

####################################################################################################
# Observers
####################################################################################################

observer = JSObserver(
    outputdir,
    5,
    dict(
        totalTiles='Rendere %d Kacheln',
        renderCompleted='Vorgang abgeschlossen. Dauer: %02d:%02d:%02d',
        renderProgress='%d von %d Kacheln gerendert (%d%%, ETA: %s)'
    )
)
