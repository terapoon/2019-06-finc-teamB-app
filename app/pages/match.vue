<template>
  <section>
    <p>{{ match.name }}さん</p>
    <p>{{ match.month }}月{{ match.date }}日 {{ match.slot }} {{ match.area }} 〇〇ジム</p>
    <p>
      <img
        v-if="match.profileImg"
        :src="`/api/uploads/${match.profileImg}`"
        width="200">
    </p>
  </section>
</template>

<script>
export default {
  data() {
    return {
      match: {},
    };
  },
  async mounted() {
    if (!this.$store.state.token) {
      this.$router.push('/login');
      return;
    }

    this.match = await this.$axios.get('/matches', {
      headers: {
        'X-AUTH-TOKEN': this.$store.state.token,
      },
    })
      .then(i => i.data[0]);

    if (!this.match) {
      this.$router.push('/swipe');
    }
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
