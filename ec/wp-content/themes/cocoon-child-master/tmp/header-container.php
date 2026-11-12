<?php //ヘッダーエリア（TOPページ /index.html と共通のヘッダーに差し替え）
if ( !defined( 'ABSPATH' ) ) exit; ?>

<div id="header-container" class="header-container hp-header-container">
  <header class="hp-header">
    <div class="hp-header-in">
      <a href="/" class="hp-logo"><img src="/asset/image/logo-mark.webp" alt="" width="46" height="46"><b>ココロノ庭園</b></a>
      <nav class="hp-gnav">
        <ul>
          <li><a href="/">ホーム</a></li>
          <li><a href="/column/">コラム</a></li>
        </ul>
      </nav>
      <div class="hp-icons">
        <a href="https://heal-place.com/ec/my-account/"><img src="/asset/image/account.svg" alt="" width="22" height="22"><span>マイアカウント</span></a>
        <a href="https://heal-place.com/ec/cart/"><img src="/asset/image/cart.svg" alt="" width="22" height="22"><b class="hp-cart-count" hidden></b><span>カート</span></a>
      </div>
    </div>
  </header>
</div><!-- /.header-container -->
