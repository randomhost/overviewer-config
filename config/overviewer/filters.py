# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4 filetype=python:

####################################################################################################
# Dependencies
####################################################################################################

import sys
sys.path.append('/home/minecraft/config/overviewer/')

global json
global os
global html
import json
import os
import html

from collections import OrderedDict

####################################################################################################
# Helpers
####################################################################################################

def initItem(stats, key, name):
    if(key not in stats['items']['items']):
        stats['items']['items'][key] = {
            'name': name,
            'actions': {
                'mined': 0,
                'broken': 0,
                'crafted': 0,
                'used': 0,
                'picked_up': 0,
                'dropped': 0
            }
        }

def initMob(stats, key, name):
    if(key not in stats['mobs']['mobs']):
        stats['mobs']['mobs'][key] = {
            'name': name,
            'actions': {
                'killed': 0,
                'killed_by': 0
            }
        }

####################################################################################################
# Filters
####################################################################################################

def playerFilter(poi):
    if poi['id'] == 'Player':
        poi['icon'] = 'https://overviewer.org/avatar/%s' % poi['EntityId']
        tooltipIcon = 'https://overviewer.org/avatar/%s/head' % poi['EntityId']

        # load translations
        translationFilePath= './de_de.json'
        if os.path.isfile(translationFilePath):
            with open(translationFilePath, 'r') as translationFile:
                decodedTranslations = json.load(translationFile)
        else:
            decodedTranslations={}

        # load player stats
        statsFilePath= '/home/minecraft/vanilla/worldstorage/randomhost/stats/%s.json' % poi['uuid']
        if os.path.isfile(statsFilePath):
            with open(statsFilePath, 'r') as statsFile:
                decodedStats = json.load(statsFile)
                if 'stats' in decodedStats:
                    # build dictionary structure
                    stats = {
                        'general': {
                            'name': decodedTranslations['stat.generalButton'],
                            'actions': {}
                        },
                        'items': {
                            'name': decodedTranslations['stat.itemsButton'],
                            'actions': {
                                'mined': decodedTranslations['stat_type.minecraft.mined'],
                                'broken': decodedTranslations['stat_type.minecraft.broken'],
                                'crafted': decodedTranslations['stat_type.minecraft.crafted'],
                                'used': decodedTranslations['stat_type.minecraft.used'],
                                'picked_up': decodedTranslations['stat_type.minecraft.picked_up'],
                                'dropped': decodedTranslations['stat_type.minecraft.dropped']
                            },
                            'items': {}
                        },
                        'mobs': {
                            'name': decodedTranslations['stat.mobsButton'],
                            'actions': {
                                'killed': 'Getötet',
                                'killed_by': 'Getötet von'
                            },
                            'mobs': {}
                        }
                    }

                    # general stats
                    if 'minecraft:custom' in decodedStats['stats']:
                        for key in decodedStats['stats']['minecraft:custom']:
                            translationKey='stat.' + key.replace(':', '.')
                            translation=decodedTranslations[translationKey]

                            stats['general']['actions'][translationKey] = {
                                'name': translation,
                                'value': decodedStats['stats']['minecraft:custom'][key]
                            }

                    # item stats: mined
                    if 'minecraft:mined' in decodedStats['stats']:
                        for key in decodedStats['stats']['minecraft:mined']:
                            translationKey='block.' + key.replace(':', '.')
                            translation=decodedTranslations[translationKey]
                            initItem(stats, key, translation)

                            stats['items']['items'][key]['actions']['mined'] = decodedStats['stats']['minecraft:mined'][key]

                    # item stats: broken
                    if 'minecraft:broken' in decodedStats['stats']:
                        for key in decodedStats['stats']['minecraft:broken']:
                            translationKey='item.' + key.replace(':', '.')
                            translation=decodedTranslations[translationKey]
                            initItem(stats, key, translation)

                            stats['items']['items'][key]['actions']['broken'] = decodedStats['stats']['minecraft:broken'][key]

                    # item stats: crafted
                    if 'minecraft:crafted' in decodedStats['stats']:
                        for key in decodedStats['stats']['minecraft:crafted']:
                            try:
                                translationKey='block.' + key.replace(':', '.')
                                translation=decodedTranslations[translationKey]
                            except KeyError:
                                translationKey='item.' + key.replace(':', '.')
                                translation=decodedTranslations[translationKey]
                            initItem(stats, key, translation)

                            stats['items']['items'][key]['actions']['crafted'] = decodedStats['stats']['minecraft:crafted'][key]

                    # item stats: used
                    if 'minecraft:used' in decodedStats['stats']:
                        for key in decodedStats['stats']['minecraft:used']:
                            try:
                                translationKey='block.' + key.replace(':', '.')
                                translation=decodedTranslations[translationKey]
                            except KeyError:
                                translationKey='item.' + key.replace(':', '.')
                                translation=decodedTranslations[translationKey]
                            initItem(stats, key, translation)

                            stats['items']['items'][key]['actions']['used'] = decodedStats['stats']['minecraft:used'][key]

                    # item stats: picked up
                    if 'minecraft:picked_up' in decodedStats['stats']:
                        for key in decodedStats['stats']['minecraft:picked_up']:
                            try:
                                translationKey='block.' + key.replace(':', '.')
                                translation=decodedTranslations[translationKey]
                            except KeyError:
                                translationKey='item.' + key.replace(':', '.')
                                translation=decodedTranslations[translationKey]
                            initItem(stats, key, translation)

                            stats['items']['items'][key]['actions']['picked_up'] = decodedStats['stats']['minecraft:picked_up'][key]

                    # item stats: dropped
                    if 'minecraft:dropped' in decodedStats['stats']:
                        for key in decodedStats['stats']['minecraft:dropped']:
                            try:
                                translationKey='block.' + key.replace(':', '.')
                                translation=decodedTranslations[translationKey]
                            except KeyError:
                                translationKey='item.' + key.replace(':', '.')
                                translation=decodedTranslations[translationKey]
                            initItem(stats, key, translation)

                            stats['items']['items'][key]['actions']['dropped'] = decodedStats['stats']['minecraft:dropped'][key]

                    # mob stats: killed
                    if 'minecraft:killed' in decodedStats['stats']:
                        for key in decodedStats['stats']['minecraft:killed']:
                            translationKey='entity.' + key.replace(':', '.')
                            translation=decodedTranslations[translationKey]
                            initMob(stats, key, translation)

                            stats['mobs']['mobs'][key]['actions']['killed'] = decodedStats['stats']['minecraft:killed'][key]

                    # mob stats: killed by
                    if 'minecraft:killed_by' in decodedStats['stats']:
                        for key in decodedStats['stats']['minecraft:killed_by']:
                            translationKey='entity.' + key.replace(':', '.')
                            translation=decodedTranslations[translationKey]
                            initMob(stats, key, translation)

                            stats['mobs']['mobs'][key]['actions']['killed_by'] = decodedStats['stats']['minecraft:killed_by'][key]
                else:
                    stats={}
        else:
            stats={}

        titleHtml='<strong class="title"><img src="{icon}" width="16" alt="" /> {player}</strong>' \
        .format(icon=tooltipIcon,player=poi['EntityId'])
        bodyHtml='''<br>
            <i>Letzte bekannte Position von &bdquo;{player}&ldquo;</i><br>
            <div class="playerskin">
                <img src="{skin}" alt="{player}" width="64" class="image-rendering-pixelated">
            </div>
            '''.format(skin=poi['icon'], player=poi['EntityId'])
        if bool(stats):
            statsHtml='''
                <p class="text-center">
                     <a href="#" data-toggle="modal" data-target="#statsModal" data-icon="{icon}" data-title="{player}" data-stats="{stats}">
                         <i class="da da-bar-chart" aria-hidden="false"></i>
                         Statistiken
                     </a>
                 </p>'''.format(icon=tooltipIcon, player=poi['EntityId'], stats=html.escape(json.dumps(stats)))
            return (poi['EntityId'],titleHtml+bodyHtml+statsHtml)
        else:
            return (poi['EntityId'],titleHtml+bodyHtml)

