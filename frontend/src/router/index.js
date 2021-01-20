import Vue from "vue";
import VueRouter from "vue-router";
const ApproveExpert = () => import ("../views/ApproveExpert");
const CompanyInfo = () => import ("../views/CompanyInfo");
const Home = () => import ("../views/Home");
const NoticeEditor = () => import ("../views/NoticeEditor");
const NoticeList = () => import ("../views/NoticeList");
const PaperDetail = () => import ("../views/PaperDetail");
const PaperEditor = () => import ("../views/PaperEditor");
const Profiles = () => import ("../views/ProfileList");
const ProfileEditor = () => import ("../views/ProfileEditor");
const AllowedUserEditor = () => import ("../views/AllowedUserEditor");
const MandateEditor = () => import ("../views/MandateEditor");
const Mandates = () => import ("../views/MandateList");
const ServiceInfoList = () => import ("../views/ServiceInfoList");
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
    path: "/company-info",
    name: "company-info",
    component: CompanyInfo
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
    path: "/notices/:id?",
    name: "notice-detail",
    component: NoticeEditor,
    props: true
  },
  {
    path: "/create/notices/",
    name: "notices-editor",
    component: NoticeEditor,
    props: true
  },
  {
    path: "/service-infos/",
    name: "service-infos",
    component: ServiceInfoList,
    props: true
  },
  {
    path: "/help-desk/",
    name: "helpdesk",
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
  routes
});

export default router;
