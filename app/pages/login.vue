<template>
  <section>
    <div>
      <div class="form-group">
        <input
          v-model="email"
          type="email"
          placeholder="メールアドレス"
          class="form-control">
      </div>
      <div class="form-group">
        <input
          v-model="password"
          type="password"
          placeholder="パスワード"
          class="form-control">
      </div>
      <button
        type="submit"
        class="btn btn-secondary btn-block mb-3"
        @click="login">ログイン</button>
      <p class="text-center"><nuxt-link to="/register">登録はこちら</nuxt-link></p>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    async login() {
      const token = await this.$axios.post('/login', {
        email: this.email,
        password: this.password,
      })
        .then(i => i.data.token)
        .catch(console.error);

      if (token) {
        this.$store.commit('setToken', token);
        document.cookie = `token=${token}`;
        this.$router.push('/filter');
      }
    },
  },
};
</script>

<style scoped>
section {
  padding: 60px;
}

section * {
  font-size: 40px;
}
</style>
