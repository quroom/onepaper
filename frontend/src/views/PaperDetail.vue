<template>
  <v-container>
    <div
      v-if="
        paper.trade_category == $getConstByName('TRADE_CATEGORY', 'rent') ||
          paper.trade_category == $getConstByName('TRADE_CATEGORY', 'depositloan')
      "
      class="mt-4 text-h4 font-weight-bold text-center"
    >
      {{ $t("realestate_lease_contract") }}
    </div>
    <div id="v-paper-detail" class="text-h6 text-center no-print">({{ paper.title }})</div>
    <div class="text-caption red--text no-print">{{ $t("paper_subtitle") }}</div>
    <v-row v-if="paper.author" class="mt-4 no-print">
      <v-col class="pa-0 pr-1" cols="12" md="8" style="position: relative;">
        <template v-if="isPaperDone || currentContractor.is_allowed == false">
          <v-btn
            id="v-hide"
            v-if="currentContractor.is_hidden == false"
            class="ml-2"
            color="red"
            @click="hidePaper(true)"
            dark
            small
          >
            <v-icon>visibility_off</v-icon>
            {{ `${$t("paper")}` + `${$t("hide")}` }}
          </v-btn>
          <v-btn v-else class="ml-2" color="black" @click="hidePaper(false)" dark small>
            <v-icon>visibility</v-icon>{{ $t("show_paper") }}
          </v-btn>
        </template>
        <div style="float:right">
          <span> {{ $t("updated_at") }}: {{ paper.updated_at }} </span>
        </div>
      </v-col>
      <v-col class="pa-0 pr-1" cols="12" md="4">
        <div style="float:right">
          <v-icon class="ma-0" left color="blue">person</v-icon>
          <span>{{ paper.author }}</span>
        </div>
      </v-col>
    </v-row>
    <ActionItems
      v-if="
        isAuthor &&
          !isPaperDone &&
          (deadlineToModify > '0001-1-1' || deadlineToModify == undefined)
      "
      :id="paper.id"
      delete_url="/api/papers/"
      delete_router_name="home"
      editor_router_name="paper-editor"
    />
    <div v-if="!isPaperDone" class="text-right text-caption white--text no-print">
      <span v-if="deadlineToModify > '0001-1-1'" class="red">
        {{ `${$t("modify_delete_deadline")} : ${deadlineToModify}` }}
      </span>
      <span v-if="deadlineToModify < '0001-1-1'" class="red">
        {{ $t("modify_delete_deadline_expired") }}
      </span>
    </div>
    <v-divider></v-divider>
    <div>{{ $t("intro") }}</div>
    <div id="v-desc-realestate">
      <div class="mt-5">1. {{ $t("desc_realestate") }}</div>
      <v-row no-gutters v-if="paper.address">
        <v-col class="text-center font-weight-bold" cols="2" sm="1">
          <v-card outlined tile>{{ $t("address") }}</v-card>
        </v-col>
        <v-col cols="10" sm="7">
          <v-card outlined tile>{{ paper.address.old_address }}</v-card>
        </v-col>
        <v-col class="text-center font-weight-bold" cols="2" sm="1">
          <v-card outlined tile>{{ $t("dong") }} / {{ $t("ho") }}</v-card>
        </v-col>
        <v-col cols="10" sm="3">
          <v-card outlined tile height="100%">
            <span v-if="!!paper.address.dong"> {{ paper.address.dong }} {{ $t("dong") }} </span>
            <span v-if="!!paper.address.ho"> {{ paper.address.ho }} {{ $t("ho") }} </span>
          </v-card>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <template v-for="(realestate_field_name, index) in fields_names.realestate_fields_name">
          <v-col class="text-center font-weight-bold" cols="3" sm="2" :key="`name` + index">
            <v-card outlined tile>{{ $t(realestate_field_name) }}</v-card>
          </v-col>
          <v-col class="text-center" cols="3" sm="2" :key="`value-` + index">
            <v-card
              v-if="
                realestate_field_name == 'building_area' || realestate_field_name == 'lot_area'
              "
              outlined
              tile
              >{{ paper[realestate_field_name] }}㎡</v-card
            >
            <v-card
              v-else-if="
                realestate_field_name == 'land_category' ||
                  realestate_field_name == 'building_category'
              "
              outlined
              tile
            >
              {{ $getConstI18(realestate_field_name, paper[realestate_field_name]) }}
            </v-card>
            <v-card v-else outlined tile>{{ paper[realestate_field_name] }}</v-card>
          </v-col>
        </template>
      </v-row>
    </div>
    <div id="v-terms-and-conditions">
      <div class="mt-5">2. {{ $t("terms_and_conditions") }}</div>
      <div>{{ $t("terms_and_conditions_intro") }}</div>
      <v-row no-gutters>
        <template v-for="(contract_field_name, index) in fields_names.contract_fields_name">
          <template v-if="paper[contract_field_name] != undefined">
            <v-col class="text-center font-weight-bold" cols="3" sm="2" :key="`name` + index">
              <v-card outlined tile>{{ $t(contract_field_name) }}</v-card>
            </v-col>
            <v-col class="text-center" cols="3" sm="2" :key="`value-` + index">
              <v-card outlined tile>{{ paper[contract_field_name] }}{{ $t("won") }}</v-card>
            </v-col>
          </template>
        </template>
        <v-row no-gutters v-if="seller && seller.profile.bank_name">
          <v-col class="text-center font-weight-bold" cols="3" sm="2">
            <v-card outlined tile>{{ $t("bank_account") }}</v-card>
          </v-col>
          <v-col class="text-center" cols="9" sm="10">
            <v-card outlined tile
              >{{ $getConstI18("bank_category", seller.profile.bank_name) }}
              {{ seller.profile.user.name }}
              {{ seller.profile.account_number }}</v-card
            >
          </v-col>
        </v-row>
        <p
          v-if="paper.from_date && paper.to_date"
          class="ma-0"
          v-html="
            $t('terms_and_conditions_period', {
              from_year: paper.from_date.split('-')[0],
              from_month: paper.from_date.split('-')[1],
              from_day: paper.from_date.split('-')[2],
              to_year: paper.to_date.split('-')[0],
              to_month: paper.to_date.split('-')[1],
              to_day: paper.to_date.split('-')[2]
            })
          "
        ></p>
      </v-row>
      <v-row class="contract-details" no-gutters>
        <v-col cols="12" class="text-right no-print">
          <v-btn
            v-if="!currentContractor"
            :to="{
              name: 'paper-editor',
              params: { contract_details: paper.contract_details }
            }"
            dark
            >{{ $t("load_contract_details") }}</v-btn
          >
        </v-col>
        <quill-editor
          id="v-special-agreement"
          ref="myQuillEditor"
          v-model="paper.contract_details"
          :options="options"
          :disabled="true"
        />
      </v-row>
    </div>
    <template v-if="paper.paper_contractors">
      <v-divider></v-divider>
      <div
        v-if="$getConstByName('status_category', 'requesting') == paper.status"
        class="text-caption red--text"
      >
        {{ $t("paper_requesting_subtitle") }}
      </div>
      <div>
        {{
          $t("paper_confirm_and_signature", {
            year: paper.updated_at.split("-")[0],
            month: paper.updated_at.split("-")[1],
            day: paper.updated_at.split("-")[2].split(" ")[0]
          })
        }}
      </div>
      <div id="v-contractor-info">
        <template v-if="seller">
          <ContractorItem
            :contractor="seller"
            :fields="fields_names.basic_profile_fields"
            :paper="paper"
            @allowPaper="allowPaper"
            @openSignaturePad="open"
          ></ContractorItem>
        </template>
        <template v-if="buyer">
          <ContractorItem
            :contractor="buyer"
            :fields="fields_names.basic_profile_fields"
            :paper="paper"
            @allowPaper="allowPaper"
            @openSignaturePad="open"
          ></ContractorItem>
        </template>
        <template v-if="expert">
          <ContractorItem
            :contractor="expert"
            :fields="fields_names.expert_profile_fields"
            :paper="paper"
            @allowPaper="allowPaper"
            @openSignaturePad="open"
          ></ContractorItem>
        </template>
      </div>
    </template>
    <div id="v-ve" v-if="expert != undefined">
      <div class="page-divide mt-4">
        <v-divider></v-divider>
      </div>
      <v-spacer></v-spacer>
      <v-btn class="mt-4 no-print" color="black" dark @click="isMobile = !isMobile">
        <span v-if="isMobile">{{ $t("view_pc_version") }}</span>
        <span v-if="isMobile == false">{{ $t("view_mobile_version") }}</span>
      </v-btn>
      <VerifyingExplanationEditor
        v-if="isMobile"
        class="mt-4"
        :ve="paper.verifying_explanation"
        :validation_check="true"
        :readonly="true"
      >
        <template v-slot:footer>
          <template v-if="seller != null">
            <ContractorItem
              :contractor="seller"
              :fields="fields_names.basic_profile_fields"
              :paper="paper"
              :isVerifyingExplanation="true"
              @allowPaper="allowPaper"
              @openSignaturePad="open"
            ></ContractorItem>
          </template>
          <template v-if="buyer != null">
            <ContractorItem
              :contractor="buyer"
              :fields="fields_names.basic_profile_fields"
              :paper="paper"
              :isVerifyingExplanation="true"
              @allowPaper="allowPaper"
              @openSignaturePad="open"
            ></ContractorItem>
          </template>
          <template v-if="expert != null">
            <ContractorItem
              :contractor="expert"
              :fields="fields_names.expert_profile_fields"
              :paper="paper"
              :isVerifyingExplanation="true"
              @allowPaper="allowPaper"
              @openSignaturePad="open"
            ></ContractorItem>
          </template>
        </template>
      </VerifyingExplanationEditor>
      <VerifyingExplanation v-if="isMobile == false" class="mt-4" :paper="paper">
        <template v-slot:footer>
          <v-btn
            id="v-ve-signature"
            class="no-print"
            v-if="
              !isPaperRequest &&
                !isVerifyingExplanationSigned &&
                currentContractor.is_allowed == true
            "
            @click="open(true)"
            color="primary"
            dark
          >
            <v-icon>create</v-icon>
            {{ `${$t("verifying_explanation")} ${$t("signature")}` }}
          </v-btn>
        </template>
      </VerifyingExplanation>
    </div>
    <div id="v-done"></div>
    <v-dialog
      class="signature-dialog-parent"
      content-class="signature-dialog"
      v-model="dialog"
      persistent
      eager
    >
      <v-card>
        <VueSignaturePad
          class="signature-pad"
          ref="signaturePad"
          :customStyle="{ border: 'black 2px solid' }"
          :options="{ ...signature_pad_options }"
        />
        <v-card-title class="justify-center">
          {{ $t("please_sign") }}
        </v-card-title>
        <v-card-text class="red--text">{{ $t("signature_effect") }}</v-card-text>
        <v-card-actions>
          <v-btn color="blue darken-1" text @click="dialog = false">{{ $t("close") }}</v-btn>
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
    <v-divider class="no-print"></v-divider>
    <v-row class="no-print" justify="end">
      <v-btn color="black" text rounded @click="window_print()" dark small>
        <v-icon>print</v-icon>
      </v-btn>
    </v-row>
    <CustomTour
      name="paper-detail"
      :steps="steps"
      :options="tourOptions"
      :callbacks="tourCallbacks"
    />
  </v-container>