def lecternFilter(poi):
    if poi['id'] == 'minecraft:lectern':
        try:
            titleHtml='<strong class="title"><img src="icons/marker_comment.png" width="16" alt="" /> {title}</strong>' \
            .format(title=poi['Book']['tag']['title'])

            bookText=''
            for page in poi['Book']['tag']['pages']:
                decodedPage = json.loads(page)
                bookText+=decodedPage['text'].replace('\n', '<br>')+' '

            bodyHtml='''<br>
                <i>Von {author}</i>
                <p>{text}</p>
                '''.format(author=poi['Book']['tag']['author'], text=bookText )
            return (poi['Book']['tag']['title'], titleHtml + bodyHtml)
        except KeyError:
            return None

def filterBuilder(id, category):
    def genericFilter(poi):
        if poi['id'] == id:
            titleHtml='''
                <strong class="title"><img src="icons/marker_{icon}.png" width="16" alt="" /> {title}</strong><br>
                <i>Kategorie: {category}</i>
            ''' \
            .format(title=poi['name'], icon=id.lower(), category=category)
            if 'screenshots' in poi:

                screenshots = []
                for screenshot in poi['screenshots']:
                    screenshots.append('''
                        <a href="#" data-toggle="modal" data-target="#screenshotModal" data-image="screenshots/{screenshot}"
                                    data-icon="icons/marker_{icon}.png" data-title="{title}" data-description="{description}">
                            <div class="screenshot-container" title="Klicken um herein zu zoomen">
                                <img src="screenshots/{screenshot}" alt="" class="img-thumbnail">
                                <i aria-hidden="true" class="da da-search-plus zoom-icon"></i>
                            </div>
                        </a>
                    '''.format(screenshot=screenshot,title=poi['name'],description=poi['description'],icon=id.lower())
                    )
                else:
                    screenshotContainerHtml = '''
                        <div class="screenshots">
                        {screenshots}
                        </div>
                    '''.format(screenshots="\n".join(screenshots))

                bodyHtml='<p>{description}</p>{screenshots}' \
                .format(description=poi['description'], screenshots=screenshotContainerHtml)
                try:
                    return (poi['name'], titleHtml + bodyHtml)
                except KeyError:
                    return (poi['name'], titleHtml)
            try:
                return (poi['name'], poi['description'])
            except KeyError:
                return (poi['name'], titleHtml)

    return genericFilter
