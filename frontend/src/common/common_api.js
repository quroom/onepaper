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

function getKeys(object) {
  return Object
      .entries(object)
      .reduce((r, [k, v]) =>{
          return r.concat(v && typeof v === 'object'
              ? getKeys(v).map(sub => [k].concat(sub))
              : v
          )},
          []
      );
}

function applyValidation(data, that) {
  console.log(data)
  var flag = true;
  if(data.count==0){
    alert("조회된 데이터가 없습니다.")
    return true;
  }
  if(data["detail"]) {
    alert(data["detail"]);
    return true;
  }
  var result = getKeys(data)
  result.map(arr => {
    console.log(arr)
    const parent_key = arr[arr.length-3]
    const vp_key = arr[arr.length-2]
    const error_message = arr[arr.length-1]
    if(that.$refs[vp_key]) {
      const ref = that.$refs[vp_key].length == undefined ? that.$refs[vp_key] : that.$refs[vp_key][0];
      if(ref._isVue) {
        flag = false;
        ref.applyResult({
          errors: error_message,
          valid: false,
          failedRules: {}
        });
      }
    } else {
      if(parent_key && that.$refs[parent_key] && that.$refs[parent_key].$refs[vp_key]) {
          const ref = that.$refs[parent_key].$refs[vp_key].length == undefined ? that.$refs[parent_key].$refs[vp_key] : that.$refs[parent_key].$refs[vp_key][0];
          if(ref._isVue){
            flag = false;
            ref.applyResult({
              errors: error_message,
              valid: false,
              failedRules: {}
            });
          }
      }
    }
  })
  if(flag == true){
    data = renameKeys(data, that)
    alert(JSON.stringify(data))
    return true;
  }
}

export { applyValidation };