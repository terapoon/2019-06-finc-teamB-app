<template>
  <section>
    <div class="appbar">
      <img
        :src="`/api/uploads/${me.profileImg}`"
        alt=""
        class="profile">
      <div class="title">
        <div class="filter">{{ area }}&nbsp;{{ me.availableMonth }}/{{ me.availableDate }}&nbsp;{{ slot }}から</div>
        <div class="header">{{ cards.length }}人の候補</div>
      </div>
      <img
        src="~/assets/chat.svg"
        alt=""
        class="chat">
    </div>

    <transition name="fade">
      <div v-if="cards.length">
        <div
          v-if="!card.liked"
          class="card-wrapper">
          <div class="card">
            <img
              :src="`/api/uploads/${card.profile_img}`"
              class="card-image"
              alt="">
            <div class="card-property">
              <div class="card-name">{{ card.name }}</div>
              <div class="card-age">19</div>
              <img
                src="~/assets/info.svg"
                alt="">
            </div>
            <div class="card-button">
              <div
                class="button outline-blue margin-right"
                @click="swipe('dislike')">やめとく</div>
              <div class="button outline-pink flex-grow">
                <img
                  src="~/assets/favorite-pink.svg"
                  alt="favorite">
                <div
                  class="button-text"
                  @click="swipe('like')">気になる</div>
              </div>
            </div>
          </div>
        </div>

        <div
          v-else
          class="card-wrapper">
          <div class="card">
            <img
              :src="`/api/uploads/${card.profile_img}`"
              class="card-image"
              alt="">
            <div class="matching-alert-wrapper">
              <div class="matching-alert">
                <img
                  src="assets/alert.svg"
                  alt="">あなたのことが気になっています
              </div>
            </div>
            <div class="card-property">
              <div class="card-name">{{ card.name }}</div>
              <div class="card-age">19</div>
              <img
                src="~/assets/info.svg"
                alt="">
            </div>
            <div class="card-button">
              <div
                class="button outline-blue margin-right"
                @click="swipe('dislike')">やめとく</div>
              <div class="button filled-pink flex-grow">
                <img
                  src="~/assets/favorite-white.svg"
                  alt="favorite">
                <div
                  class="button-text"
                  @click="swipe('like')">今すぐマッチ</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
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
</style>
