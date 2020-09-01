import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Paper from "../views/Paper.vue";
import PaperEditor from "../views/PaperEditor.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/paper/:id",
    name: "paper",
    component: Paper,
    props: true
  },
  {
    path: "/ask",
    name: "paper-editor",
    component: PaperEditor,
  }
];

const router = new VueRouter({
  mode: "history",
  // base: process.env.BASE_URL,
  routes
});

export default router;
