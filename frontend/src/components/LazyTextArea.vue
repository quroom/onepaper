<script>
import VTextArea from "vuetify/lib/components/VTextarea/VTextarea.js";
export default {
  name: "LazyTextArea",
  props: {
    hideDetails: {
      type: [Boolean, String],
      default: "auto"
    }
  },
  extends: VTextArea,
  model: {
    event: "change"
  }
};
</script>
