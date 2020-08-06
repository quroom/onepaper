import { extend, configure } from "vee-validate";
import { integer, required, email, max } from "vee-validate/dist/rules";
import {i18n} from '@/plugins/i18n';

configure({
  defaultMessage: (_, values) => {
      return i18n.t(`validation.${values._rule_}`, values);
  }
});
extend('required', required);
extend('integer', integer);
extend("max", max);
extend("email", email);