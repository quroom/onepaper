import "material-design-icons-iconfont/dist/material-design-icons.css";
import Vue from "vue";
import Vuetify from "vuetify/lib";
import Constants from "@/plugins/Constants";

Vue.use(Vuetify);
Vue.use(Constants)
export default new Vuetify({
  icons: {
    iconfont: "md"
  }
});
