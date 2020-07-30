# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4 filetype=python:

####################################################################################################
# Dependencies
####################################################################################################

import sys
sys.path.append('/home/minecraft/config/overviewer/')

from filters import *

####################################################################################################
# Markers
####################################################################################################

markers = [
    dict(
        name='Builder Kommentare',
        filterFunction=lecternFilter,
        icon='markers/marker_comment.png',
        showIconInLegend=True,
        checked=False
    ),
    dict(
        name='Spieler',
        filterFunction=playerFilter,
        icon='markers/marker_player.png',
        showIconInLegend=True,
        checked=False
    ),
    dict(
        name='Parks & Öffentliche Plätze',
        filterFunction=filterBuilder('Park', 'Parks & Öffentliche Plätze'),
        icon='markers/marker_park.png',
        showIconInLegend=True,
        checked=True
    ),
    dict(
        name='Öffentliche Gebäude',
        filterFunction=filterBuilder('Public', 'Öffentliche Gebäude'),
        icon='markers/marker_public.png',
        showIconInLegend=True,
        checked=True
    ),
    dict(
        name='Handel & Industrie',
        filterFunction=filterBuilder('Commerce', 'Handel & Industrie'),
        icon='markers/marker_commerce.png',
        showIconInLegend=True,
        checked=True
    ),
    dict(
        name='Privatgebäude',
        filterFunction=filterBuilder('Private', 'Privatgebäude'),
        icon='markers/marker_private.png',
        showIconInLegend=True,
        checked=True
    ),
    dict(
        name='Militär',
        filterFunction=filterBuilder('Military', 'Militär'),
        icon='markers/marker_military.png',
        showIconInLegend=True,
        checked=True
    ),
    dict(
        name='U-Bahnhof',
        filterFunction=filterBuilder('Subway', 'U-Bahnhof'),
        icon='markers/marker_subway.png',
        showIconInLegend=True,
        checked=True
    )
]
