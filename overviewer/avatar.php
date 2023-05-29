<?php

namespace RandomHost\Minecraft\Overviewer;

use BadMethodCallException;
use Exception;
use Memcached;
use OutOfBoundsException;
use RuntimeException;

/**
 * Retrieves a player's Minecraft skin from Mojang and renders it as a 2D avatar.
 *
 * This class is designed to be used with Minecraft Overviewer as self-hosted alternative to the
 * official Overviewer "avatar.py" endpoint at "https://overviewer.org/avatar/".
 *
 * @see       http://docs.overviewer.org/en/latest/signs/#special-pois
 *
 * @author    Ch'Ih-Yu <chi-yu@web.de>
 * @copyright 2023 Random-Host.tv
 * @license   https://opensource.org/licenses/BSD-3-Clause BSD License (3 Clause)
 *
 * @see      https://random-host.tv
 */
class Avatar
{
    /**
     * Default Minecraft player skin URL.
     */
    private const DEFAULT_PLAYER_SKIN_URL = 'https://assets.mojang.com/SkinTemplates/steve.png';

    /**
     * Renders a full front view of the player's body.
     */
    private const TYPE_BODY = 'body';

    /**
     * Renders a 16x16 pixel front view of the player's head.
     */
    private const TYPE_HEAD = 'head';

    /**
     * Renders a 64x64 pixel front view of the player's head.
     */
    private const TYPE_HEAD_BIG = 'bighead';

    /**
     * Valid avatar types.
     */
    private const VALID_TYPES = [self::TYPE_BODY, self::TYPE_HEAD, self::TYPE_HEAD_BIG];

    /**
     * Directory for caching player skin textures.
     */
    private const TEXTURE_CACHE_DIR = __DIR__.'/../.avatar_cache';

    /**
     * Number of seconds player skin textures should be cached.
     */
    private const TEXTURE_CACHE_TIME = 3600;

    /**
     * Number of seconds player skin data (except textures) should be cached.
     */
    private const DATA_CACHE_TIME = 3600;

    /**
     * Memcached instance.
     *
     * @var null|Memcached
     */
    private $memcached;

    /**
     * Avatar constructor.
     *
     * @param null|Memcached $memcached Optional: Memcached instance.
     */
    public function __construct(Memcached $memcached = null)
    {
        $this->memcached = $memcached;
    }

    /**
     * Runs the class.
     */
    public function run()
    {
        try {
            if (!is_dir(self::TEXTURE_CACHE_DIR)
                || !is_writable(self::TEXTURE_CACHE_DIR)
                || !is_readable(self::TEXTURE_CACHE_DIR)
            ) {
                throw new RuntimeException(
                    'Texture cache directory '.self::TEXTURE_CACHE_DIR.' not found or not accessible'
                );
            }

            if (empty($_REQUEST['player'])) {
                throw new BadMethodCallException('Missing required parameter "player"');
            }

            $type = Avatar::TYPE_BODY;
            if (!empty($_REQUEST['type'])) {
                $type = $_REQUEST['type'];
            }

            if (!in_array($type, Avatar::VALID_TYPES)) {
                throw new OutOfBoundsException('Avatar type not implemented');
            }

            $this->getAvatar($type, $_REQUEST['player']);

            exit(0);
        } catch (BadMethodCallException|OutOfBoundsException $e) {
            http_response_code(400);

            exit(1);
        } catch (Exception $e) {
            http_response_code(503);
            trigger_error($e->getMessage(), E_USER_WARNING);

            exit(1);
        }
    }

    /**
     * Returns an avatar image for the given type and player name.
     *
     * @param string $type       Type of avatar image to generate.
     * @param string $playerName Minecraft player name.
     */
    private function getAvatar(string $type, string $playerName)
    {
        try {
            $skinData = $this->getFromMinecraft($playerName);

            switch ($type) {
                case self::TYPE_BODY:
                    $avatar = $this->createAvatarFromTexture($skinData['skin'], $skinData['alpha'], $skinData['slim']);

                    break;

                case self::TYPE_HEAD:
                    $avatar = $this->createHeadFromTextureWithSize($skinData['skin'], $skinData['alpha'], 16, 16);

                    break;

                case self::TYPE_HEAD_BIG:
                    $avatar = $this->createHeadFromTextureWithSize($skinData['skin'], $skinData['alpha'], 64, 64);

                    break;

                default:
                    throw new OutOfBoundsException('Avatar type not implemented');
            }

            header('Content-Type: image/png');
            imagepng($avatar);
            imagedestroy($avatar);
        } catch (Exception $e) {
            http_response_code(503);

            exit(1);
        }
    }

