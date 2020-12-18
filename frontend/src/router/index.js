import Vue from "vue";
import VueRouter from "vue-router";
const ApproveExpert = () => import ("../views/ApproveExpert");
const Home = () => import ("../views/Home");
const PaperDetail = () => import ("../views/PaperDetail");
const PaperEditor = () => import ("../views/PaperEditor");
const Profiles = () => import ("../views/ProfileList");
const ProfileEditor = () => import ("../views/ProfileEditor");
const AllowedUserEditor = () => import ("../views/AllowedUserEditor");
const MandateEditor = () => import ("../views/MandateEditor");
const Mandates = () => import ("../views/MandateList");
const UserEditor = () => import ("../views/UserEditor");

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
  routes
});

export default router;
