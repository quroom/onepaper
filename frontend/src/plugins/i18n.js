import Vue from "vue";
import VueI18n from "vue-i18n";
import en from "vee-validate/dist/locale/en.json";
import ko from "vee-validate/dist/locale/ko.json";

Vue.use(VueI18n);

const i18n = new VueI18n({
  locale: "ko",
  messages: {
    en: {
      validation: en.messages,
      //Default message
      accept: "Aceept",
      and: "and", 
      attached_document: "Attached Document",
      allow: "Allowed",
      add_allowed_user: "Add user allowed to view profile",
      allow_user_list: "List of users allowed to view profile",
      add_user: "Add User",
      approve: "Approve",
      approved: "Approved",
      all: "All",
      author: "Posted by",
      back: "Back",
      bank_account: "Bank Account",
      basic: "Basic",
      brokerage: "Brokerage",
      button: "Button",
      cancel: "Cancel",
      change: "Change",
      clear: "Clear",
      close: "Close",
      contract: "Contract",
      content: "Content",
      contractor_info: "Contractor Info",
      contractor_info_intro:
        "The contractor details for the above real estate are as follows.",
      created_at: "Created Date",
      create_paper_title: "Editor - Paper",
      confirm: "Confirm",
      copy: "Copy",
      desc_realestate: "Description of Realestate",
      designator: "designator",
      designee: "designee",
      delete: "Delete",
      delete_confirm: "Do you really want to delete?",
      deny: "Deny",
      denied: "Denied",
      detail: "detail",
      edit: "Edit",
      etc: "ETC",
      garantee_insurance: "Brokerage Garantee Insurance",
      general: "General",
      hide: "Hide",
      id: "ID",
      image_file_size_error: "Image file size can't be over 500KB.",
      image_file_count_error: "You can't upload over two images.",
      image_file_type_error: "Only images can be uploaded here.",
      info: "Info",
      insert_special_agreement: "Insert special agreement",
      intro: "This is realestate contract that is made by traders.",
      landlord: "Landlord",
      language: "Language",
      last: "Last",
      link: "Link",
      link_is_copied: "Link is copied",
      load: "Load",
      logout: "Logout",
      mandate: "Mandate",
      mandate_paper: "warrant of attorney",
      manwon: "ten thousand Won",
      modify: "Modify",
      move: "Move",
      next: "Next",
      no_contract: "There is no contract",
      no_profile: "There is no profile",
      no_profile_cant_use_service:
        "You must create profile before using service.",
      paper: "Paper",
      profile: "Profile",
      period: "Period",
      profile_name: "Profile Name",
      read_mode: "Read Mode",
      realestate: "Realestate",
      realestate_agency: "Realestate Agency",
      required_item: "Item is required",
      request: "request",
      request_success: "Your request has been processed.",
      reviewing: "reviewing",
      save: "Save",
      search: "Search",
      send_your_link: "Send link to user who you want to trade.",
      select: "Select",
      special_agreement: "Special Agreement",
      special_agreement_basic_template: "",
      status: "status",
      sign: "Signature",
      signature: "Sign",
      signature_empty_warning: "Signature can't be empty",
      stamp: "Stamp",
      submit: "Submit",
      signature_and_submit: "Submit mandate after signature",
      tenant: "Tenant",
      terms_and_conditions: "Terms and conditions",
      terms_and_conditions_intro:
        "The contract details for the above real estate are as follows.",
      title: "Title",
      transaction_category: "transaction category",
      term_of_lease: "Term of Lease",
      updated_at: "Update Date",
      user: "User",
      username: "User ID",
      won: "won",
      won_paid_recieved: "won paid upon visit and received",

      //Profile message
      birthday: "Birth Day",
      name: "Name",
      mobile_number: "Conctact",
      bank_name: "Bank Name",
      account_number: "Account Number",
      registration_number: "Registration Number",
      shop_name: "Shop Name",
      shop_address: "Shop Address",
      registration_certificate: "Registration Certificate",
      agency_license: "Agency License",

      //Realestate basic message
      address: "Address",
      area: "Area",
      dong: "Dong",
      ho: "Ho",
      land_type: "Land Type",
      lot_area: "Lot Area",
      room_name: "Room Name",
      building_structure: "Building Strcuture",
      building_type: "Building Type",
      building_area: "Building Area",
      realestate_type: "Realestate Type",
      trade_type: "Trade Type",

      //terms and condition message
      from_date: "From Date",
      to_date: "To Date",
      down_payment: "Down Payment",
      security_deposit: "Security Deposit",
      monthly_fee: "Monthly Fee",
      maintenance_fee: "Maintenance Fee",

      //Land type
      buildingland: "Building Land",

      //Building type
      c1neighborfacility: "C1 Neighbor Facility",
      c2neighborfacility: "C2 Neighbor Facility",

      //Realestate model message
      oneroom: "Single Room",
      tworoom: "Double Room",
      threeroom: "Three Room",
      fourroom: "Four Room",
      sharehouse: "Share House",
      officetel: "Officetel",
      apartment: "Condominium",
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
      progress: "Progress",
      done: "Done",
      hidden: "Hidden"
    },
    ko: {
      validation: ko.messages,
      accept: "동의합니다.",
      and: "및",
      attached_document: "첨부 서류",
      allow: "허용",
      approve: "승인",
      approved: "승인됨",
      add_allowed_user: "프로필 조회 허용 회원 추가",
      allow_user_list: "프로필 조회 허용 회원 리스트",
      add_user: "회원 추가",
      all: "전체",
      author: "작성자",
      back: "뒤로",
      bank_account: "입금계좌",
      basic: "필수",
      button: "버튼",
      brokerage: "중개",
      cancel: "취소",
      change: "변경",
      clear: "지우기",
      close: "닫기",
      created_at: "등록일",
      create_paper_title: "계약서 작성",
      confirm: "확인",
      copy: "복사",
      contract: "계약서",
      content: "내용",
      contractor_info: "계약자 정보",
      contractor_info_intro: "위 부동산의 계약자 정보는 아래와 같다.",
      delete: "삭제",
      delete_confirm: "정말 삭제 하시겠습니까?",
      deny: "거절",
      denied: "거절",
      desc_realestate: "부동산 기본정보(표시)",
      designator: "위임인",
      designee: "수임인",
      detail: "상세",
      edit: "수정",
      etc: "기타",
      garantee_insurance: "중개 보증 서류",
      general: "일반",
      hide: "숨김",
      id: "ID",
      image_file_size_error: "이미지 크기는 500KB를 넘을 수 없습니다.",
      image_file_count_error: "2개 이상의 이미지를 첨부할 수 없습니다.",
      image_file_type_error: "이미지만 업로드 가능합니다.",
      info: "정보",
      insert_special_agreement: "특약을 입력해주세요.",
      intro:
        "본 부동산에 대하여 계약자 쌍방은 합의에 의하여 다음과 같이 계약을 체결한다.",
      manwon: "만원",
      landlord: "임대인",
      language: "언어",
      last: "최종",
      link: "링크",
      link_is_copied: "링크가 복사 되었습니다.",
      load: "불러오기",
      logout: "로그아웃",
      mandate: "위임",
      mandate_paper: "위임장",
      modify: "편집",
      move: "이사",
      next: "다음",
      no_contract: "작성된 계약서가 없습니다.",
      no_profile: "생성된 프로필이 없습니다.",
      no_profile_cant_use_service: "서비스 이용전 프로필을 생성하여야 합니다.",
      paper: "계약서",
      profile: "프로필",
      period: "기간",
      profile_name: "프로필명",
      read_mode: "읽기모드",
      realestate: "부동산",
      realestate_agency: "개업공인중개사",
      required_item: "필수 입력 항목입니다",
      request: "요청",
      request_success: "요청이 처리되었습니다.",
      reviewing: "검토중",
      save: "제출",
      search: "검색",
      send_your_link: "거래를 원하는 회원에게 링크를 전송하세요.",
      select: "선택",
      special_agreement: "특약",
      special_agreement_basic_template: "",
      status: "상태",
      sign: "(서명)",
      signature: "서명",
      signature_empty_warning: "서명을 비워둔 상태로 제출 할 수 없습니다.",
      stamp: "인장",
      submit: "제출",
      signature_and_submit: "서명 후 위임장 제출",
      tenant: "임차인",
      terms_and_conditions: "계약내용",
      terms_and_conditions_intro: "위 부동산의 계약내용은 아래와 같다.",
      term_of_lease: "계약기간",
      title: "제목",
      transaction_category: "거래종류(매매,전세 등)*",
      user: "회원",
      username: "회원 아이디",
      updated_at: "수정일",
      won: "원",
      won_paid_recieved: "원은 방문시 지불하고 영수함.",

      //Profile message
      birthday: "생일",
      name: "성함",
      mobile_number: "연락처",
      bank_name: "은행명",
      account_number: "계좌",
      registration_number: "등록번호",
      shop_name: "사무소명",
      shop_address: "사무소주소",
      registration_certificate: "중개사무소 등록증",
      agency_license: "자격증",

      area: "면적",
      address: "주소",
      dong: "동",
      ho: "호",
      land_type: "지목",
      lot_area: "토지면적",
      room_name: "방이름",
      building_structure: "건물구조",
      building_type: "건물용도",
      building_area: "건물면적",
      realestate_type: "부동산종류",
      trade_type: "계약 종류",

      from_date: "입주일",
      to_date: "퇴실일",
      down_payment: "계약금",
      security_deposit: "보증금",
      monthly_fee: "월세",
      maintenance_fee: "관리비",

      //Land type
      buildingland: "대",

      c1neighborfacility: "제1종근린생활시설",
      c2neighborfacility: "제2종근린생활시설",

      oneroom: "원룸",
      tworoom: "투룸",
      threeroom: "쓰리룸",
      fourroom: "포룸",
      sharehouse: "쉐어하우스",
      officetel: "오피스텔",
      apartment: "아파트",
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
      progress: "서명중",
      done: "완료",
      hidden: "숨김"
    }
  }
});

export default i18n;