    /**
     * Returns a skin resource and skin metadata for the given player name.
     *
     * @param string $playerName Minecraft player name.
     *
     * @throws Exception
     */
    private function getFromMinecraft(string $playerName): array
    {
        try {
            $uuid = $this->getUuid($playerName);
            $skinData = $this->getSkinData($uuid);
            $skinURL = $skinData['url'];
            $skinSlim = $skinData['slim'];
        } catch (Exception $e) {
            $uuid = 'na';
            $skinURL = self::DEFAULT_PLAYER_SKIN_URL;
            $skinSlim = false;
        }

        $cachePath = self::TEXTURE_CACHE_DIR.DIRECTORY_SEPARATOR.$uuid;
        if (!file_exists($cachePath) || (self::TEXTURE_CACHE_TIME <= time() - filemtime($cachePath))) {
            file_put_contents($cachePath, file_get_contents($skinURL));
        }

        $imageData = imagecreatefrompng($cachePath);
        if (false === $imageData) {
            throw new RuntimeException('Failed to retrieve skin texture');
        }

        $rgba = imagecolorat($imageData, 0, 0);
        $alpha = ($rgba & 0x7F000000) >> 24;

        return [
            'skin' => $imageData,
            'slim' => $skinSlim,
            'alpha' => $alpha,
        ];
    }

    /**
     * Returns the UUID of the given Minecraft player name.
     *
     * @param string $playerName Minecraft player name.
     *
     * @throws Exception
     */
    private function getUuid(string $playerName): string
    {
        $uuid = $this->readFromCache(__METHOD__, $playerName);
        if (!is_null($uuid)) {
            return $uuid;
        }

        $response = file_get_contents(
            sprintf(
                'https://api.mojang.com/users/profiles/minecraft/%s',
                urlencode($playerName)
            )
        );
        if (false !== $response) {
            $data = json_decode($response, true);
            if (!is_null($data)) {
                $this->writeToCache(__METHOD__, $playerName, $data['id']);

                return $data['id'];
            }
        }

        throw new RuntimeException('Failed to retrieve UUID');
    }

    /**
     * Returns skin data for the given player UUID.
     *
     * @param string $uuid Player UUID.
     *
     * @throws Exception
     */
    private function getSkinData(string $uuid): array
    {
        $skinData = $this->readFromCache(__METHOD__, $uuid);
        if (!is_null($skinData)) {
            return $skinData;
        }

        $skinData = [
            'url' => '',
            'slim' => false,
        ];

        $response = file_get_contents(sprintf('https://sessionserver.mojang.com/session/minecraft/profile/%s', $uuid));
        if (false === $response) {
            throw new RuntimeException('Failed to retrieve skin data');
        }

        $profile = json_decode($response, true);
        $properties = $profile['properties'];
        $textures = array_filter(
            $properties,
            function ($obj) {
                return 'textures' == $obj['name'];
            }
        );

        $textures = array_pop($textures);
        $textures = base64_decode($textures['value']);
        $textures = json_decode($textures, true);

        if (!array_key_exists('SKIN', $textures['textures'])) {
            throw new RuntimeException("Given UUID doesn't use a custom skin");
        }

        $skinData['url'] = $textures['textures']['SKIN']['url'];

        if (array_key_exists('metadata', $textures['textures']['SKIN'])) {
            $skinData['slim'] = ('slim' == $textures['textures']['SKIN']['metadata']['model']);
        }

        $this->writeToCache(__METHOD__, $uuid, $skinData);

        return $skinData;
    }

