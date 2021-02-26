// import Vue from 'vue'
import i18n from "@/plugins/i18n";

const Constants = {
  BANK_CATEGORY: {
    '' : '--선택--',
    '002' : '산업은행',
    '032' : '부산은행',
    '003' : '기업은행',
    '034' : '광주은행',
    '004' : '국민은행',
    '035' : '제주은행',
    '007' : '수협',
    '037' : '전북은행',
    '011' : '농협은행',
    '039' : '경남은행',
    '012' : '지역농축협',
    '045' : '새마을금고',
    '020' : '우리은행',
    '048' : '신용협동조합',
    '023' : 'SC제일은행',
    '050' : '상호저축은행',
    '027' : '한국씨티은행',
    '064' : '산림조합',
    '081' : 'KEB하나은행',
    '071' : '우체국',
    '088' : '신한은행',
    '089' : 'K뱅크',
    '031' : '대구은행',
    '090' : '카카오뱅크'
  },
  LAND_CATEGORY : {
    7: 'buildingland',
    100: "etc"
  },
  BUILDING_CATEGORY: {
    70: "c1neighborfacility",
    71: "c2neighborfacility",
    80: "house",
    81: "apartment",
    100: "etc",
  },
  // REALESTATE_CATEGORY: {
  //   0: "oneroom",
  //   1: "tworoom",
  //   2: "threeroom",
  //   3: "fourroom",
  //   4: "sharehouse",
  //   5: "officetel",
  //   20: "aprtment",
  //   21: "vailla",
  //   22: "house",
  //   23: "commercialhouse",
  //   40: "store",
  //   41: "land",
  //   99: "etc",
  // },
  TRADE_CATEGORY: {
    0: "rent",
    1: "depositloan",
    // 2: "purchase",
    // 3: "exchange",
  },
  STATUS_CATEGORY: {
    0: "requesting",
    1: "draft",
    2: "progress",
    3: "done",
  },
  CONTRACTOR_CATEGORY: {
    0: "seller",
    1: "buyer",
    2: "expert"
  },
  EXPERT_STATUS: {
    0: "requesting",
    1: "approved",
    2: "denied",
    3: "closed"
  },
  BANK_CATEGORY_LIST: [],
  LAND_CATEGORY_LIST: [],
  BUILDING_CATEGORY_LIST: [],
  // REALESTATE_CATEGORY_LIST: [],
  TRADE_CATEGORY_LIST: [],
  STATUS_CATEGORY_LIST: [],
  CONTRACTOR_CATEGORY_LIST: [],
  EXPERT_STATUS_LIST: []
};
Constants.install = function(Vue) {
  Object.keys(Constants).forEach(function(key){
    if(key.indexOf('_LIST') < 0 && key.indexOf('install') < 0){
      Object.keys(Constants[key]).forEach(function(type_val){
        const val = type_val
        const name = Constants[key][val]
        Constants[key+'_LIST'].push({text: name, value:Number(val)})
      })
    }
  })
  Vue.prototype.$getConst = (type, key) => {
    type = type.toUpperCase();
    key = type.toLowerCase()
    return Constants[type][key];
  };
  Vue.prototype.$getConstList = (type) => {
    type = type.toUpperCase();
    return Constants[type];
  };  
  Vue.prototype.$getConstI18 = (type, key) => {
    type = type.toUpperCase();
    return Constants[type][key] ? i18n.t(Constants[type][key]) : key;
  };
  Vue.prototype.$getConstByName = (type, val) => {
    type = type.toUpperCase();
    val = val.toLowerCase();
    let object = Constants[type];
    return Object.keys(object).find(key => object[key] === val);
  };
};

export default Constants;
