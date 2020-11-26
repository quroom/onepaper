<template>
  <ValidationObserver ref="obs">
    <v-container>
      <!-- UserInfo -->
      <v-row>
        <DeleteAlert v-if="id" :id="this.id" url="/api/profiles/" router_name="profiles"></DeleteAlert>
        <v-spacer></v-spacer>
        <v-btn
          style="float: right"
          color="primary"
          :to="{ name: 'allowed-user-editor', params: { id: id } }"
        >
          {{ $t("add_user") }}
        </v-btn>
      </v-row>
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
          <v-col cols="8">
            <AddressSearch
              ref_name="shop_address"
              :label="$t('shop_address') + $t('search')"
              :address.sync="address"
            ></AddressSearch>
          </v-col>
          <v-col cols="2">
            <v-text-field
              v-model="address.dong"
              :label="$t('dong')"
              outlined
              hide-details="auto"
            ></v-text-field>
          </v-col>
          <v-col cols="2">
            <v-text-field
              v-model="address.ho"
              :label="$t('ho')"
              outlined
              hide-details="auto"
            ></v-text-field>
          </v-col>
          <v-col cols="6" md="3">
            <ValidationProvider
              ref="registration_number"
              :name="$t('registration_number')"
              rules="required"
              v-slot="{ errors }"
            >
              <v-text-field
                v-model="expert_profile.registration_number"
                :error-messages="errors"
                :label="$t('registration_number')"
              ></v-text-field>
            </ValidationProvider>
          </v-col>
          <v-col cols="6" md="3">
            <ValidationProvider
              ref="shop_name"
              :name="$t('shop_name')"
              rules="required"
              v-slot="{ errors }"
            >
              <v-text-field
                v-model="expert_profile.shop_name"
                :error-messages="errors"
                :label="$t('shop_name')"
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
          <v-col cols="8">
            <AddressSearch
              ref_name="address"
              :label="$t('address') + $t('search')"
              :address.sync="address"
            ></AddressSearch>
          </v-col>
          <v-col cols="2">
            <v-text-field
              v-model="address.dong"
              :label="$t('dong')"
              outlined
              hide-details="auto"
            ></v-text-field>
          </v-col>
          <v-col cols="2">
            <v-text-field
              v-model="address.ho"
              :label="$t('ho')"
              outlined
              hide-details="auto"
            ></v-text-field>
          </v-col>
        </template>
        <v-col cols="6" md="2">
          <ValidationProvider
            ref="mobile_number"
            :name="$t('mobile_number')"
            rules="required|mobile"
            v-slot="{ errors }"
          >
            <v-text-field
              ref="mobile_number_input"
              v-model="mobile_number"
              :error-messages="errors"
              :label="$t('mobile_number')"
              maxlength="13"
              @input="addDash"
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
            <ValidationProvider
              mode="passive"
              ref="registration_certificate"
              :name="$t('registration_certificate')"
              :rules="{ required }"
              v-slot="{ errors }"
            >
              <v-file-input
                v-model="expert_profile.registration_certificate"
                :label="$t('registration_certificate')"
                accept="image/*"
                @click.stop
                @change="preview_image('registration_certificate')"
                :error-messages="errors"
              ></v-file-input>
            </ValidationProvider>
          </v-col>
          <v-col cols="4" md="2">
            <ValidationProvider
              mode="passive"
              ref="agency_license"
              :name="$t('agency_license')"
              :rules="{ required }"
              v-slot="{ errors }"
            >
              <v-file-input
                v-model="expert_profile.agency_license"
                :label="$t('agency_license')"
                accept="image/*"
                @click.stop
                @change="preview_image('agency_license')"
                :error-messages="errors"
              ></v-file-input>
            </ValidationProvider>
          </v-col>
          <v-col cols="4" md="2">
            <ValidationProvider
              mode="passive"
              ref="garantee_insurance"
              :name="$t('garantee_insurance')"
              :rules="{ required }"
              v-slot="{ errors }"
            >
              <v-file-input
                v-model="expert_profile.garantee_insurance"
                :label="$t('garantee_insurance')"
                accept="image/*"
                @click.stop
                @change="preview_image('garantee_insurance')"
                :error-messages="errors"
              ></v-file-input>
            </ValidationProvider>
          </v-col>
          <v-col cols="4" md="2">
            <ValidationProvider
              mode="passive"
              ref="stamp"
              :name="$t('stamp')"
              :rules="{ required }"
              v-slot="{ errors }"
            >
              <v-file-input
                v-model="expert_profile.stamp"
                :label="$t('stamp')"
                accept="image/*"
                @click.stop
                @change="preview_image('stamp')"
                :error-messages="errors"
              ></v-file-input>
            </ValidationProvider>
          </v-col>
        </template>
      </v-row>
      <v-row v-if="is_request_expert || is_expert">
        <v-divider class="mx-4 text-center" style="display: inline"></v-divider>
        <v-col class="text-center" cols="12">
          <div class="text-h5">
            {{ $t("attached_document") }}
          </div>
        </v-col>
      </v-row>
      <v-row>
        <v-col
          v-if="registration_certificate_url"
          class="d-flex child-flex"
          cols="6"
          md="3"
        >
          <div class="absolute_text">{{ $t("registration_certificate") }}</div>
          <a v-bind:href="registration_certificate_url" target="_blank">
            <img
              class="img"
              :src="registration_certificate_url"
              aspect-ratio="1"
            />
          </a>
        </v-col>
        <v-col
          v-if="agency_license_url"
          class="d-flex child-flex"
          cols="6"
          md="3"
        >
          <div class="absolute_text">{{ $t("agency_license") }}</div>
          <a v-bind:href="agency_license_url" target="_blank">
            <img class="img" :src="agency_license_url" aspect-ratio="1" />
          </a>
        </v-col>
        <v-col
          v-if="garantee_insurance_url"
          class="d-flex child-flex"
          cols="6"
          md="3"
        >
          <div class="absolute_text">{{ $t("garantee_insurance") }}</div>
          <a v-bind:href="garantee_insurance_url" target="_blank">
            <img class="img" :src="garantee_insurance_url" aspect-ratio="1" />
          </a>
        </v-col>
        <v-col v-if="stamp_url" class="d-flex child-flex" cols="6" md="3">
          <div class="absolute_text">{{ $t("stamp") }}</div>
          <a v-bind:href="stamp_url" target="_blank">
            <img class="img" :src="stamp_url" aspect-ratio="1" />
          </a>
        </v-col>
      </v-row>
      <v-btn class="mr-4" @click="onSubmit()">{{ $t("submit") }}</v-btn>
    </v-container>
  </ValidationObserver>
