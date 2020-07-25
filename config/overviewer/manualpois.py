# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4 filetype=python:

####################################################################################################
# Dependencies
####################################################################################################

global json
global os
import json
import logging
import os

####################################################################################################
# Points of Interest
####################################################################################################

manualpois = []

poiDirPath = '/home/minecraft/config/overviewer/poi/'
logging.info('Loading POIs from \'%s\'', poiDirPath)
if os.path.isdir(poiDirPath):
    for file in os.listdir(poiDirPath):
        poiFilePath=os.path.join(poiDirPath, file)
        if os.path.isfile(poiFilePath):
            with open(poiFilePath, 'r') as poiFile:
                poiData = json.load(poiFile)
                poiId = os.path.splitext(file)[0].capitalize()
                for poi in poiData:
                    poi['id'] = poiId
                    manualpois.append(poi)
else:
    logging.warning('Failed to load POI data from \'%s\'', poiDirPath)
