import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Paper from "../views/Paper.vue";
import PaperEditor from "../views/PaperEditor.vue";
import Profiles from "../views/ProfileList.vue";
import ProfileEditor from "../views/ProfileEditor.vue";

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
    path: "/create/paper/:id?",
    name: "paper-editor",
    component: PaperEditor,
    props: true
  },
  {
    path: "/profiles",
    name: "profiles",
    component: Profiles
  },
  {
    path: "/create/profiles/:id?",
    name: "profile-editor",
    component: ProfileEditor,
    props: true
  }
];

const router = new VueRouter({
  mode: "history",
  // base: process.env.BASE_URL,
  routes
});

export default router;
