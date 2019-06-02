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
        class="btn btn-secondary btn-block"
        @click="login">ログイン</button>
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
  async mounted() {
    const isLoggedIn = await this.$axios.get('/matches', {
      headers: {
        'X-AUTH-TOKEN': this.$store.state.token,
      },
    })
      .then(() => true)
      .catch(() => false);

    if (isLoggedIn) {
      this.$router.push('/filter');
    }
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
  head() {
    return {
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      ],
    };
  },
};
</script>

<style scoped>
section {
  padding: 30px;
}
</style>
