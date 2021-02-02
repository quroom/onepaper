import Vue from "vue";
import VueRouter from "vue-router";

import ApproveExpert from "../views/ApproveExpert";
import ServiceIntro  from "../views/ServiceIntro";
import Home  from "../views/Home";
import NoticeDetail  from "../views/NoticeDetail";
import NoticeList  from "../views/NoticeList";
import PaperDetail  from "../views/PaperDetail";
import PaperEditor  from "../views/PaperEditor";
import Profiles  from "../views/ProfileList";
import ProfileEditor  from "../views/ProfileEditor";
import AllowedUserEditor  from "../views/AllowedUserEditor";
import MandateEditor  from "../views/MandateEditor";
import Mandates  from "../views/MandateList";
import ManualDetail  from "../views/ManualDetail";
import ManualList  from "../views/ManualList";
import UserEditor  from "../views/UserEditor";

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
    path: "/service-intro",
    name: "service-intro",
    component: ServiceIntro
  },
  {
    path: "/papers/:id",
    name: "paper-detail",
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
    path: "/mandates/:id?",
    name: "mandate-detail",
    component: MandateEditor,
    props: true
  },
  {
    path: "/create/mandates/",
    name: "mandates-editor",
    component: MandateEditor,
    props: true
  },
  {
    path: "/notices/",
    name: "notices",
    component: NoticeList
  },
  {
    path: "/notices/:id",
    name: "notice-detail",
    component: NoticeDetail,
    props: true
  },
  {
    path: "/manuals/",
    name: "manuals",
    component: ManualList,
    props: true
  },
  {
    path: "/manuals/:id",
    name: "manual-detail",
    component: ManualDetail,
    props: true
  },
  {
    path: "/edit/user/",
    name: "user-editor",
    component: UserEditor
  }
];

const router = new VueRouter({
  mode: "history",
  // base: process.env.BASE_URL,
  routes,
  scrollBehavior () {
    return { x: 1, y: 1 }
  }
});

export default router;
