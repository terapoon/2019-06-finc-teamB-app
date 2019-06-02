<template>
  <div/>
</template>

<script>
export default {
  mounted() {
    this.$store.commit('setToken', '');
    setTimeout(() => this.$router.push('/login'), 1000);
  },
};
</script>
