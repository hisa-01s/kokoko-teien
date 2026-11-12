<?php //子テーマ用関数
if ( !defined( 'ABSPATH' ) ) exit;

//子テーマ用のビジュアルエディタースタイルを適用
add_editor_style();

//以下に子テーマ用の関数を書く

//商品ページ（WooCommerce）では関連記事を表示しない
add_filter('cocoon_part__tmp/related-entries', function($content){
  return is_singular('product') ? '' : $content;
});

//商品ページ（WooCommerce）ではコメント欄とモバイルのコメントボタンを表示しない
//（Cocoon本体の同名関数より先に定義して置き換える）
if ( !function_exists( 'is_single_comment_visible' ) ):
function is_single_comment_visible(){
  if (is_singular('product')) return false;
  return get_theme_option('single_comment_visible', 1);
}
endif;

//マイアカウントのメニュー「ダッシュボード」を「アカウント」、「ダウンロード」を「マイコンテンツ」に変更し、「アカウント」の右に「カート」を追加
add_filter('woocommerce_account_menu_items', function($items){
  if (isset($items['dashboard'])) $items['dashboard'] = 'アカウント';
  if (isset($items['downloads'])) $items['downloads'] = 'マイコンテンツ';
  return array_slice($items, 0, 1, true) + array('hp-cart' => 'カート') + array_slice($items, 1, null, true);
});
add_filter('woocommerce_get_endpoint_url', function($url, $endpoint){
  return 'hp-cart' === $endpoint ? wc_get_cart_url() : $url;
}, 10, 2);

//パンくずリストの「Home」をショップ（/ec/）ではなくサイトTOP（/）へリンクさせる
function hp_breadcrumbs_home_to_site_top($content){
  $shop_home = esc_url(get_home_url());
  $site_top  = preg_replace('#^(https?://[^/]+).*$#', '$1/', $shop_home);
  return preg_replace(
    '#(<div class="breadcrumb-home"[^>]*>.*?<a href=")'.preg_quote($shop_home, '#').'"#s',
    '${1}'.$site_top.'"',
    $content,
    1
  );
}
add_filter('cocoon_part__tmp/breadcrumbs', 'hp_breadcrumbs_home_to_site_top');
add_filter('cocoon_part__tmp/breadcrumbs-page', 'hp_breadcrumbs_home_to_site_top');

//商品ページのパンくずリストを「HOME > リラックスキット > 商品名」にする
add_filter('cocoon_part__tmp/breadcrumbs', function($content){
  if (!function_exists('is_product') || !is_product()) return $content;
  $site_top = preg_replace('#^(https?://[^/]+).*$#', '$1/', get_home_url());
  $sep = '<span class="sp"><span class="fa fa-angle-right" aria-hidden="true"></span></span>';
  return '<div id="breadcrumb" class="breadcrumb breadcrumb-category'.get_additional_single_breadcrumbs_classes().'" itemscope itemtype="https://schema.org/BreadcrumbList">'
    .'<div class="breadcrumb-home" itemscope itemtype="https://schema.org/ListItem" itemprop="itemListElement"><a href="'.esc_url($site_top).'" itemprop="item"><span itemprop="name" class="breadcrumb-caption">HOME</span></a><meta itemprop="position" content="1" /></div>'
    .'<div class="breadcrumb-item" itemscope itemtype="https://schema.org/ListItem" itemprop="itemListElement">'.$sep.'<span class="breadcrumb-caption" itemprop="name">リラックスキット</span><meta itemprop="position" content="2" /></div>'
    .'<div class="breadcrumb-item" itemscope itemtype="https://schema.org/ListItem" itemprop="itemListElement">'.$sep.'<span class="breadcrumb-caption" itemprop="name">'.esc_html(get_the_title()).'</span><meta itemprop="position" content="3" /></div>'
    .'</div>';
}, 20);

//マイアカウント（注文・ダウンロード・住所・アカウント詳細を含む）・お買い物カゴ・商品ページでは投稿日・更新日を表示しない
add_filter('cocoon_part__tmp/date-tags', function($content){
  if (function_exists('is_account_page') && (is_account_page() || is_cart() || is_product())) return '';
  return $content;
});

//お買い物カゴ・商品ページ・マイアカウント（住所など）では目次を表示しない
add_filter('get_toc_tag', function($html){
  if (function_exists('is_cart') && (is_cart() || is_product() || is_account_page())) return '';
  return $html;
});

//商品ページの説明タブ見出し「説明」（h2）を表示しない
add_filter('woocommerce_product_description_heading', '__return_empty_string');

