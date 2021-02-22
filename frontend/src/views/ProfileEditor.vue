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
          {{$t("trade") + $t("add_user") }}
        </v-btn>
      </v-row>
      <v-row>
        <v-col cols="4" md="2">
          <LazyTextField
            v-model="username"
            :label="$t('username')"
            readonly
          ></LazyTextField>
        </v-col>
        <v-col cols="4" md="2">
          <LazyTextField
            v-model="name"
            :label="$t('name')"
            readonly
          ></LazyTextField>
        </v-col>
        <v-col cols="4" md="2">
          <LazyTextField
            v-model="birthday"
            :label="$t('birthday')"
            readonly
          ></LazyTextField>
        </v-col>
      </v-row>
      <v-row>
        <!-- Expert Profile -->
        <template v-if="is_expert">
          <v-col cols="12">
            <div class="text-h5 text-center">
              {{ $t("realestate_agency") }} {{ $t("profile") }}
            </div>
            <div class="mt-2 text-caption text-left red--text" v-if="is_expert">
              {{ $t("use_profile_after_approval") }}
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
            <LazyTextField
              v-model="address.dong"
              :label="$t('dong')"
              outlined
              hide-details="auto"
            ></LazyTextField>
          </v-col>
          <v-col cols="2">
            <LazyTextField
              v-model="address.ho"
              :label="$t('ho')"
              outlined
              hide-details="auto"
            ></LazyTextField>
          </v-col>
          <v-col cols="6" md="3">
            <ValidationProvider
              ref="registration_number"
              :name="$t('registration_number')"
              rules="required"
              v-slot="{ errors }"
            >
              <LazyTextField
                v-model="expert_profile.registration_number"
                :error-messages="errors"
                :label="$t('registration_number')"
              ></LazyTextField>
            </ValidationProvider>
          </v-col>
          <v-col cols="6" md="3">
            <ValidationProvider
              ref="shop_name"
              :name="$t('shop_name')"
              rules="required"
              v-slot="{ errors }"
            >
              <LazyTextField
                v-model="expert_profile.shop_name"
                :error-messages="errors"
                :label="$t('shop_name')"
              ></LazyTextField>
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
            <LazyTextField
              v-model="address.dong"
              :label="$t('dong')"
              outlined
              hide-details="auto"
            ></LazyTextField>
          </v-col>
          <v-col cols="2">
            <LazyTextField
              v-model="address.ho"
              :label="$t('ho')"
              outlined
              hide-details="auto"
            ></LazyTextField>
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
          <LazyTextField
            v-model="bank_name"
            :label="$t('bank_name')"
          ></LazyTextField>
        </v-col>
        <v-col cols="6" md="2">
          <LazyTextField
            v-model="account_number"
            :label="$t('account_number')"
            type="Number"
          ></LazyTextField>
        </v-col>
        <template v-if="is_expert">
          <v-col cols="4" md="2">
            <ValidationProvider
              mode="passive"
              ref="registration_certificate"
              :name="$t('registration_certificate')"
              :rules="`required:${required}|size:1024`"
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
              :rules="`required:${required}|size:1024`"
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
              :rules="`required:${required}|size:1024`"
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
              :rules="`required:${required}|size:1024`"
              v-slot="{ errors }"
            >
              <v-file-input
                v-model="expert_profile.stamp"
                :label="$t('stamp')"
                accept="image/*"
                :required="required"
                @click.stop
                @change="preview_image('stamp')"
                :error-messages="errors"
              ></v-file-input>
            </ValidationProvider>
          </v-col>
        </template>
      </v-row>
      <v-row v-if="is_expert">
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
          <a v-bind:href="registration_certificate_url" target="_blank">
            <div class="absolute_text">{{ $t("registration_certificate") }}</div>
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
          <a v-bind:href="agency_license_url" target="_blank">
            <div class="absolute_text">{{ $t("agency_license") }}</div>
            <img class="img" :src="agency_license_url" aspect-ratio="1" />
          </a>
        </v-col>
        <v-col
          v-if="garantee_insurance_url"
          class="d-flex child-flex"
          cols="6"
          md="3"
        >
          <a v-bind:href="garantee_insurance_url" target="_blank">
            <div class="absolute_text">{{ $t("garantee_insurance") }}</div>
            <img class="img" :src="garantee_insurance_url" aspect-ratio="1" />
          </a>
        </v-col>
        <v-col v-if="stamp_url" class="d-flex child-flex" cols="6" md="3">
          <a v-bind:href="stamp_url" target="_blank">
            <div class="absolute_text">{{ $t("stamp") }}</div>
            <img class="img" :src="stamp_url" aspect-ratio="1" />
          </a>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" class="text-right">
          <v-btn class="mr-4" color="primary" @click="onSubmit()">{{ $t("submit") }}</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </ValidationObserver>
</template>

<script>
import { apiService, apiService_formData } from "@/common/api_service";
import { applyValidation } from "@/common/common_api";
import DeleteAlert from "@/components/DeleteAlert";

export default {
  name: "ProfileEditor",
  components: {
    DeleteAlert
  },
  props: {
    id: {
      type: [Number, String],
      required: false,
    },
  },
  computed: {
    //Only new expert-profile should have image field required.
    required(){ return this.id==undefined }
  },
  data() {
    return {
      is_expert: false,
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
      this.$nextTick(()=> {
        this.$refs[name].validate();
      })
    },
    onSubmit() {
      const that = this;
      this.$refs.obs.validate().then(function (v) {
        if (v == true) {
          const formData = new FormData();
          if (that.mobile_number)
            formData.append("mobile_number", that.mobile_number);
          if (that.address) {
            formData.append("address.old_address", that.address['old_address']);
            formData.append("address.old_address_eng", that.address['old_address_eng']);
            formData.append("address.new_address", that.address['new_address']);
            formData.append("address.bjdongName", that.address['bjdongName'])
            formData.append("address.bjdongName_eng", that.address['bjdongName_eng'])
            formData.append("address.sigunguCd", that.address['sigunguCd']);
            formData.append("address.bjdongCd", that.address['bjdongCd']);
            formData.append("address.bun", that.address['bun']);
            formData.append("address.ji", that.address['ji']);
            formData.append("address.dong", that.address['dong']);
            formData.append("address.ho", that.address['ho']);
          }
          if (that.bank_name) formData.append("bank_name", that.bank_name);
          if (that.account_number)
            formData.append("account_number", that.account_number);
          if (that.is_expert) {
            Object.keys(that.expert_profile).forEach(function (key) {
              if (that.expert_profile[key] != null) {
                formData.append(
                  "expert_profile." + key,
                  that.expert_profile[key]
                );
              }
            });
          }
          let endpoint = "/api/profiles/";
          let method = "POST";

          if (that.id !== undefined) {
            endpoint += `${that.id}/`;
            method = "PATCH";
          }
            apiService_formData(endpoint, method, formData).then((data) => {
              try{
                if (data.id != undefined) {
                  alert(that.$i18n.t("request_success"));
                  that.$emit("update:has_profile", data.has_profile)
                  that.$router.push({
                    name: "profiles"
                  });
                } else {
                  applyValidation(data, that);
                }
              } catch (err) {
                alert(err);
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
    
      if (data.id != undefined) {
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
        applyValidation(data);
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
    this.is_expert = window.localStorage.getItem("user_category") == "expert" ? true : false;
  },
};
</script>

<style scoped>
a {
  text-align: center;
}
.img {
  border: 1px solid gray;
  width: 100%;
}
</style>
