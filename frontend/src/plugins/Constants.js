const Constants = {
  ITEM_TYPE: {
    1: "원룸",
    2: "투룸",
  }
};

Constants.install = function (Vue) {
  Vue.prototype.$getConst = (type, key) => {
    return Constants[type][key]
  }
}

export default Constants;