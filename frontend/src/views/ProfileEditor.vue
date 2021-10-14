<template>
  <ValidationObserver ref="obs">
    <v-container>
      <!-- UserInfo -->
      <v-row>
        <DeleteAlert
          v-if="id"
          :id="this.id"
          url="/api/profiles/"
          router_name="profiles"
        ></DeleteAlert>
        <v-spacer></v-spacer>
        <v-btn color="primary" :to="{ name: 'allowed-user-editor', params: { id: id } }">
          {{ $t("add_quick_trade_user") }}
        </v-btn>
      </v-row>
      <v-row> </v-row>
      <v-row>
        <v-col cols="12" sm="4">
          <LazyTextField v-model="email" :label="$t('email')" readonly></LazyTextField>
        </v-col>
        <v-col cols="6" md="4">
          <LazyTextField v-model="name" :label="$t('name')" readonly></LazyTextField>
        </v-col>
        <v-col cols="6" md="4">
          <LazyTextField v-model="birthday" :label="$t('birthday')" readonly></LazyTextField>
        </v-col>
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
          <v-col cols="12" sm="8">
            <AddressSearch
              ref_name="shop_address"
              :label="$t('shop_address') + $t('search')"
              :address.sync="address"
            ></AddressSearch>
          </v-col>
          <v-col cols="6" sm="2">
            <LazyTextField
              v-model="address.dong"
              :label="$t('dong')"
              outlined
              hide-details="auto"
            ></LazyTextField>
          </v-col>
          <v-col cols="6" sm="2">
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
            <div id="v-profile" class="text-h5">
              {{ $t("general") }} {{ $t("user") }} {{ $t("profile") }}
            </div>
          </v-col>
          <v-col cols="12" sm="8">
            <AddressSearch
              id="v-address"
              ref_name="address"
              :label="$t('address') + $t('search')"
              :address.sync="address"
            ></AddressSearch>
          </v-col>
          <v-col cols="6" sm="2">
            <LazyTextField
              v-model="address.dong"
              :label="$t('dong')"
              outlined
              hide-details="auto"
            ></LazyTextField>
          </v-col>
          <span id="v-dong-ho"></span>
          <v-col cols="6" sm="2">
            <LazyTextField
              v-model="address.ho"
              :label="$t('ho')"
              outlined
              hide-details="auto"
            ></LazyTextField>
          </v-col>
        </template>
        <v-col cols="6" sm="4">
          <ValidationProvider
            ref="mobile_number"
            :name="$t('mobile_number')"
            rules="required|mobile"
            v-slot="{ errors }"
          >
            <div id="v-mobile-number">
              <v-text-field
                ref="mobile_number_input"
                v-model="mobile_number"
                :error-messages="errors"
                :label="$t('mobile_number')"
                maxlength="13"
                @input="addDash"
              ></v-text-field>
            </div>
          </ValidationProvider>
        </v-col>
        <v-row>
          <v-col cols="6" sm="auto">
            <div>
              <v-select
                ref="bank_name"
                v-model="bank_name"
                :items="$getConstList('BANK_CATEGORY_LIST')"
                item-text="text"
                item-value="value"
                :label="$t('bank_name')"
              >
                <template v-slot:selection="{ item }">{{ $t(item.text) }}</template>
                <template v-slot:item="{ item }">{{ $t(item.text) }}</template>
              </v-select>
            </div>
          </v-col>
          <span class="tour-set" id="v-bank"></span>
          <v-col cols="6" sm="auto">
            <LazyTextField
              v-model="account_number"
              :label="$t('account_number')"
              type="Number"
              hide-details="auto"
            ></LazyTextField>
          </v-col>
        </v-row>
        <template v-if="is_expert && !dialog.flag">
          <v-col cols="6" md="2">
            <ValidationProvider
              mode="passive"
              ref="registration_certificate"
              :name="$t('registration_certificate')"
              :rules="`${required ? 'required' : ''}|size:1024`"
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
          <v-col cols="6" md="2">
            <ValidationProvider
              mode="passive"
              ref="agency_license"
              :name="$t('agency_license')"
              :rules="`${required ? 'required' : ''}|size:1024`"
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
          <v-col cols="6" md="2">
            <ValidationProvider
              mode="passive"
              ref="stamp"
              :name="$t('stamp')"
              :rules="`${required ? 'required' : ''}|size:1024`"
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
          <template>
            <v-col v-if="!dialog.flag && id == undefined" cols="6" md="2">
              <ValidationProvider
                mode="passive"
                ref="insurance"
                :name="$t('garantee_insurance')"
                :rules="`${required ? 'required' : ''}|size:1024`"
                v-slot="{ errors }"
              >
                <v-file-input
                  v-model="expert_profile.insurance.image"
                  :label="$t('garantee_insurance')"
                  accept="image/*"
                  @click.stop
                  @change="preview_image('insurance')"
                  :error-messages="errors"
                ></v-file-input>
              </ValidationProvider>
            </v-col>
            <v-col v-if="!dialog.flag && isInsuranceValid" cols="auto">
              <v-menu
                :disabled="id != undefined"
                v-model="to_date_menu"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <ValidationProvider
                    ref="dates"
                    :name="`${$t('garantee_insurance')} ${$t('period')}`"
                    v-slot="{ errors }"
                    rules="required|date_required|period"
                  >
                    <LazyTextField
                      v-model="dates"
                      :error-messages="errors"
                      :label="`${$t('garantee_insurance')} ${$t('period')}`"
                      prepend-icon="event"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                    >
                    </LazyTextField>
                  </ValidationProvider>
                </template>
                <v-date-picker
                  v-model="dates"
                  range
                  @change="to_date_menu = false"
                  :locale="this.$i18n.locale"
                ></v-date-picker>
              </v-menu>
            </v-col>
          </template>
          <v-col cols="auto">
            <v-btn v-if="id != undefined" dark color="indigo" @click="dialog.flag = true">
              <span v-if="isInsuranceValid">
                {{ `${$t("garantee_insurance")} ${$t("manage")}` }}
              </span>
              <span v-else>
                {{ `${$t("add_garantee_insurance")}` }}
              </span>
            </v-btn>
          </v-col>
        </template>
      </v-row>
      <template v-if="is_expert">
        <v-row>
          <v-divider class="mx-4 text-center" style="display: inline"></v-divider>
          <v-col class="text-center" cols="12">
            <div class="text-h5">
              {{ $t("attached_document") }}
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="d-flex child-flex img-col" cols="6" md="3">
            <div class="absolute_text">
              {{ $t("registration_certificate") }}
            </div>
            <a
              v-if="current_registration_certificate"
              v-bind:href="current_registration_certificate"
              target="_blank"
            >
              <img class="img" :src="current_registration_certificate" aspect-ratio="1" />
            </a>
          </v-col>
          <v-col class="d-flex child-flex img-col" cols="6" md="3">
            <div class="absolute_text">{{ $t("agency_license") }}</div>
            <a v-if="current_agency_license" v-bind:href="current_agency_license" target="_blank">
              <img class="img" :src="current_agency_license" aspect-ratio="1" />
            </a>
          </v-col>
          <v-col class="d-flex child-flex img-col" cols="6" md="3">
            <div class="absolute_text">{{ $t("stamp") }}</div>
            <a v-if="current_stamp" v-bind:href="current_stamp" target="_blank">
              <img class="img" :src="current_stamp" aspect-ratio="1" />
            </a>
          </v-col>
          <v-col class="d-flex child-flex img-col" cols="6" md="3">
            <div class="absolute_text">{{ $t("garantee_insurance") }}</div>
            <a
              v-if="current_garantee_insurance"
              v-bind:href="current_garantee_insurance"
              target="_blank"
            >
              <img class="img" :src="current_garantee_insurance" aspect-ratio="1" />
            </a>
          </v-col>
        </v-row>
      </template>
      <v-row>
        <v-col cols="12" class="text-right">
          <v-btn
            id="v-submit"
            class="mr-4"
            color="primary"
            :disabled="!isInsuranceValid"
            @click="onSubmit()"
            >{{ $t("submit") }}</v-btn
          >
        </v-col>
      </v-row>
      <v-dialog v-if="dialog.flag && dialog.insurances" v-model="dialog.flag" max-width="750px">
        <v-card>
          <v-card-text>
            <v-row justify="center">
              <v-col cols="auto" v-for="insurance in dialog.insurances" :key="insurance.id">
                <v-card>
                  <v-chip class="ma-1"> {{ insurance.id }}</v-chip>
                  <v-card-subtitle>
                    <div>
                      {{ `${$t("garantee_insurance")} ${$t("period")}` }}
                    </div>
                    {{ insurance.from_date }} ~ {{ insurance.to_date }}
                  </v-card-subtitle>
                  <v-card-actions>
                    <DeleteAlert :id="insurance.id" :callback="deleteInsurance"></DeleteAlert>
                    <v-spacer></v-spacer>
                    <v-btn
                      class="ma-1 auto no-print"
                      color="green"
                      dark
                      @click="loadInsurnace(insurance.id)"
                    >
                      {{ $t("edit") }}
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
          <v-row no-gutters justify="center">
            <v-btn v-show="next" @click="getInsurances(false)" color="grey" dark>
              {{ $t("load_more") }}
            </v-btn>
          </v-row>
          <v-card class="pa-0 ma-2">
            <v-card-text>
              <v-row no-gutters justify="center">
                <v-col cols="auto">
                  <template v-if="dialog.insurance.id">
                    <v-chip class="ma-1"> {{ dialog.insurance.id }}</v-chip>
                    {{ `${$t("insurance")} ${$t("edit")}` }}
                  </template>
                  <template v-else>
                    {{ $t("add_garantee_insurance") }}
                  </template>
                </v-col>
              </v-row>
              <v-row no-gutters class="ml-4 mr-4" justify="center">
                <v-col class="pa-0 ml-4 mr-4" cols="auto" style="min-width:300px">
                  <ValidationProvider
                    mode="passive"
                    ref="insurance"
                    :name="$t('garantee_insurance')"
                    :rules="`${dialog.insurance.id == undefined ? 'required' : ''}|size:1024`"
                    v-slot="{ errors }"
                  >
                    <v-file-input
                      v-model="dialog.new_insurance"
                      :label="$t('garantee_insurance')"
                      accept="image/*"
                      @click.stop
                      :error-messages="errors"
                      @change="preview_image('insurance', 'dialog')"
                      truncate-length="12"
                    ></v-file-input>
                  </ValidationProvider>
                </v-col>
                <v-col class="pa-0" cols="auto">
                  <v-menu
                    v-model="dialog.period_menu"
                    :close-on-content-click="false"
                    :nudge-right="40"
                    transition="scale-transition"
                    offset-y
                    min-width="290px"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <ValidationProvider
                        mode="passive"
                        ref="dates"
                        :name="`${$t('garantee_insurance')}${$t('period')}`"
                        v-slot="{ errors }"
                        rules="required|date_required|period"
                      >
                        <LazyTextField
                          v-model="dialog.dates"
                          :label="`${$t('garantee_insurance')}${$t('period')}`"
                          prepend-icon="event"
                          readonly
                          :error-messages="errors"
                          v-bind="attrs"
                          v-on="on"
                        >
                        </LazyTextField>
                      </ValidationProvider>
                    </template>
                    <v-date-picker
                      v-model="dialog.dates"
                      range
                      @change="dialog.period_menu = false"
                      :locale="this.$i18n.locale"
                    ></v-date-picker>
                  </v-menu>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
          <v-row no-gutters>
            <v-col cols="12">
              <v-btn
                v-if="dialog.insurance.id"
                class="ml-2 mr-4 mb-4"
                outlined
                dark
                color="red"
                @click="init_insurance"
              >
                {{ $t("initialize") }}
              </v-btn>
              <v-btn
                v-if="dialog.insurance.id"
                class="mr-4 mb-4 right-btn"
                color="primary"
                dark
                @click="submitInsurance"
              >
                {{ `${$t("edit")} ${$t("submit")}` }}
              </v-btn>
              <v-btn
                v-else
                class="mr-4 mb-4 right-btn"
                color="primary"
                dark
                @click="submitInsurance"
              >
                <v-icon>add</v-icon>
                {{ $t("add_garantee_insurance") }}
              </v-btn>
            </v-col>
            <v-col v-if="dialog.insurance.image" class="img-col" cols="12">
              <div class="text-center">{{ $t("garantee_insurance") }}</div>
              <a v-bind:href="dialog.insurance.image" target="_blank">
                <img class="img" :src="dialog.insurance.image" aspect-ratio="1" />
              </a>
            </v-col>
          </v-row>
        </v-card>
      </v-dialog>
      <CustomTour name="profile-editor" :steps="steps" :options="tourOptions" />
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
      required: false
    }
  },
  computed: {
    //Only new expert-profile should have image field required.
    required() {
      return this.id == undefined;
    },
    isInsuranceValid() {
      if (this.id && this.is_expert) {
        if (this.dates) {
          const to_date = new Date(this.dates[1] + "T23:59:59");
          const from_date = new Date(this.dates[0] + "T00:00:00");
          const current_time = new Date();
          return to_date >= current_time && from_date <= current_time ? true : false;
        } else {
          return false;
        }
        // When create new profile, insurance is empty so it has to return valid.
      } else {
        return true;
      }
    },
    steps() {
      return [
        {
          target: "#v-profile",
          content: `${this.$t("tour_create_profile")}`,
          offset: -60
        },
        {
          target: "#v-address",
          content: `"(${this.$t("mandatory")})<br/>${this.$t("tour_address")}`,
          offset: -60,
          params: {
            highlight: true
          }
        },
        {
          target: "#v-dong-ho",
          content: `(${this.$t("optional")})<br/>${this.$t("tour_dong_ho")}`
        },
        {
          target: "#v-mobile-number",
          content: `(${this.$t("mandatory")})<br/>${this.$t("tour_mobile_number")}`,
          params: {
            highlight: true
          }
        },
        {
          target: "#v-bank",
          content: `(${this.$t("optional")})<br/>${this.$t("tour_bank")}`
        },
        {
          target: "#v-submit",
          content: `${this.$t("tour_submit")}`,
          params: {
            highlight: true
          }
        }
      ];
    }
  },
  data() {
    return {
      dialog: {
        flag: false,
        dates: [],
        period_menu: false,
        insurances: [],
        insurance: {
          id: null,
          image: null,
          from_date: null,
          to_date: null
        },
        new_insurance: null
      },
      next: undefined,
      is_expert: false,
      to_date_menu: false,
      count: undefined,
      dates: null,
      email: null,
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
        dong: "",
        ho: ""
      },
      //Bank_CATEGORY_LIST has value as integer.
      //That's why bnak_name default value is not '' 0 is computed to ''.
      bank_name: 0,
      account_number: "",
      expert_profile: {
        registration_number: null,
        shop_name: null,
        registration_certificate: null,
        agency_license: null,
        stamp: null,
        insurance: {
          image: null
        }
      },
      current_registration_certificate: null,
      current_agency_license: null,
      current_stamp: null,
      current_garantee_insurance: null,
      tourOptions: {
        stopOnTargetNotFound: false,
        useKeyboardNavigation: false
      }
    };
  },
  methods: {
    addDash() {
      var local_mobile_number = this.mobile_number.replace(/\D/g, "");
      this.mobile_number = local_mobile_number.replace(
        /(^01.{1}|[0|1|6|7|8|9]{3})([0-9]+)([0-9]{4})/,
        "$1-$2-$3"
      );
      this.$refs.mobile_number_input.lazyValue = this.mobile_number;
    },
    preview_image(name, parent) {
      this.$nextTick(() => {
        this.$refs[name].validate().then((v) => {
          if (v.valid == true) {
            if (parent) {
              if (this.dialog.new_insurance) {
                this[parent].insurance.image = window.URL.createObjectURL(
                  this.dialog.new_insurance
                );
              }
            } else if (name == "insurance") {
              console.log(name, this["expert_profile"]["insurance"]["image"]);
              if (this["expert_profile"]["insurance"]["image"] != null) {
                this["current_garantee_" + name] = window.URL.createObjectURL(
                  this["expert_profile"]["insurance"]["image"]
                );
              } else {
                this["current_" + name] = "";
              }
            } else {
              if (this["expert_profile"][name] != null) {
                this["current_" + name] = window.URL.createObjectURL(this["expert_profile"][name]);
              } else {
                this["current_" + name] = "";
              }
            }
          }
        });
      });
    },
    async deleteInsurance(insurance_id) {
      let endpoint = `/api/profiles/${this.id}/insurances/${insurance_id}/`;
      await apiService(endpoint, "DELETE").then((data) => {
        if (data == undefined) {
          alert(this.$i18n.t("delete_success"));
          const deleteInsuranceId = this.dialog.insurances.findIndex((x) => x.id == insurance_id);
          this.$delete(this.dialog.insurances, deleteInsuranceId);
        } else {
          applyValidation(data);
        }
      });
    },
    init_insurance() {
      this.dialog.insurance = {
        id: null,
        image: null,
        from_date: null,
        to_date: null
      };
      this.dialog.dates = [];
      this.dialog.new_insurance = null;
      this.dialog.period_menu = false;
    },
    loadInsurnace(insurance_id) {
      let endpoint = `/api/profiles/${this.id}/insurances/${insurance_id}/`;
      apiService(endpoint).then((data) => {
        console.log(data);
        if (data.id != undefined) {
          this.dialog.dates = [data.from_date, data.to_date];
          this.dialog.insurance.id = data.id;
          this.dialog.insurance.dates = [data.from_date, data.to_date];
          this.dialog.insurance.image = data.image;
        } else {
          applyValidation(data);
        }
      });
    },
    getInsurances(init) {
      let endpoint = `/api/profiles/${this.id}/insurances/`;
      if (this.next) {
        endpoint = this.next;
      }
      apiService(endpoint).then((data) => {
        if (data.count != undefined) {
          if (init == true) {
            this.init_insurance();
            this.dialog.insurances = data.results;
          } else {
            this.dialog.insurances.push(...data.results);
          }
          this.next = data.next;
        } else {
          applyValidation(data);
        }
      });
    },
    submitInsurance() {
      const that = this;
      this.$refs.obs.validate().then((v) => {
        if (v == true) {
          const formData = new FormData();
          let endpoint = `/api/profiles/${that.id}/insurances/`;
          let method = "POST";
          if (that.dialog.new_insurance) {
            formData.append("image", that.dialog.new_insurance);
          }
          formData.append("from_date", that.dialog.dates[0]);
          formData.append("to_date", that.dialog.dates[1]);
          if (that.dialog.insurance.id) {
            endpoint += `${that.dialog.insurance.id}/`;
            method = "PATCH";
          }
          apiService_formData(endpoint, method, formData).then(function(data) {
            try {
              if (data.id != undefined) {
                if (method == "PATCH") {
                  let foundIndex = that.dialog.insurances.findIndex((x) => x.id == data.id);
                  that.$set(that.dialog.insurances, foundIndex, data);
                } else {
                  that.dialog.insurances.unshift(data);
                }
                const to_date = new Date(data.to_date + "T23:59:59");
                const from_date = new Date(data.from_date + "T00:00:00");
                const current_time = new Date();
                //Update current insurance, If this insurance is valid today.
                if (to_date >= current_time && from_date <= current_time) {
                  that.current_garantee_insurance = data.image;
                  that.dates = [data.from_date, data.to_date];
                }
                alert(that.$i18n.t("request_success"));
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
    onSubmit() {
      const that = this;
      var endpoint = "";
      var method = "";

      this.$refs.obs.validate().then(function(v) {
        if (v == true) {
          const formData = new FormData();
          if (that.isInsuranceValid) {
            if (that.mobile_number) formData.append("mobile_number", that.mobile_number);
            if (that.address) {
              formData.append("address.old_address", that.address["old_address"]);
              formData.append("address.old_address_eng", that.address["old_address_eng"]);
              formData.append("address.new_address", that.address["new_address"]);
              formData.append("address.bjdongName", that.address["bjdongName"]);
              formData.append("address.bjdongName_eng", that.address["bjdongName_eng"]);
              formData.append("address.sigunguCd", that.address["sigunguCd"]);
              formData.append("address.bjdongCd", that.address["bjdongCd"]);
              formData.append("address.bun", that.address["bun"]);
              formData.append("address.ji", that.address["ji"]);
              formData.append("address.dong", that.address["dong"]);
              formData.append("address.ho", that.address["ho"]);
            }
            formData.append("bank_name", that.bank_name);
            formData.append("account_number", that.account_number);
            if (that.is_expert) {
              if (that.id == undefined) {
                formData.append(
                  "expert_profile.insurance.image",
                  that.expert_profile.insurance.image
                );
                formData.append("expert_profile.insurance.from_date", that.dates[0]);
                formData.append("expert_profile.insurance.to_date", that.dates[1]);
              }
              Object.keys(that.expert_profile).forEach(function(key) {
                if (that.expert_profile[key] != null) {
                  formData.append("expert_profile." + key, that.expert_profile[key]);
                }
              });
            }
            endpoint = "/api/profiles/";
            method = "POST";

            if (that.id !== undefined) {
              endpoint += `${that.id}/`;
              method = "PATCH";
            }
          } else {
            alert("please_available_garantee_insurance");
          }
          apiService_formData(endpoint, method, formData).then((data) => {
            try {
              if (data.id != undefined) {
                alert(that.$i18n.t("request_success"));
                that.$store.commit("SET_HAS_PROFILE", data.has_profile);
                if (method == "POST") {
                  that.$router.push({
                    name: "profiles"
                  });
                }
              } else {
                applyValidation(data, that);
              }
            } catch (err) {
              alert(err);
            }
          });
        }
      });
    }
  },
  async beforeRouteEnter(to, from, next) {
    if (to.params.id !== undefined) {
      let endpoint = `/api/profiles/${to.params.id}/`;
      let data = await apiService(endpoint);

      if (data.id != undefined) {
        if (data.user.is_expert) {
          return next((vm) => {
            vm.email = data.user.email;
            vm.name = data.user.name;
            vm.birthday = data.user.birthday;
            vm.address = data.address;
            vm.mobile_number = data.mobile_number;
            vm.bank_name = data.bank_name;
            vm.account_number = data.account_number;
            vm.expert_profile.registration_number = data.expert_profile.registration_number;
            vm.expert_profile.shop_name = data.expert_profile.shop_name;
            vm.current_registration_certificate = data.expert_profile.registration_certificate;
            vm.current_agency_license = data.expert_profile.agency_license;
            vm.current_stamp = data.expert_profile.stamp;
            vm.current_garantee_insurance = data.expert_profile.insurance.image;
            vm.dates = [
              data.expert_profile.insurance.from_date,
              data.expert_profile.insurance.to_date
            ];
            vm.count = data.expert_profile.insurance_count;
            vm.current_from_date = data.expert_profile.insurance.from_date;
            vm.current_to_date = data.expert_profile.insurance.to_date;
            vm.expert_profile.insurance = data.expert_profile.insurance;
          });
        } else {
          return next((vm) => {
            vm.email = data.user.email;
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
        console.log(vm);
        vm.email = vm.$store.state.user.email;
        vm.name = vm.$store.state.user.name;
        vm.birthday = vm.$store.state.user.birthday;
      });
    }
  },
  created() {
    this.is_expert = this.$store.state.user_category == "expert" ? true : false;
    if (this.id) {
      this.getInsurances(true);
    }
  },
  destroyed() {
    this.$tours["profile-editor"].stop();
  },
  mounted() {
    if (
      this.$store.state.user_setting.is_tour_on &&
      this.$store.state.user_category === "user" &&
      !this.$store.state.has_profile
    ) {
      console.log("tour_start");
      this.$tours["profile-editor"].start();
    }
  }
};
</script>

<style scoped>
.absolute_text {
  position: absolute;
  top: 0px;
}
a {
  text-align: center;
}
.img {
  border: 1px solid gray;
  width: 100%;
  margin-top: 15px;
}
.img-col {
  position: relative;
}
.right-btn {
  float: right;
}
</style>
