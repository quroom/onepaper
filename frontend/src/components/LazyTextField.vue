<script>
import VTextField from 'vuetify/lib/components/VTextField/VTextField.js'
export default {
  name: 'LazyTextField',
  props: {
    hideDetails: {
      type: [Boolean, String],
      default:"auto"
    }
  },
  extends: VTextField,
  model: {
    event: 'change'
  },
}
</script>