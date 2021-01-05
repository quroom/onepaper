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
      add_quick_trade_user: "Add quick trade user",
      add_quick_trade_user_directly: "Add quick trade user directly",
      add_quick_trader_link: "Quick trade request link",
      accept: "Aceept",
      activate: "Activate",
      and: "and",
      attached_document: "Attached Document",
      allow: "Allowed",
      quick_trade_user_list: "List of quick trading members",
      quick_trade_user_list_subtitle: "Please add quick trade memebers. You can add your profile without the contract request·approval step. \
      Please ask additional members for the'Trade Member Registration Request Link' through the menu. You can easily add members.",
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
      create_paper: "Create Paper",
      create_profile: "Create Profile",
      create_mandate: "Create Mandate",
      confirm: "Confirm",
      copy: "Copy",
      default: "Default",
      desc_realestate: "Description of Realestate",
      designator: "designator",
      designee: "designee",
      delete: "Delete",
      deleted: "Deleted",
      delete_account: "Delete Account",
      delete_confirm: "Do you really want to delete?",
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
      garantee_insurance: "Brokerage Garantee Insurance",
      general: "General",
      hide: "Hide",
      id: "ID",
      image_file_size_error: "Image file size can't be over %{0} KB.",
      image_file_count_error: "You can't upload over %{0} images.",
      image_file_type_error: "Only images can be uploaded here.",
      info: "Info",
      insert_special_agreement: "Insert special agreement",
      intro: "This is realestate contract that is made by traders.",
      landlord: "Landlord",
      language: "Language",
      last: "Last",
      link: "Link",
      list: "List",
      link_is_copied: "Link is copied",
      load: "Load",
      load_more: "Load More",
      logout: "Logout",
      mandate: "Mandate",
      mandate_subtitle: "During the mandate period, the designee may complete the contract without the representative's signature.",
      mandate_paper: "Power of Attorney",
      manwon: "ten thousand Won",
      modify: "Modify",
      move: "Move",
      next: "Next",
      no_mandate: "There is no mandate",
      no_paper: "There is no paper. Write your first paper.",
      no_profile: "There is no profile",
      no_profile_cant_use_service:
        "You must create profile before using service.",
      number: "Number",
      partial_correct_match: "Partially Correct is Matched",
      paper: "Paper",
      paper_subtitle: "This contract can be viewed by anyone to create a better contract culture, excluding personal information (name, contact number, lot number, etc.).",
      paper_requesting_subtitle: "Contracts in the requesting state can be signed and contractor information can be checked after all contractors requiring the request press the Approve button.",
      profile: "Profile",
      period: "Period",
      please_add_trade_user: "Please add user allowed to view profile",
      please_sign: "Please sign here.",
      pease_select_default_profile: "Please select default profile.",
      profile_name: "Profile Name",
      profile_list_subtitle: "This activated profile will be used in contract paper.",
      quick_trade_user: "Quick trade user",
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
      special_agreement: "Special Agreement",
      special_agreement_basic_template: "",
      status: "status",
      sign: "Signature",
      signature: "Sign",
      signature_empty_warning: "Signature can't be empty",
      stamp: "Stamp",
      submit: "Submit",
      signature_and_submit: "Submit mandate after signature",
      trade: "Trade",
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
      use_profile_after_approval: "The profile of a certified practitioner can be used after reviewing the attached documents and approval.",
      writing: "writing",
      written: "Written",
      won: "Won",
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

      requesting: "Requesting",
      draft: "Draft",
      progress: "Progress",
      done: "Done",
      hidden: "Hidden",

      //for verifying_explanation
      enforcement_rules: "■ 공인중개사법 시행규칙 [별지 제20호서식]",
      ve_updated_date: "Updated 2020. 10. 27.",
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
      verifying_explanation: "Verifying Explanation Manual",
    },
    ko: {
      validation: ko.messages,
      add_quick_trade_user: "빠른거래 회원 추가",
      add_quick_trade_user_directly: "빠른거래 회원 즉시추가",
      add_quick_trader_link: "빠른거래 등록 요청 링크",
      accept: "동의합니다.",
      activate: "활성화",
      and: "및",
      attached_document: "첨부 서류",
      allow: "허용",
      approve: "승인",
      approved: "승인됨",
      quick_trade_user_list: "빠른거래 회원 리스트",
      quick_trade_user_list_subtitle: "빠른 거래 회원을 추가 해주세요. 계약서 요청·승인 단계 없이 당신의 프로필을 추가할 수 있습니다.\
                                 추가하실 회원에게 메뉴를 통해 생성가능한 '거래회원 등록 요청 링크'를 요청하세요. 손 쉽게 회원 추가가 가능합니다.",
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
      create_paper: "계약서 작성",
      create_profile: "프로필 생성",
      create_mandate: "위임장 생성",
      confirm: "확인",
      copy: "복사",
      contract: "계약서",
      content: "내용",
      contractor_info: "계약자 정보",
      contractor_info_intro: "위 부동산의 계약자 정보는 아래와 같다.",
      default: "기본",
      delete: "삭제",
      deleted: "삭제할",
      delete_account: "회원 탈퇴",
      delete_confirm: "정말 삭제 하시겠습니까?",
      delete_success: "정상적으로 삭제되었습니다.",
      deny: "거절",
      denied: "거절",
      desc_realestate: "부동산 기본정보(표시)",
      designator: "위임인",
      designee: "수임인",
      detail: "상세",
      edit: "수정",
      edit_registor_info: "가입정보 수정",
      email: "이메일",
      etc: "기타",
      error: "요청에 오류가 있습니다.",
      exact_correct_match: "완벽히 일치 해야 검색됨",
      general: "일반",
      hide: "숨김",
      id: "ID",
      image_file_size_error: "이미지 크기는 %{0}KB를 넘을 수 없습니다.",
      image_file_count_error: "%{0}개 이상의 이미지를 첨부할 수 없습니다.",
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
      list: "목록",
      link_is_copied: "링크가 복사 되었습니다.",
      load: "불러오기",
      load_more: "더 보기",
      logout: "로그아웃",
      mandate: "위임",
      mandate_subtitle: "위임 기간 동안 수임인은 위임인의 서명 없이 계약서를 완료할 수 있습니다.",
      mandate_paper: "위임장",
      modify: "편집",
      move: "이사",
      next: "다음",
      no_mandate: "작성된 위임장이 없습니다.",
      no_paper: "작성된 계약서가 없습니다. 계약서를 작성해보세요.",
      no_profile: "생성된 프로필이 없습니다.",
      no_profile_cant_use_service: "서비스 이용전 프로필을 생성하여야 합니다.",
      number: "번호",
      partial_correct_match: "일부 일치해도 검색됨",
      paper: "계약서",
      paper_subtitle: "본 계약서는 개인정보(성함, 연락처, 지번 등)를 제외하고 더 나은 계약 문화를 만들기 위해 누구나 조회 할 수 있습니다.",
      paper_requesting_subtitle: "요청 중 상태의 계약서는 요청이 필요한 모든 계약자가 승인 버튼을 누른 후 서명 및 계약자 정보를 확인할 수 있습니다.",
      profile: "프로필",
      period: "기간",
      please_add_trade_user:
        "거래 회원을 프로필 조회 허용 리스트에 추가해주세요.",
      please_sign: "서명을 여기 해주세요.",
      pease_select_default_profile: "기본 프로필을 선택해주세요.",
      profile_name: "프로필명",
      profile_list_subtitle:
        "활성화된 프로필은 계약서 작성 시 계약자 정보로 자동 입력 가능합니다. 프로필은 단 하나만 활성화 가능합니다.",
      quick_trade_user: "빠른거래 회원",
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
      send_your_link: "거래를 원하는 회원에게 링크를 전송하세요.",
      select: "선택",
      special_agreement: "특약",
      special_agreement_basic_template: "",
      status: "상태",
      sign: "(서명)",
      signature: "서명",
      signature_empty_warning: "서명을 비워둔 상태로 제출 할 수 없습니다.",
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
      username: "회원 아이디",
      use_profile_after_approval: "개업공인중개사 프로필은 첨부해주신 서류 검토 및 관리자 승인 후 사용 가능합니다.",
      writing: "작성",
      written: "작성한",
      won: "원",
      won_paid_recieved: "원은 방문시 지불하고 영수함.",

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
      garantee_insurance: "중개 보증 서류",

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
      ve_updated_date: "개정 2020. 10. 27.",
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
      medical_center: "병운",
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
      verifying_explanation: "확인설명서",
    },
  },
});

export default i18n;
