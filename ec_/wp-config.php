<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the web site, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * Localized language
 * * ABSPATH
 *
 * @link https://wordpress.org/support/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'LAA1394630-sicklj' );

/** Database username */
define( 'DB_USER', 'LAA1394630' );

/** Database password */
define( 'DB_PASSWORD', '96zqk1DNRVzcEK0B' );

/** Database hostname */
define( 'DB_HOST', 'mysql403.phy.lolipop.lan' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',          'F6llq2l}16JR)mzF$[^>O3Xi,<4-~TXn*u1,r:03eqrBV</_*#O/u)`D9ZO>z+d=' );
define( 'SECURE_AUTH_KEY',   '`J{U>r ]]dKe~?|3JWF-Os.9~m4V3OzQ% xednYvfw{:4UIMy@}HSrsZ(/t7jA@7' );
define( 'LOGGED_IN_KEY',     'X,TE!Ho;j^Iihf6o|,vI0BLd(nx4*G$V%r9ydC*MeAsi<mflFm7,uYKesE~+!|GM' );
define( 'NONCE_KEY',         'Lo9YN y:}[>fujg|3{--EtBlY9~w_/a,( i`+s6pWspH=]~/E2cl45UY E^`0 Aw' );
define( 'AUTH_SALT',         '(M#F?X^{lGO%/B{KaNO?P#Zd+wq|H[+Up&MgUdy}~HN@LRtZL)|$0y;P~wm{a7SW' );
define( 'SECURE_AUTH_SALT',  'f7^PCcH__m#xCK7B]1`Cuv8NP^=-kv#s$xo}hZ7KfBow<KoR 6T1q~ Y~X:201g2' );
define( 'LOGGED_IN_SALT',    '?-_puMuOhx,j#bmk7d;PEO7EcoU,M,]C}tHc^0{F2Jc@i>O-AM>)dnm,&)bI}Fyx' );
define( 'NONCE_SALT',        'yKr#N Q8~j/szC&0`<WS-aw.r%T[13{CX<tDiV7*W[Ltz-TEL`+O7Xh1EIpBCD.P' );
define( 'WP_CACHE_KEY_SALT', '~WJE{O4c ;D*n,R7_/EzNV(Z|jL2sN ){BW+)Pn3sVF1;-9:IT (E!uG1e[+8YUc' );


/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp20261022205621_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/support/article/debugging-in-wordpress/
 */
define( 'WP_DEBUG', false );


/* Add any custom values between this line and the "stop editing" line. */



/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
