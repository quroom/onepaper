function applyValidation(self, data, key, parent_key) {
  if(key=="detail") {
    alert(data[key]);
    return;
  }
  Object.keys(data).forEach(function(key2){
    if(key2 != 0 ){
      applyValidation(self, data[key2], key2, key)
    }
  })

  // console.log(parent_key, ":", key)
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

export { applyValidation };

// function applyValidation(self, data, key, previous_key) {
//   if(key=="detail") {
//     alert(data[key]);
//     return;
//   }
//   if(key != 0 ){
//     Object.keys(data).forEach(function(key2){
//       self.applyValidation(self, data[key2], key2, key)
//     })
//   } else {
//     if(self.$refs[previous_key] != undefined){
//       const ref = self.$refs[previous_key].length == undefined ? self.$refs[previous_key] : self.$refs[previous_key][0];
//       ref.applyResult({
//         errors: data,
//         valid: false,
//         failedRules: {}
//       });  
//     }
//     return;
//   }      
// }

// export { applyValidation };