</template>

<script>
import { apiService } from "@/common/api_service";
import { applyValidation } from "@/common/common_api";
import ContractorItem from "@/components/ContractorItem";
import ActionItems from "@/components/ActionItems";
import VerifyingExplanation from "@/components/VerifyingExplanation";
import VerifyingExplanationEditor from "@/components/VerifyingExplanationEditor";

export default {
  name: "PaperDetail",
  props: {
    id: {
      type: [Number, String],
      required: true
    }
  },
  components: {
    ContractorItem,
    ActionItems,
    VerifyingExplanation,
    VerifyingExplanationEditor
  },
  computed: {
    isAuthor: function() {
      return this.paper.author === this.requestUser;
    },
    isPaperDone: function() {
      return this.paper.status == this.$getConstByName("STATUS_CATEGORY", "DONE");
    },
    isPaperRequest: function() {
      return this.paper
        ? this.paper.status == this.$getConstByName("STATUS_CATEGORY", "REQUESTING")
        : undefined;
    },
    isVerifyingExplanationSigned: function() {
      return this.currentContractor
        ? this.currentContractor.explanation_signature &&
            this.paper.updated_at <= this.currentContractor.explanation_signature.updated_at
        : undefined;
    },
    deadlineToModify: function() {
      let paper_updated_at = this.paper.updated_at;
      let deadline = undefined;
      if (this.paper.paper_contractors != undefined) {
        const min_sign_updated_at_str = this.paper.paper_contractors.reduce((acc, loc) => {
          let min_updated_at = acc;
          let signature_updated_at = this.$get(loc, "signature.updated_at");
          let explanation_signature_updated_at = this.$get(
            loc,
            "explanation_signature.updated_at"
          );
          if (
            signature_updated_at &&
            signature_updated_at > paper_updated_at &&
            signature_updated_at < min_updated_at
          ) {
            min_updated_at = signature_updated_at;
          }
          if (
            explanation_signature_updated_at &&
            explanation_signature_updated_at > paper_updated_at &&
            explanation_signature_updated_at < min_updated_at
          ) {
            min_updated_at = explanation_signature_updated_at;
          }
          return min_updated_at;
        }, "9999-12-31");
        //Initial date so it returns undefined.
        if (min_sign_updated_at_str == "9999-12-31") {
          return undefined;
        }
        if (paper_updated_at > min_sign_updated_at_str) {
          return undefined;
        }
        const min_sign_updated_at = new Date(min_sign_updated_at_str);
        deadline = min_sign_updated_at;
        deadline.setTime(min_sign_updated_at.getTime() + 24 * 60 * 60 * 1000);
        if (new Date() > deadline) {
          return "0000-00-00";
        }
        return `${deadline.getFullYear()}-${deadline.getMonth() + 1}-${deadline.getDate()} ${(
          "0" + deadline.getHours()
        ).slice(-2)}:${("0" + deadline.getMinutes()).slice(-2)}:${(
          "0" + deadline.getSeconds()
        ).slice(-2)}`;
      } else {
        return undefined;
      }
    },
    currentContractor: function() {
      if (this.paper.paper_contractors) {
        return this.paper.paper_contractors.find(
          (item) => item.profile.user.email == this.requestUser
        );
      } else {
        return false;
      }
    },
    steps() {
      return [
        /*The reason , offset is -100 , is scoll up app-bar hide vue-tour box.*/
        {
          target: "#v-paper-detail",
          content: `${this.$t("tour_paper_detail")}`,
          duration: 10,
          offset: -60,
          params: {
            highlight: false
          }
        },
        {
          target: "#v-hide",
          content: `${this.$t("tour_paper_hide")}`,
          duration: 10,
          offset: -60
        },
        {
          target: "#v-desc-realestate",
          content: `${this.$t("tour_detail_desc_relesate")}`,
          duration: 10,
          offset: -60
        },
        {
          target: "#v-terms-and-conditions",
          content: `${this.$t("tour_detail_terms_and_conditions")}`,
          duration: 10,
          offset: -200
        },
        {
          target: "#v-contractor-info",
          content: `${this.$t("tour_detail_contractor_info")}`,
          duration: 10,
          offset: -200
        },
        {
          target: "#v-contractor-btns",
          content: `${this.$t("tour_approve")}`,
          duration: 10,
          offset: -60
        },
        {
          target: "#v-requesting",
          content: `${this.$t("tour_requesting")}`,
          duration: 10,
          offset: -60
        },
        {
          target: "#v-contract-details",
          content: `${this.$t("tour_detail_contract_details")}`,
          duration: 10,
          offset: -200
        },
        {
          target: "#v-signature",
          content: `${this.$t("tour_signature")}`,
          duration: 10,
          offset: -60
        },
        {
          target: "#v-ve",
          content: `${this.$t("tour_ve")}`,
          duration: 10,
          offset: -220,
          params: {
            highlight: false
          }
        },
        {
          target: "#v-ve-signature",
          content: `${this.$t("tour_ve_signature")}`,
          duration: 10,
          offset: -60
        },
        {
          target: "#v-done",
          content: `${this.$t("tour_done")}`,
          duration: 10,
          offset: -60,
          params: {
            highlight: false
          }
        }
      ];
    },
    expert: function() {
      if (this.paper.paper_contractors != undefined) {
        for (let i = 0; i < this.paper.paper_contractors.length; i++) {
          if (
            this.paper.paper_contractors[i].group ==
            this.$getConstByName("CONTRACTOR_CATEGORY", "expert")
          ) {
            return this.paper.paper_contractors[i];
          }
        }
      }
      return undefined;
    },
    seller: function() {
      if (this.paper.paper_contractors != undefined) {
        for (let i = 0; i < this.paper.paper_contractors.length; i++) {
          if (
            this.paper.paper_contractors[i].group ==
            this.$getConstByName("CONTRACTOR_CATEGORY", "seller")
          ) {
            return this.paper.paper_contractors[i];
          }
        }
      }
      return undefined;
    },
    buyer: function() {
      if (this.paper.paper_contractors != undefined) {
        for (let i = 0; i < this.paper.paper_contractors.length; i++) {
          if (
            this.paper.paper_contractors[i].group ==
            this.$getConstByName("CONTRACTOR_CATEGORY", "buyer")
          ) {
            return this.paper.paper_contractors[i];
          }
        }
      }
      return undefined;
    }
  },
  data() {
    return {
      refresh_key: 0,
      isLoading: true,
      isMobile: false,
      dialog: false,
      paper: { trade_category: null, paper_contractors: null },
      is_explanation_signature: false,
      is_paper_updated: false,
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
          {
            name: "address",
            key: "full_address",
            is_computed: true,
            cols: "9",
            md: "10",
            lg: "11"
          },
          { name: "name", key: "user.name", cols: "9", sm: "3", md: "2" },
          {
            name: "birthday",
            key: "user.birthday",
            cols: "9",
            sm: "3",
            md: "2"
          },
          { name: "mobile_number", cols: "9", sm: "3", md: "2" },
          {
            name: "bank_name",
            const_name: "bank_category",
            cols: "9",
            sm: "3",
            md: "2"
          },
          { name: "account_number", cols: "9", sm: "3", md: "2" }
        ],
        expert_profile_fields: [
          {
            name: "registration_number",
            key: "expert_profile.registration_number",
            cols: "9",
            md: "10",
            lg: "4"
          },
          {
            name: "shop_name",
            key: "expert_profile.shop_name",
            cols: "9",
            md: "10",
            lg: "6"
          },
          {
            name: "address",
            key: "full_address",
            is_computed: true,
            cols: "9",
            md: "10",
            lg: "11"
          },
          { name: "name", key: "user.name", cols: "9", sm: "3", md: "2" },
          {
            name: "birthday",
            key: "user.birthday",
            cols: "9",
            sm: "3",
            md: "2"
          },
          { name: "mobile_number", cols: "9", sm: "3", md: "2" },
          {
            name: "bank_name",
            const_name: "bank_category",
            cols: "9",
            sm: "3",
            md: "2"
          },
          { name: "account_number", cols: "9", sm: "3", md: "2" }
        ]
      },
      requestUser: null,
      signature_pad_options: {
        minWidth: 3,
        maxWidth: 3,
        penColor: "black"
      },
      options: {
        modules: {
          toolbar: false
        }
      },
      tourCallbacks: {
        onPreviousStep: this.previousStepTour,
        onNextStep: this.nextStepTour
      },
      tourOptions: {
        highlight: true,
        stopOnTargetNotFound: false,
        useKeyboardNavigation: false
      }
    };
  },
  methods: {
    window_print() {
      window.print();
    },
    allowPaper(is_allowed) {
      this.isLoading = true;
      let endpoint = `/api/contractors/${this.currentContractor.id}/allow-paper/`;
      let method = "PUT";

      apiService(endpoint, method, {
        is_allowed: is_allowed
      }).then((data) => {
        if (data.id != undefined) {
          this.is_paper_updated = true;
          this.paper = data;
        } else {
          applyValidation(data);
        }
        this.isLoading = false;
      });
    },
    hidePaper(is_hidden) {
      this.isLoading = true;
      let endpoint = `/api/contractors/${this.currentContractor.id}/hide-paper/`;
      let method = "PUT";

      apiService(endpoint, method, {
        is_hidden: is_hidden
      }).then((data) => {
        if (data.id != undefined) {
          this.is_paper_updated = true;
          this.paper = data;
        } else {
          applyValidation(data);
        }
        this.isLoading = false;
      });
    },
    getPaperData() {
      this.isLoading = true;
      let endpoint = `/api/papers/${this.id}/`;
      apiService(endpoint).then((data) => {
        if (data.id != undefined) {
          this.paper = data;
        } else {
          applyValidation(data);
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
        alert(this.$i18n.t("signature_empty_warning"));
      }

      if (this.is_explanation_signature == true) {
        if (this.currentContractor.explanation_signature != undefined) {
          method = "PUT";
          endpoint = `/api/papers/${this.id}/explanation-signatures/${that.currentContractor.explanation_signature.id}/`;
        } else {
          endpoint = `/api/papers/${this.id}/explanation-signature/`;
        }
      } else {
        if (this.currentContractor.signature != undefined) {
          method = "PUT";
          endpoint = `/api/papers/${this.id}/signatures/${that.currentContractor.signature.id}/`;
        } else {
          endpoint = `/api/papers/${this.id}/signature/`;
        }
      }
      try {
        apiService(endpoint, method, {
          image: data,
          contractor: that.currentContractor.id
        }).then((data) => {
          if (data.id != undefined) {
            alert(that.$i18n.t("request_success"));
            this.is_paper_updated = true;
            if (that.is_explanation_signature == true) {
              that.currentContractor.explanation_signature = data;
            } else {
              that.currentContractor.signature = data;
            }
            that.dialog = false;
          } else {
            applyValidation(data);
          }
        });
      } catch (err) {
        alert(err);
      }
    },
    open(is_explanation_signature) {
      this.dialog = true;
      this.is_explanation_signature = is_explanation_signature;
      this.$nextTick(() => {
        this.$refs.signaturePad.resizeCanvas();
      });
    },
    nextStepTour(currentStep) {
      console.log(currentStep);
      for (var i = currentStep + 1; i < this.steps.length; i++) {
        const target_element = document.querySelector(this.steps[i].target);
        if (target_element) {
          if (i != currentStep + 1) {
            const tour = this.$tours["paper-detail"];
            this.$nextTick(() => {
              tour.currentStep = i;
            });
          }
          break;
        }
      }
    },
    previousStepTour(currentStep) {
      for (var i = currentStep - 1; i > -1; i--) {
        const target_element = document.querySelector(this.steps[i].target);
        if (target_element) {
          console.log(target_element, i);
          const tour = this.$tours["paper-detail"];
          this.$nextTick(() => {
            tour.currentStep = i;
          });
          break;
        }
      }
    }
  },
  beforeDestroy() {
    this.$store.commit("SET_IS_PAPER_UPDATED", this.is_paper_updated);
    this.$tours["paper-detail"].stop();
  },
  created() {
    this.getPaperData();
    this.$store.commit("SET_IS_PAPER_UPDATED", false);
    this.requestUser = this.$store.state.user.email;
  },
  mounted() {
    if (this.$store.state.user_setting.is_tour_on && this.$store.state.user_category === "user") {
      this.$tours["paper-detail"].start();
    }
  }
};
</script>
<style scoped>
.container {
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  -o-user-select: none;
  user-select: none;
}
.signature-dialog-parent {
  z-index: 90000001 !important;
}
.contract-details /deep/ p {
  margin-bottom: 0px !important;
}
hr {
  margin-top: 16px;
}
.quill-editor /deep/ .ql-snow {
  border: 0px !important;
}
.quill-editor /deep/ .ql-editor {
  padding: 0px !important;
}
.row {
  margin: 0px !important;
}
.theme--light.v-sheet--outlined {
  border: 1px solid rgba(0, 0, 0, 0.6);
}
</style>
