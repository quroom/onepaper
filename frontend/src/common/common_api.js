function renameKeys(obj, newKeys, that) {
  Object.keys(obj).map((key) => {
    let newKey = that.$i18n.t(key)
    if (Array.isArray(obj[key]) == false) {
      renameKeys(obj[key], newKeys, that);
    }
    // console.log(newKey, "]", obj[key]);
    obj[newKey]=obj[key];
    delete obj[key];
  });
}


function applyValidation(data, that, key, parent_key) {
  var flag;
  if(data.count==0){
    alert("조회할 수 있는 데이터가 없습니다.")
    return true;
  }
  if(data["detail"]) {
    alert(data["detail"]);
    return true;
  }
  Object.keys(data).forEach(function(key2){
    if(key2 != 0 ){
      flag = applyValidation(data[key2], that, key2, key)
    }
  })
  if(that != undefined){
    if(parent_key != undefined){
      if(that.$refs[parent_key] != undefined) {
        if(that.$refs[parent_key].$refs[key] != undefined){
          if(that.$refs[parent_key].$refs[key]._isVue){
            const ref = that.$refs[parent_key].$refs[key].length == undefined ? that.$refs[parent_key].$refs[key] : that.$refs[parent_key].$refs[key][0];
            if(ref.applyResult === undefined){
              return true
            }
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
        if(that.$refs[key]._isVue){
          const ref = that.$refs[key].length == undefined ? that.$refs[key] : that.$refs[key][0];
          
          if(ref.applyResult === undefined){
            return true
          }
          ref.applyResult({
            errors: data,
            valid: false,
            failedRules: {}
          });
        }
      }
    }
  }
  if(flag == true){
    renameKeys(data, undefined, that)
    alert(JSON.stringify(data))
    return true;
  }
}

export { applyValidation };