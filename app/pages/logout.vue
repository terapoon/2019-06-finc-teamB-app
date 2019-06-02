<template>
  <div/>
</template>

<script>
export default {
  mounted() {
    this.$store.commit('setToken', '');
    this.$router.push('/login');
  },
};
</script>
