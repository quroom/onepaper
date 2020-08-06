import Vue from "vue";
import VueI18n from 'vue-i18n'
import en from "vee-validate/dist/locale/en.json";
import ko from "vee-validate/dist/locale/ko.json";

Vue.use(VueI18n)

const i18n = new VueI18n({
  locale: "ko",
  messages: {
    en: {
    all: 'all',
    back: 'back',
    basic: 'Basic',
    brokerage: 'brokerage',
    etc: 'Additional information',
    info: 'info',
    required_item: 'Item is required',
    move: 'move',
    next: 'next',
    realestate: 'Realestate',
    transaction_category: 'transaction category',
    validation: en.messages
  },
    ko: {
      all: '모든',
      back: '뒤로',
      basic: '필수',
      brokerage: '중개',
      etc: '기타 요청사항',
      info: '정보',
      required_item: '필수 입력 항목입니다',
      move: '이사',
      next: '다음',
      realestate: '부동산',
      transaction_category: '거래종류(매매,전세 등)*',
      validation: ko.messages
    }
  }
});

export { i18n };