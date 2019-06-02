<template>
  <section>
    <div>
      <p>{{ area }}&nbsp;{{ me.availableMonth }}/{{ me.availableDate }}&nbsp;{{ slot }}から</p>
      <p style="font-size: 150%;">{{ cards.length }}人の候補</p>
      <transition name="fade">
        <div v-if="cards.length">
          <p v-text="card.name"/>
          <p v-if="card.liked">あなたのことが気になっています</p>
          <p>
            <img
              :src="`/api/uploads/${card.profile_img}`"
              width="200">
          </p>
          <p><button
            class="btn btn-primary"
            @click="swipe('like')">like</button>
            <button
              class="btn btn-danger"
              @click="swipe('dislike')">dislike</button></p>
        </div>
      </transition>
      <!-- <img
        :src="`/api/uploads/${me.profileImg}`"
        width="100"> -->
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      cards: [],
      areas: [],
      me: {},
      year: null,
      month: null,
      date: null,
      slots: [],
    };
  },
  computed: {
    card() {
      return this.cards[0] || {};
    },
    area() {
      const i = this.areas.find(j => j.id === this.me.availableArea);
      return i && i.name;
    },
    slot() {
      const i = this.slots.find(j => j.id === this.me.availableSlot);
      return i && i.name;
    },
  },
  async mounted() {
    if (!this.$store.state.token) {
      this.$router.push('/login');
      return;
    }

    const hasMatch = await this.$axios.get('/matches', {
      headers: { 'X-AUTH-TOKEN': this.$store.state.token },
    })
      .then(i => i.data.length > 0);

    if (hasMatch) {
      this.$router.push('/match');
      return;
    }

    this.areas = await this.$axios.get('/areas').then(i => i.data);
    this.slots = await this.$axios.get('/slots').then(i => i.data);

    this.me = await this.$axios.get('/me', {
      headers: { 'X-AUTH-TOKEN': this.$store.state.token },
    })
      .then(i => i.data);

    const isValid = (() => {
      const now = this.$moment();
      if (this.me.availableYear < now.year()) return false;
      if (this.me.availableMonth < now.month() + 1) return false;
      if (this.me.availableDate < now.date()) return false;
      if (this.me.availableArea !== 0 && !this.me.availableArea) return false;
      if (this.me.availableSlot !== 0 && !this.me.availableSlot) return false;
      return true;
    })();

    if (!isValid) {
      this.$router.push('/filter');
      return;
    }

    this.cards = await this.$axios.get('/cards', {
      headers: { 'X-AUTH-TOKEN': this.$store.state.token },
    })
      .then(i => i.data);
  },
  methods: {
    async swipe(type) {
      const [first, ...rest] = this.cards;

      if (!first) {
        return;
      }

      const { matched } = await this.$axios.post('/likes', {
        type,
        to: first.id,
      }, {
        headers: { 'X-AUTH-TOKEN': this.$store.state.token },
      })
        .then(i => i.data);

      if (matched) {
        this.$router.push('/match');
        return;
      }

      this.cards = rest;
    },
  },
};
</script>

<style>
.container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}
</style>
