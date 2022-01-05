<script>
import VRadioGroup from "vuetify/lib/components/VRadioGroup/VRadioGroup.js";
export default {
  name: "NullRadioGroup",
  extends: VRadioGroup,
  methods: {
    getValue(item) {
      return item.value;
    }
  }
};
</script>
