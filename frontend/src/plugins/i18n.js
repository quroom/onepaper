import Vue from "vue";
import VueI18n from "vue-i18n";
import en from "vee-validate/dist/locale/en.json";
import ko from "vee-validate/dist/locale/ko.json";

Vue.use(VueI18n);

const i18n = new VueI18n({
  locale: navigator.language,
  messages: {
    en: {
      validation: en.messages,
      //Default message
      add_garantee_insurance: "Add garantee insurance",
      add_quick_trade_user: "Add quick trade user",
      add_quick_trade_user_directly: "Add quick trade user directly",
      add_quick_trader_link: "Quick trade request link",
      accept: "Aceept",
      ascending: "Ascending",
      activate: "Activate",
      alpha: "alpha",
      and: "and",
      answer: "Answer",
      attached_document: "Attached Document",
      allow: "Allowed",
      all_papers: "All Papers",
      company_info: "Company",
      quick_trade_user_list: "List of quick trading members",
      quick_trade_user_list_subtitle:
        "Please add quick trade memebers. You can add your profile without the contract request·approval step. \
      Please ask additional members for the'Trade Member Registration Request Link' through the menu. You can easily add members.",
      add_user: "Add User",
      approve: "Approve",
      approved: "Approved",
      all: "All",
      author: "author",
      back: "Back",
      bank_account: "Bank Account",
      basic: "Basic",
      before_create_contract: "Before create contract",
      bjdong: "Beopjeong Dong(Li)",
      brokerage: "Brokerage",
      button: "Button",
      buyer: "Tenant(Buyer)",
      cancel: "Cancel",
      change: "Change",
      clear: "Clear",
      close: "Close",
      connect_social: "Connect Social",
      contact_us: "Contact Us",
      content: "Content",
      contract: "Contract",
      contractor_info: "Contractor Info",
      contractor_info_intro: "The contractor details for the above real estate are as follows.",
      created_at: "Created Date",
      create_paper: "Create Contract",
      create_profile: "Create Profile",
      create_mandate: "Create Mandate",
      creating_profile_is_mandatory: "Before writing contract, Creating profile is mandatory.",
      confirm: "Confirm",
      copy: "Copy",
      descending: "Descending",
      default: "Default",
      desc_realestate: "Description of Realestate",
      designator: "designator",
      designee: "designee",
      delete: "Delete",
      deleted: "Deleted",
      delete_account: "Delete Account",
      delete_confirm: "Do you really want to delete?",
      delete_profile_subtitle:
        "Member ID, e-mail, and name must be exactly the same for withdrawal processing, and account DB will be completely deleted only if there is no created profile. \
      If there is a profile created, the account will no longer be available, and the database will be preserved for future legal disputes. You can rest assured that the preserved data is only provided to you.",
      delete_success: "It has been deleted.",
      deny: "Deny",
      denied: "Denied",
      detail: "detail",
      edit: "Edit",
      edit_registor_info: "Edit registor info",
      email: "이메일",
      etc: "ETC",
      error: "There is a request error",
      exact_correct_match: "Exactly Correct is Matched",
      expiry_date: "expiry date",
      filter: "filter",
      general: "General",
      footer_info: "Company: Quroom | Registration Number: 246-86-01161",
      hide: "Hide",
      how_to_use: "How to use",
      id: "ID",
      initialize: "Initialize",
      image_file_size_error: "Image file size can't be over %{0} KB.",
      image_file_count_error: "You can't upload over %{0} images.",
      image_file_type_error: "This file extension is not supported.",
      info: "Info",
      insert_special_agreement: "Insert special agreement",
      intro: "This is realestate contract that is made by traders.",
      landlord: "Landlord",
      landlord_or_tenant: "Are you landlord or tenant?",
      language: "Language",
      language_change: "언어 변경",
      last: "Last",
      learn_how_to_use: "Learn how to use",
      link: "Link",
      list: "List",
      link_is_copied: "Link is copied",
      load: "Load",
      load_list: "Load List",
      load_default: "Load Default",
      load_more: "Load More",
      load_special_agreement: "Load Special Agreement",
      lookup_scope: "Lookup Scope",
      logout: "Logout",
      manage: "Manage",
      manual_search: "Manual Search",
      mandate: "Mandate",
      mandate_subtitle:
        "During the delegation period, the contract written by the mandate is completed without the signature of the mandate.",
      mandate_paper: "Power of Attorney",
      mandatory: "mandatory",
      manwon: "ten thousand Won",
      menu: "Menu",
      modify: "Modify",
      modify_delete_deadline: "Modify and Delete dealine",
      modify_delete_deadline_expired: "Modify and Delete deadline is expired",
      move: "Move",
      next: "Next",
      none: "None",
      notice: "Notice",
      number: "Number",
      no_mandate: "There is no mandate",
      no_paper: "There is no paper.",
      no_paper_redirect_to_all_paper:
        "There is no contract included as a contractor, so the entire contract is searched.",
      no_profile: "There is no profile",
      no_profile_cant_use_service: "You must create profile before using service.",
      onepaper: "Onepaper",
      only_my_papers: "Only mine",
      ordering: "Ordering",
      password_change: "Password Change",
      partial_correct_match: "Partially Correct is Matched",
      paper: "Paper",
      paper_subtitle:
        "To create a better contract culture, the written contract can be viewed by anyone in the entire contract tab except for personal information (name, detailed lot number, etc.)",
      paper_requesting_subtitle:
        "Contracts in the requesting state can be signed and contractor information can be checked after all contractors requiring the request press the Approve button.",
      profile: "Profile",
      permanence: "Permanence",
      period: "Period",
      please_add_trade_user: "Please add user allowed to view profile",
      please_available_garantee_insurance: "Please add available garantee insurance today.",
      please_sign: "Please sign here.",
      pease_select_default_profile: "Please select default profile.",
      profile_name: "Profile Name",
      profile_number: "Profile Number",
      profile_list_subtitle:
        "Only one profile can be activated and will be used when writing the contract. When adding a quick transaction member, the other party can add your profile without searching.",
      quickness: "Quickness",
      quick_trade_user: "Quick tradeuser",
      read_mode: "Read Mode",
      realestate: "Realestate",
      realestate_agency: "Realestate Agency",
      required_item: "Item is required",
      request: "request",
      request_agent_account: "Request to agent account.",
      request_success: "Your request has been processed.",
      reviewing: "reviewing",
      save: "Save",
      search: "Search",
      send_your_link: "Send link to user who you want to trade.",
      select: "Select",
      seller: "Landlor(Seller)",
      service_intro: "Service Intro",
      special_agreement: "Special Agreement",
      special_agreement_basic_template: "",
      status: "status",
      share: "Share",
      show: "Show",
      show_paper: "Show Paper",
      sign: "Signature",
      signature: "Sign",
      signature_effect:
        "If you agree that this signature will have the same effect as the conclusion of a paper contract, please sign it.",
      signature_and_submit: "Submit mandate after signature",
      signature_empty_warning: "Signature can't be empty",
      stamp: "Stamp",
      submit: "Submit",
      trade: "Trade",
      tenant: "Tenant",
      terms_and_conditions: "Terms and conditions",
      terms_and_conditions_intro: "The contract details for the above real estate are as follows.",
      title: "Title",
      transaction_category: "transaction category",
      term_of_lease: "Term of Lease",
      updated_at: "Last U",
      user: "User",
      use_profile_after_approval:
        "The profile of a certified practitioner can be used after reviewing the attached documents and approval.",
      unspport_function: "This feature is not currently available on this page.",
      view_mobile_version: "View Mobile Ver",
      view_pc_version: "View PC Ver(Printable)",
      writing: "writing",
      written: "Written",
      won: "Won",
      won_paid_recieved: "won paid upon visit and received",
      year: "year",

      //Tour translation
      done_tour: "Done",
      skip_tour: "Skip tour",
      start_tour: "Start Tour",
      tour_if_don_have_profile: "If you do not have a profile, click the Create Profile button",
      tour_create_paper_button_click: "Click button to create paper!",
      tour_create_profile:
        "Shall we start creating a profile? </br> You do not need to enter the (optional) field.",
      tour_address: "Click the address search bar and enter the address",
      tour_dong_ho:
        "As in the example, when inputting, omit the letter of the same name and number. <br/> Ex) 201, B",
      tour_mobile_number: "Enter your mobile phone number (numbers only)",
      tour_bank_name: "Select bank name",
      tour_bank_account: "Enter account number",
      tour_submit: "When you are finished, click the Submit button",
      optional: "optional",

      //Bank List
      "--선택--": "--Choose--",
      산업은행: "(KDB)KoreaDevelopmentBank",
      부산은행: "(BNK)BusanBank",
      기업은행: "(IBK)IndustrialBank",
      광주은행: "KwangjuBank",
      국민은행: "(KB)KookminBank",
      제주은행: "JejuBank",
      수협: "Soohyup",
      전북은행: "JeonbukBank",
      농협은행: "(Central)NonghyupBank",
      경남은행: "KyungnamBank",
      지역농축협: "(Local)NonghyupBank",
      새마을금고: "(MG)SaemaulBank",
      우리은행: "WooriBank",
      신용협동조합: "CreditAssociation",
      SC제일은행: "SCJeilBank",
      상호저축은행: "MutualSavingBank",
      한국씨티은행: "CityBank",
      산림조합: "(SJ)SanlimJohap",
      KEB하나은행: "(KEB)HanaBank",
      우체국: "EpostBank",
      신한은행: "ShinhanBank",
      K뱅크: "KBank",
      대구은행: "DaeguBank",
      카카오뱅크: "KakaoBank",

      //Service Intro
      service_intro_title:
        "OnePaper's value is reducing the risk and time of real estate transactions through technology.",
      service_intro_text1:
        "Are you still having trouble filling out the contract by hand?\
      Are you writing what you wrote again? Now, read the content you wrote once and write the contract.\
      With a mobile phone and a PC, you can write a contract anytime, anywhere.\
      <br/>I will narrow the distance between you and others.",
      service_intro_text2:
        "No more worrying about losing your contract. Check your contract anytime, anywhere.\
      Contract data written on mobile phones and PCs is safely stored on AWS RDS for the duration of the service.\
      <br/>Keep your contract permanent",
      service_intro_text3:
        "Not sure how to write the contract?\
      Are you worried that the contract I wrote is well written?\
      Share your contracts, and share contracts from friends.\
      And refer to the well-written contract.<br/>You can write a better contract.",

      //Profile message
      birthday: "Birthday",
      name: "Name",
      mobile_number: "Conctact",
      bank_name: "Bank Name",
      account_number: "Account Number",
      registration_number: "Registration Number",
      shop_name: "Shop Name",
      shop_address: "Shop Address",
      registration_certificate: "Registration Certificate",
      agency_license: "Agency License",
      insurnace: "insurance",
      garantee_insurance: "Brokerage Garantee Insurance",

      //Realestate basic message
      address: "Address",
      area: "Area",
      dong: "Dong",
      ho: "Ho",
      land_category: "Land Type",
      lot_area: "Lot Area",
      room_name: "Room Name",
      building_structure: "Building Strcuture",
      building_category: "Building Type",
      building_area: "Building Area",
      realestate_category: "Realestate Type",
      trade_category: "Trade Type",

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
      purchase: "Purchase",
      exchange: "Exchange",

      requesting: "Request",
      draft: "Draft",
      progress: "Progress",
      done: "Done",
      hidden: "Hidden",

      //for verifying_explanation
      enforcement_rules: "■ 공인중개사법 시행규칙 [별지 제20호서식]",
      ve_amendment_updated_date: "Updated 2021. 1. 12.",
      ve_subject: "중개대상물 확인·설명서[Ⅰ] (주거용 건축물)",
      materials_for_ve: "확인ㆍ설명자료",
      explanation_evidence: "확인ㆍ설명 근거자료 등",
      explanation_evidence_info: "대상물건의 상태에 관한 자료요구 사항",
      land_area: "Land Area",
      ledger_land_category: "ledger land category",
      actual_land_category: "actual land category",
      net_area: "net area",
      land_share: "land share",
      year_of_completion: "year of completion",
      ledger_building_category: "ledger building category",
      actual_building_category: "actual building category",
      building_direction: "building direction",
      seismic_design: "seismic design",
      seismic_capacity: "seismic capacity",
      legal_status: "legal status",
      matters_of_violation: "matters of violation",
      land_ownership: "land ownership",
      building_ownership: "building ownership",
      land_other: "land other",
      building_other: "building other",
      rental_housing_registration: "rental housing registration",
      use_area: "use area",
      use_district: "use district",
      use_zone: "use zone",
      building_coverage_limit: "building coverage limit",
      floor_area_limit: "floor area limit",
      planning_facilities: "planning facilities",
      permission_report_zone: "permission report zone",
      speculative_area: "speculative area",
      unit_planning_area_others: "unit planning area others",
      other_use_restriction: "other use restriction",
      relative_with_roads: "relative with roads",
      is_paved_rode: "is paved rode",
      accessibility: "accessibility",
      bus_stop: "bus stop",
      bus_by_foot: "bus by foot",
      bus_required_time: "bus required time",
      subway_station: "subway station",
      subway_by_foot: "subway by foot",
      subway_required_time: "subway required time",
      parking_lot: "parking lot",
      parking_lot_info: "parking lot info",
      elementary_school: "elementary school",
      elementary_school_by_foot: "elementary school by foot",
      elementary_school_required_time: "elementary school required time",
      middle_school: "middle school",
      middle_school_by_foot: "middle school by foot",
      middle_school_required_time: "middle school required time",
      high_school: "high school",
      high_school_by_foot: "high school by foot",
      high_school_required_time: "high school required time",
      department_store: "department store",
      department_store_by_foot: "department store by foot",
      department_store_required_time: "department store required time",
      medical_center: "medical center",
      medical_center_by_foot: "medical center by foot",
      medical_center_required_time: "medical center required time",
      is_security_office: "is security office",
      management: "management",
      undesirable_facilities: "undesirable facilities",
      undesirable_facilities_info: "undesirable facilities info",
      expected_transaction_price: "expected transaction price",
      land_prcie_recorded: "land prcie recorded",
      building_price_recorded: "building price recorded",
      acquisition_tax: "acquisition tax",
      special_tax: "special tax",
      local_education_tax: "local education tax",
      water_damage_status: "water damage status",
      water_damage_status_info: "water damage status info",
      water_capacity_status: "water capacity status",
      water_capacity_status_info: "water capacity status info",
      electricity_supply_status: "electricity supply status",
      electricity_supply_status_info: "electricity supply status info",
      gas_supply_status: "gas supply status",
      gas_supply_status_info: "gas supply status info",
      is_fire_alarm_detector: "is fire alarm detector",
      fire_alarm_detector_quantity: "fire alarm detector quantity",
      heating_supply_method: "heating supply method",
      heating_status: "heating status",
      heating_status_info: "heating status info",
      heating_type: "heating type",
      heating_type_info: "heating type info",
      is_elevator: "is elevator",
      elevator_status: "elevator status",
      drainage_status: "drainage status",
      drainage_status_info: "drainage status info",
      other_facilities: "other facilities",
      wall_crack_status: "wall crack status",
      wall_crack_status_info: "wall crack status info",
      water_leak_status: "water leak status",
      water_leak_status_info: "water leak status info",
      wall_paper_status: "wall paper status",
      wall_paper_status_info: "wall paper status info",
      sunshine_status: "sunshine status",
      sunshine_status_info: "sunshine status info",
      noise_status: "noise status",
      vibration: "vibration",
      comission: "comission",
      actual_expenses: "actual expenses",
      payment_period: "payment period",
      calculation_info: "calculation info",
      verifying_explanation: "Verifying Explanation Manual"
    },
    ko: {
      validation: ko.messages,
      add_garantee_insurance: "중개보증서류 추가",
      add_quick_trade_user: "빠른거래회원 추가",
      add_quick_trade_user_directly: "빠른거래회원 즉시추가",
      add_quick_trader_link: "빠른거래 등록 요청 링크",
      accept: "동의합니다.",
      activate: "활성화",
      and: "및",
      alpha: "알파",
      answer: "답변",
      attached_document: "첨부 서류",
      allow: "허용",
      approve: "승인",
      approved: "승인됨",
      quick_trade_user_list: "빠른거래회원 리스트",
      quick_trade_user_list_subtitle:
        "빠른 거래 회원을 추가 해주세요. 계약서 요청·승인 단계 없이 당신의 프로필을 추가할 수 있습니다.\
                                 추가하실 회원에게 메뉴를 통해 생성가능한 '거래회원 등록 요청 링크'를 요청하세요. 손 쉽게 회원 추가가 가능합니다.",
      ascending: "오름차순",
      add_user: "회원 추가",
      all: "전체",
      all_papers: "전체 계약서",
      author: "작성자",
      back: "뒤로",
      bank_account: "입금계좌",
      basic: "필수",
      before_create_contract: "계약서 작성 전",
      button: "버튼",
      buyer: "임차인(매수인)",
      bjdong: "법정동(리)",
      brokerage: "중개",
      cancel: "취소",
      change: "변경",
      clear: "지우기",
      close: "닫기",
      company_info: "회사소개",
      connect_social: "소셜계정 연결",
      contact_us: "문의하기",
      confirm: "확인",
      copy: "복사",
      contract: "계약서",
      content: "내용",
      contractor_info: "계약자 정보",
      contractor_info_intro: "위 부동산의 계약자 정보는 아래와 같다.",
      created_at: "등록일",
      create_paper: "계약서 작성",
      create_profile: "프로필 생성",
      create_mandate: "위임장 생성",
      creating_profile_is_mandatory: "계약서 작성 전 프로필 생성은 필수입니다.",
      descending: "내림차순",
      default: "기본",
      delete: "삭제",
      deleted: "삭제할",
      delete_account: "회원 탈퇴",
      delete_confirm: "정말 삭제 하시겠습니까?",
      delete_profile_subtitle:
        "회원 아이디, 이메일, 성함이 정확히 일치해야 탈퇴 처리 되며, 작성된 프로필이 없는 경우에만 계정 DB는 완전히 삭제됩니다.\
      작성된 프로필이 있는 경우 계정은 더이상 이용할 수 없도록 처리되며, 데이터베이스를 향후 법적 분쟁 시 활용하기 위해 보존 됩니다. 보존되는 데이터는 본인에게만 제공되니 안심하셔도 됩니다.",
      delete_success: "정상적으로 삭제되었습니다.",
      deny: "거절",
      denied: "거절됨",
      desc_realestate: "부동산 기본정보(표시)",
      designator: "위임인",
      designee: "수임인",
      detail: "상세",
      edit: "수정",
      edit_registor_info: "가입정보 수정",
      email: "이메일",
      etc: "기타",
      error: "요청에 오류가 있습니다.",
      exact_correct_match: "완벽히 일치시 검색됨",
      expiry_date: "만료일",
      filter: "필터",
      footer_info: "상호명: 주식회사 큐룸 | 사업자등록번호: 246-86-01161",
      general: "일반",
      hide: "숨김",
      how_to_use: "이용방법",
      id: "ID",
      initialize: "초기화",
      image_file_size_error: "이미지 크기는 %{0}KB를 넘을 수 없습니다.",
      image_file_count_error: "%{0}개 이상의 이미지를 첨부할 수 없습니다.",
      image_file_type_error: "지원하지 않는 파일 종류 입니다.",
      info: "정보",
      insert_special_agreement: "특약을 입력해주세요.",
      intro: "본 부동산에 대하여 계약자 쌍방은 합의에 의하여 다음과 같이 계약을 체결한다.",
      landlord: "임대인",
      landlord_or_tenant: "당신은 임대인입니까? 임차인입니까?",
      language: "언어",
      language_change: "Language Change",
      last: "최종",
      learn_how_to_use: "이용방법 알아보기",
      link: "링크",
      list: "목록",
      link_is_copied: "링크가 복사 되었습니다.",
      load: "불러오기",
      load_list: "목록보기",
      load_default: "기본값 불러오기",
      load_more: "더 보기",
      load_special_agreement: "특약 불러오기",
      lookup_scope: "조회 범위",
      logout: "로그아웃",
      manage: "관리",
      manual_search: "직접검색",
      mandate: "위임",
      mandate_subtitle:
        "위임 기간 동안 위임인의 서명이 없어도 수임인이 작성한 계약서는 완료됩니다.",
      mandate_paper: "위임장",
      mandatory: "필수",
      manwon: "만원",
      menu: "메뉴",
      modify: "편집",
      modify_delete_deadline: "수정/삭제 가능기한",
      modify_delete_deadline_expired: "수정/삭제 가능기한 만료.",
      move: "이사",
      next: "다음",
      notice: "공지사항",
      no_mandate: "작성된 위임장이 없습니다.",
      no_paper: "작성된 계약서가 없습니다.",
      no_paper_redirect_to_all_paper: "계약자로 포함된 계약서가 없어 전체 계약서를 조회합니다.",
      no_profile: "생성된 프로필이 없습니다.",
      no_profile_cant_use_service: "서비스 이용전 프로필을 생성하여야 합니다.",
      none: "없음",
      number: "번호",
      onepaper: "원페이퍼",
      only_my_papers: "내 계약서",
      ordering: "정렬",
      password_change: "비밀번호 변경",
      partial_correct_match: "일부 일치시 검색됨",
      paper: "계약서",
      paper_subtitle:
        "더 나은 계약 문화를 만들기 위해 작성 계약서는 개인정보(성함, 세부지번 등)를 제외하고 전체 계약서 탭에서 누구나 조회 할 수 있습니다.",
      paper_requesting_subtitle:
        "요청 중 상태의 계약서는 요청이 필요한 모든 계약자가 승인 버튼을 누른 후 서명 및 계약자 정보를 확인할 수 있습니다.",
      profile: "프로필",
      permanence: "영속성",
      period: "기간",
      please_add_trade_user: "거래 회원을 프로필 조회 허용 리스트에 추가해주세요.",
      please_available_garantee_insurance: "현재일 기준으로 유효한 중개보증서류를 추가해주세요.",
      please_sign: "서명을 여기 해주세요.",
      pease_select_default_profile: "기본 프로필을 선택해주세요.",
      profile_name: "프로필명",
      profile_number: "프로필 번호",
      profile_list_subtitle:
        "프로필은 단 하나만 활성화 가능하며 계약서 작성시 사용됩니다. 빠른거래 회원 추가 시 검색 없이 상대방이 회원님의 프로필을 추가할 수 있습니다.",
      quick_trade_user: "빠른거래회원",
      quickness: "신속성",
      read_mode: "읽기모드",
      realestate: "부동산",
      realestate_agency: "개업공인중개사",
      required_item: "필수 입력 항목입니다",
      request: "요청",
      request_agent_account: "중개사 회원 신청",
      request_success: "요청이 처리되었습니다.",
      reviewing: "검토중",
      save: "제출",
      search: "검색",
      seller: "임대인(매도인)",
      send_your_link: "거래를 원하는 회원에게 링크를 전송하세요.",
      select: "선택",
      service_intro: "서비스 소개",
      special_agreement: "특약",
      special_agreement_basic_template: "",
      share: "공유",
      show: "보이기",
      show_paper: "계약서보임",
      sign: "(서명)",
      signature: "서명",
      signature_effect:
        "본 서명을 통해 종이계약 체결과 동일한 효력이 발생함에 동의하시면 서명해주세요.",
      signature_empty_warning: "서명을 비워둔 상태로 제출 할 수 없습니다.",
      status: "상태",

      submit: "제출",
      signature_and_submit: "서명 후 위임장 제출",
      trade: "거래",
      tenant: "임차인",
      terms_and_conditions: "계약내용",
      terms_and_conditions_intro: "위 부동산의 계약내용은 아래와 같다.",
      term_of_lease: "계약기간",
      title: "제목",
      transaction_category: "거래종류(매매,전세 등)*",
      updated_at: "수정일",
      user: "회원",
      use_profile_after_approval:
        "개업공인중개사 프로필은 첨부해주신 서류 검토 및 관리자 승인 후 사용 가능합니다.",
      unspport_function: "현재 페이지에서는 해당 기능이 제공되지 않습니다.",
      view_mobile_version: "모바일 버전 보기",
      view_pc_version: "원래대로 보기(인쇄용)",
      writing: "작성",
      written: "작성한",
      won: "원",
      won_paid_recieved: "원은 방문시 지불하고 영수함.",
      year: "년",

      //Tour translation
      done_tour: "종료",
      skip_tour: "다시보지 않기",
      start_tour:
        "👏원페이퍼를 이용해줘서 정말 감사해요!<br/>\
      여러분을 위한 서비스 가이드를 준비했어요.<br/>\
      함께 알아보려면 다음버튼을 눌러요.<br/>\
      가이드를 더이상 보지않으려면<br/>\
      다시보지 않기버튼을 눌러주세요.<br/>\
      가이드는 \
      <i data-v-e439781a='' aria-hidden='true' class='v-icon notranslate material-icons theme--light white--text text--darken-2'>help</i>\
      버튼으로 다시 볼수 있어요😊",
      tour_if_don_have_profile:
        "프로필이 없으시네요? <br/>\
      먼저 프로필 생성부터 해주세요😊😊",
      tour_home_menu:
        "상단메뉴 소개에요.<br/>\
        계약서 / 프로필 메뉴가 존재해요.<br/>\
        ✔️ 계약서 메뉴 - 계약서 조회/생성 <br/>\
        ✔️ 프로필 메뉴 - 계약자 정보를 생성/조회 <br/>\
        프로필은 재사용할 수 있지만, <br/>\
        주소 등이 바뀌면 다시 생성 해야해요",
      tour_paper_list:
        "작성 중인 계약서가 있군요? 축하해요🎉🎉<br/>\
        가이드와 함께 계약서를 검토볼까요?<br/>\
        검토하려면 계약서를 클릭해봐요😊😊",
      tour_toggle_menu:
        "좌측 메뉴에서는 상단 메뉴에 없는<br/>\
      추가적인 메뉴가 있으니 필요에 따라<br/>\
      활용하세요!",
      tour_help_menu:
        "도움말 버튼이에요.<br/>\
      이용에 어려움이 있을 때 눌러주세요!<br/>\
      가이드가 이용에 도움을 줄거에요.😊",
      tour_filter:
        "필터 메뉴소개<br/>\
      ✔️ 내 계약서 - 내가 포함된 계약서만 검색<br/>\
      ✔️ 전체계약서 - 타인 계약서까지 조회<br/>\
      ✔️ 필터 - 상태, 주소 등 계약서 세부검색",
      tour_create_paper_button_click: "계약서 작성을 위해 버튼 클릭!",

      //Tour paper-detail
      tour_paper_detail:
        "안녕하세요? 계약서 검토 도우미에요.😊😊\
        서비스 이용이 처음이라면 함께해봐요.",
      tour_paper_hide:
        "계약서 숨김을 하게 되면,<br/>\
        홈 화면에서 계약서가 노출되지 않아요.<br/>\
        <i data-v-e439781a='' aria-hidden='true' class='v-icon notranslate material-icons theme--light white--text text--darken-2'>help</i>\
        필터 버튼을 통해서 숨긴 계약서 조회가 가능해요.",
      tour_detail_desc_relesate:
        "부동산표시는 건물/토지대장으로 검토해요.<br/>\
      대장은 <a href='https://www.gov.kr/search/apply/?srhQuery=%EB%8C%80%EC%9E%A5&policyType=&sort=&dateDvs=&sdate=&edate=&sfield=' target='_blank' >정부24</a> PC에서 열람 가능해요. <br/>\
      정보 중 주소와 동/호는 절대 틀리면 안되요!",
      tour_detail_terms_and_conditions:
        "합의한것과 계약내용이 같은지 체크해요! <br/>\
    쉬운 내용이니 세부설명은 패스할게요. <br/>",
      tour_detail_contractor_info:
        "⚠️계약자 정보는 가장 중요한 사항이에요. <br/>\
      승인 후 세부정보 조회가 가능하며, <br/>\
      등기부/신분증 등으로 권한을 꼭 확인해요. <br/>",
      tour_approve:
        "요청 계약서가 맞으면 승인버튼을 눌러요<br/>\
        요청 계약서가 아니면 거절버튼을 눌러요😊<br/>\
        서명은 승인후 가능하고 특약검토 후 하세요",
      tour_requesting:
        "계약서를 승인하지 않은 계약자가 있어요.<br/>\
          상대방에게 승인버튼 클릭을 요청하세요.<br/>",
      tour_detail_special_agreement:
        "불공정한 특약이 없는지 확인하세요.<br/>\
        특약에 있더라도 무효인 경우가 있으니,<br/>\
        꼭 검토하세요 ex)강제퇴거특약",
      tour_signature:
        "서명을 원하시면 클릭 해주세오.<br/>\
      최초 서명 후 계약서는 24시간 이내에만<br/>\
      수정이 가능하고, 24시간 지나면 \
      계약서는 더이상 수정 할 수 없어요.",
      tour_ve:
        "확인설명서는 중개사가 설명해줄거에요<br/>\
      등기부기재사항은 꼼꼼히 확인하고,<br/>\
      권리분석을 꼭 해야해요<br/>\
      모바일에선 모바일버전보기를 클릭😊",
      tour_ve_signature:
        "계약자 모두가 서명버튼을 누르고 서명하면,<br/>\
      계약서는 완료상태로 자동으로 바뀌고,<br/>\
      계약서 수정은 더이상 할 수 없어요.",
      tour_done: "서명을 마치셨다면 축하드려요.<br/>\
      계약서 검토를 함께해서 행복했어요😊",

      //Tour paper-editor
      tour_create_paper:
        "당신의 계약서 작성 도우미에요.<br/>\
        첫 사용자는 저와 함께하는게 편할거에요.<br/>\
        기존사용자는 지금보지않기를 눌러도되요.<br/>\
        실수로 끈 경우 오른쪽 상단 \
        <i data-v-e439781a='' aria-hidden='true' class='v-icon notranslate material-icons theme--light white--text text--darken-2'>help</i>버튼을 \
        통해 다시 활성화 할 수 있어요^^",
      tour_select_landlord_tenant:
        "당신이 임대인인지,임차인인지 선택하세요.<br/>\
        선택에 따라 계약자를 자동으로 입력할게요.<br/>\
        이후 계약자정보에서 수정할 수 있어요.",
      tour_create_paper_title:
        "(필수)<br/>계약서 제목부터 입력 해볼까요?<br/>(선택)항목은 선택입력 할 수 있어요.",
      tour_desc_relesate:
        "부동산 기본정보는 건물/토지대장 참고작성.<br/>\
        대장은 <a href='https://www.gov.kr/search/apply/?srhQuery=%EB%8C%80%EC%9E%A5&policyType=&sort=&dateDvs=&sdate=&edate=&sfield=' target='_blank' >정부24</a> PC에서 열람 가능. <br/>\
        스마트폰은 앱스토어로 정부24 설치후 가능.",
      tour_paper_address:
        "주소검색창 클릭 후 입력칸을 통해 주소 입력<br/>\
      주소를 입력하기 전에 대장은 꼭 준비.",
      tour_paper_dong_ho:
        "실제동/호와 건물대장이 다를시 주의!<br/>\
      ex)건축물대장에 없는 동/호로 계약시,<br/>\
      보증금이 🚨위험🚨해요, 필수확인",
      tour_land_category: "토지대장 지목과 동일하게 작성해요",
      tour_lot_area: "토지대장 면적과 동일하게 작성해요",
      tour_buildling_structure: "건축물대장 주구조와 동일하게 작성해요",
      tour_buildling_category:
        "🎉🎉부동산 기본정보 완료까지 힘내요! <br/>건축물대장 주용도와 동일하게 작성해요",
      tour_buildling_area: "건축물대장 연면적과 동일하게 작성해요",
      tour_terms_and_conditions:
        "👏👏 드디어 계약정보란 입니다. <br/>\
      본 항목들은 합의한 내용 그대로 적으면되요. <br/>\
      쉬운 내용이니 세부설명은 패스! <br/>",
      tour_contractor_info:
        "⚠️계약자 정보는 가장 중요한 사항이에요. <br/>\
        등기부, 신분증등으로 권한을 꼭 확인해요.",
      tour_landlord_switch:
        "임대인/임차인 선택을 잘못하셨다면,<br/>\
        토글버튼을 눌러 재선택하세요.",
      tour_profile_search: "계약자 입력을 위해 직접검색 버튼을 클릭.",
      tour_profile_input: "상대방의 이메일 또는 연락처 입력 후 검색버튼 클릭",
      tour_profile_select:
        "검색 결과가 여러개인 경우<br/>\
      이메일 주소 확인 후 선택 버튼 클릭.",
      tour_special_agreement:
        "🎉🎉👏👏정말 축하해요!<br/>\
        추가특약 작성후 제출버튼을 눌러주세요.<br/>\
        ⚠️작성란이 가려질때 살짝위로 스크롤해서,<br/>\
        가이드가 안보이게 하시면 작성이 수월해요.",

      //Tour profile-editor
      tour_create_profile:
        "프로필 생성을 시작해볼까요?</br>(선택)항목은 입력하지 않으셔도 됩니다.",
      tour_address: "주소검색창 클릭 후 입력칸을 통해 주소 입력",
      tour_dong_ho: "입력 시 예처럼 동/호 문자빼고 입력. <br/> 예) 201, B",
      tour_mobile_number: "휴대폰 번호 입력(숫자만)",
      tour_bank:
        "은행명 선택 / 계좌번호 선택입력</br/>\
      입력을 원치 않는 분은 비워둬도되요.😊😊",
      tour_submit:
        "작성 내용을 다시 한번 확인해주세요.<br/>\
          내용에 이상이 없다면 제출하기 버튼 클릭",
      optional: "선택",

      //Bank List
      "--선택--": "--선택--",
      산업은행: "산업은행",
      부산은행: "부산은행",
      기업은행: "기업은행",
      광주은행: "광주은행",
      국민은행: "국민은행",
      제주은행: "제주은행",
      수협: "수협",
      전북은행: "전북은행",
      농협은행: "농협은행",
      경남은행: "경남은행",
      지역농축협: "지역농축협",
      새마을금고: "새마을금고",
      우리은행: "우리은행",
      신용협동조합: "신용협동조합",
      SC제일은행: "SC제일은행",
      상호저축은행: "상호저축은행",
      한국씨티은행: "한국씨티은행",
      산림조합: "산림조합",
      KEB하나은행: "KEB하나은행",
      우체국: "우체국",
      신한은행: "신한은행",
      K뱅크: "K뱅크",
      대구은행: "대구은행",
      카카오뱅크: "카카오뱅크",

      //Service Intro
      service_intro_title:
        "원페이퍼는 기술을 통해 부동산 거래 위험과 시간을 줄이는데 가치를 두고 있습니다.",
      service_intro_text1:
        "계약서 아직도 손으로 번거롭게 작성하고 계시나요?\
      썼던 내용 또 쓰고 계세요? 이제는 한번 쓴 내용은 불러와서 계약서 작성해보세요.\
      휴대폰, PC만 있으면 언제 어디서든 계약서를 작성할 수 있답니다.\
      <br/>당신과 타인의 거리를 좁혀드리겠습니다.",
      service_intro_text2:
        "계약서 분실을 더이상 걱정할 필요없습니다. 언제 어디서든 당신의 계약서를 확인하세요.\
      휴대폰, PC로 작성한 계약 데이터는 서비스 기간동안 AWS RDS에 안전하게 저장됩니다.\
      <br/>당신의 계약서를 영구히 보존해보세요.",
      service_intro_text3:
        "계약서를 어떻게 작성해야할지 모르겠다구요?\
      내가 쓴 계약서가 잘 작성되었는지 걱정 되시나요?\
      당신이 작성한 계약서를 공유하고, 친구가 작성한 계약서를 공유받으세요.\
      그리고 잘 작성된 계약서를 참고해보세요. \
      <br/>더 나은 계약서를 작성할 수 있을거에요.",
      //Profile message
      birthday: "생일",
      name: "성함",
      mobile_number: "연락처",
      bank_name: "은행명",
      account_number: "계좌",
      registration_number: "등록번호",
      shop_name: "상호명",
      shop_address: "사무실 주소",
      registration_certificate: "중개사 등록증",
      agency_license: "자격증",
      stamp: "인장",
      insurance: "보증서",
      garantee_insurance: "중개보증서류",

      area: "면적",
      address: "주소",
      dong: "동",
      ho: "호",
      land_category: "지목",
      lot_area: "토지면적",
      room_name: "방이름",
      building_structure: "건물구조",
      building_category: "건물용도",
      building_area: "건물면적",
      realestate_category: "부동산종류",
      trade_category: "계약 종류",

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
      purchase: "매매",
      exchange: "교환",

      requesting: "요청중",
      draft: "작성중",
      progress: "서명중",
      done: "완료",
      hidden: "숨긴",

      //for verifying_explanation
      enforcement_rules: "■ 공인중개사법 시행규칙 [별지 제20호서식]",
      ve_amendment_updated_date: "개정 2021. 1. 12.",
      ve_subject: "중개대상물 확인·설명서[Ⅰ] (주거용 건축물)",
      materials_for_ve: "확인ㆍ설명자료",
      explanation_evidence: "확인ㆍ설명 근거자료 등",
      explanation_evidence_info: "대상물건의 상태에 관한 자료요구 사항",
      land_area: "토지면적",
      ledger_land_category: "공부상지목",
      actual_land_category: "토지실제이용상태",
      net_area: "전용면적",
      land_share: "대지지분",
      year_of_completion: "준공년도",
      ledger_building_category: "건축물 대장상용도",
      actual_building_category: "건축물 실제용도",
      building_direction: "건물 방향",
      seismic_design: "내진설계 적용여부",
      seismic_capacity: "내진능력",
      legal_status: "건축물 대장상 위반건축물 여부",
      matters_of_violation: "위반내용",
      land_ownership: "토지 소유권에 관한 사항",
      building_ownership: "건축물 소유권에 관한 사항",
      land_other: "토지 소유권 외의 권리사항",
      building_other: "건축물 소유권 외의 권리사항",
      rental_housing_registration: "민간임대 등록여부",
      use_area: "용도지역",
      use_district: "용도지구",
      use_zone: "용도구역",
      building_coverage_limit: "건폐율 상한",
      floor_area_limit: "용적률 상한",
      planning_facilities: "도시ㆍ군계획시설",
      permission_report_zone: "허가ㆍ신고구역여부",
      speculative_area: "투기지역 여부",
      unit_planning_area_others: "지구단위계획구역ㆍ그 밖의 도시ㆍ군관리계획",
      other_use_restriction: "그 밖의 이용제한 및 거래규제사항",
      relative_with_roads: "도로와의 관계",
      is_paved_rode: "포장 여부",
      accessibility: "접근성",
      bus_stop: "버스 정류장",
      bus_by_foot: "버스 도보 이용여부",
      bus_required_time: "버스 정류장 도착 소요시간",
      subway_station: "지하철역",
      subway_by_foot: "지하철 도보 이용여부",
      subway_required_time: "지하철역 도착 소요시간",
      parking_lot: "주차장",
      parking_lot_info: "주차장 상세정보",
      elementary_school: "초등학교",
      elementary_school_by_foot: "초등학교 도보 이용여부",
      elementary_school_required_time: "초등학교 도착 소요시간",
      middle_school: "중학교",
      middle_school_by_foot: "중학교 도보 이용여부",
      middle_school_required_time: "중학교 도착 소요시간",
      high_school: "고등학교",
      high_school_by_foot: "고등학교 도보 이용여부",
      high_school_required_time: "고등학교 도착 소요시간",
      department_store: "백화점",
      department_store_by_foot: "백화점 도보 이용여부",
      department_store_required_time: "백화점 도착 소요시간",
      medical_center: "병원",
      medical_center_by_foot: "병원 도보 이용여부",
      medical_center_required_time: "병원 도착 소요시간",
      is_security_office: "경비실 여부",
      management: "관리주체",
      undesirable_facilities: "비선호시설",
      undesirable_facilities_info: "비선호시설 종류 및 위치",
      expected_transaction_price: "거래예정금액",
      land_prcie_recorded: "개별공시지가",
      building_price_recorded: "건물(주택)공시가격",
      acquisition_tax: "취득세",
      special_tax: "농어촌특별세",
      local_education_tax: "지방교육세",
      water_damage_status: "수도 파손여부",
      water_damage_status_info: "수도 파손 상세정보",
      water_capacity_status: "수도 용수량",
      water_capacity_status_info: "수도 용수량 상세정보",
      electricity_supply_status: "전기 공급상태",
      electricity_supply_status_info: "전기 공급상태 상세정보",
      gas_supply_status: "가스 공급방식",
      gas_supply_status_info: "가스 공급방식 상세정보",
      is_fire_alarm_detector: "소방경보감지기 여부",
      fire_alarm_detector_quantity: "소방경보감지기 수량",
      heating_supply_method: "난방 공급방식",
      heating_status: "난방 상태",
      heating_status_info: "난방 상태 상세정보",
      heating_type: "난방 종류",
      heating_type_info: "난방 종류 상세정보",
      is_elevator: "승강기 여부",
      elevator_status: "승강기 상태",
      drainage_status: "배수 상태",
      drainage_status_info: "배수 상태 상세정보",
      other_facilities: "그 밖의 시설물",
      wall_crack_status: "벽면 균열 여부",
      wall_crack_status_info: "벽면 균열 위치",
      water_leak_status: "벽면 누수 여부",
      water_leak_status_info: "벽면 누수 위치",
      wall_paper_status: "도배 상태",
      wall_paper_status_info: "도배 필요 상세정보",
      sunshine_status: "일조량",
      sunshine_status_info: "일조량 불충분 이유",
      noise_status: "소음",
      vibration: "진동",
      comission: "중개보수",
      actual_expenses: "실비",
      payment_period: "지급시기",
      calculation_info: "합계",
      verifying_explanation: "확인설명서"
    }
  }
});

export default i18n;
