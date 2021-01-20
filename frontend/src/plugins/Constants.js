// import Vue from 'vue'
import i18n from "@/plugins/i18n";

const Constants = {
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
