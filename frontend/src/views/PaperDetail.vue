<template>
  <v-container>
    <div class="mt-4 text-h4 font-weight-bold text-center">{{ `${$t('realestate')} ${$getConstI18('TRADE_CATEGORY', paper.trade_category)} ${$t('contract')}` }}</div>
    <v-row class="mt-4">
      <v-col class="pa-0 pr-1" cols="12" md="8">
        <div style="float:right">
          <v-icon left color="blue">person</v-icon>
          <span>{{ $t("author") }}: {{ paper.author }}</span>
        </div>
      </v-col>
      <v-col class="pa-0 pr-1" cols="12" md="4">
        <div style="float:right">
          <span
              >{{ $t("last") }}{{ $t("updated_at") }} :
              {{ paper.updated_at }}
          </span>
        </div>
      </v-col>
    </v-row>
    <Actions v-if="isPaperAuthor && !isPaperDone" :id="paper.id" delete_url="/api/papers/" delete_router_name="home" editor_router_name="paper-editor"/>
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
        <v-card outlined tile>{{ $t("dong") }} / {{ $t("ho") }}</v-card>
      </v-col>
      <v-col cols="9" sm="2">
        <v-card outlined tile height="100%">
          <span v-if="paper.address.dong !='' || paper.address.ho !=''" >
            {{ paper.address.dong }} {{ $t("dong") }} {{ paper.address.ho }} {{ $t("ho") }}
          </span>
        </v-card>
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
          <v-card v-else-if="realestate_field_name == 'land_category' || realestate_field_name =='building_category'" outlined tile>
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
      <v-col class="text-center" cols="2" md="1">
        <v-card class="pa-0" outlined tile>
          <v-btn  v-if="!isExpertSigned && requestUser === expert.profile.user.username" class="signature-button" @click="open(false)" color="red" dark>
            <v-icon>create</v-icon>
            {{ $t("signature") }}
          </v-btn>
          <template v-else>
            {{ $t("sign") }}
          </template>
          <a v-if="isExpertSigned" v-bind:href="expert.signature.image" target="_blank">
            <img class="signature-img" :src="expert.signature.image" />
          </a>
        </v-card>
      </v-col>
      <Contractor :contractor="expert.profile" :fields="fields_names.expert_profile_fields"></Contractor>
    </v-row>
    <v-row class="mt-5" v-if="!isLoading && seller != null" no-gutters>
      <v-col class="text-center font-weight-bold" cols="10" md="11">
        <v-card outlined tile color="blue lighten-4">{{
          $t("landlord")
        }}</v-card>
      </v-col>
      <v-col class="text-center" cols="2" md="1">
        <v-card class="pa-0" outlined tile>
          <v-btn
            v-if="!isSellerSigned && requestUser === seller.profile.user.username"
            class="signature-button"
            @click="open(false)"
            color="red"
            dark
          >
            <v-icon>create</v-icon>
            {{ $t("signature") }}
          </v-btn>
          <template v-else>
            {{ $t("sign") }}
          </template>
          <a v-if="isSellerSigned" v-bind:href="seller.signature.image" target="_blank">
            <img class="signature-img" :src="seller.signature.image" />
          </a>
        </v-card>
      </v-col>

      <Contractor :contractor="seller.profile" :fields="fields_names.basic_profile_fields"></Contractor>
    </v-row>
    <v-row class="mt-5" v-if="!isLoading && buyer != null" no-gutters>
      <v-col class="text-center font-weight-bold" cols="10" md="11">
        <v-card outlined tile color="blue lighten-4">{{ $t("tenant") }}</v-card>
      </v-col>
      <v-col class="text-center" cols="2" md="1">
        <v-card class="pa-0" outlined tile> 
          <v-btn
            v-if="!isBuyerSigned && requestUser === buyer.profile.user.username"
            class="signature-button"
            @click="open(false)"
            color="red"
            dark
          >
            <v-icon>create</v-icon>
            {{ $t("signature") }}
          </v-btn>
          <template v-else>
            {{ $t("sign") }}
          </template>
          <a v-if="isBuyerSigned" v-bind:href="buyer.signature.image" target="_blank">
            <img class="signature-img" :src="buyer.signature.image" />
          </a>
        </v-card>
      </v-col>
      <Contractor :contractor="buyer.profile" :fields="fields_names.basic_profile_fields"></Contractor>
    </v-row>
    <div class="mt-5">4. {{ $t("special_agreement") }}</div>
    
    <quill-editor
      ref="myQuillEditor"
      v-model="paper.special_agreement"
      :options="options"
      :disabled="true"
    />
    <v-dialog v-model="dialog" width="50vh" height="25vh" eager>
      <v-card>
        <VueSignaturePad
          class="signature-pad"
          width="50vh"
          height="25vh"
          ref="signaturePad"
          :customStyle="{ border: 'black 2px solid' }"
          :options="{...signature_pad_options}"
        />
        <v-card-title class="justify-center">
          {{ $t("please_sign") }}
        </v-card-title>
        <v-card-actions>
          <v-btn color="blue darken-1" text @click="dialog = false">{{
            $t("close")
          }}</v-btn>
          <v-btn color="blue darken-1" text @click="clear()">{{
            `${$t("signature")} ${$t("clear")}`
          }}</v-btn>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="save()">{{
            `${$t("signature")} ${$t("save")}`
          }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <template v-if="!isLoading && paper.verifying_explanation != null">
      <VerifyingExplanation class="mt-4" :ve="paper.verifying_explanation" :updated_at="paper.updated_at"></VerifyingExplanation>
      <v-row v-if="expert != null && !isLoading" no-gutters>
        <v-col class="contractor-title text-center font-weight-bold" cols="10" md="11">
          <v-card outlined tile color="blue lighten-4">
            {{ $t("realestate_agency") }}
              <a
                v-if="expert.profile.expert_profile.stamp"
                v-bind:href="expert.profile.expert_profile.stamp"
                target="_blank"
              >
                <img
                  class="stamp-img"
                  :src="expert.profile.expert_profile.stamp"
                />
              </a>
          </v-card>
        </v-col>
        <v-col class="text-center" cols="2" md="1">
          <v-card class="pa-0" outlined tile>
            <v-btn 
              v-if="!isExpertExplanationSigned && requestUser === expert.profile.user.username"
              class="signature-button"
              @click="open(true)"
              color="blue"
              dark>
            <v-icon>create</v-icon>
            {{ $t("signature") }}
          </v-btn>
          <template v-else>
            {{ $t("sign") }}
          </template>
          <a v-if="isExpertExplanationSigned" v-bind:href="expert.explanation_signature.image" target="_blank">
            <img class="signature-img" :src="expert.explanation_signature.image" />
          </a>
          </v-card>
        </v-col>
        <Contractor :contractor="expert.profile" :fields="fields_names.expert_profile_fields"></Contractor>
      </v-row>
      <v-row class="mt-5" v-if="!isLoading && seller != null" no-gutters>
        <v-col class="text-center font-weight-bold" cols="10" md="11">
          <v-card outlined tile color="blue lighten-4">{{
            $t("landlord")
          }}</v-card>
        </v-col>
        <v-col class="text-center" cols="2" md="1">
          <v-card class="pa-0" outlined tile> 
            <v-btn
              v-if="!isSellerExplanationSigned && requestUser === seller.profile.user.username"
              class="signature-button"
              @click="open(true)"
              color="blue"
              dark
            >
              <v-icon>create</v-icon>
              {{ $t("signature") }}
            </v-btn>
            <template v-else>
              {{ $t("sign") }}
            </template>
            <a v-if="isSellerExplanationSigned" v-bind:href="seller.explnation_signature.image" target="_blank">
              <img class="signature-img" :src="seller.explnation_signature.image" />
            </a>
          </v-card>
        </v-col>

      <Contractor :contractor="seller.profile" :fields="fields_names.basic_profile_fields"></Contractor>
      </v-row>
      <v-row class="mt-5" v-if="!isLoading && buyer != null" no-gutters>
        <v-col class="text-center font-weight-bold" cols="10" md="11">
          <v-card outlined tile color="blue lighten-4">{{ $t("tenant") }}</v-card>
        </v-col>
        <v-col class="text-center" cols="2" md="1">
          <v-card class="pa-0" outlined tile> 
            <v-btn
              v-if="!isBuyerExplanationSigned && requestUser === buyer.profile.user.username"
              class="signature-button"
              @click="open(true)"
              color="blue"
              dark
            >
              <v-icon>create</v-icon>
              {{ $t("signature") }}
            </v-btn>
            <template v-else>
              {{ $t("sign") }}
            </template>
            <a v-if="isBuyerExplanationSigned" v-bind:href="buyer.explanation_signature.image" target="_blank">
              <img class="signature-img" :src="buyer.explanation_signature.image" />
            </a>
          </v-card>
        </v-col>
        <Contractor :contractor="buyer.profile" :fields="fields_names.basic_profile_fields"></Contractor>
      </v-row>
    </template>
  </v-container>
</template>

<script>
import { apiService, apiService_formData } from "@/common/api.service";
import { applyValidation } from "@/common/common_api";
import Contractor from "@/components/Contractor";
import Actions from "@/components/Actions";
import VerifyingExplanation from "@/components/VerifyingExplanation";
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'

import { quillEditor } from 'vue-quill-editor'


export default {
  name: "PaperDetail",
  props: {
    id: {
      type: [Number, String],
      required: true
    }
  },
  components: {
    Contractor,
    Actions,
    VerifyingExplanation,
    quillEditor
  },
  computed: {
    isPaperAuthor() {
      return this.paper.author === this.requestUser;
    },
    isPaperDone() {
      return this.paper.status == this.$getConstByName('STATUS_CATEGORY', 'DONE')
    },
    isExpertSigned: function() {
      return this.expert.signature != undefined && this.paper.updated_at <= this.expert.signature.updated_at ;
    },
    isSellerSigned: function() {
      return this.seller.signature != undefined && this.paper.updated_at <= this.seller.signature.updated_at ;
    },
    isBuyerSigned: function() {
      return this.buyer.signature != undefined && this.paper.updated_at <= this.buyer.signature.updated_at ;
    },
    isExpertExplanationSigned: function() {
      console.log(this.expert.explanation_signature);
      return this.expert.explanation_signature != undefined && this.paper.updated_at <= this.expert.explanation_signature.updated_at ;
    },
    isSellerExplanationSigned: function() {
      return this.seller.explanation_signature != undefined && this.paper.updated_at <= this.seller.explanation_signature.updated_at ;
    },
    isBuyerExplanationSigned: function() {
      return this.buyer.explanation_signature != undefined && this.paper.updated_at <= this.buyer.explanation_signature.updated_at ;
    },
    contractor: function() {
      if(this.paper.paper_contractors != undefined){
        for (let i = 0; i < this.paper.paper_contractors.length; i++) {
          if(this.paper.paper_contractors[i].profile.user.username == this.requestUser ) {
            return this.paper.paper_contractors[i]
          }
        }
      }
      return null
    },
    expert: function() {
      if(this.paper.paper_contractors != undefined){
        for (let i = 0; i < this.paper.paper_contractors.length; i++) {
          if (this.paper.paper_contractors[i].group == this.$getConstByName("CONTRACTOR_CATEGORY", "expert")) {
            return this.paper.paper_contractors[i];
          }
        }
      }
      return undefined
    },
    seller: function() {
      if(this.paper.paper_contractors != undefined){
        for (let i = 0; i < this.paper.paper_contractors.length; i++) {
          if (this.paper.paper_contractors[i].group == this.$getConstByName("CONTRACTOR_CATEGORY", "seller")) {
            return this.paper.paper_contractors[i];
          }
        }
      }
      return undefined
    },
    buyer: function() {
      if(this.paper.paper_contractors != undefined){
        for (let i = 0; i < this.paper.paper_contractors.length; i++) {
          if (this.paper.paper_contractors[i].group == this.$getConstByName("CONTRACTOR_CATEGORY", "buyer")) {
            return this.paper.paper_contractors[i];
          }
        }
      }
      return undefined
    }
  },
  data() {
    return {
      refresh_key: 0,
      isLoading: true,
      dialog: false,
      expert_dialog: false,
      seller_dialog: false,
      buyer_dialog: false,
      paper: {},
      is_explanation_signature: false,
      fields_names: {
        realestate_fields_name: [
          "land_category",
          "lot_area",
          "building_structure",
          "building_category",
          "building_area"
        ],
        contract_fields_name: [
          "security_deposit",
          "monthly_fee",
          "maintenance_fee",
          "down_payment"
        ],
        basic_profile_fields: [
        { name: "address"
          , key: "address.old_address"
          , cols:"9", md:"10", lg:"11" },
        { name: "name"
          , key: "user.name"
          , cols:"9", sm:"3", md:"2"},
        { name: "birthday"
          , key: "user.birthday"
          , cols:"9", sm:"3", md:"2"}, 
        { name: "mobile_number"
          , cols:"9", sm:"3", md:"2"}, 
        { name: "bank_name"
          , cols:"9", sm:"3", md:"2"}, 
        { name: "account_number"
          , cols:"9", sm:"3", md:"2"}
        ],
        expert_profile_fields: [
        { name: "registration_number"
          , key: "expert_profile.registration_number"
          , cols:"9", md:"10", lg:"4" },
        { name: "shop_name"
          , key: "expert_profile.shop_name"
          , cols:"9", md:"10", lg:"6" },
        { name: "address"
          , key: "address.old_address"
          , cols:"9", md:"10", lg:"11" },
        { name: "name"
          , key: "user.name"
          , cols:"9", sm:"3", md:"2" },
        { name: "birthday"
          , key: "user.birthday"
          , cols:"9", sm:"3", md:"2" },
        { name: "mobile_number"
          , cols:"9", sm:"3", md:"2" },
        { name: "bank_name"
          , cols:"9", sm:"3", md:"2" },
        { name: "account_number"
          , cols:"9", sm:"3", md:"2" }
        ]
      },
      requestUser: null,
      signature_pad_options: {
        minWidth: 3,
        maxWidth: 3,
        penColor: '#F44336'
      },
      options : {
        modules: {
          toolbar: false
        }
      },
    };
  },
  methods: {
    getPaperData() {
      this.isLoading = true;
      let endpoint = `/api/papers/${this.id}/`;
      apiService(endpoint).then(data => {
        if(data.id != undefined){
          this.paper = data;
        } else {
          applyValidation(data)
        }
        this.isLoading = false;
      });
    },
    clear() {
      this.$refs.signaturePad.clearSignature();
    },
    save() {
      const { isEmpty, data } = this.$refs.signaturePad.saveSignature();
      let that = this;
      let endpoint = "";
      var method = "POST";

      if (isEmpty) {
        alert(this.$i18n.t("signature_empty_warning"))
      }
      
      if(this.is_explanation_signature == true ){
         if(this.contractor.explanation_signature != undefined){
          method = "PUT";
          endpoint = `/api/papers/${this.id}/explanation-signatures/${that.contractor.explanation_signature.id}/`;
        } else {
          endpoint = `/api/papers/${this.id}/explanation-signature/`;
        }
      }else {
        if(this.contractor.signature != undefined){
          method = "PUT";
          endpoint = `/api/papers/${this.id}/signatures/${that.contractor.signature.id}/`;
        } else {
          endpoint = `/api/papers/${this.id}/signature/`;
        }
      }
      try {
        fetch(data)
          .then(res => {
            return res.blob();
          })
          .then(myblob => {
            const formData = new FormData();
            if(this.is_explanation_signature == true){
              formData.append(
                "image",
                myblob,
                "explanation_signature_" + that.contractor.id + ".png"
              );
            } else {
              formData.append(
              "image",
              myblob,
              "signature_" + that.contractor.id + ".png"
            );
            }
            
            formData.append("contractor", that.contractor.id);

            apiService_formData(endpoint, method, formData).then(data => {
              if (data.id != undefined) {
                console.log("success")
                alert(that.$i18n.t("request_success"))
                if(that.is_explanation_signature == true){
                  that.contractor.explanation_signature = data;
                } else {
                  that.contractor.signature = data;
                }
                that.dialog = false;
              } else {
                applyValidation(data)
              }
            });
          });
      } catch (err) {
        alert(err);
      }
    },
    open(is_explanation_signature) {
      // if( is_explanation_signature == true) {
      //   this.signature_pad_options.penColor = "#2196F3"
      // } else {
      //   this.signature_pad_options.penColor = "#F44336"
      // }
      
      this.dialog = true;
      this.is_explanation_signature = is_explanation_signature;
      this.$nextTick(() => {
        this.$refs.signaturePad.resizeCanvas();
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
/* .v-card {
  height: 100%;  
  padding: 2px 8px 2px 8px;
  border: thin solid rgba(0, 0, 0, 0.2) !important;
}
.LazyTextField > .v-input__control > .v-input__slot:before {
  border: 0 !important;
  border-style: none !important;
}
.LazyTextField > .v-input__control > .v-input__slot:after {
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
.signature-pad {
  border-bottom: double 3px transparent;
  border-radius: 5px;
  background-image: linear-gradient(white, white),
    radial-gradient(circle at top left, #4bc5e8, #9f6274);
  background-origin: border-box;
  background-clip: content-box, border-box;
} */
.signature-button {
  z-index: 2;
  height: 100% !important;
  width: 100% !important;
}
.signature-img {
  width: 100%;
  height: 30px;
  z-index: 1;
  position: absolute;
  top: -3px;
  left: -5px;
  cursor: pointer;
}
.stamp-img {
  height: 60px;
  z-index: 1;
  position: absolute;
  top: -30px;
  cursor: pointer;
}
.contractor-title {
  background: #BBDEFB !important;
}
</style>