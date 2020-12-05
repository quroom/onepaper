function applyValidation(data, self, key, parent_key) {
  if(key=="detail") {
    alert(data);
    return;
  }
  Object.keys(data).forEach(function(key2){
    if(key2 != 0 ){
      applyValidation(data[key2], self, key2, key)
    }
  })
  if(self != undefined){
    if(parent_key != undefined){
      if(self.$refs[parent_key] != undefined) {
        if(self.$refs[parent_key].$refs[key] != undefined){
          // console.log(parent_key,":", key)
          if(!self.$refs[parent_key].$refs[key]._isVue){
            const ref = self.$refs[parent_key].$refs[key].length == undefined ? self.$refs[parent_key].$refs[key] : self.$refs[parent_key].$refs[key][0];
            ref.applyResult({
              errors: data,
              valid: false,
              failedRules: {}
            });
          }
        }
      }
    } else {
      if(self.$refs[key] != undefined) {
        console.log(key)
        if(!self.$refs[key]._isVue){
          const ref = self.$refs[key].length == undefined ? self.$refs[key] : self.$refs[key][0];
          ref.applyResult({
            errors: data,
            valid: false,
            failedRules: {}
          });
        }
      }
    }
  }
}

export { applyValidation };