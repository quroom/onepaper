import Vue from "vue";
import VueSignaturePad from 'vue-signature-pad';
import VueDaumPostcode from "vue-daum-postcode"
import App from "./App";
import router from "./router";
import vuetify from "./plugins/vuetify";
import i18n from "@/plugins/i18n";
import getSafe from "@/plugins/get_safe";
import Constants from "@/plugins/Constants";
import LazyTextArea from "@/components/LazyTextArea";
import LazyTextField from "@/components/LazyTextField";
import "./vee-validate";
import { ValidationProvider, ValidationObserver } from 'vee-validate';

Vue.component('ValidationProvider', ValidationProvider)
Vue.component('ValidationObserver', ValidationObserver)
Vue.component('LazyTextArea', LazyTextArea)
Vue.component('LazyTextField', LazyTextField)
Vue.use(getSafe);
Vue.use(Constants);
Vue.use(VueDaumPostcode);
Vue.use(VueSignaturePad);
Vue.config.productionTip = false;

new Vue({
  i18n,
  router,
  vuetify,
  render: h => h(App)
}).$mount("#app");
