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
          <LazyTextField :label="$t('profile') + ' ' + $t('number')" type="Number" v-model="id" readonly></LazyTextField>
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
            <v-chip class="ma-1">{{ profile.id }}</v-chip>
            <v-chip class="ma-1" color="primary" style="float: right;" v-if="profile.user.is_expert && profile.expert_profile.status == $getConstByName('expert_status', 'approved')">{{$t("approved")}}</v-chip>
            <v-chip class="ma-1" style="float: right;" v-if="profile.user.is_expert && profile.expert_profile.status == $getConstByName('expert_status', 'request')">{{$t("reviewing")}}</v-chip>
            <v-chip class="ma-1" color="error" style="float: right;" v-if="profile.user.is_expert && profile.expert_profile.status == $getConstByName('expert_status', 'denied')">{{$t("denied")}}</v-chip>
            <v-card-title>
              {{ profile.address.old_address }}
            </v-card-title>
            <v-card-subtitle class="ma-0 pb-0">
              <span class="pa-1"> {{ profile.user.name }} </span>
              <span class="pa-1"> {{ profile.user.birthday }} </span>
              <span class="pa-1"> {{ profile.mobile_number }} </span>
            </v-card-subtitle>
            <v-card-subtitle v-if="profile.user.is_expert" class="ma-0 pb-0">
              <span class="pa-1"> {{ profile.expert_profile.registration_number }} </span>
              <span class="pa-1"> {{ profile.expert_profile.shop_name }} </span>
            </v-card-subtitle>
            <v-card-subtitle class="pt-0">
              <span class="pa-1"> {{ profile.bank_name }} </span>
              <span class="pa-1"> {{ profile.account_number }} </span>
            </v-card-subtitle>
            <v-card-actions v-if="username != undefined">
              <v-spacer></v-spacer>
              <v-btn color="primary" @click.prevent="addUserDialog(profile.id)"> {{ $t("request") }} {{ $t("add_user") }} </v-btn>
            </v-card-actions>
            <v-card-actions v-else>
              <v-spacer></v-spacer>
              <v-btn color="green" dark :to="{ name: 'profile-editor', params: { id: profile.id } }"> {{ $t("edit") }} </v-btn>
              <v-btn color="primary" :to="{ name: 'allowed-user-editor', params: { id: profile.id } }"> {{ $t("trade") + $t("add_user") }} </v-btn>
            </v-card-actions>
          </v-card>
        </router-link>
      </v-col>
    </v-row>
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
    }
  },
  data() {
    return {
      profiles: [],
      id: undefined,
      dialog: false,
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
      endpoint = `/api/profiles/${this.profiles[0].id}/allowed-users/`
      apiService(endpoint, "POST", data).then(data => {
        if(data.id) {
          alert(this.$i18n.t("request_success"))
        } else {
          applyValidation(data)
        }
        this.dialog = false
      })
    },
    getProfiles() {
      let endpoint = "/api/profiles/";
      apiService(endpoint).then(data => {
        if(data.length == 0){
            this.$emit("update:has_profile", false)
        } else {
          this.$emit("update:has_profile", true)
        }
        this.profiles.push(...data);

        if(this.username != undefined && this.name != undefined && this.profiles.length == 1){
          this.dialog = true;
          this.id = this.profiles[0].id;
        }
      });
    },
  },
  created() {
    this.getProfiles();
  }
};
</script>
