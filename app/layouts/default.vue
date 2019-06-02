<template>
  <div>
    <p class="small">
      <nuxt-link to="/swipe">スワイプ</nuxt-link>
      <nuxt-link to="/filter">設定</nuxt-link>
      <nuxt-link to="/match">マッチ</nuxt-link>
      <nuxt-link to="/register">登録</nuxt-link>
      <nuxt-link to="/login">ログイン</nuxt-link>
      <nuxt-link to="/logout">ログアウト</nuxt-link>
    </p>
    <section class="container">
      <nuxt/>
    </section>
  </div>
</template>

<style>
html {
  font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI',
    Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 16px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}

*,
*:before,
*:after {
  box-sizing: border-box;
  margin: 0;
}
</style>
