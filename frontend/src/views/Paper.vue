<template>
  <div class="ma-5">
    <v-container class="my-5">
      <PaperActions v-if="isPaperAuthor" :id="paper.id" />
      <v-dialog v-model="warning_dialog">
        <v-row no-gutters>
          <v-col class="text-center" cols="12">
            <v-card v-model="error">
              <div class="text-h6 red--text ">
                {{ error }}
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-dialog>
      <v-row>
        <v-col cols="6">
          <v-icon left color="blue">person</v-icon>
          <span>{{ $t("author") }}: {{ paper.author }}</span>
        </v-col>
        <v-col cols="6">
          <v-row>
            <span>{{ $t("last") }} {{ $t("updated_at") }} : {{ paper.created_at }}</span>
          </v-row>
        </v-col>
      </v-row>
      <v-divider></v-divider>
      <v-row>
        <v-col
          class="text-h4 text-center text-decoration-underline"
          cols="12"
          xs="12"
        >{{ paper.title }}</v-col>
      </v-row>
      <div>{{ $t("intro") }}</div>

      <div class="mt-5">1. {{ $t("desc_realestate") }}</div>
      <v-row no-gutters>
        <v-col class="text-center font-weight-bold" cols="2">
          <v-card outlined tile>{{ $t("address") }}</v-card>
        </v-col>
        <v-col cols="10">
          <v-card outlined tile>{{ paper.address }}</v-card>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <template v-for="(realestate_field_name, index) in fields_names.realestate_fields_name">
          <v-col class="text-center font-weight-bold" cols="2" :key="`name`+index">
            <v-card outlined tile>{{ $t(realestate_field_name) }}</v-card>
          </v-col>
          <v-col class="text-center" cols="2" :key="`value-`+index">
            <v-card
              v-if="realestate_field_name=='building_area' || realestate_field_name=='lot_area'"
              outlined
              tile
            >{{ paper[realestate_field_name] }}㎡</v-card>
            <v-card v-else outlined tile>{{ paper[realestate_field_name] }}</v-card>
          </v-col>
        </template>
      </v-row>

      <div class="mt-5">2. {{ $t("terms_and_conditions") }}</div>
      <div>{{ $t("terms_and_conditions_intro") }}</div>
      <v-row no-gutters>
        <v-col class="text-center font-weight-bold" cols="2">
          <v-card outlined tile>{{ $t("term_of_lease")}}</v-card>
        </v-col>
        <v-col class="text-center font-weight-bold" cols="10">
          <v-card outlined tile>{{ paper.from_date }} ~ {{ paper.to_date }}</v-card>
        </v-col>
        <template v-for="(contract_field_name, index) in fields_names.contract_fields_name">
          <v-col class="text-center font-weight-bold" cols="2" md="1" :key="`name`+index">
            <v-card outlined tile>{{ $t(contract_field_name) }}</v-card>
          </v-col>
          <v-col class="text-center" cols="4" md="2" :key="`value-`+index">
            <v-card outlined tile>{{ paper[contract_field_name] }}</v-card>
          </v-col>
        </template>
      </v-row>
      <v-row no-gutters>
        <v-col class="text-center font-weight-bold" cols="2">
          <v-card outlined tile>{{$t("bank_account")}}</v-card>
        </v-col>
        <v-col class="text-center" cols="10">
          <v-card
            v-if="!isLoading"
            outlined
            tile
          >{{ paper.seller_profile.bank_name }} {{ paper.seller_profile.user.name }} {{ paper.seller_profile.account_number }}</v-card>
        </v-col>
      </v-row>

      <div class="mt-5">3. {{ $t("contractor_info") }}</div>
      <div>{{ $t("contractor_info_intro") }}</div>
      <v-row v-if="paper.expert_profile!=null && !isLoading" no-gutters>
        <v-col class="text-center font-weight-bold" cols="12">
          <v-card outlined tile color="blue lighten-4">{{ $t("realestate_agency") }}</v-card>
        </v-col>
        <template v-for="(field_name, index) in fields_names.expert_fields_name">
          <v-col class="text-center font-weight-bold" cols="2" md="2" :key="`name`+index">
            <v-card outlined tile>{{ $t(field_name) }}</v-card>
          </v-col>
          <v-col
            v-if="field_name==='name' || field_name==='birthday'"
            class="text-center"
            cols="4"
            md="2"
            :key="`value-`+index"
          >
            <v-card outlined tile>{{ paper.expert_profile['user'][field_name]}}</v-card>
          </v-col>
          <v-col v-else class="text-center" cols="4" md="2" :key="`value-`+index">
            <v-card outlined tile>{{ paper.expert_profile[field_name]}}</v-card>
          </v-col>
        </template>
        <v-col>
          <v-btn
            v-if="paper.expert_signature===null && requestUser===paper.expert_profile.user.username"
            color="red"
            dark
            fab
            top
            right
          >
            <v-icon>create</v-icon>
            {{$t("signature")}}
          </v-btn>
          <template v-if="paper.expert_signature">
            <div class="top-mid">{{$t("signature")}}</div>
            <img width="60px" :src="paper.expert_signature.image" />
          </template>
        </v-col>
      </v-row>
      <v-row class="mt-5" v-if="!isLoading" no-gutters>           
          <v-dialog v-model="seller_dialog" height="400px" max-width="400px" eager>
              <v-card>
                <VueSignaturePad
                  class="signature_pad"
                  width="100%"
                  height="400px"
                  ref="seller_signaturePad"
                  :options= "{
                    minWidth: 3,
                    maxWidth: 3,
                    penColor: 'red',
                  }"
                />
                <v-card-actions>
                  <v-btn color="blue darken-1" text @click="seller_dialog = false">{{$t('close')}}</v-btn>
                  <v-btn
                    color="blue darken-1"
                    text
                    @click="clear('seller_signaturePad')"
                  >{{$t('clear')}}</v-btn>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="blue darken-1"
                    text
                    @click="save('seller_signaturePad')"
                  >{{$t('save')}}</v-btn>
                </v-card-actions>
              </v-card>
          </v-dialog>
          <v-btn
            style="position:absolute; z-index:2;"
            @click="open('seller')"
            v-if="paper.seller_signature===null && requestUser===paper.seller_profile.user.username"
            color="red"
            dark
            fab
            top
            right
          >
            <v-icon>create</v-icon>
            {{$t("signature")}}
          </v-btn>
        
        <v-col class="text-center" cols="1">
          <v-card outlined tile> {{ $t("sign") }} </v-card>
            <template v-if="paper.seller_signature">              
              <img @click="newtab(paper.seller_signature.image)" class="signature_img" :src="paper.seller_signature.image" />
            </template>
        </v-col>
        <v-col class="text-center font-weight-bold" cols="11">
          <v-card outlined tile color="blue lighten-4">{{ $t("landlord") }}</v-card>
        </v-col>
        <template v-for="(field_name, index) in fields_names.basic_profile_fields_name">
          <v-col class="text-center font-weight-bold" cols="2" md="2" :key="`name`+index">
            <v-card outlined tile>{{ $t(field_name) }}</v-card>
          </v-col>
          <v-col
            v-if="field_name==='name' || field_name==='birthday'"
            class="text-center"
            cols="4"
            md="2"
            :key="`value-`+index"
          >
            <v-card outlined tile>{{ paper.seller_profile['user'][field_name]}}</v-card>
          </v-col>
          <v-col v-else class="text-center" cols="4" md="2" :key="`value-`+index">
            <v-card outlined tile>{{ paper.seller_profile[field_name]}}</v-card>
          </v-col>
        </template>         
      </v-row>
      <v-row class="mt-5" v-if="!isLoading" no-gutters>
        <v-dialog v-model="buyer_dialog" height="400px" max-width="400px" eager>
          <v-card>
            <VueSignaturePad
              class="signature_pad"
              width="100%"
              height="400px"
              ref="buyer_signaturePad"
              :options= "{
                  minWidth: 3,
                  maxWidth: 3,
                  penColor: 'red',
              }"
            />
              <v-card-actions>
                <v-btn color="blue darken-1" text @click="buyer_dialog = false">{{$t('close')}}</v-btn>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="clear('buyer_signaturePad')"
                >{{$t('clear')}}</v-btn>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="save('buyer_signaturePad')">{{$t('save')}}</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-btn
            style="position:absolute; z-index:1"
            @click="open('buyer')"
            v-if="paper.buyer_signature===null && requestUser===paper.buyer_profile.user.username"
            color="red"
            dark
            fab
            top
            right
          >
            <v-icon>create</v-icon>
            {{$t("signature")}}
          </v-btn>
        <v-col class="text-center" cols="1">
          <v-card outlined tile> {{$t("sign")}} </v-card>
          <template v-if="paper.buyer_signature">
            <img @click="newtab(paper.buyer_signature.image)" class="signature_img" :src="paper.buyer_signature.image" />
          </template>
        </v-col>
        <v-col class="text-center font-weight-bold" cols="11">
          <v-card outlined tile color="blue lighten-4">{{ $t("tenant") }}</v-card>
        </v-col>
        <template v-for="(field_name, index) in fields_names.basic_profile_fields_name">
          <v-col class="text-center font-weight-bold" cols="2" md="2" :key="`name`+index">
            <v-card outlined tile>{{ $t(field_name) }}</v-card>
          </v-col>
          <v-col
            v-if="field_name==='name' || field_name==='birthday'"
            class="text-center"
            cols="4"
            md="2"
            :key="`value-`+index"
          >
            <v-card outlined tile>{{ paper.buyer_profile['user'][field_name]}}</v-card>
          </v-col>
          <v-col v-else class="text-center" cols="4" md="2" :key="`value-`+index">
            <v-card outlined tile>{{ paper.buyer_profile[field_name]}}</v-card>
          </v-col>
        </template>
      </v-row>
      <div class="mt-5">4. {{ $t("special_agreement") }}</div>
      <v-textarea class="no_underline" auto-grow readonly :value="paper.special_agreement"></v-textarea>
    </v-container>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service";
