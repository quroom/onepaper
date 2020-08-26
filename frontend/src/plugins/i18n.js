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
      all: "All",
      author: "Posted by",
      back: "Back",
      bank_account: "Bank Account",
      basic: "Basic",
      brokerage: "Brokerage",
      created_at: "Created Date",
      desc_realestate: "Description of Realestate",
      etc: "Additional information",
      info: "Info",
      intro: "This is realestate contract that is made by traders.",
      last: "Last",
      logout: "Logout",
      move: "Move",
      next: "Next",
      realestate: "Realestate",
      required_item: "Item is required",
      special_agreement: "Special Agreement",
      terms_and_conditions: "Terms and conditions",
      terms_and_conditions_intro: "The contract details for the above real estate are as follows.",
      transaction_category: "transaction category",
      term_of_lease: "Term of Lease",
      updated_at: "Update Date",
      validation: en.messages,
      won: "won",
      won_paid_recieved: "won paid upon visit and received",

      //Realestate basic message
      address: "Address",
      area: "Area",
      land_type: "Land Type",
      lot_area: "Lot Area",
      room_name: "Rent Room",
      building_structure: "Building Strcuture",
      building_type: "Building Type",
      building_area: "Building Area",

      //terms and condition message
      down_payment: "Down Payment",
      security_deposit: "Security Deposit",
      monthly_fee: "Monthly Fee",
      maintenance_fee: "Maintenance Fee",

      //Realestate model message
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
      author: "작성자",
      back: "뒤로",
      bank_account: "입금계좌",
      basic: "필수",
      brokerage: "중개",
      created_at: "등록일",
      desc_realestate: "부동산의 표시",
      etc: "기타 요청사항",
      info: "정보",
      intro: "본 부동산에 대하여 계약자 쌍방은 합의에 의하여 다음과 같이 계약을 체결한다.",
      last: "최종",
      logout: "로그아웃",
      move: "이사",
      next: "다음",
      realestate: "부동산",
      required_item: "필수 입력 항목입니다",
      special_agreement: "특약",
      terms_and_conditions: "계약내용",
      terms_and_conditions_intro: "위 부동산의 계약내용은 아래와 같다.",
      term_of_lease: "계약기간",
      transaction_category: "거래종류(매매,전세 등)*",
      updated_at: "수정일",
      validation: ko.messages,
      won: "원",
      won_paid_recieved: "원은 방문시 지불하고 영수함.",

      area: "면적",
      address: "주소",
      land_type: "지목",
      lot_area: "토지면적",
      room_name: "임대할부분",
      building_structure: "건물구조",
      building_type: "건물용도",
      building_area: "건물면적",

      down_payment: "계약금",
      security_deposit: "보증금",
      monthly_fee: "월세",
      maintenance_fee: "관리비",

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

export default i18n;
