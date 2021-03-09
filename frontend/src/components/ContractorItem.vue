<template>
  <div>
    <v-row v-if="paper" no-gutters>
      <v-col v-if="contractor.group==$getConstByName('CONTRACTOR_CATEGORY', 'expert')" class=" text-center font-weight-bold">
        <v-card outlined tile color="grey lighten-2">
          {{ $t("realestate_agency") }}
            <img class="stamp-img" :src="contractor.profile.expert_profile.stamp"/>
        </v-card>
      </v-col>
      <v-col v-else class="text-center font-weight-bold">
        <v-card outlined tile color="grey lighten-2">{{ $getConstI18('CONTRACTOR_CATEGORY', contractor.group) }}</v-card>
      </v-col>
      <v-col class="text-center" cols="auto">
        <v-card v-if="isAllowed" class="pa-0" outlined tile>
          <template v-if="!isVerifyingExplanation">
            <v-btn
              v-if="!isPaperRequest && !isSigned && isContractor"
              class="signature-button"
              @click="openSignaturePad()"
              color="red"
              dark
            >
              <v-icon>create</v-icon>
              {{ $t("signature") }}
            </v-btn>
            <template v-else>
              {{ $t("sign") }}
            </template>
            <a v-if="isSigned" v-bind:href="contractor.signature.image" target="_blank">
              <img class="signature-img" :src="contractor.signature.image" />
            </a>
          </template>
          <template v-else>
            <v-btn
              v-if="!isPaperRequest && !isVerifyingExplanationSigned && isContractor"
              class="signature-button"
              @click="openSignaturePad()"
              color="red"
              dark
            >
              <v-icon>create</v-icon>
              {{ $t("signature") }}
            </v-btn>
            <template v-else>
              {{ $t("sign") }}
            </template>
            <a v-if="isVerifyingExplanationSigned" v-bind:href="contractor.explanation_signature.image" target="_blank">
              <img class="signature-img" :src="contractor.explanation_signature.image" />
            </a>
          </template>
        </v-card>
        <v-card v-else>
          <v-btn  v-if="isContractor" class="signature-button" @click="allowPaper" color="deep-purple" dark>
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
        <template v-if="field.key && $get(computed_profile, field.key)">
          <v-col class="text-center font-weight-bold" :cols="label_cols ? label_cols.cols : '3' " :md="label_cols ? label_cols.md : '2'" :lg="label_cols ? label_cols.lg : '1'" :key="`name`+index">
            <v-card outlined tile>{{ $t(field.name) }}</v-card>
          </v-col>
          <v-col
            class="text-center"
            :cols="field.cols"
            :xs="field.xs"
            :md="field.md"
            :lg="field.lg"
            :key="`value-` + index"
          >
            <v-card outlined tile>{{ $get(computed_profile, field.key) }}</v-card>
          </v-col>
        </template>
        <template v-else-if="computed_profile[field.name]">
          <v-col class="text-center font-weight-bold" :cols="label_cols ? label_cols.cols : '3' " :md="label_cols ? label_cols.md : '2'" :lg="label_cols ? label_cols.lg : '1'" :key="`name`+index">
          <v-card outlined tile>{{ $t(field.name) }}</v-card>
          </v-col>
          <v-col v-if="field.const_name"
            class="text-center"
            :cols="field.cols"
            :xs="field.xs"
            :md="field.md"
            :lg="field.lg"
            :key="`value-` + index">
            <v-card outlined tile>{{ $getConstI18(field.const_name, computed_profile[field.name]) }}</v-card>
          </v-col>
          <v-col
            v-else
            class="text-center"
            :cols="field.cols"
            :xs="field.xs"
            :md="field.md"
            :lg="field.lg"
            :key="`value-` + index"
          >
            <v-card outlined tile>{{ computed_profile[field.name] }}</v-card>
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
      default: false,
    }
  },
  data() {
    return {
      requestUser: null
    }
  },
  computed: {
    isAllowed: function() {
      return this.contractor ? this.contractor.is_allowed : undefined;
    },
    isSigned: function() {
      return this.contractor ? this.contractor.signature && this.paper.updated_at <= this.contractor.signature.updated_at : undefined;
    },
    isPaperRequest: function() {
      return this.paper ? this.paper.status == this.$getConstByName('STATUS_CATEGORY', 'REQUESTING') : undefined;
    },
    isContractor: function() {
      return this.contractor ? this.requestUser === this.contractor.profile.user.email : undefined;
    },
    isVerifyingExplanationSigned: function() {
      return this.contractor ? this.contractor.explanation_signature && this.paper.updated_at <= this.contractor.explanation_signature.updated_at : undefined;
    },
    computed_profile: function() {
      return this.profile ? this.profile : this.contractor.profile;
    }
  },
  methods: {
    allowPaper() {
      this.$emit("allowPaper")
    },
    openSignaturePad() {
      this.$emit("openSignaturePad", this.isVerifyingExplanation)
    }
  },
  created() {
    this.requestUser = window.localStorage.getItem('email')
  }
}
</script>

<style scoped>
.signature-button {
  z-index: 2;
  height: 100% !important;
  width: 100% !important;
}
.signature-img {
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
  right: 0px;
  top: -15px;
  cursor: pointer;
}
</style>