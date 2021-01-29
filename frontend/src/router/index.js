import Vue from "vue";
import VueRouter from "vue-router";
const ApproveExpert = () => import ("../views/ApproveExpert");
const ServiceIntro = () => import ("../views/ServiceIntro");
const Home = () => import ("../views/Home");
const NoticeDetail = () => import ("../views/NoticeDetail");
const NoticeList = () => import ("../views/NoticeList");
const PaperDetail = () => import ("../views/PaperDetail");
const PaperEditor = () => import ("../views/PaperEditor");
const Profiles = () => import ("../views/ProfileList");
const ProfileEditor = () => import ("../views/ProfileEditor");
const AllowedUserEditor = () => import ("../views/AllowedUserEditor");
const MandateEditor = () => import ("../views/MandateEditor");
const Mandates = () => import ("../views/MandateList");
const ManualDetail = () => import ("../views/ManualDetail");
const ManualList = () => import ("../views/ManualList");
const UserEditor = () => import ("../views/UserEditor");
const HelpDesk = () => import ("../views/HelpDesk");

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
    path: "/help-desk/",
    name: "help-desk",
    component: HelpDesk
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
