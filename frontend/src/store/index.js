import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    user: null,
    user_setting: null,
    has_profile: true,
    user_category: "user",
    is_paper_updated: false,
    tour_index: 0
  },
  mutations: {
    SET_USER_SETTING(state, payload) {
      for (const [key, value] of Object.entries(payload)) {
        state.user_setting[key] = value;
      }
    },
    SET_TOUR_INDEX(state, payload) {
      state.tour_index = payload;
    },
    SET_IS_PAPER_UPDATED(state, payload) {
      state.is_paper_updated = payload;
    },
    SET_HAS_PROFILE(state, payload) {
      state.has_profile = payload;
    },
    initialiseStore(state, payload) {
      state.user = payload;
      state.user_setting = payload.user_setting;
      state.tour_enabled = payload.user_setting.is_tour_on;
      state.has_profile = payload.has_profile;

      if (payload.is_expert) {
        state.user_category = "expert";
      } else if (payload.is_staff) {
        state.user_category = "staff";
      }
    }
  }
});