    /**
     * Pastes the given section of the source image into the destination image and returns the updated resource.
     *
     * @param resource $dst       Destination image.
     * @param resource $src       Source image.
     * @param int      $dstX      Destination X coordinate.
     * @param int      $dstY      Destination X coordinate.
     * @param int      $srcX      Source X coordinate.
     * @param int      $srcY      Source Y coordinate.
     * @param int      $srcWidth  Source width.
     * @param int      $srcHeight Source height.
     *
     * @return resource
     *
     * @throws Exception
     */
    private function paste($dst, $src, int $dstX, int $dstY, int $srcX, int $srcY, int $srcWidth, int $srcHeight)
    {
        if (false === imagecopy($dst, $src, $dstX, $dstY, $srcX, $srcY, $srcWidth, $srcHeight)) {
            throw new RuntimeException('Failed to copy texture');
        }

        return $dst;
    }

    /**
     * Creates an avatar image from the given texture resource.
     *
     * @param resource $texture  Texture resource.
     * @param bool     $hasAlpha Whether the texture uses an alpha channel.
     * @param bool     $slim     Whether the texture uses the slim player model.
     *
     * @return false|resource
     */
    private function createAvatarFromTexture($texture, bool $hasAlpha, bool $slim)
    {
        $avatar = imagecreatetruecolor($slim ? 14 : 16, 32);
        imagesavealpha($avatar, true);
        $color = imagecolorallocatealpha($avatar, 0, 0, 0, 127);
        imagefill($avatar, 0, 0, $color);
        if (false === $avatar) {
            throw new RuntimeException('Failed to create avatar image');
        }

        $isLegacySkin = (imagesy($texture) <= 32);

        /**
         * IMPORTANT:
         * When reading the following coordinates, please remember that "left" and "right" refer to
         * the player's ego perspective.
         *
         * The render order is reversed since from our "front view" perspective, we have to render
         * the model from "right to left". If we wanted to render the "back view", the order would
         * be "left to right" accordingly.
         */
        switch (true) {
            /*
             * Pre Minecraft 1.8 "legacy" skin:
             *  - head
             *  - hat
             *  - body
             *  - shared leg texture for both left and right leg
             *  - shared arm texture for both left and right arm
             *  - no armor layer except head/hat
             */
            case $isLegacySkin:
                $pastes = [
                    // body layer
                    [4, 0, 8, 8, 8, 8], // head
                    [4, 8, 20, 20, 8, 12], // body
                    [0, 8, 44, 20, 4, 12], // right arm
                    [12, 8, 44, 20, 4, 12], // left arm
                    [4, 20, 4, 20, 4, 12], // right leg
                    [8, 20, 4, 20, 4, 12], // left leg
                ];
                // armor layer
                if ($hasAlpha) {
                    $pastes = array_merge(
                        $pastes,
                        [
                            [4, 0, 40, 8, 8, 8], // head
                        ]
                    );
                }

                break;
                /*
                 * Post Minecraft 1.8 "modern" skin with slim player model:
                 *  - head
                 *  - head armor
                 *  - body
                 *  - body armor
                 *  - right leg
                 *  - right leg armor
                 *  - left arm (3px wide)
                 *  - left arm armor (3px wide)
                 *  - right arm (3px wide)
                 *  - right arm armor (3px wide)
                 */
            case $slim:
                $pastes = [
                    // body layer
                    [3, 0, 8, 8, 8, 8], // head
                    [3, 8, 20, 20, 8, 12], // body
                    [0, 8, 44, 20, 3, 12], // right arm
                    [11, 8, 36, 52, 3, 12], // left arm
                    [3, 20, 4, 20, 4, 12], // right leg
                    [7, 20, 20, 52, 4, 12], // left leg
                ];
                // armor layer
                if ($hasAlpha) {
                    $pastes = array_merge(
                        $pastes,
                        [
                            [3, 0, 40, 8, 8, 8], // head
                            [3, 8, 20, 36, 8, 12], // body
                            [0, 8, 44, 36, 3, 12], // right arm
                            [11, 8, 52, 52, 3, 12], // left arm
                            [3, 20, 4, 36, 4, 12], // right leg
                            [7, 20, 4, 52, 4, 12], // left lag
                        ]
                    );
                }

                break;
                /*
                 * Post Minecraft 1.8 "modern" skin with normal player model:
                 *  - head
                 *  - head armor
                 *  - body
                 *  - body armor
                 *  - right leg
                 *  - right leg armor
                 *  - left arm (4px wide)
                 *  - left arm armor (4px wide)
                 *  - right arm (4px wide)
                 *  - right arm armor (4px wide)
                 */
            default:
                $pastes = [
                    // body layer
                    [4, 0, 8, 8, 8, 8], // head
                    [4, 8, 20, 20, 8, 12], // body
                    [0, 8, 44, 20, 4, 12], // right arm
                    [12, 8, 36, 52, 4, 12], // left arm
                    [4, 20, 4, 20, 4, 12], // right leg
                    [8, 20, 20, 52, 4, 12], // left leg
                ];
                // armor layer
                if ($hasAlpha) {
                    $pastes = array_merge(
                        $pastes,
                        [
                            [4, 0, 40, 8, 8, 8], // head
                            [4, 8, 20, 36, 8, 12], // body
                            [0, 8, 44, 36, 4, 12], // right arm
                            [12, 8, 52, 52, 4, 12], // left arm
                            [4, 20, 4, 36, 4, 12], // right leg
                            [8, 20, 4, 52, 4, 12], // left leg
                        ]
                    );
                }

                break;
        }

        foreach ($pastes as $coords) {
            $params = [$avatar, $texture];
            $params = array_merge($params, $coords);
            call_user_func_array(
                [$this, 'paste'],
                $params
            );
        }

        return $avatar;
    }