</template>

<script>
import { apiService, apiService_formData } from "@/common/api.service";
import AddressSearch from "@/components/AddressSearch";
import DeleteAlert from "@/components/DeleteAlert"

export default {
  name: "ProfileEditor",
  components: {
    AddressSearch,
    DeleteAlert
  },
  props: {
    id: {
      type: [Number, String],
      required: false,
    },
  },
  computed: {
    required(){ return this.id==undefined }
  },
  data() {
    return {
      is_expert: false,
      is_request_expert: false,
      username: null,
      name: null,
      birthday: null,
      mobile_number: null,
      address: {
        old_address: null,
        new_address: null,
        sigunguCd: null,
        bjdongCd: null,
        bun: null,
        ji: null,
        dong: '',
        ho: '',
      },
      bank_name: null,
      account_number: null,
      expert_profile: {
        registration_number: null,
        shop_name: null,
        registration_certificate: null,
        agency_license: null,
        stamp: null,
        garantee_insurance: null,
      },
      registration_certificate_url: null,
      agency_license_url: null,
      stamp_url: null,
      garantee_insurance_url: null,
    };
  },
  methods: {
    addDash(){
      var local_mobile_number = this.mobile_number.replace(/\D/g, '')
      this.mobile_number = local_mobile_number.replace(/(^01.{1}|[0|1|6|7|8|9]{3})([0-9]+)([0-9]{4})/,"$1-$2-$3")
      this.$refs.mobile_number_input.lazyValue = this.mobile_number
    },
    preview_image(name) {
      if(this["expert_profile"][name] != null){
        this[name + "_url"] = window.URL.createObjectURL(
          this["expert_profile"][name]
        );
      } else {
        this[name + "_url"] = ''
      }
    },
    onSubmit() {
      const self = this;
      this.$refs.obs.validate().then(function (v) {
        if (v == true) {
          const formData = new FormData();
          if (self.mobile_number)
            formData.append("mobile_number", self.mobile_number);
          if (self.address) {
            formData.append("address.old_address", self.address['old_address']);
            formData.append("address.new_address", self.address['new_address']);
            formData.append("address.sigunguCd", self.address['sigunguCd']);
            formData.append("address.bjdongCd", self.address['bjdongCd']);
            formData.append("address.bun", self.address['bun']);
            formData.append("address.ji", self.address['ji']);
            formData.append("address.dong", self.address['dong']);
            formData.append("address.ho", self.address['ho']);
          }
          if (self.bank_name) formData.append("bank_name", self.bank_name);
          if (self.account_number)
            formData.append("account_number", self.account_number);
          if (self.is_request_expert || self.is_expert) {
            Object.keys(self.expert_profile).forEach(function (key) {
              if (self.expert_profile[key] != null) {
                formData.append(
                  "expert_profile." + key,
                  self.expert_profile[key]
                );
              }
            });
          }
          let endpoint = "/api/profiles/";
          let method = "POST";

          if (self.id !== undefined) {
            endpoint += `${self.id}/`;
            method = "PATCH";
          }
          apiService_formData(endpoint, method, formData).then((data) => {
            if (data.id) {
              alert(self.$i18n.t("request_success"));
              self.$emit("update:has_profile", data.has_profile)
              self.$router.push({
                name: "profiles"
              });
            } else {
              Object.keys(data).forEach(function (key) {
                if(key=="detail") {
                  alert(data[key]);
                  return;
                } 
                self.$refs[key].applyResult({
                  errors: data[key],
                  valid: false,
                  failedRules: {},
                });
              });
            }
          });
        }
      });
    },
  },
  async beforeRouteEnter(to, from, next) {
    if (to.params.id !== undefined) {
      let endpoint = `/api/profiles/${to.params.id}/`;
      let data = await apiService(endpoint);
      if (data.user.is_expert) {
        return next((vm) => {
          vm.username = data.user.username;
          vm.name = data.user.name;
          vm.birthday = data.user.birthday;
          vm.address = data.address;
          vm.mobile_number = data.mobile_number;
          vm.bank_name = data.bank_name;
          vm.account_number = data.account_number;
          vm.expert_profile.registration_number =
            data.expert_profile.registration_number;
          vm.expert_profile.shop_name = data.expert_profile.shop_name;
          vm.registration_certificate_url =
            data.expert_profile.registration_certificate;
          vm.agency_license_url = data.expert_profile.agency_license;
          vm.stamp_url = data.expert_profile.stamp;
          vm.garantee_insurance_url = data.expert_profile.garantee_insurance;
        });
      } else {
        return next((vm) => {
          vm.username = data.user.username;
          vm.name = data.user.name;
          vm.birthday = data.user.birthday;
          vm.address = data.address;
          vm.mobile_number = data.mobile_number;
          vm.bank_name = data.bank_name;
          vm.account_number = data.account_number;
        });
      }
    } else {
      return next((vm) => {
        vm.username = window.localStorage.getItem("username");
        vm.name = window.localStorage.getItem("name");
        vm.birthday = window.localStorage.getItem("birthday");
      });
    }
  },
  created() {
    if (window.localStorage.getItem("is_expert") == "true") {
      this.is_expert = true;
    } else if (window.localStorage.getItem("request_expert") == "true") {
      this.is_request_expert = true;
    }
  },
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
