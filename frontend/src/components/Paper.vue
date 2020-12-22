<template>
  <v-col
        cols="12"
        md="6"
        lg="4"
        xl="3"
      >
    <v-card
      class="outlined tile"
      :to="{ name: 'paper', params: { id: paper.id } }"
    >
      <v-chip class="ma-1 mr-0">
        {{ paper.id }}
      </v-chip>
      <v-chip
        class="ma-1 mr-0"
         :color="status == $getConstByName('status_category', 'progress') ? 'primary' : status == $getConstByName('status_category', 'done') ? 'success' : ''"
         dark
        label
      >
        <v-icon left>
          label
        </v-icon>
        {{ $getConstI18('status_category', status) }}
      </v-chip>
      <div class="text-body-2 pa-1" style="float:right">
        {{ $t("last") }}{{ $t("updated_at") }} : {{ paper.updated_at }}
        <div>
          <div class="author-name-position">
            {{ $t("author") }}:
            <span class="author-name-font"> {{ paper.author }} </span>
          </div>
        </div>
      </div>
      
      <v-card-title class="card-title pa-0 pl-4">
        {{ $getConstI18("trade_category", paper.trade_category) }}
      </v-card-title>
      <v-card-text v-if="paper.address">
        <div>
          {{ paper.address.old_address }}
          <span v-if="paper.address.dong!=''"> {{ paper.address.dong }}{{ $t("dong") }}</span>
          <span v-if="paper.address.ho!=''"> {{ paper.address.ho }}{{ $t("ho") }}</span>
        </div>
        <span>
          [{{ $getConstI18("building_category", paper.building_category) }}]
        </span>
        <span v-if="paper.trade_category == $getConstByName('trade_category', 'rent')">
          {{ `${$t("security_deposit")}${paper.security_deposit} / ${$t("monthly_fee")}${paper.monthly_fee}${$t("manwon")} / ${$t("maintenance_fee")}${paper.maintenance_fee}${$t("manwon")}`}}
        </span>
        <span
          v-else-if="paper.trade_category==$getConstByName('trade_category', 'depositloan')"
        >
        {{ `${$t("security_deposit")}${paper.security_deposit}${$t("manwon")} / ${$t("maintenance_fee")} ${paper.maintenance_fee}${$t("manwon")}`}}
          <!-- {{$t("security_deposit")}}{{ paper.security_deposit }} / 관{{ paper.maintenance_fee }} -->
        </span>
        <!-- To be updated -->
        <span
          v-else-if="
            paper.trade_category == $getConstByName('trade_category', 'purchase')
          "
        >
        </span>
        <span
          v-else-if="
            paper.trade_category == $getConstByName('trade_category', 'exchange')
          "
        >
        </span>
      </v-card-text>
    </v-card>
  </v-col>
</template>

<script>
import { apiService_formData } from "@/common/api.service.js"
import { applyValidation } from "@/common/common_api";

export default {
  name: "Paper",
  props: {
    paper: {
      type: Object,
      required: true
    },
    requestUser: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      error: null,
      paper_status: null,
    }
  },
  computed: {
    status() {
      return this.paper_status ? this.paper_status : this.paper.status;
    }
  },
  methods: {
    clear() {
      this.$refs["signaturePad"].clearSignature();
    },
    open() {
      this.$nextTick(() => {
        this.$refs["signaturePad"].resizeCanvas();
      });
    },
    newtab(image) {
      let newTab = window.open();
      newTab.document.body.innerHTML =
        "<img src=" + image + ' width="500px" height="500px">';
    }
  }
}
</script>

<style>

</style>