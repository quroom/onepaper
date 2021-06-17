import i18n from "@/plugins/i18n";
import { extend, configure } from "vee-validate";
import { max, max_value, regex, required, size } from "vee-validate/dist/rules";

configure({
  defaultMessage: (_, values) => {
    return i18n.t(`validation.${values._rule_}`, values);
  }
});
extend("required", required);
extend("max", max);
extend("max_value", max_value);
extend("regex", regex);
extend("size", size);
extend("mobile", {
  validate(value) {
    // return /(^01.{1}|[0|1|6|7|8|9]{3})([0-9]+)([0-9]{4})/g.test(value);
    return /^01([0|1|6|7|8|9])-([0-9]{3,4})-([0-9]{3,4})$/.test(value);
  },
  message(_, values) {
    return i18n.t("validation.regex", values);
  }
});
extend("date_required", {
  validate(dates) {
    if (!dates || !dates[0] || !dates[1]) {
      return false;
    }
    return true;
  },
  message() {
    return "시작일과 종료일을 모두 입력해주세요.";
  }
});
extend("period", {
  validate(dates) {
    if (!dates || dates[1] < dates[0]) {
      return false;
    } else {
      return true;
    }
  },
  message() {
    return "보증서류 종료일이 시작일보다 작을 수 없습니다.";
  }
});