import i18n from "@/plugins/i18n";
import PaperActions from "@/components/PaperActions.vue";

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
  },
  data() {
    return {
      isLoading: true,
      seller_dialog: false,
      buyer_dialog: false,
      warning_dialog: false,
      error: null,
      paper: {},
      fields_names: {
        realestate_fields_name: [
          "room_name",
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
          "name",
          "birthday",
          "mobile_number",
          "address",
          "bank_name",
          "account_number"
        ],
        expert_fields_name: [
          "registration_number",
          "name",
          "birthday",
          "mobile_number",
          "shop_name",
          "shop_address",
          "bank_name",
          "account_number"
        ]
      },
      requestUser: null
    };
  },
  computed: {
    isPaperAuthor() {
      return this.paper.author === this.requestUser;
    }
  },
  methods: {
    getPaperData() {
      this.isLoading = true;
      let endpoint = `/api/papers/${this.id}/`;
      apiService(endpoint).then(data => {
        this.paper = data;
        console.log(this.paper.buyer_signature)
        this.isLoading = false;
      });
    },
    clear(padName) {
      this.$refs[padName].clearSignature();
    },
    save(padName) {
      const { isEmpty, data } = this.$refs[padName].saveSignature();
      if(isEmpty) {
        this.warning_dialog = true;
        this.error = i18n.t("signature_empty_warning");
      }

      let self = this;      
      let endpoint = `/api/papers/${this.id}/signature/`;
      let content_type = 'multipart/form-data'
      try {
        apiService(endpoint, 'POST', {
          image:data
        },content_type).then(data => {
          if (data.id) {
            window.location.reload()
          } else {
            this.warning_dialog = true;
            self.error= data;            
          }
        });
      } catch (err) {
        console.log(err);
      }
    },
    open(user) {
      this[user + "_dialog"] = true;
      this.$nextTick(() => {
        this.$refs[user + "_signaturePad"].resizeCanvas();
      });
    },
    newtab(image) {
      var newTab = window.open();
      newTab.document.body.innerHTML = '<img src=' + image + ' width="500px" height="500px">';
    } 
  },
  created() {
    this.getPaperData();
    this.requestUser = window.localStorage.getItem("username");
  }
};
</script>
<style scoped>
.v-text-field>.v-input__control>.v-input__slot:before {
  border: 0 !important;
  border-style: none !important;
}
.v-text-field>.v-input__control>.v-input__slot:after {
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
.signature_pad {
  border-bottom: double 3px transparent;
  border-radius: 5px;
  background-image: linear-gradient(white, white),
    radial-gradient(circle at top left, #4bc5e8, #9f6274);
  background-origin: border-box;
  background-clip: content-box, border-box;
}
.signature_img { 
  width:50px;
  z-index: 1;
  position: absolute;
  top: -10px;
  left: 20px;
  cursor: pointer;
}
</style>