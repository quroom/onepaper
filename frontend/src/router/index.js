import Vue from "vue";
import VueRouter from "vue-router";
import ApproveExpert from "../views/ApproveExpert";
import Home from "../views/Home";
import PaperDetail from "../views/PaperDetail";
import PaperEditor from "../views/PaperEditor";
import Profiles from "../views/ProfileList";
import ProfileEditor from "../views/ProfileEditor";
import AllowedUserEditor from "../views/AllowedUserEditor";
import MandateEditor from "../views/MandateEditor";
import Mandates from "../views/MandateList";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/approve-expert",
    name: "approve-expert",
    component: ApproveExpert
  },
  {
    path: "/paper/:id",
    name: "paper",
    component: PaperDetail,
    props: true
  },
  {
    path: "/create/paper/:id?",
    name: "paper-editor",
    component: PaperEditor,
    props: true
  },
  {
    path: "/profiles/:id?/allowed-users",
    name: "allowed-user-editor",
    component: AllowedUserEditor,
    props: true
  },
  {
    path: "/profiles/:username?/:name?",
    name: "profiles",
    component: Profiles,
    props: true
  },
  {
    path: "/create/profiles/:id?",
    name: "profile-editor",
    component: ProfileEditor,
    props: true
  },
  {
    path: "/mandates/",
    name: "mandates",
    component: Mandates
  },
  {
    path: "/create/mandates/:id?",
    name: "mandates-editor",
    component: MandateEditor,
    props: true
  }
];

const router = new VueRouter({
  mode: "history",
  // base: process.env.BASE_URL,
  routes
});

export default router;
