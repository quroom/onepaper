<template>
  <v-container>
    <!-- eslint-disable-next-line vue/require-component-is -->
    <component is="script" src="https://code.jquery.com/jquery-1.12.4.min.js" async></component>
    <!-- iamport.payment.js -->
    <!-- eslint-disable-next-line vue/require-component-is -->
    <component
      is="script"
      src="https://cdn.iamport.kr/js/iamport.payment-1.1.8.js"
      async
    ></component>
    <div v-if="is_expert" class="text-caption blue--text">
      {{ $t("use_profile_after_approval") }}
    </div>
    <v-dialog v-model="dialog" max-width="400px">
      <v-card>
        <v-card-title>
          {{ `${$t("quick_trade_user")} ${$t("info")}` }}
        </v-card-title>
        <v-card-text class="text-body-1 text--primary">
          <LazyTextField :label="$t('email')" v-model="email" readonly></LazyTextField>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click.prevent="addUser(activated_profile)">
            {{ $t("add_quick_trade_user") }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-row>
      <v-btn align="center" color="green" dark :to="{ name: 'user-editor' }">
        <v-icon>account_box</v-icon>
        {{ $t("edit_registor_info") }}
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn align="center" color="green" dark href="accounts/social/connections/">
        {{ $t("connect_social") }}
      </v-btn>
    </v-row>
    <div v-if="profiles.length == 0 && !isLoading" class="text-center">
      <div class="text-h5 ">
        {{ $t("no_profile") }}
      </div>
      <div class="text-subtitle-1 red--text">
        {{ $t("creating_profile_is_mandatory") }}
      </div>
    </div>
    <template v-else>
      <div class="mt-2 text-caption red--text">
        {{ $t("profile_list_subtitle") }}
      </div>
      <v-row>
        <!--FIXME: update cols/md/lg/xs number-->
        <v-col cols="12" md="6" lg="4" xs="3" v-for="profile in profiles" :key="profile.id">
          <router-link :to="{ name: 'profile-editor', params: { id: profile.id } }">
            <v-card>
              <v-chip class="ma-1" v-if="profile.is_activated" color="primary">{{
                profile.id
              }}</v-chip>
              <template v-else>
                <v-chip class="ma-1"> {{ profile.id }}</v-chip>
                <v-btn
                  class="mt-1 mr-2 pa-1"
                  color="primary"
                  style="float: right;"
                  @click.prevent="activateProfile(profile)"
                >
                  <v-icon>check</v-icon>
                  {{ $t("activate") }}
                </v-btn>
              </template>
              <v-chip v-if="profile.certification.is_certificated" color="primary">
                {{ $t("certified") }}
              </v-chip>
              <v-chip v-else> {{ $t("uncertified") }} </v-chip>
              <template v-if="is_expert">
                <v-chip
                  class="ma-1"
                  color="primary"
                  v-if="
                    profile.expert_profile.status == $getConstByName('expert_status', 'approved')
                  "
                >
                  {{ $t("approved") }}
                </v-chip>
                <v-chip
                  class="ma-1"
                  v-if="
                    profile.is_activated &&
                      profile.expert_profile.status ==
                        $getConstByName('expert_status', 'requesting')
                  "
                >
                  {{ $t("reviewing") }}
                </v-chip>
                <v-chip
                  class="ma-1"
                  color="error"
                  v-if="
                    profile.expert_profile.status == $getConstByName('expert_status', 'denied')
                  "
                >
                  {{ $t("denied") }}
                </v-chip>
              </template>
              <v-card-title class="pb-2">
                {{ profile.address.old_address }}
              </v-card-title>
              <v-card-subtitle v-if="is_expert" class="ma-0 pb-0">
                <span class="pa-1">
                  {{ profile.expert_profile.registration_number }}
                </span>
                <span class="pa-1">
                  {{ profile.expert_profile.shop_name }}
                </span>
              </v-card-subtitle>
              <v-card-subtitle class="ma-0 pt-1 pb-0">
                <span class="pa-1"> {{ profile.user.name }} </span>
                <span class="pa-1"> {{ profile.user.birthday }} </span>
                <span class="pa-1"> {{ profile.mobile_number }} </span>
              </v-card-subtitle>
              <v-card-subtitle
                v-if="profile.bank_name || profile.account_number"
                class="pt-0 pb-0"
              >
                <span class="pa-1">
                  {{ $getConstI18("bank_category", profile.bank_name) }}
                </span>
                <span class="pa-1"> {{ profile.account_number }} </span>
              </v-card-subtitle>
              <v-card-actions v-if="email">
                <v-spacer></v-spacer>
                <v-btn color="primary" @click.prevent="addUser(profile)">
                  <v-icon>person_add</v-icon>
                  {{ $t("add_quick_trade_user_directly") }}
                </v-btn>
              </v-card-actions>
              <v-card-actions v-else>
                <v-btn
                  color="green"
                  dark
                  :to="{ name: 'profile-editor', params: { id: profile.id } }"
                >
                  {{ $t("edit") }}
                </v-btn>
                <v-spacer></v-spacer>
                <template v-if="profile.is_activated">
                  <v-btn
                    v-if="profile.certification.is_certificated === false"
                    dark
                    @click.prevent="onCertification(profile)"
                    >{{ $t("self_authentication") }}</v-btn
                  >
                  <v-btn
                    v-else-if="
                      (new Date() - new Date(profile.certification.updated_at)) / (3600 * 1000) >
                        24
                    "
                    @click.prevent="onCertification(profile)"
                    >{{ $t("reauthentication") }}</v-btn
                  >
                </template>
              </v-card-actions>
            </v-card>
          </router-link>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-btn v-show="next" @click="getProfiles" color="grey" dark>
          {{ $t("load_more") }}
        </v-btn>
      </v-row>
    </template>
    <v-row justify="end">
      <v-btn :to="{ name: 'profile-editor' }" color="primary" dark>
        <v-icon>add</v-icon>
        {{ $t("create_profile") }}
      </v-btn>
    </v-row>
  </v-container>
</template>
<script>
import { apiService } from "@/common/api_service";
import { applyValidation } from "@/common/common_api";

export default {
  name: "Profiles",
  props: {
    email: {
      type: [String],
      required: false
    }
  },
  computed: {
    profile_length: function() {
      return this.profiles.length;
    },
    activated_profile: function() {
      for (let i = 0; i < this.profiles.length; i++) {
        if (this.profiles[i].is_activated == true) {
          return this.profiles[i];
        }
      }
      return undefined;
    }
  },
  data() {
    return {
      profiles: [],
      is_expert: false,
      isLoading: false,
      dialog: false,
      next: null
    };
  },
  methods: {
    addUser(profile) {
      let endpoint = ``;
      let data = {
        allowed_users: {
          email: this.email
        }
      };
      endpoint = `/api/profiles/${profile.id}/allowed-users/`;
      apiService(endpoint, "POST", data).then((data) => {
        if (!data.count) {
          applyValidation(data);
        } else {
          alert(this.$i18n.t("request_success"));
        }
        this.dialog = false;
      });
    },
    getProfiles() {
      let endpoint = "/api/profiles/";
      if (this.next) {
        endpoint = this.next;
      }
      this.isLoading = true;
      apiService(endpoint).then((data) => {
        if (data.count != undefined) {
          this.profiles.push(...data.results);
          this.next = data.next;
          if (data.count == 0) {
            this.$store.commit("SET_HAS_PROFILE", false);
          } else {
            this.$store.commit("SET_HAS_PROFILE", true);
          }
        } else {
          applyValidation(data);
        }
        this.isLoading = false;
        if (this.email != undefined) {
          this.dialog = true;
        }
      });
    },
    onCertification() {
      /* 1. 가맹점 식별하기 */
      const vm = this;
      const { IMP } = window;
      IMP.init("imp42655352");

      /* 2. 본인인증 데이터 정의하기 */
      const data = {
        merchant_uid: `mid_${new Date().getTime()}`, // 주문번호
        company: "큐룸", // 회사명 또는 URL
        carrier: undefined, // 통신사
        name: this.activated_profile.user.name, // 이름
        phone: this.activated_profile.mobile_number // 전화번호
      };

      /* 4. 본인인증 창 호출하기 */
      IMP.certification(data, (response) => {
        /* 3. 콜백 함수 정의하기 */
        const { success, error_code, error_msg } = response;

        if (success) {
          let endpoint = `/api/certification/`;
          apiService(endpoint, "PUT", { imp_uid: response.imp_uid }).then((data) => {
            if (data.id != undefined) {
              if (vm.activated_profile) {
                alert(vm.$t("self_authentication_success"), success);
                vm.activated_profile.certification = data;
              } else {
                alert(vm.$t("please_select_activated_profile"));
              }
            } else {
              applyValidation(data);
            }
          });
        } else {
          if (error_code != "F0000") {
            alert(`${vm.$t("self_authentication_fail")} ${error_msg}`);
          }
        }
      });
    },
    activateProfile(profile) {
      let endpoint = `/api/profiles/${profile.id}/activate/`;
      apiService(endpoint, "POST").then((data) => {
        if (data.id != undefined) {
          if (this.activated_profile != undefined) {
            this.activated_profile.is_activated = false;
          }
          this.$set(this.profiles, this.profiles.indexOf(profile), data);
        }
      });
    }
  },
  created() {
    this.getProfiles();
    let offset = new Date().getTimezoneOffset() * 60000;
    this.today = new Date(Date.now() - offset);
    this.is_expert = this.$store.state.user_category == "expert" ? true : false;
  }
};
</script>
