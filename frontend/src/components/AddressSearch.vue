<template>
  <div>
    <ValidationProvider
      :ref="ref_name"
      mode="passive"
      :name="$t('address')"
      rules="required"
      v-slot="{ errors }"
    >
      <v-text-field
        v-model="address.old_address"
        :label="label"
        outlined
        hide-details="auto"
        readonly
        required
        :error-messages="errors"
        @click="dialog = true"
        data-vv-validate-on="none"
      >
      </v-text-field>
      <v-dialog v-if="!readonly" v-model="dialog">
        <v-card>
          <v-card-text class="pt-5">
            <vue-daum-postcode
              :no-auto-mapping="true"
              :key="key"
              @complete=" address_local = $event;
                onSubmitAddress();
              "
            />
          </v-card-text>
        </v-card>
      </v-dialog>
    </ValidationProvider>
  </div>
</template>
<script>
export default {
  name: "AddressSearch",
  props: {
    label: {
      type: String,
      required: true
    },
    readonly: {
      type: Boolean,
      required: false
    },
    old_address: {
      type: String,
      required: false
    },
    ref_name: {
      type: String,
      reuiqred: true
    },
    address: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      dialog: false,
      key: 0,
      address_local: null,
      dong: null,
      ho: null
    };
  },
  methods: {
    onSubmitAddress() {
      this.address.old_address = this.address_local.jibunAddress;
      this.address.new_address = this.address_local.address;
      this.address.sigunguCd = this.address_local.bcode.substring(0,5);
      this.address.bjdongCd = this.address_local.bcode.substring(0,5);
      this.address.bun = this.address_local.jibunAddress.split("-")[0].split(" ")[this.address_local.jibunAddress.split("-")[0].split(" ").length - 1]      
      this.address.ji = this.address_local.jibunAddress.split("-")[1] ? this.address_local.jibunAddress.split("-")[1].split(" ")[0] : "";
      this.$emit("update:address", this.address);
      this.dialog = false;
      this.key += 1;
    }
  }
};
</script>

<style scoped>
.vue-daum-postcode-container {
  width: 100% !important;
  height: 444px !important;
}
</style>
