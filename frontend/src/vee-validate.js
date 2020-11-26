import i18n from "@/plugins/i18n";
import { extend, configure } from "vee-validate";
import { integer, email, required, max, regex } from "vee-validate/dist/rules";

configure({
  defaultMessage: (_, values) => {
    return i18n.t(`validation.${values._rule_}`, values);
  }
});
extend("required", required);
extend("integer", integer);
extend("max", max);
extend("email", email);
extend("regex", regex);
extend("mobile", {
  validate(value) {
    // return /(^01.{1}|[0|1|6|7|8|9]{3})([0-9]+)([0-9]{4})/g.test(value);
    return /^01([0|1|6|7|8|9])-([0-9]{3,4})-([0-9]{3,4})$/.test(value);
  },
  message(_, values) {
    return i18n.t("validation.regex", values);
  }
});
