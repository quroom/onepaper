import i18n from "@/plugins/i18n";

const Constants = {
  REALESTATE_TYPE: {
    1: "oneroom",
    2: "tworoom",
    3: "threeroom",
    4: "fourroom",
    5: "sharehouse",
    6: "officetel",
    20: "aprtment",
    21: "vailla",
    22: "house",
    23: "commercialhouse",
    40: "store",
    41: "land",
  },
  TRADE_TYPE: {
    1: "rent",
    2: "depositloan",
    3: "trade",
    4: "exchange",
  },
  STATUS_TYPE: {
    1: "draft",
    2: "done",
    3: "hidden"
  },
  REALESTATE_TYPE_LIST: [],
  TRADE_TYPE_LIST: [],
  STATUS_TYPE_LIST: [],
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
    return i18n.t(Constants[type][key]);
  };
  Vue.prototype.$getConstByVal = (type, val) => {
    type = type.toUpperCase();
    let object = Constants[type];
    return Object.keys(object).find(key => object[key] === val);
  };
};

export default Constants;
