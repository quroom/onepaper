<template>
  <div class="ma-5">
    <v-container class="my-5">
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
        >
          {{ paper.title }}
        </v-col>
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
            <v-card v-if="realestate_field_name=='building_area' || realestate_field_name=='lot_area'" outlined tile>{{ paper[realestate_field_name] }}㎡</v-card>
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
          <v-card v-if="!loading" outlined tile>{{ paper.seller_profile.bank_name }} {{ paper.seller_profile.name }} {{ paper.seller_profile.account_number }}</v-card>
        </v-col>
      </v-row>

      <v-textarea
        auto-grow
        readonly
        :value="paper.special_agreement"
      >
      </v-textarea>

      <div class="mt-5">3. {{ $t("contractor_info") }}</div>
      <div>{{ $t("contractor_info_intro") }}</div>
      <v-row v-if="paper.expert_profile!=null && !loading" no-gutters>
        <v-col class="text-center font-weight-bold" cols="12">
          <v-card outlined tile>{{ $t("realestate_agency") }}</v-card>
        </v-col>
        <template v-for="(field_name, index) in fields_names.expert_fields_name">
          <v-col class="text-center font-weight-bold" cols="2" md="2" :key="`name`+index">
            <v-card outlined tile>{{ $t(field_name) }}</v-card>
          </v-col>
          <v-col class="text-center" cols="4" md="2" :key="`value-`+index">
            <v-card outlined tile>{{ paper.expert_profile[field_name]}}</v-card>
          </v-col>
        </template>
      </v-row>
      <v-row class="mt-5" v-if="!loading" no-gutters>
        <v-col class="text-center font-weight-bold" cols="12">
          <v-card outlined tile>{{ $t("landlord") }}</v-card>
        </v-col>
        <template v-for="(field_name, index) in fields_names.basic_profile_fields_name">
          <v-col class="text-center font-weight-bold" cols="2" md="2" :key="`name`+index">
            <v-card outlined tile>{{ $t(field_name) }}</v-card>
          </v-col>
          <v-col class="text-center" cols="4" md="2" :key="`value-`+index">
            <v-card outlined tile>{{ paper.seller_profile[field_name]}}</v-card>
          </v-col>
        </template>
      </v-row>
      <v-row class="mt-5" v-if="!loading" no-gutters>
        <v-col class="text-center font-weight-bold" cols="12">
          <v-card outlined tile>{{ $t("tenant") }}</v-card>
        </v-col>
        <template v-for="(field_name, index) in fields_names.basic_profile_fields_name">
          <v-col class="text-center font-weight-bold" cols="2" md="2" :key="`name`+index">
            <v-card outlined tile>{{ $t(field_name) }}</v-card>
          </v-col>
          <v-col class="text-center" cols="4" md="2" :key="`value-`+index">
            <v-card outlined tile>{{ paper.buyer_profile[field_name]}}</v-card>
          </v-col>
        </template>
      </v-row>

    </v-container>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service";

export default {
  name: "Paper",
  props: {
    id: {
      type: [Number, String],
      required: true
    }
  },
  data() {
    return {
      loading: false,
      paper: {},
      fields_names: {
        "realestate_fields_name":[
          "room_name",
          "land_type",
          "lot_area",
          "building_structure",
          "building_type",
          "building_area"
        ],
        "contract_fields_name": [
          "security_deposit",
          "monthly_fee",
          "maintenance_fee",
          "down_payment",
        ],
        "profile_type_fields_name": [
          "expert_profile",
          "seller_profile",
          "buyer_profile"
        ],
        "basic_profile_fields_name": [
          "name",
          "birthday",
          "mobile_number",
          "address",
          "bank_name",
          "account_number"
        ],
        "expert_fields_name": [
          "registration_number",
          "name",
          "birthday",
          "mobile_number",
          "shop_name",
          "shop_address",
          "bank_name",
          "account_number",
        ]
      }     
      
        // "from_date",
        // "to_date",
        // "special_agreement"
    };
  },
  methods: {
    getPaperData() {
      this.loading = true;
      let endpoint = `/api/papers/${this.id}/`;
      apiService(endpoint).then(data => {
        this.paper = data;
        this.loading = false;
      });
    }
  },
  created() {
    this.getPaperData();
  }
};
</script>
