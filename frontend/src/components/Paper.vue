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
      <v-chip
        class="ma-2"
         :color="status == $getConstByName('status_category', 'progress') ? 'primary' : status == $getConstByName('status_category', 'done') ? 'success' : ''"
         dark
        label
      >
        <v-icon left>
          label
        </v-icon>
        {{ $getConstI18('status_category', status) }}
      </v-chip>
      <div class="text-body-2 pa-2" style="float:right">
        {{ $t("last") }}{{ $t("updated_at") }} : {{ paper.updated_at }}
        <div>
          <div class="author-name-position">
            {{ $t("author") }}:
            <span class="author-name-font"> {{ paper.author }} </span>
          </div>
        </div>
      </div>
      
      <v-card-title class="card-title pa-0 pl-4">
        {{ paper.room_name }}
        {{ $getConstI18("trade_category", paper.trade_category) }}
      </v-card-title>
      <v-card-text v-if="paper.address">
        <div>
          {{ paper.address.old_address }}
        </div>
        <span>
          {{ $getConstI18("building_category", paper.building_category) }}
        </span>
        <span v-if="paper.trade_category == $getConstByName('trade_category', 'rent')">
          보{{ paper.security_deposit }} / 월{{ paper.monthly_fee }} / 관{{ paper.maintenance_fee }}
        </span>
        <span
          v-else-if="paper.trade_category==$getConstByName('trade_category', 'depositloan')"
        >
          보{{ paper.security_deposit }} / 관{{ paper.maintenance_fee }}
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
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          style="z-index:2;"
          @click.prevent="open()"
          v-if="!IsSigned"
          color="red"
          dark
          top
          right
        >
          <v-icon>create</v-icon>
          {{ $t("signature") }}
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-dialog v-model="dialog" height="40%" max-width="60%" eager>
        <v-card>
          <VueSignaturePad
            class="signature_pad"
            width="100%"
            height="400px"
            ref="signaturePad"
            :options="{
              minWidth: 3,
              maxWidth: 3,
              penColor: 'red'
            }"
          />
          <v-card-actions>
            <v-btn color="blue darken-1" text @click="dialog = false">{{
              $t("close")
            }}</v-btn>
            <v-btn color="blue darken-1" text @click="clear('seller')">{{
              $t("clear")
            }}</v-btn>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="save('seller')">{{
              $t("save")
            }}</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
  </v-col>
</template>

<script>
import { apiService_formData } from "@/common/api.service.js"

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
      dialog: false,
      error: null,
      paper_status: null,
    }
  },
  computed: {
    status() {
      return this.paper_status ? this.paper_status : this.paper.status;
    },
    contractor() {
      const contractors = this.paper.paper_contractors;
      for (let i = 0; i < contractors.length; i++) {
        let contractor = contractors[i];
        if (contractor.profile.user.username == this.requestUser) {
          return contractor;
        }
      }
      return undefined;
    },
    IsSigned(){
      const contractors = this.paper.paper_contractors
      for (let i = 0; i < contractors.length; i++) {
        let contractor = contractors[i];
        console.log(this.requestUser)
        if (contractor.profile.user.username == this.requestUser) {
          console.log(contractor.signature)
          var updated_at = this.$get(contractor, "signature.updated_at", "0000-00-00")
          console.log(this.paper.updated_at < updated_at)
          return this.paper.updated_at <= this.$get(contractor, "signature.updated_at", "0000-00-00");
        }
      }
      return false;
    }
  },
  methods: {
    clear() {
      this.$refs["signaturePad"].clearSignature();
    },
    save() {
      const { isEmpty, data } = this.$refs["signaturePad"].saveSignature();
      const self = this;
      if (isEmpty) {
        alert(this.$i18n.t("signature_empty_warning"));
        return;
      }

      let endpoint = `/api/papers/${this.paper.id}/signature/`;
      let method = "POST";

      if(self.contractor.signature != null) {
        endpoint = `/api/papers/${this.paper.id}/signatures/${self.contractor.signature.id}/`;
        method = "PUT";
      }

      try {
        fetch(data)
          .then(res => {
            return res.blob();
          })
          .then(myblob => {
            const formData = new FormData();
            formData.append(
              "image",
              myblob,
              "signature_" + self.contractor.id + ".png"
            );
            formData.append("contractor", self.contractor.id);

            apiService_formData(endpoint, method, formData).then(data => {
              if (data.id) {
                alert(this.$i18n.t("request_success"))
                self.contractor.signature = data;
                self.paper_status = data.paper_status;
                self.dialog = false;
              }
            });
          });
      } catch (err) {
        alert(err);
      }
    },
    open() {
      this.dialog = true;
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