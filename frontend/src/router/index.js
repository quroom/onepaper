import Vue from "vue";
import VueRouter from "vue-router";

import ApproveExpert from "../views/ApproveExpert";
import ServiceIntro from "../views/ServiceIntro";
import Home from "../views/Home";
import NoticeDetail from "../views/NoticeDetail";
import NoticeList from "../views/NoticeList";
import PaperDetail from "../views/PaperDetail";
import PaperEditor from "../views/PaperEditor";
import Profiles from "../views/ProfileList";
import ProfileEditor from "../views/ProfileEditor";
import AllowedUserEditor from "../views/AllowedUserEditor";
import MandateEditor from "../views/MandateEditor";
import Mandates from "../views/MandateList";
import ManualDetail from "../views/ManualDetail";
import ManualList from "../views/ManualList";
import UserEditor from "../views/UserEditor";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: Home,
    meta: { title: "계약서리스트(홈)-Onepaper" }
  },
  {
    path: "/approve-expert",
    name: "approve-expert",
    component: ApproveExpert,
    meta: { title: "전문가 승인-Onepaper" }
  },
  {
    path: "/service-intro",
    name: "service-intro",
    component: ServiceIntro,
    meta: { title: "서비스 소개-Onepaper" }
  },
  {
    path: "/papers/:id",
    name: "paper-detail",
    component: PaperDetail,
    props: true,
    meta: { title: "계약서 조회-Onepaper" }
  },
  {
    path: "/create/paper/:id?",
    name: "paper-editor",
    component: PaperEditor,
    props: true,
    meta: { title: "계약서 작성-Onepaper" }
  },
  {
    path: "/profiles/:id?/allowed-users",
    name: "allowed-user-editor",
    component: AllowedUserEditor,
    props: true,
    meta: { title: "빠른거래회원 추가-Onepaper" }
  },
  {
    path: "/profiles/:email?/:name?",
    name: "profiles",
    component: Profiles,
    props: true,
    meta: { title: "프로필 리스트-Onepaper" }
  },
  {
    path: "/create/profiles/:id?",
    name: "profile-editor",
    component: ProfileEditor,
    props: true,
    meta: { title: "프로필 작성-Onepaper" }
  },
  {
    path: "/mandates/",
    name: "mandates",
    component: Mandates,
    meta: { title: "위임장 리스트-Onepaper" }
  },
  {
    path: "/mandates/:id?",
    name: "mandate-detail",
    component: MandateEditor,
    props: true,
    meta: { title: "위임장 조회-Onepaper" }
  },
  {
    path: "/create/mandates/",
    name: "mandates-editor",
    component: MandateEditor,
    props: true,
    meta: { title: "위임장 작성-Onepaper" }
  },
  {
    path: "/notices/",
    name: "notices",
    component: NoticeList,
    meta: { title: "공지사항-Onepaper" }
  },
  {
    path: "/notices/:id",
    name: "notice-detail",
    component: NoticeDetail,
    props: true,
    meta: { title: "공지사항 조회-Onepaper" }
  },
  {
    path: "/manuals/",
    name: "manuals",
    component: ManualList,
    props: true,
    meta: { title: "이용방법 리스트-Onepaper" }
  },
  {
    path: "/manuals/:id",
    name: "manual-detail",
    component: ManualDetail,
    props: true,
    meta: { title: "이용방법 조회-Onepaper" }
  },
  {
    path: "/edit/user/",
    name: "user-editor",
    component: UserEditor,
    meta: { title: "회원정보 수정-Onepaper" }
  }
];

const router = new VueRouter({
  mode: "history",
  // base: process.env.BASE_URL,
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(savedPosition);
        }, 70);
      });
    } else {
      return { x: 1, y: 1 };
    }
  }
});

window.popStateDetected = false;
window.addEventListener("popstate", () => {
  window.popStateDetected = true;
});

router.beforeEach((to, from, next) => {
  const IsItABackButton = window.popStateDetected;
  window.popStateDetected = false;
  if (!IsItABackButton) {
    if (to.name == "paper-detail") {
      to.meta.isDestroied = false;
    } else if (to.name == "home") {
      to.meta.isDestroied = false;
    } else {
      to.meta.isDestroied = true;
    }
  } else {
    if (
      (from.name == "paper-detail" && to.name == "home") ||
      (from.name == "home" && to.name == "paper-detail")
    ) {
      to.meta.isDestroied = false;
    } else {
      to.meta.isDestroied = true;
    }
  }
  next();
});
export default router;
