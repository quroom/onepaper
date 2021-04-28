<template>
  <div>
    <ValidationProvider
      :ref="ref_name"
      mode="passive"
      :name="$t('address')"
      rules="required"
      v-slot="{ errors }"
    >
      <LazyTextField
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
      </LazyTextField>
      <v-dialog v-if="!readonly" v-model="dialog" persistent eager>
        <v-card>
          <v-icon class="address-close-btn" @click="close()">close</v-icon>
          <v-card-text class="pa-0 pt-2">
            <DaumPostcode
              :autoMapping="false"
              :on-complete="handleAddress"
              :key="key"
            />
          </v-card-text>
        </v-card>
      </v-dialog>
    </ValidationProvider>
  </div>
</template>
<script>
import DaumPostcode from "vuejs-daum-postcode";

export default {
  name: "AddressSearch",
  components: {
    DaumPostcode
  },
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
    handleAddress(data) {
      this.address.old_address = data.jibunAddress;
      this.address.old_address_eng = data.jibunAddressEnglish;
      this.address.new_address = data.address;
      this.address.bjdongName = data.bname;
      this.address.bjdongName_eng = data.bnameEnglish;
      this.address.sigunguCd = data.bcode.substring(0, 5);
      this.address.bjdongCd = data.bcode.substring(0, 5);
      this.address.bun = data.jibunAddress.split("-")[0].split(" ")[
        data.jibunAddress.split("-")[0].split(" ").length - 1
      ];
      this.address.ji = data.jibunAddress.split("-")[1]
        ? data.jibunAddress.split("-")[1].split(" ")[0]
        : "";
      this.$emit("update:address", this.address);
      this.dialog = false;
      this.key += 1;
    },
    close() {
      this.key += 1;
      this.dialog = false;
    }
  }
};
</script>

<style>
.address-close-btn {
  position: absolute !important;
  right: 4px;
  color: aliceblue !important;
  background-color: black;
  z-index: 1;
}
</style>
