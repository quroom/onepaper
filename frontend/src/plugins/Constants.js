// import Vue from 'vue'
import i18n from "@/plugins/i18n";

const Constants = {
  BANK_CATEGORY: {
    0: "--선택--",
    2: "산업은행",
    32: "부산은행",
    3: "기업은행",
    34: "광주은행",
    4: "국민은행",
    35: "제주은행",
    7: "수협",
    37: "전북은행",
    11: "농협은행",
    39: "경남은행",
    12: "지역농축협",
    45: "새마을금고",
    20: "우리은행",
    48: "신용협동조합",
    23: "SC제일은행",
    50: "상호저축은행",
    27: "한국씨티은행",
    64: "산림조합",
    81: "KEB하나은행",
    71: "우체국",
    88: "신한은행",
    89: "K뱅크",
    31: "대구은행",
    90: "카카오뱅크"
  },
  LAND_CATEGORY: {
    7: "buildingland",
    99: "etc"
  },
  BUILDING_CATEGORY: {
    70: "c1neighborfacility",
    71: "c2neighborfacility",
    80: "house",
    81: "apartment",
    99: "etc"
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
    1: "rent",
    2: "depositloan"
    // 2: "purchase",
    // 3: "exchange",
  },
  STATUS_CATEGORY: {
    0: "done",
    1: "requesting",
    2: "draft",
    3: "progress"
  },
  CONTRACTOR_CATEGORY: {
    1: "seller",
    2: "buyer",
    3: "expert"
  },
  EXPERT_STATUS: {
    0: "closed",
    1: "requesting",
    2: "approved",
    3: "denied"
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
  Object.keys(Constants).forEach(function(key) {
    if (key.indexOf("_LIST") < 0 && key.indexOf("install") < 0) {
      Object.keys(Constants[key]).forEach(function(type_val) {
        const val = type_val;
        const name = Constants[key][val];
        Constants[key + "_LIST"].push({ text: name, value: Number(val) });
      });
    }
  });
  Vue.prototype.$getConst = (type, key) => {
    type = type.toUpperCase();
    key = type.toLowerCase();
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
    return Object.keys(object).find((key) => object[key] === val);
  };
};

export default Constants;
