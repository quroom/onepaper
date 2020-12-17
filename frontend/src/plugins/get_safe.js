const getSafe = {
  install(Vue){
    Vue.prototype.$get = function(obj, key, default_value) {
      return key.split(".").reduce(function(o, x) {
        if(default_value != undefined){
          return (typeof o == "undefined" || o === null) ? default_value : o[x];
        } else {
          return (typeof o == "undefined" || o === null) ? o : o[x];
        }
          
      }, obj);
    }
  }
}

export default getSafe;