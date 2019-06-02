<template>
  <section>
    <div>
      <p>日付・時間・場所を選択</p>
      <div class="form-group">
        <select
          v-model="area"
          class="form-control">
          <template v-for="a in areas">
            <option
              :value="a.id"
              :key="a.id">{{ a.name }} </option>
          </template>
        </select>
      </div>
      <div class="form-group">
        <select
          v-model="slot"
          class="form-control">
          <template v-for="s in slots">
            <option
              :value="s.id"
              :key="s.id">{{ s.name }} </option>
          </template>
        </select>
      </div>
      <div class="form-group">
        <select
          v-model="dateIdx"
          class="form-control">
          <template v-for="(d,idx) in dates">
            <option
              :value="idx"
              :key="idx">{{ d.display }} </option>
          </template>
        </select>
      </div>
      <div class="form-group">
        <button
          class="btn btn-secondary btn-block"
          @click="update">次へ</button>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      dateIdx: 0,
      area: 0,
      slot: 0,
      areas: [],
      slots: [],
      count: 0,
    };
  },
  computed: {
    dates() {
      const now = this.$moment();

      return [2, 3, 4, 5, 6, 7].map(i => ({
        display: now.clone().add(i, 'days').format('YYYY-MM-DD'),
        year: now.clone().add(i, 'days').year(),
        month: now.clone().add(i, 'days').month() + 1,
        date: now.clone().add(i, 'days').date(),
      }));
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

    const isValid = await (async () => {
      const me = await this.$axios.get('/me', {
        headers: { 'X-AUTH-TOKEN': this.$store.state.token },
      })
        .then(i => i.data);

      const now = this.$moment();
      if (me.availableYear < now.year()) return false;
      if (me.availableMonth < now.month() + 1) return false;
      if (me.availableDate < now.date()) return false;
      if (me.availableArea !== 0 && !me.availableArea) return false;
      if (me.availableSlot !== 0 && !me.availableSlot) return false;
      return true;
    })();

    if (isValid) {
      this.$router.push('/swipe');
      return;
    }

    this.areas = await this.$axios.get('/areas').then(i => i.data);
    this.slots = await this.$axios.get('/slots').then(i => i.data);

    this.area = this.areas[0].id;
    this.slot = this.slots[0].id;
  },
  methods: {
    async update() {
      await this.$axios.put('/me', {
        availableYear: Number(this.dates[this.dateIdx].year),
        availableMonth: Number(this.dates[this.dateIdx].month),
        availableDate: Number(this.dates[this.dateIdx].date),
        availableArea: Number(this.area),
        availableSlot: Number(this.slot),
      }, {
        headers: { 'X-AUTH-TOKEN': this.$store.state.token },
      });

      this.$router.push('/swipe');
    },
  },
};
</script>

<style scoped>
section {
  width: 300px;
}
</style>
