<template>
  <div>
    <v-row v-if="paper" no-gutters>
      <v-col v-if="isExpert" class="text-center font-weight-bold">
        <v-card outlined tile color="grey lighten-2">
          {{ $t("realestate_agency") }}
          <img v-if="isSigned" class="stamp-img" :src="contractor.profile.expert_profile.stamp" />
        </v-card>
      </v-col>
      <v-col v-else class="text-center font-weight-bold">
        <v-card outlined tile color="grey lighten-2">{{
          $getConstI18("CONTRACTOR_CATEGORY", contractor.group)
        }}</v-card>
      </v-col>
      <v-col class="text-center" cols="auto">
        <v-card v-if="isAllowed" class="pa-0" outlined tile min-width="80">
          <v-btn
            v-if="!isPaperRequest && !isSigned && isContractor"
            class="signature-button"
            @click="openSignaturePad(isVerifyingExplanation)"
            color="red"
            dark
          >
            <v-icon>create</v-icon>
            {{ $t("signature") }}
          </v-btn>
          <template v-else>
            {{ $t("sign") }}
          </template>
          <img v-if="isSigned" class="signature-img" :src="signature_src" />
        </v-card>
        <v-card v-else>
          <v-btn
            v-if="isContractor"
            class="signature-button"
            @click="allowPaper"
            color="deep-purple"
            dark
          >
            <v-icon>done</v-icon>
            {{ $t("approve") }}
          </v-btn>
          <template v-else>
            <v-icon>donut_large</v-icon>
            {{ $t("requesting") }}
          </template>
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
    isAllowed: function() {
      return this.$get(this.contractor, "is_allowed", false);
    },
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
    isPaperRequest: function() {
      return this.paper.status == this.$getConstByName("STATUS_CATEGORY", "REQUESTING");
    },
    isContractor: function() {
      return this.contractor ? this.requestUser === this.contractor.profile.user.email : false;
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
        return null;
      }
    }
  },
  methods: {
    getComputed(key) {
      return this[key];
    },
    allowPaper() {
      this.$emit("allowPaper");
    },
    openSignaturePad(isVE) {
      this.$emit("openSignaturePad", isVE);
    }
  },
  created() {
    this.requestUser = window.localStorage.getItem("email");
  }
};
</script>

<style scoped>
.signature-button {
  z-index: 2;
  height: 100% !important;
  width: 100% !important;
}
.signature-img {
  width: 80px;
  z-index: 1;
  position: absolute;
  top: -8px;
  right: 0px;
}
.stamp-img {
  height: 50px;
  z-index: 1;
  position: absolute;
  top: -8px;
  right: 0px;
}
</style>
