<template>
  <ValidationObserver ref="obj">
    <v-container class="my-5">
      <!-- UserInfo -->
      <v-btn style="float:right" color="primary" :to="{ name: 'allowed-user-editor', params: { id: id } }"> {{ $t("add_user") }} </v-btn>
      <v-row>
        <v-col cols="4" md="2">
          <v-text-field
            v-model="username"
            :label="$t('username')"
            readonly
          ></v-text-field>
        </v-col>
        <v-col cols="4" md="2">
          <v-text-field
            v-model="name"
            :label="$t('name')"
            readonly
          ></v-text-field>
        </v-col>
        <v-col cols="4" md="2">
          <v-text-field
            v-model="birthday"
            :label="$t('birthday')"
            readonly
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <!-- Expert Profile -->
        <template v-if="is_request_expert || is_expert">
          <v-col class="text-center" cols="12">
            <div class="text-h5">
              {{ $t("realestate_agency") }} {{ $t("profile") }}
            </div>
          </v-col>
          <v-col cols="6" md="3">
            <ValidationProvider
              ref="registration_number"
              :name="$t('registration_number')"
              rules="required" v-slot="{ errors }">
              <v-text-field
                v-model="expert_profile.registration_number"
                :error-messages="errors"
                :label="$t('registration_number')"
              ></v-text-field>
            </ValidationProvider>
          </v-col>
          <v-col cols="6" md="3">
            <ValidationProvider ref="shop_name"  :name="$t('shop_name')" rules="required" v-slot="{ errors }">
              <v-text-field
                v-model="expert_profile.shop_name"
                :error-messages="errors"
                :label="$t('shop_name')"
              ></v-text-field>
            </ValidationProvider>
          </v-col>
          <v-col cols="10">
            <ValidationProvider ref="shop_address" :name="$t('address')" rules="required" v-slot="{ errors }">
              <v-text-field
                v-model="address"
                :error-messages="errors"
                :label="$t('shop_address')"
              ></v-text-field>
            </ValidationProvider>
          </v-col>
        </template>
        <template v-else>
          <v-col class="text-center" cols="12">
            <div class="text-h5">
              {{ $t("general") }} {{ $t("user") }} {{ $t("profile") }}
            </div>
          </v-col>
          <v-col cols="10">
            <ValidationProvider ref="address" :name="$t('address')" rules="required" v-slot="{ errors }">
              <v-text-field
                v-model="address"
                :error-messages="errors"
                :label="$t('address')"
              ></v-text-field>
            </ValidationProvider>
            </v-col>
        </template>
        <v-col cols="6" md="2">
          <ValidationProvider ref="address" :name="$t('address')" rules="required" v-slot="{ errors }">
            <v-text-field
              v-model="mobile_number"
              :error-messages="errors"
              :label="$t('mobile_number')"
            ></v-text-field>
          </ValidationProvider>
        </v-col>
        <v-col cols="6" md="2">
          <v-text-field
            v-model="bank_name"
            :label="$t('bank_name')"
          ></v-text-field>
        </v-col>
        <v-col cols="6" md="2">
          <v-text-field
            v-model="account_number"
            :label="$t('account_number')"
          ></v-text-field>
        </v-col>
        <template v-if="is_request_expert || is_expert">
          <v-col cols="4" md="2">
            <v-file-input
              v-model="expert_profile.business_registration_certificate"
              :label="$t('business_registration_certificate')"
              accept="image/*"
              @click.stop
              @change="preview_image('business_registration_certificate')"
            ></v-file-input>
          </v-col>
          <v-col cols="4" md="2">
            <v-file-input
              v-model="expert_profile.agency_license"
              :label="$t('agency_license')"
              accept="image/*"
              @click.stop
              @change="preview_image('agency_license')"
            ></v-file-input>
          </v-col>
          <v-col cols="4" md="2">
            <v-file-input
              v-model="expert_profile.garantee_insurance"
              :label="$t('garantee_insurance')"
              accept="image/*"
              @click.stop
              @change="preview_image('garantee_insurance')"
            ></v-file-input>
          </v-col>
          <v-col cols="4" md="2">
            <v-file-input
              v-model="expert_profile.stamp"
              :label="$t('stamp')"
              accept="image/*"
              @click.stop
              @change="preview_image('stamp')"
            ></v-file-input>
          </v-col>
          <v-row>
            <v-divider class="mx-4 text-center" style="display: inline;"></v-divider>
            <v-col class="text-center" cols="12">
            <div class="text-h5">
              {{ $t("attached_document") }}
            </div>
          </v-col>
          </v-row>
          <v-row>
            <v-col v-if="business_registration_certificate_url" class="d-flex child-flex" cols="6" md="3">
              <div class="absolute_text"> {{ $t("business_registration_certificate") }} </div>
              <a v-bind:href="business_registration_certificate_url" target="_blank">
                <img class="img" :src="business_registration_certificate_url" aspect-ratio="1" />
              </a>
            </v-col>
            <v-col v-if="agency_license_url" class="d-flex child-flex" cols="6" md="3">
              <div class="absolute_text"> {{ $t("agency_license") }} </div>
              <a v-bind:href="agency_license_url" target="_blank">
                <img class="img" :src="agency_license_url" aspect-ratio="1" />
              </a>
            </v-col>
            <v-col v-if="garantee_insurance_url" class="d-flex child-flex" cols="6" md="3">
              <div class="absolute_text"> {{ $t("garantee_insurance") }} </div>
              <a v-bind:href="garantee_insurance_url" target="_blank">
                <img class="img" :src="garantee_insurance_url" aspect-ratio="1" />
              </a>
            </v-col>
            <v-col v-if="stamp_url" class="d-flex child-flex" cols="6" md="3">
              <div class="absolute_text"> {{ $t("stamp") }} </div>
              <a v-bind:href="stamp_url" target="_blank">
                <img class="img" :src="stamp_url" aspect-ratio="1" />
              </a>
            </v-col>
          </v-row>
        </template>
      </v-row>
      <v-btn class="mr-4" @click="onSubmit()">{{ $t("submit") }}</v-btn>
    </v-container>
  </ValidationObserver>
