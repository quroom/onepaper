import i18n from "@/plugins/i18n";

const Constants = {
  LAND_TYPE : {
    7: 'buildingland'
  },
  BUILDING_TYPE: {
    70: "c1neighborfacility",
    71: "c2neighborfacility",
    80: "house",
    81: "apartment",
    100: "etc",
  },
  // REALESTATE_TYPE: {
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
  TRADE_TYPE: {
    0: "rent",
    1: "depositloan",
    // 2: "trade",
    // 3: "exchange",
  },
  STATUS_TYPE: {
    0: "draft",
    1: "done",
    2: "confirm",
    3: "hidden"
  },
  CONTRACTOR_TYPE: {
    0: "seller",
    1: "buyer",
    2: "expert"
  },
  LAND_TYPE_LIST: [],
  BUILDING_TYPE_LIST: [],
  // REALESTATE_TYPE_LIST: [],
  TRADE_TYPE_LIST: [],
  STATUS_TYPE_LIST: [],
  CONTRACTOR_TYPE_LIST: []
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

  Vue.prototype.$getConst = (type) => {
    type = type.toUpperCase();
    return Constants[type];
  };
  
  Vue.prototype.$getConstI18 = (type, key) => {
    type = type.toUpperCase();
    return Constants[type][key] ? i18n.t(Constants[type][key]) : key;
  };
  Vue.prototype.$getConstByName = (type, val) => {
    type = type.toUpperCase();
    let object = Constants[type];
    return Object.keys(object).find(key => object[key] === val);
  };
};

export default Constants;
