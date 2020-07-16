<?php

namespace RandomHost\Minecraft\Overviewer;

use DateTime;
use Exception;
use RuntimeException;
use stdClass;

/**
 * Retrieves localization assets from Mojang.
 *
 * @author    Ch'Ih-Yu <chi-yu@web.de>
 * @copyright 2020 Random-Host.tv
 * @license   https://opensource.org/licenses/BSD-3-Clause BSD License (3 Clause)
 * @link      https://random-host.tv
 */
class L10n
{
    /**
     * URL to download the "version_manifest.json" file from.
     */
    const VERSION_MANIFEST_URL = 'https://launchermeta.mojang.com/mc/game/version_manifest.json';

    /**
     * Path prefix for identifying localization file assets.
     */
    const L10N_ASSET_FILE_PREFIX = 'minecraft/lang/';

    /**
     * Pattern for asset file download URLs.
     */
    const ASSET_URL_PATTERN = 'https://resources.download.minecraft.net/%s/%s';

    /**
     * Local directory for caching language assets.
     */
    const LOCALIZATION_CACHE_DIR = __DIR__.'/../.l10n_cache';

    /**
     * Decoded version manifest data.
     *
     * @var stdClass
     */
    private $versionManifest;

    /**
     * Decoded version data.
     *
     * @var stdClass
     */
    private $versionData;

    /**
     * Decoded asset index.
     *
     * @var stdClass
     */
    private $assetIndex;

    /**
     * Minecraft version.
     *
     * @var string
     */
    private $version;

    /**
     * - Download asset file from http://resources.download.minecraft.net/ (e.g. http://resources.download.minecraft.net/d5/d5ac095a840888885e98927079a94b515f742c21).
     */
    public function run()
    {
        try {
            $this
                ->parseCmdLineOptions()
                ->checkCacheDir()
                ->loadVersionManifest()
                ->loadVersionData()
                ->loadAssetIndex()
                ->downloadLocalizationAssets();

            $this->status('Done.');

            exit(0);
        } catch (Exception $e) {
            $this->status('', true, false);
            $this->status(sprintf('Error: %s', $e->getMessage()));
            exit(1);
        }
    }

    private function parseCmdLineOptions(): self
    {
        $shortOpts = 'hv:';
        $longOpts = ['help', 'version:'];

        $options = getopt($shortOpts, $longOpts);

        if (empty($options)
            || array_key_exists('h', $options)
            || array_key_exists('help', $options)
        ) {
            $this->printUsageHint(true);
            exit(0);
        }

        switch (true) {
            case array_key_exists('version', $options):
                $version = $options['version'];
                break;
            case array_key_exists('v', $options):
                $version = $options['v'];
                break;
            default:
                $this->printUsageHint();
                exit(1);
        }

        if (!preg_match('#^(\d+\.)?(\d+\.)?(\d+)$#', $version)
            && !preg_match('#^\d+w\d+a$#', $version)) {
            $this->status("Invalid version number \"{$version}\"", true, false);
            $this->printUsageHint();
            exit(1);
        }

        $this->status("Minecraft version: {$version}");

        $this->version = $version;

        return $this;
    }

    /**
     * Checks whether the cache directory for l10n files exists.
     *
     * @return $this
     *
     * @throws RuntimeException in case the cache directory does not exist or is not accessible.
     */
    private function checkCacheDir(): self
    {
        $this->status('Checking cache directory... ', false);

        if (!is_dir(self::LOCALIZATION_CACHE_DIR)
            || !is_writable(self::LOCALIZATION_CACHE_DIR)
            || !is_readable(self::LOCALIZATION_CACHE_DIR)
        ) {
            throw new RuntimeException(
                'Localization cache directory "'.self::LOCALIZATION_CACHE_DIR.'" not found or not accessible'
            );
        }

        $this->status('ok.', true, false);

        return $this;
    }

    /**
     * Loads the version manifest from Mojang.
     *
     * @return $this
     */
    private function loadVersionManifest(): self
    {
        $this->status('Loading version manifest... ', false);

        $versionManifest = file_get_contents(self::VERSION_MANIFEST_URL);
        if (false === $versionManifest) {
            throw new RuntimeException('Failed to fetch version manifest from Mojang');
        }

        $versionManifest = json_decode($versionManifest);
        if (is_null($versionManifest)) {
            throw new RuntimeException('Failed to decode version manifest');
        }

        if (!property_exists($versionManifest, 'versions')) {
            throw new RuntimeException('Version manifest doesn\'t include any versions');
        }

        $this->versionManifest = $versionManifest;

        $this->status('ok.', true, false);

        return $this;
    }

