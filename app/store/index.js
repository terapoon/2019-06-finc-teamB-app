export const state = () => ({
  token: '',
});

export const mutations = {
  setToken(state, token) {
    // eslint-disable-next-line
    state.token = token;
  },
};
