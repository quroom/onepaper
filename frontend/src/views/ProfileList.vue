<template>
  <v-container>
    <v-dialog
      v-model="dialog"
      max-width="400px"
    >
      <v-card>
        <v-card-title>
          {{ $t("add_allowed_user") }}
        </v-card-title>
        <v-card-text class="text-body-1 text--primary">
          <LazyTextField :label="$t('default') + $t('profile') + ' ' + $t('number')" type="Number" v-model="id" readonly></LazyTextField>
          <LazyTextField :label="$t('username')" v-model="username" readonly></LazyTextField>
          <LazyTextField :label="$t('name')" v-model="name" readonly></LazyTextField>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            @click.prevent="addUser()"
          >
            {{ $t("trade") + $t("add_user") }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <div v-if="profiles.length == 0 && !isLoading" class="text-h5 text-center">
      {{$t("no_contents")}}
    </div>
    <template v-else>
      <div class="text-h5 text-center">{{ `${$t('written')} ${$t('profile')} ${$t('list')}` }}</div>
      <div class="text-body text-center">{{ $t("profile_list_detail") }}</div>
      <v-btn
        align="center"
        color="green"
        dark
        :to="{ name: 'user-editor'}"
      >
        <v-icon>account_box</v-icon>
        {{$t("edit_registor_info")}}
      </v-btn>
      <v-row>
        <v-col
          cols="12"
          md="6"
          lg="4"
          xs="3"
          v-for="profile in profiles"
          :key="profile.id"
        >
          <router-link :to="{ name: 'profile-editor' , params: { id: profile.id } }">
            <v-card>
              <v-chip class="ma-1" v-if="profile.is_default" color="primary">{{ profile.id }}</v-chip>
              <template v-else>
                <v-chip class="ma-1"> {{ profile.id }}</v-chip>
                <v-btn class="mt-1 mr-2 pa-1" color="primary" style="float:right" @click.prevent="setDefault(profile)">
                    <v-icon>check</v-icon>
                    {{ $t("set_default_profile") }}
                </v-btn>
              </template>
              <v-chip class="ma-1" color="primary" style="float: right;" v-if="profile.user.is_expert && profile.expert_profile.status == $getConstByName('expert_status', 'approved')"> {{$t("approved")}} </v-chip>
              <v-chip class="ma-1" style="float: right;" v-if="profile.user.is_expert && profile.expert_profile.status == $getConstByName('expert_status', 'request')"> {{$t("reviewing")}} </v-chip>
              <v-chip class="ma-1" color="error" style="float: right;" v-if="profile.user.is_expert && profile.expert_profile.status == $getConstByName('expert_status', 'denied')"> {{$t("denied")}} </v-chip>
              <v-card-title class="pb-2">
                {{ profile.address.old_address }}
              </v-card-title>
              <v-card-subtitle class="ma-0 pb-0">
                <span class="pa-1"> {{ profile.user.name }} </span>
                <span class="pa-1"> {{ profile.user.birthday }} </span>
                <span class="pa-1"> {{ profile.mobile_number }} </span>
              </v-card-subtitle>
              <v-card-subtitle v-if="profile.user.expert_profile" class="ma-0 pb-0">
                <span class="pa-1"> {{ profile.expert_profile.registration_number }} </span>
                <span class="pa-1"> {{ profile.expert_profile.shop_name }} </span>
              </v-card-subtitle>
              <v-card-subtitle v-if="profile.bank_name || profile.account_number" class="pt-0 pb-0">
                <span class="pa-1"> {{ profile.bank_name }} </span>
                <span class="pa-1"> {{ profile.account_number }} </span>
              </v-card-subtitle>
              <v-card-actions v-if="username != undefined && name != undefined">
                <v-spacer></v-spacer>
                <v-btn color="primary" @click.prevent="addUser(profile.id)">
                  <v-icon>person_add</v-icon>
                  {{ $t("add_trade_user_directly") }}
                </v-btn>
              </v-card-actions>
              <v-card-actions v-else>
                <v-btn color="green" dark :to="{ name: 'profile-editor', params: { id: profile.id } }"> {{ $t("edit") }} </v-btn>
                <v-spacer></v-spacer>
                <v-btn color="primary" :to="{ name: 'allowed-user-editor', params: { id: profile.id } }">
                  <v-icon>person_add</v-icon>
                  {{ $t("trade") + $t("add_user") }}
                </v-btn>
              </v-card-actions>
            </v-card>
          </router-link>
        </v-col>
      </v-row>
    </template>
    <router-link :to="{ name: 'profile-editor' }">
      <v-btn color="grey" dark fixed fab right bottom>
        <v-icon>add</v-icon>
      </v-btn>
    </router-link>
  </v-container>
</template>
<script>
import { apiService } from "@/common/api.service";
import { applyValidation } from "@/common/common_api";

export default {
  name: "Profiles",
  props: {
    username: {
      type: [String],
      required: false
    },
    name: {
      type: [String],
      required: false
    },
  },
  computed: {
    profile_length: function(){
      return this.profiles.length;
    },
    default_profile: function(){
      for(let i=0; i<this.profiles.length; i++){
        if(this.profiles[i].is_default==true){
          return this.profiles[i]
        }
      }
    }
  },
  data() {
    return {
      profiles: [],
      isLoading: false,
      id: undefined,
      dialog: false
    };
  },
  methods: {
    addUserDialog(id){
      this.id= id;
      this.dialog= true;
    },
    addUser(id) {
      let endpoint = ``;
      let data = {
        "allowed_users" : {
          "name": this.name,
          "username": this.username
        }
      }
      endpoint = `/api/profiles/${id}/allowed-users/`
      apiService(endpoint, "POST", data).then(data => {
        if(data.count != undefined) {
          alert(this.$i18n.t("request_success"))
        } else {
          applyValidation(data)
        }
        this.dialog = false
      })
    },
    getProfiles() {
      let endpoint = "/api/profiles/";
      this.isLoading = true;
      apiService(endpoint).then(data => {
        if(data.length != undefined){
          this.profiles.push(...data);
          
          if(data.length == 0){
              this.$emit("update:has_profile", false)
          } else {
            this.$emit("update:has_profile", true)
          }
        } else {
          applyValidation(data)
        }
        this.isLoading = false;
        if(this.username != undefined && this.name != undefined){
          this.dialog = true;
          this.id = this.default_profile.id;
        }
      });
    },
    setDefault(profile){
      let endpoint = `/api/profiles/${profile.id}/default/`
      apiService(endpoint, "POST").then(data=> {
        if(data.id != undefined){
          this.default_profile.is_default = false;
          this.$set(this.profiles, this.profiles.indexOf(profile), data);
        } else {
          applyValidation(data)
        }
      })
    }
  },
  created() {
    this.getProfiles();
  }
};
</script>
