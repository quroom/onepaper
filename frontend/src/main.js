import Vue from "vue";
import VueSignaturePad from "vue-signature-pad";
import App from "./App";
import { apiService } from "@/common/api_service";
import router from "./router";
import vuetify from "./plugins/vuetify";
import i18n from "@/plugins/i18n";
import getSafe from "@/plugins/get_safe";
import Constants from "@/plugins/Constants";
import AddressSearch from "@/components/AddressSearch";
import CustomTour from "@/components/CustomTour.vue";
import LazyTextArea from "@/components/LazyTextArea";
import LazyTextField from "@/components/LazyTextField";
import RightMenu from "@/components/RightMenu";
import "./vee-validate";
import { ValidationProvider, ValidationObserver } from "vee-validate";
import VueQuillEditor from "vue-quill-editor";
import "quill/dist/quill.core.css"; // import styles
import "quill/dist/quill.snow.css"; // for snow theme
import "quill/dist/quill.bubble.css"; // for bubble theme
import VueTour from "vue-tour";
import store from "./store";

require("vue-tour/dist/vue-tour.css");

(async () => {
  const data = await apiService("/api/user/").then((data) => {
    return data;
  });

  const DEFAULT_TITLE = "원페이퍼";
  router.afterEach((to) => {
    // Use next tick to handle router history correctly
    // see: https://github.com/vuejs/vue-router/issues/914#issuecomment-384477609
    Vue.nextTick(() => {
      document.title = to.meta.title || DEFAULT_TITLE;
    });
  });

  //Components
  Vue.component("ValidationProvider", ValidationProvider);
  Vue.component("ValidationObserver", ValidationObserver);
  Vue.component("AddressSearch", AddressSearch);
  Vue.component("CustomTour", CustomTour);
  Vue.component("LazyTextArea", LazyTextArea);
  Vue.component("LazyTextField", LazyTextField);
  Vue.component("RightMenu", RightMenu);
  //Plugins
  Vue.use(getSafe);
  Vue.use(Constants);
  Vue.use(VueSignaturePad);
  Vue.use(VueQuillEditor /* { default global options } */);
  Vue.use(VueTour);
  Vue.config.productionTip = false;

  new Vue({
    i18n,
    router,
    store,
    vuetify,
    beforeCreate() {
      this.$store.commit("initialiseStore", data);
    },
    render: (h) => h(App)
  }).$mount("#app");
})();
