<script>
import VTextArea from 'vuetify/lib/components/VTextarea/VTextarea.js'
export default {
  name: 'LazyTextArea',
  extends: VTextArea,
  model: {
    event: 'change'
  },
}
</script>