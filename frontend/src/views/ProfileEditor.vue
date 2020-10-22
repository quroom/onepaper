<template>
  <v-container class="my-5">
    <!-- For expert user -->
    <v-row>      
      <v-col cols="4" md="2">
        <v-text-field v-model="name" :label="$t('name')" readonly></v-text-field>
      </v-col>
      <v-col cols="4" md="2">
        <v-text-field v-model="birthday" :label="$t('birthday')" readonly></v-text-field>
      </v-col>
    </v-row>
    <v-row v-if="is_request_expert || is_expert">
      <v-col class="text-center" cols="12">
        <div class="text-h5">{{ $t("profile") }}</div>
      </v-col>
      <v-col cols="12">
        <v-text-field
          class="profile_name"
          v-model="profile_name"
          :label="$t('profile_name')"
        ></v-text-field>
      </v-col>
      <v-col cols="4" md="2">
        <v-text-field
          v-model="registration_number"
          :label="$t('registration_number')"
        ></v-text-field>
      </v-col>
      <v-col cols="4" md="2">
        <v-text-field
          v-model="shop_name"
          :label="$t('shop_name')"
        ></v-text-field>
      </v-col>
      <v-col cols="8">
        <v-text-field
          v-model="address"
          :label="$t('shop_address')"
        ></v-text-field>
      </v-col>
      <v-col cols="4" md="2">
        <v-text-field
          v-model="mobile_number"
          :label="$t('mobile_number')"
        ></v-text-field>
      </v-col>
      <v-col cols="4" md="2">
        <v-text-field
          v-model="bank_name"
          :label="$t('bank_name')"
        ></v-text-field>
      </v-col>
      <v-col cols="4" md="2">
        <v-text-field
          v-model="account_number"
          :label="$t('account_number')"
        ></v-text-field>
      </v-col>
    </v-row>    
    <!-- For general user -->
    <v-row v-else>
      <v-col class="text-center" cols="12">
        <div class="text-h5">
          {{ $t("realestate_agency") }} {{ $t("profile") }}
        </div>
      </v-col>
      <v-col cols="12">
        <v-text-field
          class="profile_name"
          v-model="profile_name"
          :label="$t('profile_name')"
        ></v-text-field>
      </v-col>
      <v-col cols="8">
        <v-text-field v-model="address" :label="$t('address')"></v-text-field>
      </v-col>      
    </v-row>
    <v-row>
      <v-col cols="4" md="2">
        <v-file-input
          v-model="business_registration_certificate"
          :label="$t('business_registration_certificate')"
          accept="image/*"
          @click.stop
          @change="preview_image('business_registration_certificate')"
        ></v-file-input>
      </v-col>
      <v-col cols="4" md="2">
        <v-file-input
          v-model="agency_license"
          :label="$t('agency_license')"
          accept="image/*"
          @click.stop
          @change="preview_image('agency_license')"
        ></v-file-input>
      </v-col>
      <v-col cols="4" md="2">
        <v-file-input
          v-model="stamp"
          :label="$t('stamp')"
          accept="image/*"
          @click.stop
          @change="preview_image('stamp')"
        ></v-file-input>
      </v-col>
    </v-row>
    <v-btn class="mr-4" @click="onSubmit()">{{$t('submit')}}</v-btn>
    <v-row>
      <v-col
        class="d-flex child-flex"
        cols="4"
      >
        <img :src="business_registration_certificate_url" aspect-ratio="1"/>
      </v-col>
      <v-col
        class="d-flex child-flex"
        cols="4"
      >
        <img :src="agency_license_url" aspect-ratio="1"/>
      </v-col>
      <v-col
        class="d-flex child-flex"
        cols="4"
      >
        <img :src="stamp_url" aspect-ratio="1"/>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { apiService, apiService_formData } from "@/common/api.service";

export default {
  name: "ProfileEditor",
  props: {
    id: {
      type: [Number, String],
      required: false
    }
  },
  data() {
    return {
      is_expert: false,
      is_request_expert: false,
      name: null,
      birthday: null,
      profile_name: null,
      mobile_number: null,
      address: null,
      bank_name: null,
      account_number: null,
      registration_number: null,
      shop_name: null,
      business_registration_certificate: null,
      business_registration_certificate_url: null,
      agency_license: null,
      agency_license_url: null,
      stamp: null,
      stamp_url: null
    };
  },
  methods: {
    preview_image(name){
      console.log(name)
      this[name+"_url"] = window.URL.createObjectURL(this[name])
    },
    onSubmit() {
      const self = this;
      const formData = new FormData();
      formData.append('profile', this.profile_name);
      formData.append('mobile_number', this.mobile_number);
      formData.append('address', this.address);
      formData.append('bank_name', this.bank_name);
      formData.append('account_number', this.account_number);
      if(self.is_request_expert || self.is_expert) {
        formData.append('expert_profile.registration_number', this.registration_number);
        formData.append('expert_profile.shop_name', this.shop_name);
        formData.append('expert_profile.business_registration_certificate', this.business_registration_certificate);
        formData.append('expert_profile.agency_license', this.agency_license);
        formData.append('expert_profile.stamp', this.stamp);
      }      
      let endpoint = "/api/profiles/";
      let method = "POST";
      
      if (self.id !== undefined) {
        endpoint += `${self.id}/`;
        method = "PUT";
      }
      apiService_formData(endpoint, method, formData).then(data => {
        console.log(data)
      });
    }
  },
  async beforeRouteEnter(to, from, next) {
    console.log(to.params.id);
    if (to.params.id !== undefined) {
      let endpoint = `/api/profiles/${to.params.id}/`;
      let data = await apiService(endpoint);
      return next(
        vm => (
          (vm.name = data.user.name),
          (vm.birthday = data.user.birthday),
          (vm.profile_name = data.profile_name),
          (vm.address = data.address),
          (vm.mobile_number = data.mobile_number),
          (vm.bank_name = data.bank_name),
          (vm.account_number = data.account_number),
          (vm.registration_number = data.expert_profile.registration_number),
          (vm.shop_name = data.expert_profile.shop_name),
          (vm.business_registration_certificate_url = data.expert_profile.business_registration_certificate),
          (vm.agency_license_url = data.expert_profile.agency_license),
          (vm.stamp_url = data.expert_profile.stamp)
        )
      );
    } else {
      return next();
    }
  },
  created() {
    if (window.localStorage.getItem("is_expert") == "true") {
      this.is_expert = true;
    } else if (window.localStorage.getItem("request_expert") == "true") {
      this.is_request_expert = true;
    }
  }
};
</script>

<style>
.profile_name {
  width: 400px;
}
</style>
