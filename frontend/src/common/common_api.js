function applyValidation(data, that, key, parent_key) {
  if(data.count==0){
    alert("조회할 수 있는 데이터가 없습니다.")
    return;
  }
  if(key=="detail") {
    alert(data);
    return;
  }
  Object.keys(data).forEach(function(key2){
    if(key2 != 0 ){
      applyValidation(data[key2], that, key2, key)
    }
  })
  if(that != undefined){
    if(parent_key != undefined){
      if(that.$refs[parent_key] != undefined) {
        if(that.$refs[parent_key].$refs[key] != undefined){
          // console.log(parent_key,":", key)
          if(that.$refs[parent_key].$refs[key]._isVue){
            const ref = that.$refs[parent_key].$refs[key].length == undefined ? that.$refs[parent_key].$refs[key] : that.$refs[parent_key].$refs[key][0];
            ref.applyResult({
              errors: data,
              valid: false,
              failedRules: {}
            });
          }
        }
      }
    } else {
      if(that.$refs[key] != undefined) {
        console.log(key)
        if(that.$refs[key]._isVue){
          const ref = that.$refs[key].length == undefined ? that.$refs[key] : that.$refs[key][0];
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