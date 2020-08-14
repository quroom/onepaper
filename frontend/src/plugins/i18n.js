import Vue from "vue";
import VueI18n from "vue-i18n";
import en from "vee-validate/dist/locale/en.json";
import ko from "vee-validate/dist/locale/ko.json";

Vue.use(VueI18n);

const i18n = new VueI18n({
  locale: "ko",
  messages: {
    en: {
      //Default message
      all: "all",
      back: "back",
      basic: "Basic",
      brokerage: "brokerage",
      etc: "Additional information",
      info: "info",
      logout: "Logout",
      move: "move",
      next: "next",
      realestate: "Realestate",
      required_item: "Item is required",
      transaction_category: "transaction category",
      validation: en.messages,

      //Realestate message
      oneroom: "Single Room",
      tworoom: "Double Room",
      threeroom: "Three Room",
      fourroom: "Four Room",
      sharehouse: "Share House",
      officetel: "Officetel",
      aprtment: "Condominium",
      vailla: "Apartment",
      house: "House",
      commercialhouse: "Commercial House",
      store: "Store",
      land: "Land",

      rent: "Rent",
      depositloan: "Desposit Loan",
      trade: "Trade",
      exchange: "Exchange",

      draft: "Draft",
      done: "Done",
      hidden: "Hidden"

    },
    ko: {
      all: "모든",
      back: "뒤로",
      basic: "필수",
      brokerage: "중개",
      etc: "기타 요청사항",
      info: "정보",
      logout: "로그아웃",
      move: "이사",
      next: "다음",
      realestate: "부동산",
      required_item: "필수 입력 항목입니다",
      transaction_category: "거래종류(매매,전세 등)*",
      validation: ko.messages,

      oneroom: "원룸",
      tworoom: "투룸",
      threeroom: "쓰리룸",
      fourroom: "포룸",
      sharehouse: "쉐어하우스",
      officetel: "오피스텔",
      aprtment: "아파트",
      vailla: "빌라",
      house: "단독주택",
      commercialhouse: "상가주택",
      store: "상가",
      land: "토지",

      rent: "월세",
      depositloan: "전세",
      trade: "매매",
      exchange: "교환",

      draft: "작성중",
      done: "완료",
      hidden: "숨김"
    }
  }
});

export default i18n ;