</template>

<script>
import { apiService, apiService_formData } from "@/common/api.service";
import { ValidationProvider, ValidationObserver } from "vee-validate";

export default {
  name: "ProfileEditor",
  props: {
    id: {
      type: [Number, String],
      required: false
    }
  },
  components: {
    ValidationObserver,
    ValidationProvider
  },
  data() {
    return {
      is_expert: false,
      is_request_expert: false,
      username: null,
      name: null,
      birthday: null,
      mobile_number: null,
      address: null,
      bank_name: null,
      account_number: null,
      expert_profile: {
        registration_number: null,
        shop_name: null,
        business_registration_certificate: null,
        agency_license: null,
        stamp: null,
      },
      business_registration_certificate_url: null,
      agency_license_url: null,
      stamp_url: null,
      garantee_insurance_url: null
    };
  },
  methods: {
    preview_image(name) {
      this[name + "_url"] = window.URL.createObjectURL(this['expert_profile'][name]);
    },
    onSubmit() {
      const self = this;
      const formData = new FormData();
      
      if (this.mobile_number) formData.append("mobile_number", this.mobile_number)
      if (this.address) formData.append("address", this.address)
      if (this.bank_name) formData.append("bank_name", this.bank_name)
      if (this.account_number) formData.append("account_number", this.account_number)
      if (self.is_request_expert || self.is_expert) {
        Object.keys(self.expert_profile).forEach(function(key) {
          if(self.expert_profile[key] != null) {
            formData.append('expert_profile.'+key, self.expert_profile[key])
          }
        });
      }
      let endpoint = "/api/profiles/";
      let method = "POST";

      if (self.id !== undefined) {
        endpoint += `${self.id}/`;
        method = "PATCH";
      }
      apiService_formData(endpoint, method, formData).then(data => {
        if (data.id) {
          alert(self.$i18n.t("request_success"))
          self.$router.push({
            name: "profiles"
          });
        } else {          
          Object.keys(data).forEach(function(key) {
            self.$refs[key].applyResult({
              errors: data[key],
              valid: false,
              failedRules: {}
            });
          });
        }
      });
    }
  },
  async beforeRouteEnter(to, from, next) {
    if (to.params.id !== undefined) {
      let endpoint = `/api/profiles/${to.params.id}/`;
      let data = await apiService(endpoint);
      if (data.user.is_expert) {
        return next(
        vm => {
          vm.username = data.user.username;
          vm.name = data.user.name;
          vm.birthday = data.user.birthday;
          vm.address = data.address;
          vm.mobile_number = data.mobile_number;
          vm.bank_name = data.bank_name;
          vm.account_number = data.account_number;
          vm.expert_profile.registration_number = data.expert_profile.registration_number;
          vm.expert_profile.shop_name = data.expert_profile.shop_name;
          vm.business_registration_certificate_url = data.expert_profile.business_registration_certificate;
          vm.agency_license_url = data.expert_profile.agency_license;
          vm.stamp_url = data.expert_profile.stamp;
          vm.garantee_insurance_url = data.expert_profile.garantee_insurance;
        }
      );
      } else {
        return next(
        vm => {
          vm.username = data.user.username;
          vm.name = data.user.name;
          vm.birthday = data.user.birthday;
          vm.address = data.address;
          vm.mobile_number = data.mobile_number;
          vm.bank_name = data.bank_name;
          vm.account_number = data.account_number;
        }
      );
      }
      
    } else {
      let endpoint = `/api/user/`;
      let data = await apiService(endpoint);
      return next(
      vm => {
          vm.username = data.username;
          vm.name = data.name;
          vm.birthday = data.birthday;
        }
      );
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
  .img {
    border: 1px solid gray;
    width: 100%;
  }
  .absolute_text {
    z-index: 1;
    position: absolute;
    margin-left: auto;
    margin-right: auto;
    top: -10px;
    left: 0;
    right: 0;
    text-align: center;
  }
</style>
