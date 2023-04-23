# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4 filetype=python:

####################################################################################################
# Dependencies
####################################################################################################

import sys
sys.path.append('/home/minecraft/config/overviewer/')

global html
global json
global locale
global os
global statsCache
import datetime
import html
import json
import locale
import logging
import os

####################################################################################################
# Load Translations
####################################################################################################

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

translationFilePath= '/home/minecraft/.l10n_cache/de_de.json'
logging.info('Loading translations from \'%s\'', translationFilePath)
if os.path.isfile(translationFilePath):
    with open(translationFilePath, 'r') as translationFile:
        decodedTranslations = json.load(translationFile)
else:
    logging.warning('Failed to load translations from \'%s\'', translationFilePath)
    decodedTranslations={}

####################################################################################################
# Load and cache Player Statistics
####################################################################################################

# Initialize Item Stats Item
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

# Initialize Mob Stats Item
def initMob(stats, key, name):
    if(key not in stats['mobs']['mobs']):
        stats['mobs']['mobs'][key] = {
            'name': name,
            'actions': {
                'killed': 0,
                'killed_by': 0
            }
        }

# Format Distance
def formatDistance(value):
    if(value < 100):
        return formatFloatAsString(value) + ' cm'

    if(value < 100000):
        value = round(value/100, 2)
        return formatFloatAsString(value) + ' m'

    value = round(value/100000, 2)
    return formatFloatAsString(value) + ' km'

# Format Time
def formatTime(value):
    time = str(datetime.timedelta(seconds=value))
    time = time.replace('days', 'Tage')
    time = time.replace('day', 'Tag')

    return time

# Format Time ago
def formatTimeAgo(value):
    timeAgo = str(datetime.timedelta(seconds=value))
    timeAgo = timeAgo.replace('days', 'Tagen')
    timeAgo = timeAgo.replace('day', 'Tag')

    return 'vor ' + timeAgo

# Format Float
def formatFloat(value):
    return formatFloatAsString(value / 10)

# Format Float String
def formatFloatAsString(value):
    return locale.format('%.2f', value, True)

# Format Int String
def formatIntAsString(value):
    return locale.format('%.0f', value, True)

# Format General Statistics
def formatGeneralStats(key, value):
    formatMappings = {
        # Distance
        'minecraft:aviate_one_cm': formatDistance,
        'minecraft:boat_one_cm': formatDistance,
        'minecraft:climb_one_cm': formatDistance,
        'minecraft:crouch_one_cm': formatDistance,
        'minecraft:fall_one_cm': formatDistance,
        'minecraft:fly_one_cm': formatDistance,
        'minecraft:horse_one_cm': formatDistance,
        'minecraft:minecart_one_cm': formatDistance,
        'minecraft:pig_one_cm': formatDistance,
        'minecraft:sprint_one_cm': formatDistance,
        'minecraft:swim_one_cm': formatDistance,
        'minecraft:walk_on_water_one_cm': formatDistance,
        'minecraft:walk_one_cm': formatDistance,
        'minecraft:walk_under_water_one_cm': formatDistance,

        # Time
        'minecraft:play_time': formatTime,
        'minecraft:sneak_time': formatTime,

        # Time ago
        'minecraft:time_since_death': formatTimeAgo,
        'minecraft:time_since_rest': formatTimeAgo,

        # Float
        'minecraft:damage_absorbed': formatFloat,
        'minecraft:damage_blocked_by_shield': formatFloat,
        'minecraft:damage_dealt': formatFloat,
        'minecraft:damage_dealt_absorbed': formatFloat,
        'minecraft:damage_dealt_resisted': formatFloat,
        'minecraft:damage_resisted': formatFloat,
        'minecraft:damage_taken': formatFloat,

        # Integer
        #'minecraft:animals_bred':,
        #'minecraft:bell_ring':,
        #'minecraft:clean_armor':,
        #'minecraft:clean_banner':,
        #'minecraft:clean_shulker_box':,
        #'minecraft:deaths':,
        #'minecraft:drop':,
        #'minecraft:eat_cake_slice':,
        #'minecraft:enchant_item':,
        #'minecraft:fill_cauldron':,
        #'minecraft:fish_caught':,
        #'minecraft:inspect_dispenser':,
        #'minecraft:inspect_dropper':,
        #'minecraft:inspect_hopper':,
        #'minecraft:interact_with_beacon':,
        #'minecraft:interact_with_blast_furnace':,
        #'minecraft:interact_with_brewingstand':,
        #'minecraft:interact_with_campfire':,
        #'minecraft:interact_with_cartography_table':,
        #'minecraft:interact_with_crafting_table':,
        #'minecraft:interact_with_furnace':,
        #'minecraft:interact_with_lectern':,
        #'minecraft:interact_with_loom':,
        #'minecraft:interact_with_smoker':,
        #'minecraft:interact_with_stonecutter':,
        #'minecraft:jump':,
        #'minecraft:junk_fished':,
        #'minecraft:leave_game':,
        #'minecraft:mob_kills':,
        #'minecraft:open_barrel':,
        #'minecraft:open_chest':,
        #'minecraft:open_enderchest':,
        #'minecraft:open_shulker_box':,
        #'minecraft:play_noteblock':,
        #'minecraft:play_record':,
        #'minecraft:player_kills':,
        #'minecraft:pot_flower':,
        #'minecraft:raid_trigger':,
        #'minecraft:raid_win':,
        #'minecraft:ring_bell':,
        #'minecraft:sleep_in_bed':,
        #'minecraft:talked_to_villager':,
        #'minecraft:traded_with_villager':,
        #'minecraft:treasure_fished':,
        #'minecraft:trigger_trapped_chest':,
        #'minecraft:tune_noteblock':,
        #'minecraft:use_cauldron':,
    }

    func = formatMappings.get(key, lambda value: formatIntAsString(value))

    return func(value)

