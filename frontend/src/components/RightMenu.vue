<script>
import VMenu from "vuetify/lib/components/VMenu/VMenu";

export default {
  name: "RightMenu",
  extends: VMenu,
  computed: {
    styles() {
      return {
        maxHeight: this.calculatedMaxHeight,
        minWidth: this.calculatedMinWidth,
        maxWidth: this.calculatedMaxWidth,
        top: this.calculatedTop,
        right: document.body.clientWidth - this.dimensions.activator.right + "px",
        transformOrigin: this.origin,
        zIndex: this.zIndex || this.activeZIndex
      };
    }
  }
};
</script>