    /**
     * Loads version data for the given version from Mojang.
     *
     * @return $this
     */
    private function loadVersionData(): self
    {
        $this->status('Loading version data... ', false);

        foreach ($this->versionManifest->versions as $versionData) {
            if (!property_exists($versionData, 'id')) {
                throw new RuntimeException('Version data doesn\'t include "id" key');
            }
            if (!property_exists($versionData, 'url')) {
                throw new RuntimeException('Version data doesn\'t include "url" key');
            }

            if ($versionData->id === $this->version) {
                $url = $versionData->url;
                break;
            }
        }

        if (!isset($url)) {
            throw new RuntimeException("Version \"{$this->version}\"not found in version manifest");
        }

        $versionData = file_get_contents($url);
        if (false === $versionData) {
            throw new RuntimeException('Failed to fetch version data from Mojang');
        }

        $versionData = json_decode($versionData);
        if (is_null($versionData)) {
            throw new RuntimeException('Failed to decode version data');
        }

        if (!property_exists($versionData, 'assetIndex')) {
            throw new RuntimeException('Version data doesn\'t include "assetIndex" key');
        }

        if (!property_exists($versionData->assetIndex, 'url')) {
            throw new RuntimeException('Asset index data doesn\'t include "url" key');
        }

        $this->versionData = $versionData;

        $this->status('ok.', true, false);

        return $this;
    }

    /**
     * Loads the asset index from Mojang.
     *
     * @return $this
     */
    private function loadAssetIndex(): self
    {
        $this->status('Loading asset index... ', false);

        $assetIndex = file_get_contents($this->versionData->assetIndex->url);
        if (false === $assetIndex) {
            throw new RuntimeException('Failed to fetch asset index from Mojang');
        }

        $assetIndex = json_decode($assetIndex);
        if (is_null($assetIndex)) {
            throw new RuntimeException('Failed to decode asset index data');
        }

        if (!property_exists($assetIndex, 'objects')) {
            throw new RuntimeException('Asset index doesn\'t include "objects" key');
        }

        $this->assetIndex = $assetIndex;

        $this->status('ok.', true, false);

        return $this;
    }

    /**
     * Downloads localization assets from Mojang.
     *
     * @return $this
     */
    private function downloadLocalizationAssets(): self
    {
        $this->status('Downloading localization assets.');

        foreach ($this->assetIndex->objects as $name => $object) {
            $l10nPathPrefix = self::L10N_ASSET_FILE_PREFIX;
            if ($l10nPathPrefix !== substr($name, 0, strlen($l10nPathPrefix))) {
                continue;
            }

            $fileName = substr($name, strlen($l10nPathPrefix));
            $langCacheFile = self::LOCALIZATION_CACHE_DIR.'/'.$fileName;

            $fileUrl = sprintf(self::ASSET_URL_PATTERN, substr($object->hash, 0, 2), $object->hash);

            $this->status(sprintf('- Downloading language "%s"... ', substr($fileName, 0, -5)), false);

            $langFile = file_get_contents($fileUrl);
            if (false === $langFile) {
                throw new RuntimeException("Failed to fetch asset \"{$fileUrl}\" from Mojang");
            }

            if (false === file_put_contents($langCacheFile, $langFile)) {
                throw new RuntimeException('Failed to save downloaded asset to disk');
            }

            $this->status('ok.', true, false);
        }

        return $this;
    }

    /**
     * Outputs a status message.
     *
     * @param string $message   Message string.
     * @param bool   $linebreak Optional: Whether to append a linebreak. Default: true
     * @param bool   $timestamp Optional: Whether to prepend a timestamp. Default: true
     *
     * @return $this
     */
    private function status(string $message, bool $linebreak = true, bool $timestamp = true): self
    {
        $dateTime = new DateTime();

        echo sprintf(
            '%s%s%s',
            $timestamp ? $dateTime->format('[Y-m-d H:i:s] ') : '',
            $message,
            $linebreak ? PHP_EOL : ''
        );

        return $this;
    }

    /**
     * Outputs usage information about this script.
     *
     * @param bool $withIntro Includes an introduction snippet.
     */
    private function printUsageHint(bool $withIntro = false)
    {
        $fileName = basename(__FILE__);
        $output = '';
        if($withIntro) {
            $output .= <<< EOT
This script downloads Minecraft localization assets from Mojang, ready to be used to localize
player statistics shown within Minecraft Overviewer's "last known player location" type POIs.


EOT;
        }

        $output .= <<< EOT
Usage: {$fileName} [OPTIONS] --version=<version>

Options
-h, --help              Shows this help.
-v, --version=<version> Specifies the Minecraft release version or snapshot name to download
                        translation assets for (e.g. "1.15", "1.16.1", "20w06a", etc.).
EOT;
        $this->status($output, true, false);
    }
}

$penis = new L10n();
$penis->run();
