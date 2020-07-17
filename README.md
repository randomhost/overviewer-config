Random-Host.tv Overviewer
=========================

Table of Contents
-----------------

* [Introduction](#introduction)
* [Disclaimer](#disclaimer)
* [Usage](#usage)
* [Updating Localization Files](#updating-localization-files)
* [License](#license)

Introduction
------------

This is the [Minecraft Overviewer][1] configuration used to render the [Minecraft Map][2]
on [Random-Host.tv][3].

Disclaimer
----------

This configuration is being provided for **reference purposes** and will likely not work on
other Overviewer installations without extensive modifications, especially with regards to hardcoded
file paths and HTML snippets.

**WARNING: Do not use this configuration before you finished customizing it to fit your needs.**

Usage
-----

This section describes the file structure of the package and the purpose of each component.

For general information on how to use Overviewer, please refer to the [Overviewer documentation][4]. 

* `.avatar_cache`  
  This directory holds cached player skin textures retrieved from Mojang's servers by
  `overviewer/avatar.php`. It's only needed when using the included PHP player skin fetcher instead
  of the official one.
  
  **Note:** This directory must be readable and writable by the web server.
  
* `.l10n_cache`  
  This directory holds localization assets retrieved from Mojang's servers by `bin/fetch-localizations.php`.
  
  **Note:** This directory must be readable and writable by the PHP script.

* `bin/overviever`  
  This is a Bash script wrapper for `overviewer.py` which utilized Linux's `nice` command to modify
  the process priority of Overviewer so it doesn't use up all available system resources.
  
  The script renders both tiles and POIs by default. Run `bin/overviever -h` for more options. 
  
* `bin/fetch-localizations.php`  
  This PHP script is used to download the Minecraft localization assets for translating player
  statistics into the chosen language.
  
  **Note:** This script has to be executed after every Minecraft update. See section
  [Updating Localization Files](#updating-localization-files) for more information.
  
* `config/overviewer/filters.py`  
  This file holds the filter functions which contain the logic for building custom POI popups,
  including all the fancy stuff like screenshots, book contents and player statistics.
 
* `config/overviewer/main.py`  
  This is the main configuration file which is loaded by Overviewer. It holds all the configuration
  which has not been extracted into separate files.
  
* `config/overviewer/manualpois.py`  
  All manual points of interest are configured here, including descriptions and screenshots.
  
* `config/overviewer/markers.py`  
  These are the selectable markers shown on the map with their corresponding filter function
  (defined in `filters.py`) which maps the POIs (built-in ones and those defined in `manualpois.py`)
  to their corresponding map overlay.
  
* `overviewer/css/`  
  Custom cascading style sheets for the Overviewer map page, based on Bootstrap 4.
  
* `overviewer/fonts/`  
  Custom IcoMoon font based on FontAwesome 4 for the Overviewer map page.
  
* `overviewer/icons/`  
  Custom marker icons.
  
* `overviewer/images/`  
  Custom images such as the Random-Host.tv logo, player skin background and the screenshots attached
  to the POIs defined in `manualpois.py`.
  
* `overviewer/js/`  
  JavaScript files including Bootstrap 4, jQuery and custom logic for displaying screenshot and
  player stats modals.
  
* `overviewer/index.php`  
  Custom PHP index file which provides more flexibility than the placeholders supported by the
  `customwebassets` config option. 
  
* `overviewer/avatar.php`  
  Custom PHP player skin fetcher.
  
  At the time of writing, this one fixes some of the bugs which the official avatar endpoint at
  `https://overviewer.org/avatar/<playerName>` has while also being a bit faster.

Updating Localization Files
---------------------------

Users who intend on including the "last known player location" special point of interest into their
Overviewer renders **must** execute the included `bin/fetch-localizations.php` script at least once
after **every** Minecraft version change to download localization assets for the corresponding
Minecraft version.

These localization assets must match the used Minecraft version **exactly** or Overviewer may fail
to generate points of interest if any translations were renamed or removed between versions.

**Example for Minecraft release versions**

```bash
php bin/fetch-localizations.php --version 1.16.1
```

**Example for Minecraft snapshot versions**

```bash
php bin/fetch-localizations.php --version 20w06a
```

Downloaded translation assets are stored in the `.l10n_cache` folder. 

License
-------

See LICENSE.txt for full license details.

[1]: https://github.com/overviewer/Minecraft-Overviewer/
[2]: https://random-host.tv/games/minecraft/overviewer/
[3]: https://random-host.tv/
[4]: https://docs.overviewer.org/en/latest/
