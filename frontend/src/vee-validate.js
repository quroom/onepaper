import i18n from "@/plugins/i18n";
import { extend, configure } from "vee-validate";
import { required, max_value, regex, size } from "vee-validate/dist/rules";

configure({
  defaultMessage: (_, values) => {
    return i18n.t(`validation.${values._rule_}`, values);
  }
});
extend("required", required);
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
