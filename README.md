Random-Host.tv Overviewer
=========================

This is the [Minecraft Overviewer][1] configuration used to render the [Minecraft Map][2]
on [Random-Host.tv][3].

Usage
-----

**Note:**  
This configuration is being provided for **reference purposes** and will likely not work on
other Overviewer installations without extensive modifications, especially with regards to hardcoded
file paths and HTML snippets.

**WARNING: Do not use this configuration before you finished customizing it to fit your needs.**

* `.avatar_cache`  
  This directory holds cached player skin textures retrieved from Mojang's servers by
  `overviewer/avatar.php`. It's only needed when using the included PHP player skin fetcher instead
  of the official one.
  
  **Note:** This directory must be readable and writable by the web server.

* `bin/overviever`  
  This is a Bash script wrapper for `overviewer.py` which utilized Linux's `nice` command to modify
  the process priority of Overviewer so it doesn't use up all available system resources.
  
  The script renders both tiles and POIs by default. Run `bin/overviever -h` for more options. 
  
* `config/overviewer/de_de.json`  
  This is a snapshot of Minecraft's language files - German in this case - which is used to
  translate player statistics into human readable strings.
  
  **Note:** This file has to be extracted from Minecraft's `assets` folder after every update. See
  section [Updating Translation Files](#updating-translation-files) for more information.
  
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

Updating Translation Files
--------------------------

The Minecraft client stores resources like language files under a cryptic name and path. To figure
out where to find the corresponding translations for your desired language (e.g. `de_de.json`),
open `C:\Users\<user>\AppData\Roaming\.minecraft\assets\indexes\<version>.json` (assuming you are
playing on Windows) in a text editor and identify the corresponding hash value (e.g.
`"minecraft/lang/de_de.json": {"hash": "a7aee558478697d29ac284e041dbc38dc7804e0e", "size": 292313}`).

Then go to `C:\Users\<user>\AppData\Roaming\.minecraft\assets\objects\`, find the folder which
matches the first 2 letters of the hash (e.g. `a7`) and copy the file which matches the hash value
(e.g. `a7aee558478697d29ac284e041dbc38dc7804e0e`). Finally rename the file back to it's proper
name (e.g. `de_de.json`).

License
-------

See LICENSE.txt for full license details.

[1]: https://github.com/overviewer/Minecraft-Overviewer/
[2]: https://random-host.tv/games/minecraft/overviewer/
[3]: https://random-host.tv/
