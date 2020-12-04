<script>
import VTextField from 'vuetify/lib/components/VTextField/VTextField.js'
export default {
  name: 'LazyTextField',
  extends: VTextField,
  model: {
    event: 'change'
  },
}
</script>