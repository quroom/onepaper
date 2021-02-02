import Vue from "vue";
import VueSignaturePad from 'vue-signature-pad';
import App from "./App";
import router from "./router";
import vuetify from "./plugins/vuetify";
import i18n from "@/plugins/i18n";
import AddressSearch from "@/components/AddressSearch";
import getSafe from "@/plugins/get_safe";
import Constants from "@/plugins/Constants";
import LazyTextArea from "@/components/LazyTextArea";
import LazyTextField from "@/components/LazyTextField";
import "./vee-validate";
import { ValidationProvider, ValidationObserver } from 'vee-validate';
import VueQuillEditor from 'vue-quill-editor'
import 'quill/dist/quill.core.css' // import styles
import 'quill/dist/quill.snow.css' // for snow theme
import 'quill/dist/quill.bubble.css' // for bubble theme

Vue.component('ValidationProvider', ValidationProvider)
Vue.component('ValidationObserver', ValidationObserver)
Vue.component('LazyTextArea', LazyTextArea)
Vue.component('LazyTextField', LazyTextField)
Vue.use(AddressSearch);
Vue.use(getSafe);
Vue.use(Constants);
Vue.use(VueSignaturePad);
Vue.use(VueQuillEditor, /* { default global options } */);
Vue.config.productionTip = false;

new Vue({
  i18n,
  router,
  vuetify,
  render: h => h(App)
}).$mount("#app");
