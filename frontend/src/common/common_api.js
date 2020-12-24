function renameKeys(obj, that) {
  const keyValues = Object.entries(obj).map(([key, value]) => {
    let newKey = that.$i18n.t(key);
    if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      value = renameKeys(value, that);
    }
    return [newKey, value];
  });
  return Object.fromEntries(keyValues);
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
    data = renameKeys(data, that)
    alert(JSON.stringify(data))
    return true;
  }
}

export { applyValidation };