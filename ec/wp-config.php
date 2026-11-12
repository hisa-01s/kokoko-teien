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
define( 'DB_NAME', 'LAA1394630-pvdrkc' );

/** Database username */
define( 'DB_USER', 'LAA1394630' );

/** Database password */
define( 'DB_PASSWORD', 'eRNzqNNTRfbVCLjc' );

/** Database hostname */
define( 'DB_HOST', 'mysql404.phy.lolipop.lan' );

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
define( 'AUTH_KEY',          '1SN<x)iV6~XtMqj]Xgi$Y22CFwp+FNH4a07iCXTQ/a$,6CS~ypX+%0HJbJe2vUTH' );
define( 'SECURE_AUTH_KEY',   ';8|YH1^YD`l,(199Y!;B.O n31p|fU[!uJA/%r1.wk[P%(`[0g0#UMqKan}nzI3t' );
define( 'LOGGED_IN_KEY',     'c<RihbhmWq72|c(fkf!56>8D.(G.01*<Sh%#Iv <g6+VAq_m34<C~BPu}8zU}XI;' );
define( 'NONCE_KEY',         'S7`,YA^Mvt6.&K`F5Fi5gFGT@g.uofW+SQt,tICNYOF[E$+Xaq)!Xm;oEP@kYr5 ' );
define( 'AUTH_SALT',         'N0r+zfP)oBJ9&M*v~Y051.jiPX4gHMU.ckFcPYCsk4Fn^UM-JPsJAfUtlMY-lKe<' );
define( 'SECURE_AUTH_SALT',  'Zr#ZNjl0{bh;Q^nEZ1gdM;@J~hRy&.PA;.LJt`9N#:IX~=jDk 2_DpYp}Q+f&nS4' );
define( 'LOGGED_IN_SALT',    '@bX.HR0c:WO?@A)DCCd56ilMzbxA`D<$92YnGe+.:Hq@ ?5cS/9w5;?bc&*E6tU<' );
define( 'NONCE_SALT',        '@H(Vv_X);9.dQAPV;tv4GMQF+0-/rJBv&,{UHh3NQZvL>/yaWJK$n`74Nj=yKW4_' );
define( 'WP_CACHE_KEY_SALT', 'n~~U&N {39pwxyy_s[0@Vk@AqBa[+BtKErrWGb7~RH^v@r#DY^}aK,[Q@8[~7<o-' );


/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp20261017150616_';

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