//ヘッダーのカートマークに商品数バッジを表示
//ページキャッシュに他人の数が残らないよう、HTMLには空のバッジだけ出し、数はカートフラグメント（Ajax）で入れる
//TOP・コラムの静的ページも同じフラグメントを読んでいる
add_filter('woocommerce_add_to_cart_fragments', function($fragments){
  $count = WC()->cart ? WC()->cart->get_cart_contents_count() : 0;
  $label = $count > 99 ? '99+' : $count;
  $fragments['b.hp-cart-count'] = '<b class="hp-cart-count"'.($count ? '' : ' hidden').'>'.$label.'</b>';
  return $fragments;
});
add_action('wp_enqueue_scripts', function(){
  if (function_exists('WC')) wp_enqueue_script('wc-cart-fragments');
});

//商品ページ：右カラムを「商品名→価格→数量→ボタン→商品説明」の順に並べる
add_action('wp', function(){
  if (!function_exists('is_product') || !is_product()) return;
  remove_action('woocommerce_single_product_summary', 'woocommerce_template_single_excerpt', 20);
  add_action('woocommerce_single_product_summary', 'woocommerce_template_single_excerpt', 35);
  //説明タブも右カラムの中に入れる
  remove_action('woocommerce_after_single_product_summary', 'woocommerce_output_product_data_tabs', 10);
  add_action('woocommerce_single_product_summary', 'woocommerce_output_product_data_tabs', 60);
});

//商品ページ：ギャラリーをスライドでなく一覧で出し、写真を左カラムに2列で並べる（列はstyle.css）
add_filter('woocommerce_single_product_flexslider_enabled', '__return_false');
add_filter('woocommerce_single_product_zoom_enabled', '__return_false');
add_filter('woocommerce_gallery_image_size', function(){
  return 'woocommerce_single';
});
add_action('woocommerce_single_product_summary', function(){
  echo '<h1 class="hp-product-title">'.esc_html(get_the_title()).'</h1>';
}, 5);

//商品ページ：数量欄に見出しと－／＋ボタンを付ける（カートページの数量欄はそのまま）
function hp_show_quantity_stepper(){
  global $product;
  return is_product() && $product && !$product->is_sold_individually();
}
add_action('woocommerce_before_add_to_cart_quantity', function(){
  if (hp_show_quantity_stepper()) echo '<p class="hp-qty-label">数量</p>';
});
add_action('woocommerce_before_quantity_input_field', function(){
  if (hp_show_quantity_stepper()) echo '<button type="button" class="hp-qty-btn" data-step="-1" aria-label="数量を減らす">−</button>';
});
add_action('woocommerce_after_quantity_input_field', function(){
  if (hp_show_quantity_stepper()) echo '<button type="button" class="hp-qty-btn" data-step="1" aria-label="数量を増やす">＋</button>';
});
add_action('wp_footer', function(){
  if (!function_exists('is_product') || !is_product()) return;
  ?>
<script>
document.addEventListener('click',function(e){
  var btn=e.target.closest('.hp-qty-btn');
  if(!btn)return;
  var input=btn.parentNode.querySelector('input.qty');
  if(btn.dataset.step>0){input.stepUp()}else{input.stepDown()}
  input.dispatchEvent(new Event('change',{bubbles:true}));
});
</script>
  <?php
});

//商品ページ：「カートに追加」の下に「今すぐ購入」ボタンを置き、押すとカートに入れてご注文手続きへ進む
add_filter('woocommerce_product_single_add_to_cart_text', function(){
  return 'カートに追加する';
});
add_action('woocommerce_after_add_to_cart_button', function(){
  global $product;
  if (!$product || !$product->is_type('simple')) return;
  printf(
    '<button type="submit" name="add-to-cart" value="%d" class="button hp-buy-now" formaction="%s">今すぐ購入</button>',
    $product->get_id(),
    esc_url(add_query_arg('hp_buy_now', '1', get_permalink($product->get_id())))
  );
});
add_filter('woocommerce_add_to_cart_redirect', function($url){
  return empty($_GET['hp_buy_now']) ? $url : wc_get_checkout_url(); // phpcs:ignore WordPress.Security.NonceVerification
});

//マイアカウントからの新規登録を常に受け付ける（WooCommerceの設定がOFFでも登録フォームを使えるようにする）
add_filter('pre_option_woocommerce_enable_myaccount_registration', function(){
  return 'yes';
});

//販売先・配送先の国を日本だけにする（支払い画面の国欄を日本で固定。見た目はstyle.css）
function hp_only_japan($countries){
  return array_intersect_key($countries, array('JP' => true));
}
add_filter('woocommerce_countries_allowed_countries', 'hp_only_japan');
add_filter('woocommerce_countries_shipping_countries', 'hp_only_japan');

