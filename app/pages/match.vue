<template>
  <section class="bg-pink">
    <div class="appbar">
      <img
        :src="`/api/uploads/${match.profileImg}`"
        alt=""
        class="profile">
      <div class="title">
        <div class="filter grey-white">{{ match.area }} {{ match.month }}/{{ match.date }} {{ match.slot }}から</div>
        <div class="header white">マッチしました！</div>
      </div>
      <img
        src="~/assets/chat-white.svg"
        alt=""
        class="chat">
    </div>
    <div class="card-wrapper">
      <div class="card">
        <img
          :src="`/api/uploads/${match.profileImg}`"
          class="card-image"
          alt="">
        <div class="card-property padding-bottom">
          <div class="card-name">{{ match.name }}</div>
          <div class="card-age">19</div>
          <img
            src="~/assets/info.svg"
            alt="">
        </div>
      </div>
    </div>
    <div class="bg-blue">
      <div class="header white tac padding-bottom">予約詳細</div>
      <div class="row">
        <div class="row-left grey-white">日時</div>
        <div class="row-right white">{{ match.month }}/{{ match.date }} {{ match.slot }}</div>
      </div>
      <div class="row">
        <div class="row-left grey-white">エリア</div>
        <div class="row-right white">{{ match.area }}</div>
      </div>
      <div class="card-wrapper">
        <div class="card mb-clear">
          <img
            src="~/assets/school.jpeg"
            class="card-image gym-image"
            alt="">
          <div class="card-property">
            <div class="card-name gym-name">BELE MODY MAKE STUDIO</div>
            <img
              src="~/assets/google-maps.svg"
              alt="">
          </div>
          <div class="card-button">
            <div class="reserved">
              <img
                src="~/assets/check-green.svg"
                alt="">予約済み
            </div>
            <div class="cancel grey-text">キャンセルする</div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="row-left grey-white">料金</div>
        <div class="row-right white">¥1,800</div>
        <div class="row-left grey-white paid">請求済み</div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      match: {},
      me: {},
    };
  },
  async mounted() {
    if (!this.$store.state.token) {
      this.$router.push('/login');
      return;
    }

    this.me = await this.$axios.get('/me', {
      headers: {
        'X-AUTH-TOKEN': this.$store.state.token,
      },
    });

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
        { name: 'viewport', content: '' },
      ],
    };
  },
};
</script>
