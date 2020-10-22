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
      button: "Button",
      clear: "Clear",
      close: "Close",
      contract: "Contract",
      contractor_info: "Contractor Info",
      contractor_info_intro: "The contractor details for the above real estate are as follows.",
      created_at: "Created Date",
      create_paper_title: "Editor - Paper",      
      desc_realestate: "Description of Realestate",
      delete: "Delete",
      detail: "detail",
      etc: "Additional information",
      info: "Info",
      intro: "This is realestate contract that is made by traders.",
      landlord: "Landlord",
      last: "Last",
      logout: "Logout",
      manwon: "ten thousand Won",
      modify: "Modify",      
      move: "Move",
      next: "Next",
      profile: "Profile",
      profile_name: "Profile Name",
      realestate: "Realestate",
      realestate_agency: "Realestate Agency",
      required_item: "Item is required",
      save: "Save",
      search: "search",
      special_agreement: "Special Agreement",
      sign: "Signature",
      signature: "Sign",
      signature_empty_warning: "Signature can't be empty",
      stamp: "Stamp",
      submit: "Submit",
      tenant: "Tenant",
      terms_and_conditions: "Terms and conditions",
      terms_and_conditions_intro: "The contract details for the above real estate are as follows.",
      title: "Title",
      transaction_category: "transaction category",
      term_of_lease: "Term of Lease",
      updated_at: "Update Date",
      username: "User ID",
      validation: en.messages,
      won: "won",
      won_paid_recieved: "won paid upon visit and received",

      //Profile message
      birthday: "Birth Day",
      name: "Name",
      mobile_number: "Mobile Number",
      bank_name: "Bank Name",
      account_number: "Account Number",
      registration_number: "Registration Number",
      shop_name: "Shop Name",
      shop_address: "Shop Address",
      business_registration_certificate: "Registration Certificate",
      agency_license: "Agency License",

      //Realestate basic message
      address: "Address",
      area: "Area",
      land_type: "Land Type",
      lot_area: "Lot Area(㎡)",
      room_name: "Detail Room Name",
      building_structure: "Building Strcuture",
      building_type: "Building Type",
      building_area: "Building Area(㎡)",
      realestate_type: "Realestate Type",
      trade_type: "Trade Type",

      //terms and condition message
      from_date: "From Date",
      to_date: "To Date",
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
      button: "버튼",
      brokerage: "중개",
      clear: "지우기",
      close: "닫기",
      created_at: "등록일",
      create_paper_title: "계약서 작성",      
      contract: "계약서",
      contractor_info: "계약자 정보",
      contractor_info_intro: "위 부동산의 계약자 정보는 아래와 같다.",
      delete: "삭제",
      desc_realestate: "부동산 기본정보(표시)",
      detail: "상세",
      etc: "기타 요청사항",
      info: "정보",
      intro: "본 부동산에 대하여 계약자 쌍방은 합의에 의하여 다음과 같이 계약을 체결한다.",
      manwon: "만원",
      landlord: "임대인",
      last: "최종",
      logout: "로그아웃",
      modify: "편집",
      move: "이사",
      next: "다음",
      profile: "프로필",
      profile_name: "프로필명",
      realestate: "부동산",
      realestate_agency: "개업공인중개사",
      required_item: "필수 입력 항목입니다",
      save: "제출",
      search: "검색",
      special_agreement: "특약",      
      sign: "(서명)",
      signature: "서명",
      signature_empty_warning: "서명을 비워둔 상태로 제출 할 수 없습니다.",
      stamp: "인장",
      submit: "제출",
      tenant: "임차인",
      terms_and_conditions: "계약내용",
      terms_and_conditions_intro: "위 부동산의 계약내용은 아래와 같다.",
      term_of_lease: "계약기간",
      title: "제목",
      transaction_category: "거래종류(매매,전세 등)*",
      username: "회원아이디",
      updated_at: "수정일",
      validation: ko.messages,
      won: "원",
      won_paid_recieved: "원은 방문시 지불하고 영수함.",

      //Profile message
      birthday: "생년월일",
      name: "성함",
      mobile_number: "연락처",
      bank_name: "은행명",
      account_number: "계좌번호",
      registration_number: "등록번호",
      shop_name: "사무소 명칭",
      shop_address: "사무소 소재지",
      business_registration_certificate: "사업자 등록증",
      agency_license: "자격증",

      area: "면적",
      address: "주소",
      land_type: "지목",
      lot_area: "토지면적(㎡)",
      room_name: "동 호수(또는 방이름)",
      building_structure: "건물구조",
      building_type: "건물용도",
      building_area: "건물면적(㎡)",
      realestate_type: "부동산종류",
      trade_type: "계약 종류",
      
      from_date: "입주일",
      to_date: "퇴실일",
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