    /**
     * Creates a player head image with the given dimensions from the given texture resource.
     *
     * @param resource $texture  Texture resource.
     * @param bool     $hasAlpha Whether the texture uses an alpha channel.
     * @param int      $width    Head width.
     * @param int      $height   Head size.
     *
     * @return false|resource
     */
    private function createHeadFromTextureWithSize($texture, bool $hasAlpha, int $width, int $height)
    {
        $avatar = imagecreatetruecolor($width, $height);
        imagesavealpha($avatar, true);
        $color = imagecolorallocatealpha($avatar, 0, 0, 0, 127);
        imagefill($avatar, 0, 0, $color);
        if (false === $avatar) {
            throw new RuntimeException('Failed to create avatar image');
        }

        // body layer
        imagecopyresized($avatar, $texture, 0, 0, 8, 8, $width, $height, 8, 8);

        // armor layer
        if ($hasAlpha) {
            imagecopyresized($avatar, $texture, 0, 0, 40, 8, $width, $height, 8, 8);
        }

        return $avatar;
    }

    /**
     * Returns the value of the given cache key or null.
     *
     * @param string $method Caller method name.
     * @param string $key    Memcached key.
     *
     * @return null|mixed
     */
    private function readFromCache(string $method, string $key)
    {
        if (is_null($this->memcached)) {
            return null;
        }

        $fullKey = __CLASS__.'-'.$method.'-'.$key;

        $cached = $this->memcached->get($fullKey);
        if (false === $cached) {
            return null;
        }

        return $cached;
    }

    /**
     * Writes the given value to Memcached under the given key for the given time.
     *
     * @param string $method Caller method name.
     * @param string $key    Memcached key.
     * @param mixed  $value  Memcached value.
     */
    private function writeToCache(string $method, string $key, $value)
    {
        if (is_null($this->memcached)) {
            return;
        }

        $fullKey = __CLASS__.'-'.$method.'-'.$key;

        $this->memcached->set($fullKey, $value, self::DATA_CACHE_TIME);
    }
}

/**
 * If you are not running Memcached, you can remove the two following lines and pass nothing to the
 * Avatar class constructor.
 *
 * WARNING:
 * Be aware that removing caching may cause a significant amount of extra requests to the Mojang API
 * which may have a negative impact on performance and cause you to run into API quota issues.
 */
$memcached = new Memcached();
$memcached->addServer('127.0.0.1', 11211);

$avatar = new Avatar($memcached);
$avatar->run();
