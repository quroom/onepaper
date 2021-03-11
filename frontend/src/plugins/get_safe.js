const getSafe = {
  install(Vue){
    Vue.prototype.$get = function(obj, key, default_value = "") {
      return key.split(".").reduce(function(o, x) {
        if(default_value != undefined){
          return !o ? default_value : o[x];
        } else {
          return !o ? o : o[x];
        }
      }, obj);
    }
  }
}

export default getSafe;