statsCache = {}
def loadPlayerStats(poi):
    if(poi['uuid'] in statsCache):
        return statsCache[poi['uuid']]

    # load player stats
    statsFilePath= '/home/minecraft/vanilla/worldstorage/randomhost/stats/%s.json' % poi['uuid']
    logging.info('Loading player stats for \'%s\' from \'%s\'', poi['EntityId'], statsFilePath)
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
                        try:
                            translationKey='stat.' + key.replace(':', '.')
                            translation=decodedTranslations[translationKey]
                        except KeyError:
                            translationKey='stat.' + key.replace(':', '.')
                            translation=translationKey
                        sortKey=translation + '_' + translationKey

                        stats['general']['actions'][sortKey] = {
                            'name': translation,
                            'value': formatGeneralStats(key, decodedStats['stats']['minecraft:custom'][key])
                        }

                # item stats: mined
                if 'minecraft:mined' in decodedStats['stats']:
                    for key in decodedStats['stats']['minecraft:mined']:
                        translationKey='block.' + key.replace(':', '.')
                        translation=decodedTranslations[translationKey]
                        sortKey=translation + '_' + translationKey
                        initItem(stats, sortKey, translation)

                        stats['items']['items'][sortKey]['actions']['mined'] = decodedStats['stats']['minecraft:mined'][key]

                # item stats: broken
                if 'minecraft:broken' in decodedStats['stats']:
                    for key in decodedStats['stats']['minecraft:broken']:
                        translationKey='item.' + key.replace(':', '.')
                        translation=decodedTranslations[translationKey]
                        sortKey=translation + '_' + translationKey
                        initItem(stats, sortKey, translation)

                        stats['items']['items'][sortKey]['actions']['broken'] = decodedStats['stats']['minecraft:broken'][key]

                # item stats: crafted
                if 'minecraft:crafted' in decodedStats['stats']:
                    for key in decodedStats['stats']['minecraft:crafted']:
                        try:
                            translationKey='block.' + key.replace(':', '.')
                            translation=decodedTranslations[translationKey]
                        except KeyError:
                            translationKey='item.' + key.replace(':', '.')
                            translation=decodedTranslations[translationKey]
                        sortKey=translation + '_' + translationKey
                        initItem(stats, sortKey, translation)

                        stats['items']['items'][sortKey]['actions']['crafted'] = decodedStats['stats']['minecraft:crafted'][key]

                # item stats: used
                if 'minecraft:used' in decodedStats['stats']:
                    for key in decodedStats['stats']['minecraft:used']:
                        try:
                            translationKey='block.' + key.replace(':', '.')
                            translation=decodedTranslations[translationKey]
                        except KeyError:
                            try:
                                translationKey='item.' + key.replace(':', '.')
                                translation=decodedTranslations[translationKey]
                            except KeyError:
                                translationKey='item.' + key.replace(':', '.')
                                translation=translationKey
                        sortKey=translation + '_' + translationKey
                        initItem(stats, sortKey, translation)

                        stats['items']['items'][sortKey]['actions']['used'] = decodedStats['stats']['minecraft:used'][key]

                # item stats: picked up
                if 'minecraft:picked_up' in decodedStats['stats']:
                    for key in decodedStats['stats']['minecraft:picked_up']:
                        try:
                            translationKey='block.' + key.replace(':', '.')
                            translation=decodedTranslations[translationKey]
                        except KeyError:
                            translationKey='item.' + key.replace(':', '.')
                            translation=decodedTranslations[translationKey]
                        sortKey=translation + '_' + translationKey
                        initItem(stats, sortKey, translation)

                        stats['items']['items'][sortKey]['actions']['picked_up'] = decodedStats['stats']['minecraft:picked_up'][key]

                # item stats: dropped
                if 'minecraft:dropped' in decodedStats['stats']:
                    for key in decodedStats['stats']['minecraft:dropped']:
                        try:
                            translationKey='block.' + key.replace(':', '.')
                            translation=decodedTranslations[translationKey]
                        except KeyError:
                            translationKey='item.' + key.replace(':', '.')
                            translation=decodedTranslations[translationKey]
                        sortKey=translation + '_' + translationKey
                        initItem(stats, sortKey, translation)

                        stats['items']['items'][sortKey]['actions']['dropped'] = decodedStats['stats']['minecraft:dropped'][key]

                # mob stats: killed
                if 'minecraft:killed' in decodedStats['stats']:
                    for key in decodedStats['stats']['minecraft:killed']:
                        translationKey='entity.' + key.replace(':', '.')
                        translation=decodedTranslations[translationKey]
                        sortKey=translation + '_' + translationKey
                        initMob(stats, sortKey, translation)

                        stats['mobs']['mobs'][sortKey]['actions']['killed'] = decodedStats['stats']['minecraft:killed'][key]

                # mob stats: killed by
                if 'minecraft:killed_by' in decodedStats['stats']:
                    for key in decodedStats['stats']['minecraft:killed_by']:
                        translationKey='entity.' + key.replace(':', '.')
                        translation=decodedTranslations[translationKey]
                        sortKey=translation + '_' + translationKey
                        initMob(stats, sortKey, translation)

                        stats['mobs']['mobs'][sortKey]['actions']['killed_by'] = decodedStats['stats']['minecraft:killed_by'][key]
            else:
                stats={}
    else:
        stats={}

    statsCache[poi['uuid']] = stats

    return stats