//支払い画面：「アカウントを作成する」のチェックを最初から入れておく
//（ブロック版の支払い画面はPHPのフィルターが効かないので、表示された時に一度だけクリックする。その後はお客様が外せる）
add_action('wp_footer', function(){
  if (!function_exists('is_checkout') || !is_checkout() || is_user_logged_in()) return;
  ?>
<script>
(function(){
  var observer=new MutationObserver(check);
  function check(){
    var box=document.querySelector('.wc-block-checkout__create-account input[type="checkbox"]');
    if(!box)return;
    observer.disconnect();
    if(!box.checked)box.click();
  }
  observer.observe(document.body,{childList:true,subtree:true});
  check();
})();
</script>
  <?php
});

//マイアカウント：挨拶文「〇〇さん、こんにちは」をメニューカードの上に中央寄せで表示
//（「（〇〇さんでない場合はログアウトしてください）」の部分と、ダッシュボードの説明文は出さない）
add_action('woocommerce_before_account_navigation', 'hp_account_greeting');
function hp_account_greeting() {
  $user = wp_get_current_user();
  if (!$user->exists()) return;
  printf('<p class="hp-account-greeting"><strong>%s</strong>さん、こんにちは</p>', esc_html($user->display_name));
}

//WordPressのログイン画面のロゴをサイトロゴ（マーク＋ココロノ庭園）にし、リンク先をサイトTOPにする
add_filter('login_headerurl', function(){
  return preg_replace('#^(https?://[^/]+).*$#', '$1/', get_home_url());
});
add_filter('login_headertext', function(){
  return 'ココロノ庭園';
});
add_action('login_enqueue_scripts', function(){
  wp_enqueue_style('hp-login-font', 'https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@700&display=swap', array(), null);
  wp_add_inline_style('hp-login-font', '
    .login h1.wp-login-logo a{display:inline-flex;align-items:center;gap:10px;width:auto;height:auto;margin:0 auto 24px;background:none;color:#033521;font-family:"Zen Kaku Gothic New",sans-serif;font-size:30px;font-weight:700;font-feature-settings:"palt";letter-spacing:.06em;line-height:1;text-indent:0;overflow:visible}
    .login h1.wp-login-logo a::before{content:"";width:46px;height:46px;background:url(/asset/image/logo-mark.webp) center/contain no-repeat}
    .login h1.wp-login-logo{text-align:center}
    body.login{background:#fff}
    .login form{border:none;box-shadow:none}
    #backtoblog{display:none}
  ');
});

//管理画面の左メニュー（黒いバー）をサイトの濃い緑にする
add_action('admin_head', function(){
  echo '<style>
    #adminmenuback,#adminmenuwrap,#adminmenu{background:#033521}
    #adminmenu .wp-submenu,
    #adminmenu .wp-has-current-submenu .wp-submenu,
    #adminmenu .wp-has-current-submenu.opensub .wp-submenu,
    #adminmenu a.wp-has-current-submenu:focus+.wp-submenu,
    .folded #adminmenu .wp-has-current-submenu .wp-submenu{background:#022616}
    #adminmenu .wp-submenu:after,#adminmenu .wp-has-current-submenu .wp-submenu:after{border-right-color:#022616}
    #adminmenu li.menu-top:hover,#adminmenu li.opensub>a.menu-top,#adminmenu li>a.menu-top:focus{background:#0b5236;color:#fff}
    #adminmenu li.current a.menu-top,
    #adminmenu li.wp-has-current-submenu a.wp-has-current-submenu,
    #adminmenu .wp-menu-arrow,#adminmenu .wp-menu-arrow div{background:#1c7a52}
    #adminmenu .awaiting-mod,#adminmenu .update-plugins{background:#d63638}
    #collapse-button:hover{color:#fff}
  </style>';
});

//上部の管理バー（黒いバー）も同じ濃い緑にする（管理画面と、ログイン中のサイト表示の両方）
function hp_admin_bar_green(){
  if (!is_admin_bar_showing()) return;
  echo '<style>
    #wpadminbar{background:#033521}
    #wpadminbar .ab-sub-wrapper,#wpadminbar .quicklinks .menupop ul.ab-sub-secondary,#wpadminbar .quicklinks .menupop ul.ab-sub-secondary .ab-submenu{background:#022616}
    #wpadminbar:not(.mobile) .ab-top-menu>li:hover>.ab-item,
    #wpadminbar:not(.mobile) .ab-top-menu>li>.ab-item:focus,
    #wpadminbar .ab-top-menu>li.hover>.ab-item,
    #wpadminbar.nojq .quicklinks .ab-top-menu>li>.ab-item:focus{background:#0b5236;color:#fff}
  </style>';
}
add_action('admin_head', 'hp_admin_bar_green');
add_action('wp_head', 'hp_admin_bar_green');
