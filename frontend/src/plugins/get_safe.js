const getSafe = {
  install(Vue){
    Vue.prototype.$get = function(obj, key, default_value = "") {
      const value = key.split(".").reduce(function(o, x) {
        if(default_value != undefined){
          return !o ? default_value : o[x];
        } else {
          return !o ? o : o[x];
        }
      }, obj);
      if(!value){
        return default_value == "" ? default_value : value;
      } else {
        return value;
      }
    }
  }
}

export default getSafe;