####################################################################################################
# Filters
####################################################################################################

def playerFilter(poi):
    if poi['id'] == 'Player':
        #poi['icon'] = 'https://overviewer.org/avatar/%s' % poi['EntityId']
        #tooltipIcon = 'https://overviewer.org/avatar/%s/head' % poi['EntityId']
        poi['icon'] = 'https://random-host.tv/games/minecraft/overviewer/avatar/%s/body' % poi['EntityId']
        tooltipIcon = 'https://random-host.tv/games/minecraft/overviewer/avatar/%s/head' % poi['EntityId']

        stats=loadPlayerStats(poi)

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
                        <a href="#" data-toggle="modal" data-target="#screenshotModal" data-image="{screenshot}" data-images="{screenshots}"
                                    data-icon="icons/marker_{icon}.png" data-title="{title}" data-description="{description}">
                            <div class="screenshot-container" title="Klicken um herein zu zoomen">
                                <img src="images/screenshots/{screenshot}" alt="" class="img-thumbnail">
                                <i aria-hidden="true" class="da da-search-plus zoom-icon"></i>
                            </div>
                        </a>
                    '''.format(screenshot=screenshot,title=html.escape(poi['name']),description=html.escape(poi['description']),icon=id.lower(),screenshots=html.escape(json.dumps(poi['screenshots'])))
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
