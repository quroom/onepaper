<template>
  <v-container>
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
            <v-card-title>
              {{ profile.address }}
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
            <v-card-actions>
              <v-btn color="green" dark :to="{ name: 'profile-editor', params: { id: profile.id } }">
                {{ $t("edit") }}
              </v-btn>
              <v-btn color="error" @click.stop="deletePaper(profile.id)">{{ $t("delete") }}</v-btn>
              <v-spacer></v-spacer>
              <v-btn color="primary" :to="{ name: 'allowed-user-editor', params: { id: profile.id } }"> {{ $t("add_user") }} </v-btn>
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

export default {
  name: "Profiles",
  data() {
    return {
      profiles: [],
    };
  },
  methods: {
    getProfiles() {
      let endpoint = "api/profiles/";
      apiService(endpoint).then(data => {
        this.profiles.push(...data);
      });
    },
    deletePaper(id) {
      let self = this
      let endpoint = `api/profiles/${id}/`;
      apiService(endpoint, "DELETE").then(() => {
        alert(self.$i18n.t("request_success"))
        self.$router.go(self.$router.currentRoute);
      });
    },
    addUser(username){
      this.username_list.push(username)
    }
  },
  created() {
    this.getProfiles();
  }
};
</script>
