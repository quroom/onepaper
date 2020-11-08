<template>
  <v-container>
    <v-row>
      <v-col class="pa-0" cols="12" sm="4">
        <PaperActions v-if="isPaperAuthor" :id="paper.id" />
      </v-col>
      <v-col class="pa-0 pr-1" cols="12" sm="4">
        <div style="float:right">
          <v-icon left color="blue">person</v-icon>
          <span>{{ $t("author") }}: {{ paper.author }}</span>          
        </div>
      </v-col>
      <v-col class="pa-0 pr-1" cols="12" sm="4">
        <div style="float:right">
          <span
              >{{ $t("last") }}{{ $t("updated_at") }} :
              {{ paper.created_at }}
          </span>
        </div>
      </v-col>
    </v-row>
    <v-divider></v-divider>
    <v-row>
      <v-col
        class="text-h4 text-center text-decoration-underline"
        cols="12"
        xs="12"
        >{{ paper.title }}</v-col
      >
    </v-row>
    <div>{{ $t("intro") }}</div>
    <div class="mt-5">1. {{ $t("desc_realestate") }}</div>
    <v-row no-gutters v-if="paper.address">
      <v-col class="text-center font-weight-bold" cols="2" sm="1">
        <v-card outlined tile>{{ $t("address") }}</v-card>
      </v-col>
      <v-col cols="10" sm="6">
        <v-card outlined tile>{{ paper.address.old_address }}</v-card>
      </v-col>
      <v-col class="text-center font-weight-bold" cols="3" sm="3">
        <v-card outlined tile>{{ $t("room_name") }}</v-card>
      </v-col>
      <v-col cols="9" sm="2">
        <v-card outlined tile>{{ paper.room_name }}</v-card>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <template
        v-for="(realestate_field_name,
        index) in fields_names.realestate_fields_name"
      >
        <v-col
          class="text-center font-weight-bold"
          cols="3"
          sm="2"
          :key="`name` + index"
        >
          <v-card outlined tile>{{ $t(realestate_field_name) }}</v-card>
        </v-col>
        <v-col class="text-center" cols="3" sm="2" :key="`value-` + index">
          <v-card
            v-if="
              realestate_field_name == 'building_area' ||
                realestate_field_name == 'lot_area'
            "
            outlined
            tile
            >{{ paper[realestate_field_name] }}㎡</v-card
          >
          <v-card v-else-if="realestate_field_name == 'land_type' || realestate_field_name =='building_type'" outlined tile>
            {{$getConstI18(realestate_field_name, paper[realestate_field_name])}}
          </v-card>
          <v-card v-else outlined tile>{{ paper[realestate_field_name] }}</v-card>
        </v-col>
      </template>
    </v-row>
    <div class="mt-5">2. {{ $t("terms_and_conditions") }}</div>
    <div>{{ $t("terms_and_conditions_intro") }}</div>
    <v-row no-gutters>
      <v-col class="text-center font-weight-bold" cols="3" sm="2">
        <v-card outlined tile>{{ $t("term_of_lease") }}</v-card>
      </v-col>
      <v-col class="text-center font-weight-bold" cols="9" sm="10">
        <v-card outlined tile
          >{{ paper.from_date }} ~ {{ paper.to_date }}</v-card
        >
      </v-col>
      <template
        v-for="(contract_field_name,
        index) in fields_names.contract_fields_name"
      >
        <template v-if="paper[contract_field_name] != undefined">
          <v-col
            class="text-center font-weight-bold"
            cols="3"
            sm="2"
            :key="`name` + index"
          >
            <v-card outlined tile>{{ $t(contract_field_name) }}</v-card>
          </v-col>
          <v-col class="text-center" cols="3" sm="2" :key="`value-` + index">
            <v-card outlined tile>{{ paper[contract_field_name] }}</v-card>
          </v-col>
        </template>
      </template>
    </v-row>
    <v-row no-gutters>
      <v-col class="text-center font-weight-bold" cols="3" sm="2">
        <v-card outlined tile>{{ $t("bank_account") }}</v-card>
      </v-col>
      <v-col class="text-center" cols="9" sm="10">
        <v-card v-if="!isLoading && seller != null" outlined tile
          >{{ seller.profile.bank_name }} {{ seller.profile.user.name }}
          {{ seller.profile.account_number }}</v-card
        >
      </v-col>
    </v-row>
    <div class="mt-5">3. {{ $t("contractor_info") }}</div>
    <div>{{ $t("contractor_info_intro") }}</div>
    <v-row v-if="expert != null && !isLoading" no-gutters>
      <v-dialog v-model="expert_dialog" height="40%" max-width="60%" eager>
        <v-card>
          <VueSignaturePad
            class="signature-pad"
            width="100%"
            height="400px"
            ref="expert_signaturePad"
            :options="{
              minWidth: 3,
              maxWidth: 3,
              penColor: 'red'
            }"
          />
          <v-card-actions>
            <v-btn color="blue darken-1" text @click="expert_dialog = false">{{
              $t("close")
            }}</v-btn>
            <v-btn color="blue darken-1" text @click="clear('expert')">{{
              $t("clear")
            }}</v-btn>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="save('expert')">{{
              $t("save")
            }}</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-col class="text-center" cols="2" md="1">
        <v-card class="pa-0" outlined tile>
          <template v-if="expert.signature === null && requestUser === expert.profile.user.username">
            <v-btn class="signature-button" @click="open('expert')" color="red" dark>
            <v-icon>create</v-icon>
            {{ $t("signature") }}
          </v-btn>
          </template>
          <template v-else>
            {{ $t("sign") }}
          </template>
        </v-card>
        <template v-if="expert.signature">
          <a v-bind:href="expert.signature.image" target="_blank">
            <img class="signature-img" :src="expert.signature.image" />
          </a>
        </template>
      </v-col>
      <v-col class="contractor-title text-center font-weight-bold" cols="10" md="11">
        <v-card outlined tile color="blue lighten-4">
          {{ $t("realestate_agency") }}
          <template v-if="expert.profile.expert_profile.stamp">
            <a
              v-bind:href="expert.profile.expert_profile.stamp"
              target="_blank"
            >
              <img
                class="stamp-img"
                :src="expert.profile.expert_profile.stamp"
              />
            </a>
          </template>
        </v-card>
      </v-col>
      <template v-for="(field_name, index) in fields_names.expert_fields_name">
        <v-col
          class="text-center font-weight-bold"
          cols="3"
          md="2"
          lg="1"
          :key="`name` + index"
        >
          <v-card outlined tile>{{ $t(field_name) }}</v-card>
        </v-col>
        <v-col
          v-if="field_name === 'registration_number'"
          class="text-center"
          cols="9"
          md="10"
          lg="2"
          :key="`value-` + index"
        >
          <v-card outlined tile>{{ expert.profile.expert_profile[field_name] }}</v-card>
        </v-col>
        <v-col
          v-else-if="field_name === 'shop_name'"
          class="text-center"
          cols="9"
          md="10"
          lg="4"
          :key="`value-` + index"
        >
          <v-card outlined tile>{{
            expert.profile.expert_profile[field_name]
          }}</v-card>
        </v-col>
        <v-col
          v-else-if="field_name === 'address'"
          class="text-center"
          cols="9"
          md="10"
          lg="6"
          :key="`value-` + index"
        >
          <v-card outlined tile>{{ expert.profile[field_name] }}</v-card>
        </v-col>
        <v-col
          v-else-if="field_name === 'name' || field_name === 'birthday'"
          class="text-center"
          cols="9"
          sm="3"
          md="2"
          :key="`value-` + index"
        >
          <v-card outlined tile>{{
            expert.profile.user[field_name]
          }}</v-card>
        </v-col>
        <v-col
          v-else
          class="text-center"
          cols="9"
          sm="3"
          md="2"
          :key="`value-` + index"
        >
          <v-card outlined tile>{{ expert.profile[field_name] }}</v-card>
        </v-col>
      </template>
    </v-row>
    <v-row class="mt-5" v-if="!isLoading && seller != null" no-gutters>
      <v-dialog v-model="seller_dialog" height="40%" max-width="60%" eager>
        <v-card>
          <VueSignaturePad
            class="signature-pad"
            width="100%"
            height="400px"
            ref="seller_signaturePad"
            :options="{
              minWidth: 3,
              maxWidth: 3,
              penColor: 'red'
            }"
          />
          <v-card-actions>
            <v-btn color="blue darken-1" text @click="seller_dialog = false">{{
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
      <v-col class="text-center" cols="2" md="1">
        <v-card class="pa-0" outlined tile> 
          <template v-if="seller.signature === null && requestUser === seller.profile.user.username">
            <v-btn
              class="signature-button"
              @click="open('seller')"
              color="red"
              dark
            >
              <v-icon>create</v-icon>
              {{ $t("signature") }}
            </v-btn>
          </template>
          <template v-else>
            {{ $t("sign") }}
          </template>
        </v-card>
        <template v-if="seller.signature">
          <a v-bind:href="seller.signature.image" target="_blank">
            <img class="signature-img" :src="seller.signature.image" />
          </a>
        </template>
      </v-col>

      <v-col class="text-center font-weight-bold" cols="10" md="11">
        <v-card outlined tile color="blue lighten-4">{{
          $t("landlord")
        }}</v-card>
      </v-col>
      <template
        v-for="(field_name, index) in fields_names.basic_profile_fields_name"
      >
        <v-col
          class="text-center font-weight-bold"
          cols="3"
          md="2"
          lg="1"
          :key="`name` + index"
        >
          <v-card outlined tile>{{ $t(field_name) }}</v-card>
        </v-col>
        <v-col
          v-if="field_name === 'address'"
          class="text-center"
          cols="9"
          md="10"
          lg="11"
          :key="`value-` + index"
        >
          <v-card outlined tile>{{ buyer.profile[field_name] }}</v-card>
        </v-col>
        <v-col
          v-else-if="field_name === 'name' || field_name === 'birthday'"
          class="text-center"
          cols="9"
          sm="3"
          md="2"
          :key="`value-` + index"
        >
          <v-card outlined tile>{{ seller.profile.user[field_name] }}</v-card>
        </v-col>
        <v-col
          v-else
          class="text-center"
          cols="9"
          sm="3"
          md="2"
          :key="`value-` + index"
        >
          <v-card outlined tile>{{ seller.profile[field_name] }}</v-card>
        </v-col>
      </template>
    </v-row>
    <v-row class="mt-5" v-if="!isLoading && buyer != null" no-gutters>
      <v-dialog v-model="buyer_dialog" height="40%" max-width="60%" eager>
        <v-card>
          <VueSignaturePad
            class="signature-pad"
            width="100%"
            height="400px"
            ref="buyer_signaturePad"
            :options="{
              minWidth: 3,
              maxWidth: 3,
              penColor: 'red'
            }"
          />
          <v-card-actions>
            <v-btn color="blue darken-1" text @click="buyer_dialog = false">{{
              $t("close")
            }}</v-btn>
            <v-btn color="blue darken-1" text @click="clear('buyer')">{{
              $t("clear")
            }}</v-btn>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="save('buyer')">{{
              $t("save")
            }}</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-col class="text-center" cols="2" md="1">
        <v-card class="pa-0" outlined tile> 
          <template v-if="buyer.signature === null && requestUser === buyer.profile.user.username">
            <v-btn
              class="signature-button"
              @click="open('buyer')"
              color="red"
              dark
            >
              <v-icon>create</v-icon>
              {{ $t("signature") }}
            </v-btn>
          </template>
          <template v-else>
            {{ $t("sign") }}
          </template>
        </v-card>
        <template v-if="buyer.signature">
          <a v-bind:href="buyer.signature.image" target="_blank">
            <img class="signature-img" :src="buyer.signature.image" />
          </a>
        </template>
      </v-col>
      <v-col class="text-center font-weight-bold" cols="10" md="11">
        <v-card outlined tile color="blue lighten-4">{{ $t("tenant") }}</v-card>
      </v-col>
      <template
        v-for="(field_name, index) in fields_names.basic_profile_fields_name"
      >
        <v-col
          class="text-center font-weight-bold"
          cols="3"
          md="2"
          lg="1"
          :key="`name` + index"
        >
          <v-card outlined tile>{{ $t(field_name) }}</v-card>
        </v-col>
        <v-col
          v-if="field_name === 'address'"
          class="text-center"
          cols="9"
          md="10"
          lg="11"
          :key="`value-` + index"
        >
          <v-card outlined tile>{{ buyer.profile[field_name] }}</v-card>
        </v-col>
        <v-col
          v-else-if="field_name === 'name' || field_name === 'birthday'"
          class="text-center"
          cols="9"
          sm="3"
          md="2"
          :key="`value-` + index"
        >
          <v-card outlined tile>{{ buyer.profile.user[field_name] }}</v-card>
        </v-col>
        <v-col
          v-else
          class="text-center"
          cols="9"
          sm="3"
          md="2"
          :key="`value-` + index"
        >
          <v-card outlined tile>{{ buyer.profile[field_name] }}</v-card>
        </v-col>
      </template>
    </v-row>
    <div class="mt-5">4. {{ $t("special_agreement") }}</div>
    
    <quill-editor
        ref="myQuillEditor"
        v-model="paper.special_agreement"
        :options="options"
        :disabled="true"
      />
  </v-container>
</template>

<script>
import { apiService, apiService_formData } from "@/common/api.service";
import i18n from "@/plugins/i18n";
import PaperActions from "@/components/PaperActions.vue";
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'

import { quillEditor } from 'vue-quill-editor'


export default {
  name: "Paper",
  props: {
    id: {
      type: [Number, String],
      required: true
    }
  },
  components: {
    PaperActions,
    quillEditor
  },
  data() {
    return {
      isLoading: true,
      expert_dialog: false,
      seller_dialog: false,
      buyer_dialog: false,
      paper: {},
      expert: null,
      seller: null,
      buyer: null,
      fields_names: {
        realestate_fields_name: [
          "land_type",
          "lot_area",
          "building_structure",
          "building_type",
          "building_area"
        ],
        contract_fields_name: [
          "security_deposit",
          "monthly_fee",
          "maintenance_fee",
          "down_payment"
        ],
        profile_type_fields_name: [
          "expert_profile",
          "seller_profile",
          "buyer_profile"
        ],
        basic_profile_fields_name: [
          "address",
          "name",
          "birthday",
          "mobile_number",
          "bank_name",
          "account_number"
        ],
        expert_fields_name: [
          "address",
          "shop_name",
          "registration_number",
          "name",
          "birthday",
          "mobile_number",
          "bank_name",
          "account_number"
        ]
      },
      requestUser: null,
      options : {
        modules: {
          toolbar: false
        }
      },
    };
  },
  computed: {
    isPaperAuthor() {
      return this.paper.author === this.requestUser;
    }
  },
  methods: {
    initialize_contractors(contractors) {
      for (let i = 0; i < contractors.length; i++) {
        if (contractors[i].group == this.$getConstByName("CONTRACTOR_TYPE", "expert")) {
          this.expert = contractors[i];
        } else if (contractors[i].group == this.$getConstByName("CONTRACTOR_TYPE", "seller")) {
          this.seller = contractors[i];
        } else {
          this.buyer = contractors[i];
        }
      }
    },
    getPaperData() {
      this.isLoading = true;
      let endpoint = `/api/papers/${this.id}/`;
      apiService(endpoint).then(data => {
        this.paper = data;
        this.initialize_contractors(this.paper.paper_contractors);
        this.isLoading = false;
      });
    },
    clear(group) {
      this.$refs[group + "_signaturePad"].clearSignature();
    },
    save(group) {
      const { isEmpty, data } = this.$refs[
        group + "_signaturePad"
    ].saveSignature();
      // let parseFile = new Parse.File('signature'+self[group].id, { base64: base64 });
      if (isEmpty) {
        alert(i18n.t("signature_empty_warning"))
      }

      let self = this;
      let endpoint = `/api/papers/${this.id}/signature/`;
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
              "signature_" + self[group].id + ".png"
            );
            formData.append("contractor", self[group].id);

            apiService_formData(endpoint, "POST", formData).then(data => {
              if (data.id) {
                alert(self.$i18n.t("request_success"))
                window.location.reload();
              } else {
                alert(data);
              }
            });
          });
      } catch (err) {
        alert(err);
      }
    },
    open(user) {
      this[user + "_dialog"] = true;
      this.$nextTick(() => {
        this.$refs[user + "_signaturePad"].resizeCanvas();
      });
    },
    newtab(image) {
      let newTab = window.open();
      newTab.document.body.innerHTML =
        "<img src=" + image + ' width="500px" height="500px">';
    }
  },
  created() {
    this.getPaperData();
    this.requestUser = window.localStorage.getItem("username");
  }
};
</script>
<style scoped>
.v-text-field > .v-input__control > .v-input__slot:before {
  border: 0 !important;
  border-style: none !important;
}
.v-text-field > .v-input__control > .v-input__slot:after {
  border-style: none !important;
}
img {
  z-index: -1;
}
.top-mid {
  position: absolute;
  top: -25px;
  right: -45px;
}
.signature-button {
  z-index:2;
}
.signature-pad {
  border-bottom: double 3px transparent;
  border-radius: 5px;
  background-image: linear-gradient(white, white),
    radial-gradient(circle at top left, #4bc5e8, #9f6274);
  background-origin: border-box;
  background-clip: content-box, border-box;
}
.signature-img {
  height: 40px;
  z-index: 1;
  position: absolute;
  top: -10px;
  left: 5px;
  cursor: pointer;
}
.stamp-img {
  height: 60px;
  z-index: 1;
  position: absolute;
  top: -30px;
  cursor: pointer;
}
.v-card {
  padding: 2px 8px 2px 8px;
  border: thin solid rgba(0, 0, 0, 0.2) !important;
}
.contractor-title {
  background: #BBDEFB !important;
}
</style>