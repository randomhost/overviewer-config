<?php
setlocale(LC_TIME, 'de_DE.UTF-8');
$indexFile = 'index.html';
$update = 0;
if(file_exists($indexFile)) {
    $update = filemtime($indexFile);
}
?>
<!DOCTYPE html>
<html lang="de">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no"/>
    <title>Minecraft Map - Random-Host.tv</title>
    <link rel="stylesheet" type="text/css" href="leaflet.css">
    <link rel="stylesheet" type="text/css" href="overviewer.css">
    <link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="css/custom.min.css">
    <link rel="stylesheet" type="text/css" href="css/dingawesome.min.css">
</head>

<body onload="overviewer.util.initialize()">

<header>
    <nav class="navbar navbar-expand-sm navbar-dark bg-dark">
        <a class="navbar-brand mr-auto" href="/">
            <img src="images/logo.png" class="d-inline-block align-top" width="32" height="32" alt="">&nbsp;Random-Host.tv
            <small class="ml-3"><i class="da da-map" aria-hidden="true"></i> Minecraft Map</small>
        </a>
        <div class="navbar-nav">
            <span class="navbar-text">
                <i class="da da-clock-o" aria-hidden="true"></i>
                Stand: <?= strftime("%A %d.%m.%Y, %H:%M:%S", $update) ?>
            </span>
            <a class="btn btn-secondary ml-2" title="Mehr über diese Karte erfahren" href="#" data-toggle="modal" data-target="#infoModal">
                <i class="da da-info-circle" aria-hidden="true"></i>
                <span class="sr-only">Mehr über diese Karte erfahren</span>
            </a>
        </div>
    </nav>
</header>

<div id="NoJSWarning" class="alert alert-warning">
    <strong>Mist!</strong> Beim Laden der Karte ist etwas schief gelaufen.
</div>

<a class="btn btn-dark" id="refresh-button" href="javascript:location.reload();">
    <i class="da da-refresh" aria-hidden="true"></i>
    Aktualisieren
</a>

<div id="mcmap"></div>

