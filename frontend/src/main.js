import Vue from "vue";
import VueSignaturePad from 'vue-signature-pad';
import VueDaumPostcode from "vue-daum-postcode"
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify";
import i18n from "@/plugins/i18n";
import "./vee-validate";

Vue.use(VueDaumPostcode)
Vue.use(VueSignaturePad);
Vue.config.productionTip = false;

new Vue({
  i18n,
  router,
  vuetify,
  render: h => h(App)
}).$mount("#app");
