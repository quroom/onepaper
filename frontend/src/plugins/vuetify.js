import Vue from "vue";
import Vuetify from "vuetify/lib";

import en from "../i18n/vuetify/en.ts";
import ko from "../i18n/vuetify/ko.ts";

Vue.use(Vuetify);

Vue.component("my-component", {
  methods: {
    changeLocale() {
      this.$vuetify.lang.current = "ko";
    }
  }
});

export default new Vuetify({
  lang: {
    locales: { en, ko },
    current: "ko"
  }
});
