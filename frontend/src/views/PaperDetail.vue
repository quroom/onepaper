<template>
  <v-container v-if="!isLoading" fluid>
    <template>
      <div
        v-if="paper.trade_category != null"
        class="mt-4 text-h4 font-weight-bold text-center"
      >
        {{
          `${$t("realestate")} ${$getConstI18(
            "TRADE_CATEGORY",
            paper.trade_category
          )} ${$t("contract")}`
        }}
      </div>
      <div class="text-caption red--text">{{ $t("paper_subtitle") }}</div>
      <v-row v-if="paper.author" class="mt-4 no-print">
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
      <ActionItems
        v-if="
          isPaperAuthor &&
            !isPaperDone &&
            (deadlineToModify > '0001-1-1' || deadlineToModify == undefined)
        "
        :id="paper.id"
        delete_url="/api/papers/"
        delete_router_name="home"
        editor_router_name="paper-editor"
      />
      <div
        v-if="!isPaperDone"
        class="text-right text-caption white--text no-print"
      >
        <span v-if="deadlineToModify > '0001-1-1'" class="red">
          {{ `${$t("modify_delete_deadline")} : ${deadlineToModify}` }}
        </span>
        <span v-if="deadlineToModify < '0001-1-1'" class="red">
          {{ $t("modify_delete_deadline_expired") }}
        </span>
      </div>
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
        <v-col cols="10" sm="7">
          <v-card outlined tile>{{ paper.address.old_address }}</v-card>
        </v-col>
        <v-col class="text-center font-weight-bold" cols="2" sm="1">
          <v-card outlined tile>{{ $t("dong") }} / {{ $t("ho") }}</v-card>
        </v-col>
        <v-col cols="10" sm="3">
          <v-card outlined tile height="100%">
            <span v-if="!!paper.address.dong">
              {{ paper.address.dong }} {{ $t("dong") }}
            </span>
            <span v-if="!!paper.address.ho">
              {{ paper.address.ho }} {{ $t("ho") }}
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
            <v-card
              v-else-if="
                realestate_field_name == 'land_category' ||
                  realestate_field_name == 'building_category'
              "
              outlined
              tile
            >
              {{
                $getConstI18(
                  realestate_field_name,
                  paper[realestate_field_name]
                )
              }}
            </v-card>
            <v-card v-else outlined tile>{{
              paper[realestate_field_name]
            }}</v-card>
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
              <v-card outlined tile
                >{{ paper[contract_field_name] }}{{ $t("won") }}</v-card
              >
            </v-col>
          </template>
        </template>
      </v-row>
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
      <div class="mt-5">3. {{ $t("contractor_info") }}</div>
      <div
        v-if="$getConstByName('status_category', 'requesting') == paper.status"
        class="text-caption red--text"
      >
        {{ $t("paper_requesting_subtitle") }}
      </div>
      <div>{{ $t("contractor_info_intro") }}</div>
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
      <div class="mt-5">4. {{ $t("special_agreement") }}</div>
      <quill-editor
        ref="myQuillEditor"
        v-model="paper.special_agreement"
        :options="options"
        :disabled="true"
      />
    </template>
    <template v-if="expert != undefined">
      <div class="page-divide mt-4">
        <v-divider></v-divider>
      </div>
      <v-spacer></v-spacer>
      <v-btn
        class="mt-4 no-print"
        color="black"
        dark
        @click="isMobile = !isMobile"
      >
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
      <VerifyingExplanation
        v-if="isMobile == false"
        class="mt-4"
        :paper="paper"
      >
        <template v-slot:footer>
          <v-btn
            class="no-print"
            v-if="!isPaperRequest && !isVerifyingExplanationSigned"
            @click="open(true)"
            color="red"
            dark
          >
            <v-icon>create</v-icon>
            {{ `${$t("verifying_explanation")} ${$t("signature")}` }}
          </v-btn>
        </template>
      </VerifyingExplanation>
    </template>
    <v-dialog
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
    isPaperAuthor: function() {
      return this.paper.author === this.requestUser;
    },
    isPaperDone: function() {
      return (
        this.paper.status == this.$getConstByName("STATUS_CATEGORY", "DONE")
      );
    },
    isPaperRequest: function() {
      return this.paper
        ? this.paper.status ==
            this.$getConstByName("STATUS_CATEGORY", "REQUESTING")
        : undefined;
    },
    isVerifyingExplanationSigned: function() {
      return this.currentContractor
        ? this.currentContractor.explanation_signature &&
            this.paper.updated_at <=
              this.currentContractor.explanation_signature.updated_at
        : undefined;
    },
    deadlineToModify: function() {
      let paper_updated_at = this.paper.updated_at;
      let deadline = undefined;
      if (this.paper.paper_contractors != undefined) {
        const min_sign_updated_at_str = this.paper.paper_contractors.reduce(
          (acc, loc) => {
            let min_updated_at = acc;
            let signature_updated_at = this.$get(loc, "signature.updated_at");
            let explanation_signature_updated_at = this.$get(
              loc,
              "explanation_signature.updated_at"
            );
            if (signature_updated_at && signature_updated_at < min_updated_at) {
              min_updated_at = signature_updated_at;
            }
            if (
              explanation_signature_updated_at &&
              explanation_signature_updated_at < min_updated_at
            ) {
              min_updated_at = explanation_signature_updated_at;
            }
            return min_updated_at;
          },
          "9999-12-31"
        );
        //Initial date so it returns undefined.
        if (min_sign_updated_at_str == "9999-12-31") {
          return undefined;
        }
        if (paper_updated_at > min_sign_updated_at_str) {
          return undefined;
        }
        const min_sign_updated_at = new Date(min_sign_updated_at_str);
        deadline = min_sign_updated_at;
        deadline.setTime(min_sign_updated_at.getTime() + 12 * 60 * 60 * 1000);
        if (new Date() > deadline) {
          return "0000-00-00";
        }
        return `${deadline.getFullYear()}-${deadline.getMonth() +
          1}-${deadline.getDate()} ${("0" + deadline.getHours()).slice(-2)}:${(
          "0" + deadline.getMinutes()
        ).slice(-2)}:${("0" + deadline.getSeconds()).slice(-2)}`;
      } else {
        return undefined;
      }
    },
    currentContractor: function() {
      return this.paper.paper_contractors.find(
        item => item.profile.user.email == this.requestUser
      );
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
      paper: { trade_category: null },
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
      }
    };
  },
  methods: {
    allowPaper() {
      this.isLoading = true;
      let endpoint = `/api/contractors/${this.currentContractor.id}/allow-paper/`;
      apiService(endpoint).then(data => {
        if (data.id != undefined) {
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
      apiService(endpoint).then(data => {
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
        }).then(data => {
          if (data.id != undefined) {
            alert(that.$i18n.t("request_success"));
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
    }
  },
  created() {
    this.getPaperData();
    this.requestUser = window.localStorage.getItem("email");
  }
};
</script>
<style scoped></style>
