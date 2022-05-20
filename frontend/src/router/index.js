import Vue from "vue";
import VueRouter from "vue-router";

import AskListingList from "../views/AskListingList";
const ApproveExpert = () => import("../views/ApproveExpert");
const ServiceIntro = () => import("../views/ServiceIntro");
const PaperList = () => import("../views/PaperList");
const NoticeDetail = () => import("../views/NoticeDetail");
const NoticeList = () => import("../views/NoticeList");
const PaperDetail = () => import("../views/PaperDetail");
const PaperEditor = () => import("../views/PaperEditor");
const Profiles = () => import("../views/ProfileList");
const ProfileEditor = () => import("../views/ProfileEditor");
const AllowedUserEditor = () => import("../views/AllowedUserEditor");
const ListingList = () => import("../views/ListingList");
const ListingEditor = () => import("../views/ListingEditor");
const MandateEditor = () => import("../views/MandateEditor");
const Mandates = () => import("../views/MandateList");
const UserEditor = () => import("../views/UserEditor");

Vue.use(VueRouter);
//home 매물 리스트로 바꾸기.
const routes = [
  {
    path: "/",
    name: "listings",
    component: ListingList,
    meta: { title: "매물 리스트-원페이퍼" }
  },
  {
    path: "/listings/:id?",
    name: "listing-detail",
    component: ListingEditor,
    props: true,
    meta: { title: "매물 조회-원페이퍼" }
  },
  {
    path: "/asklistings",
    name: "asklistings",
    component: AskListingList,
    meta: { title: "매물 요청 리스트-원페이퍼" }
  },
  {
    path: "/create/listing",
    name: "listing-editor",
    component: ListingEditor,
    meta: { title: "매물 등록-원페이퍼" }
  },
  {
    path: "/approve-expert",
    name: "approve-expert",
    component: ApproveExpert,
    meta: { title: "전문가 승인-원페이퍼" }
  },
  {
    path: "/papers",
    name: "papers",
    component: PaperList,
    meta: { title: "계약서리스트-원페이퍼" }
  },
  {
    path: "/papers/:id",
    name: "paper-detail",
    component: PaperDetail,
    props: true,
    meta: { title: "계약서 조회-원페이퍼" }
  },
  {
    path: "/create/paper/:id?",
    name: "paper-editor",
    component: PaperEditor,
    props: true,
    meta: { title: "계약서 작성-원페이퍼" }
  },
  {
    path: "/profiles/:id?/allowed-users",
    name: "allowed-user-editor",
    component: AllowedUserEditor,
    props: true,
    meta: { title: "빠른거래회원 추가-원페이퍼" }
  },
  {
    path: "/profiles/:email?/:name?",
    name: "profiles",
    component: Profiles,
    props: true,
    meta: { title: "프로필 리스트-원페이퍼" }
  },
  {
    path: "/service-intro",
    name: "service-intro",
    component: ServiceIntro,
    meta: { title: "서비스 소개-원페이퍼" }
  },
  {
    path: "/create/profiles/:id?",
    name: "profile-editor",
    component: ProfileEditor,
    props: true,
    meta: { title: "프로필 작성-원페이퍼" }
  },
  {
    path: "/mandates/",
    name: "mandates",
    component: Mandates,
    meta: { title: "위임장 리스트-원페이퍼" }
  },
  {
    path: "/mandates/:id?",
    name: "mandate-detail",
    component: MandateEditor,
    props: true,
    meta: { title: "위임장 조회-원페이퍼" }
  },
  {
    path: "/create/mandates/",
    name: "mandates-editor",
    component: MandateEditor,
    props: true,
    meta: { title: "위임장 작성-원페이퍼" }
  },
  {
    path: "/notices/",
    name: "notices",
    component: NoticeList,
    meta: { title: "공지사항-원페이퍼" }
  },
  {
    path: "/notices/:id",
    name: "notice-detail",
    component: NoticeDetail,
    props: true,
    meta: { title: "공지사항 조회-원페이퍼" }
  },
  {
    path: "/edit/user/",
    name: "user-editor",
    component: UserEditor,
    meta: { title: "회원정보 수정-원페이퍼" }
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
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({ x: 0, y: 0 });
        }, 70);
      });
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
  const isListingUpdated = router.app.$store ? router.app.$store.state.is_listing_updated : false;
  if (!IsItABackButton) {
    if (to.name == "paper-detail") {
      to.meta.isPaperDestroied = false;
    } else if (to.name == "papers") {
      to.meta.isPaperDestroied = false;
    } else {
      to.meta.isPaperDestroied = true;
    }
    if (to.name == "listing-detail" && !isListingUpdated) {
      to.meta.isListingDestroied = false;
    } else if (to.name == "listings" && !isListingUpdated) {
      to.meta.isListingDestroied = false;
    } else {
      to.meta.isListingDestroied = true;
    }
    if (to.name == "asklistings" || (from.name != "listings" && to.name == "listing-detail")) {
      to.meta.isAskListingDestroied = false;
    } else {
      to.meta.isAskListingDestroied = true;
    }
  } else {
    if (
      (from.name == "paper-detail" && to.name == "papers") ||
      (from.name == "papers" && to.name == "paper-detail")
    ) {
      to.meta.isPaperDestroied = false;
    } else {
      to.meta.isPaperDestroied = true;
    }

    if (
      (from.name == "listing-detail" && to.name == "listings" && !isListingUpdated) ||
      (from.name == "listings" && to.name == "listing-detail" && !isListingUpdated)
    ) {
      to.meta.isListingDestroied = false;
    } else {
      to.meta.isListingDestroied = true;
    }

    if (to.name == "asklistings" || (from.name == "asklistings" && to.name == "listing-detail")) {
      to.meta.isAskListingDestroied = false;
    } else {
      to.meta.isAskListingDestroied = true;
    }
  }
  next();
});
export default router;
