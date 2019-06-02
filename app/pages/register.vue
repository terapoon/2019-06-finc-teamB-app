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
          v-model="name"
          type="text"
          placeholder="名前"
          class="form-control">
      </div>
      <div class="form-group">
        <input
          v-model="hobbies"
          type="text"
          placeholder="趣味"
          class="form-control">
      </div>
      <div class="form-group">
        <textarea
          v-model="introduction"
          placeholder="自己紹介"
          class="form-control"/>
      </div>
      <div class="form-group">
        <input
          v-model="password"
          type="password"
          placeholder="パスワード"
          class="form-control">
      </div>
      <div class="form-group">
        <select
          v-model="gender"
          class="form-control">
          <option value="0">男性</option>
          <option value="1">女性</option>
        </select>
      </div>
      <div class="form-group">
        <input
          type="file"
          @change="onFileChange">
      </div>
      <div class="form-group">
        <button
          type="submit"
          class="btn btn-secondary btn-block"
          @click="register">登録</button>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
      fileToUpload: '',
      gender: '0',
      name: '',
      introduction: '',
      hobbies: '',
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
    onFileChange(e) {
      const files = e.target.files || e.dataTransfer.files;
      [this.fileToUpload] = files;
    },
    async register() {
      if (
        !this.email
        || !this.password
        || !this.fileToUpload
        || !this.name
        || !this.introduction
        || !this.hobbies
      ) {
        return;
      }

      const formData = new FormData();
      formData.append('profile', this.fileToUpload);

      const { filename } = await this.$axios.post('/image', formData, {
        headers: {
          'content-type': 'multipart/form-data',
        },
      })
        .then(i => i.data);

      const token = await this.$axios.post('/register', {
        filename,
        name: this.name,
        introduction: this.introduction,
        hobbies: this.hobbies,
        gender: Number(this.gender),
        email: this.email,
        password: this.password,
      })
        .then(i => i.data.token)
        .catch(console.error);

      if (token) {
        this.$store.commit('setToken', token);
        this.$router.push('/swipe');
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
  font-size: 30px;
}
</style>