<div class="modal fade" id="screenshotModal" tabindex="-1" role="dialog"
     aria-labelledby="screenshotModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="screenshotModalLabel">
                    <img src="icons/marker_location.png" alt="" id="screenshot-icon">
                    <span id="screenshot-title">Screenshot</span>
                </h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <figure class="figure">
                    <img id="screenshot-image" src="images/logo.png" alt="" class="figure-img img-fluid rounded">
                    <figcaption class="figure-caption" id="screenshot-description"></figcaption>
                </figure>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">
                    <i class="da da-close" aria-hidden="true"></i>
                    Schließen
                </button>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="statsModal" tabindex="-1" role="dialog"
     aria-labelledby="statsModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="statsModalLabel">
                    <img src="icons/marker_player.png" alt="" id="stats-icon">
                    Spieler Statistik für &bdquo;<span id="stats-title"></span>&ldquo;
                </h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <ul class="nav nav-tabs" id="myTab" role="tablist">
                    <li class="nav-item" role="presentation">
                        <a class="nav-link active" id="stats-general-tab" data-toggle="tab" href="#stats-general" role="tab" aria-controls="stats-general" aria-selected="true">
                            <i class="da da-bar-chart" aria-hidden="true"></i>
                            Allgemein
                        </a>
                    </li>
                    <li class="nav-item" role="presentation">
                        <a class="nav-link" id="stats-items-tab" data-toggle="tab" href="#stats-items" role="tab" aria-controls="stats-items" aria-selected="false">
                            <i class="da da-diamond" aria-hidden="true"></i>
                            Gegenstände
                        </a>
                    </li>
                    <li class="nav-item" role="presentation">
                        <a class="nav-link" id="stats-mobs-tab" data-toggle="tab" href="#stats-mobs" role="tab" aria-controls="stats-mobs" aria-selected="false">
                            <i class="da da-paw" aria-hidden="true"></i>
                            Kreaturen
                        </a>
                    </li>
                </ul>
                <div class="tab-content" id="myTabContent">
                    <div class="tab-pane fade show active" id="stats-general" role="tabpanel" aria-labelledby="stats-general-tab">
                        <table class="table table-sm table-striped">
                            <thead></thead>
                            <tbody>
                            <tr>
                                <td class="text-center">
                                    <i class="da da-spinner da-spin" aria-hidden="true"></i> Lade...
                                </td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="tab-pane fade" id="stats-items" role="tabpanel" aria-labelledby="stats-items-tab">
                        <table class="table table-sm table-striped">
                            <thead></thead>
                            <tbody>
                            <tr>
                                <td class="text-center">
                                    <i class="da da-spinner da-spin" aria-hidden="true"></i> Lade...
                                </td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="tab-pane fade" id="stats-mobs" role="tabpanel" aria-labelledby="stats-mobs-tab">
                        <table class="table table-sm table-striped">
                            <thead></thead>
                            <tbody>
                            <tr>
                                <td class="text-center">
                                    <i class="da da-spinner da-spin" aria-hidden="true"></i> Lade...
                                </td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">
                    <i class="da da-close" aria-hidden="true"></i>
                    Schließen
                </button>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="infoModal" tabindex="-1" role="dialog"
     aria-labelledby="infoModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="infoModalLabel">
                    <i class="da da-info-circle" aria-hidden="true"></i>
                    Über diese Karte
                </h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <p>
                    Diese Karte wurde mit Hilfe von
                    <a href="https://overviewer.org/" class="text-nowrap" target="_blank"><i class="da da-external-link" aria-hidden="true"></i> Minecraft Overviewer</a>,
                    einer kostenlosen <strong>Open Source</strong> Software deren Quellcode frei auf
                    <a href="https://github.com/overviewer/Minecraft-Overviewer/" class="text-nowrap" target="_blank"><i class="da da-github" aria-hidden="true"></i> GitHub</a>
                    verfügbar ist, aus der Minecraft Welt des
                    <a href="https://random-host.tv" class="text-nowrap" target="_blank"><i class="da da-external-link" aria-hidden="true"></i> Random-Host.tv</a>
                    Servers generiert.
                </p>
                <p>
                    Ganz im Sinne des <strong>Open Source</strong> Gedankens stellen wir die
                    Konfigurationsdateien und selbst geschriebenen Scripte welche wir zur Bereitstellung
                    der Karte einsetzen ebenfalls unter einer
                    <a href="https://github.com/randomhost/overviewer-config/blob/master/LICENSE.txt" class="text-nowrap" target="_blank"><i class="da da-balance-scale" aria-hidden="true"></i> Open Source Lizenz</a>
                    auf
                    <a href="https://github.com/randomhost/overviewer-config" class="text-nowrap" target="_blank"><i class="da da-github" aria-hidden="true"></i> GitHub</a>
                    zur Verfügung.
                </p>
                <p class="alert alert-info">
                    <strong>Hinweis:</strong><br>
                    Bitte beachte dass unsere Konfigurationsdateien nur zu Anschauungszwecken dienen
                    und nicht ohne Anpassungen auf anderen Minecraft Servern funktionieren werden.
                </p>
                <p>
                    <a href="https://github.com/randomhost/overviewer-config" class="btn btn-primary" target="_blank">
                        <i class="da da-github" aria-hidden="true"></i> GitHub Projekt
                    </a>
                </p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">
                    <i class="da da-close" aria-hidden="true"></i>
                    Schließen
                </button>
            </div>
        </div>
    </div>
</div>

<script type="text/javascript" src="js/jquery.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/custom.min.js"></script>

<script type="text/javascript" src="overviewerConfig.js"></script>
<script type="text/javascript" src="overviewer.js"></script>
<script type="text/javascript" src="baseMarkers.js"></script>
<script type="text/javascript" src="leaflet.js"></script>

</body>
</html>
