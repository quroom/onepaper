<template>
  <div class="contractor">
    <v-row
      :id="isNotAuthorAndContractor && !isPaperDone ? 'v-contractor-btns' : ''"
      v-if="paper"
      no-gutters
      align="center"
    >
      <v-col v-if="isNotAuthorAndContractor" class="text-center" cols="auto">
        <v-card
          v-if="!isPaperProgress && !isPaperDone && contractor.is_allowed !== false"
          class="pa-0"
          outlined
          tile
          min-width="80"
        >
          <v-btn class="signature-button" @click="allowPaper(false)" color="red" dark tile>
            <v-icon>do_not_disturb</v-icon>
            {{ $t("deny") }}
          </v-btn>
        </v-card>
      </v-col>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-col
            v-bind="attrs"
            v-on="on"
            v-if="isExpert"
            class="contractor-print-title text-center font-weight-bold"
          >
            <v-card outlined tile color="grey lighten-2">
              {{ $t("realestate_agency") }}
              <img
                v-if="isSigned"
                class="stamp-img"
                :src="contractor.profile.expert_profile.stamp"
              />
            </v-card>
          </v-col>
          <v-col
            v-bind="attrs"
            v-on="on"
            v-else
            class="contractor-print-title text-center font-weight-bold"
          >
            <v-card outlined tile color="grey lighten-2">{{
              $getConstI18("CONTRACTOR_CATEGORY", contractor.group)
            }}</v-card>
          </v-col>
        </template>
        <span>{{ contractor.profile.user.email }}</span>
      </v-tooltip>
      <v-col class="contractor-print-title text-center" cols="auto">
        <v-card v-if="contractor.is_allowed == true" class="pa-0" tile min-width="80">
          <v-btn
            id="v-signature"
            v-if="!isPaperRequest && !isPaperDone && !isSigned && isContractor"
            class="signature-button"
            @click="openSignaturePad(isVerifyingExplanation)"
            color="primary"
            dark
            tile
          >
            <v-icon>create</v-icon>
            {{ $t("signature") }}
          </v-btn>
          <template v-else>
            {{ $t("sign") }}
          </template>
          <img v-if="isSigned || !isPaperRequest" class="signature-img" :src="signature_src" />
        </v-card>
        <v-card v-else class="pa-0" outlined tile min-width="80">
          <template v-if="contractor.is_hidden == false">
            <v-btn
              v-if="isContractor"
              class="signature-button"
              @click="allowPaper(true)"
              color="deep-purple"
              dark
              tile
            >
              <v-icon>done</v-icon>
              {{ $t("approve") }}
            </v-btn>
            <div id="v-requesting" v-else-if="contractor.is_allowed == null">
              <v-icon>donut_large</v-icon>
              {{ $t("requesting") }}
            </div>
            <span v-else-if="contractor.is_allowed == false" class="red--text">
              <v-icon class="red--text">do_not_disturb</v-icon>
              {{ $t("denied") }}
            </span>
          </template>
          <span v-else-if="contractor.is_allowed == false" class="red--text">
            <v-icon class="red--text">do_not_disturb</v-icon>
            {{ $t("denied") }}
          </span>
        </v-card>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <template v-for="(field, index) in fields">
        <v-col
          class="text-center font-weight-bold"
          :cols="label_cols ? label_cols.cols : '3'"
          :md="label_cols ? label_cols.md : '2'"
          :lg="label_cols ? label_cols.lg : '1'"
          :key="`name` + index"
        >
          <v-card outlined tile>{{ $t(field.name) }}</v-card>
        </v-col>
        <template>
          <v-col
            class="text-center"
            :cols="field.cols"
            :xs="field.xs"
            :md="field.md"
            :lg="field.lg"
            :key="`value-` + index"
          >
            <!--#FIXME: Need to add commend -->
            <v-card outlined tile>
              {{
                field.is_computed
                  ? getComputed(field.key)
                  : field.key && $get(computed_profile, field.key)
                  ? $get(computed_profile, field.key)
                  : computed_profile[field.name]
                  ? field.const_name
                    ? $getConstI18(field.const_name, computed_profile[field.name])
                    : computed_profile[field.name]
                  : ""
              }}
            </v-card>
          </v-col>
        </template>
      </template>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "ContractorItem",
  props: {
    contractor: {
      type: Object,
      required: false
    },
    fields: {
      type: Array,
      required: true
    },
    label_cols: {
      type: Object
    },
    paper: {
      type: Object,
      required: false
    },
    profile: {
      type: Object,
      required: false
    },
    isVerifyingExplanation: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  data() {
    return {
      requestUser: null
    };
  },
  computed: {
    isExpert: function() {
      return this.contractor.group == this.$getConstByName("CONTRACTOR_CATEGORY", "expert");
    },
    isSigned: function() {
      if (this.isVerifyingExplanation) {
        return (
          this.contractor.explanation_signature &&
          this.paper.updated_at <= this.contractor.explanation_signature.updated_at
        );
      } else {
        return (
          this.contractor.signature &&
          this.paper.updated_at <= this.contractor.signature.updated_at
        );
      }
    },
    isPaperDone: function() {
      return this.paper.status == this.$getConstByName("STATUS_CATEGORY", "DONE");
    },
    isPaperProgress: function() {
      return this.paper.status == this.$getConstByName("STATUS_CATEGORY", "PROGRESS");
    },
    isPaperRequest: function() {
      return this.paper.status == this.$getConstByName("STATUS_CATEGORY", "REQUESTING");
    },
    isContractor: function() {
      return this.contractor ? this.requestUser === this.contractor.profile.user.email : false;
    },
    isNotAuthorAndContractor: function() {
      return this.contractor
        ? this.requestUser != this.paper.author &&
            this.requestUser === this.contractor.profile.user.email
        : false;
    },
    computed_profile: function() {
      return this.profile ? this.profile : this.contractor.profile;
    },
    full_address: function() {
      const address = this.computed_profile.address;
      var fullAddress = address.old_address;
      var dongExist = false;
      if (address.dong) {
        fullAddress += `, ${address.dong}${this.$i18n.t("dong")}`;
        dongExist = true;
      }
      if (address.ho) {
        if (dongExist) {
          fullAddress += ` ${address.ho}${this.$i18n.t("ho")}`;
        } else {
          fullAddress += `, ${address.ho}${this.$i18n.t("ho")}`;
        }
      }
      return fullAddress;
    },
    signature_src: function() {
      if (this.isSigned) {
        return this.isVerifyingExplanation
          ? this.$get(this.contractor, "explanation_signature.image", null)
          : this.$get(this.contractor, "signature.image", null);
      } else {
        if (this.paper.mandates) {
          const matched_profile = this.paper.mandates.find(
            (item) => item.designator.user.email == this.contractor.profile.user.email
          );
          if (matched_profile) {
            return matched_profile.designator_signature;
          }
        }
        return null;
      }
    }
  },
  methods: {
    getComputed(key) {
      return this[key];
    },
    allowPaper(is_allowed) {
      this.$emit("allowPaper", is_allowed);
    },
    openSignaturePad(isVE) {
      this.$emit("openSignaturePad", isVE);
    }
  },
  created() {
    this.requestUser = this.$store.state.user.email;
  }
};
</script>

<style scoped>
.contractor {
  -webkit-user-select: text;
  -moz-user-select: text;
  -ms-user-select: text;
  -o-user-select: text;
  user-select: text;
}
@media print {
  .contractor-print-title {
    position: relative;
    font-size: 13px;
  }
}
.signature-button {
  z-index: 2;
  height: 100% !important;
  width: 100% !important;
}
.signature-img {
  height: 40px;
  z-index: 1;
  position: absolute;
  top: 0px;
  right: 0px;
  bottom: 0px;
  left: 0px;
  margin: auto;
}
.stamp-img {
  height: 40px;
  z-index: 1;
  position: absolute;
  top: -8px;
  right: 0px;
}
</style>
