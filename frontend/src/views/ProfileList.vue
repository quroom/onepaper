<template>
  <div class="mt-5">
    <v-container class="my-5">
      <v-row no-gutters>
        <v-col cols="12" md="6" lg="4" xs="3" v-for="profile in profiles" :key="profile.id">
          <v-card>
            <v-card-title v-if="profile.user.is_expert">
              {{ profile.profile_name }} / {{ profile.registration_number }}
            </v-card-title>
            <v-card-title v-else>{{ profile.profile_name }}</v-card-title>
            <v-card-subtitle v-if="profile.user.is_expert" class="ma-0 pb-0">
              {{ profile.shop_name }} /
              {{ profile.shop_address}}
            </v-card-subtitle>
            <v-card-subtitle v-else class="pb-0">{{ profile.address}}</v-card-subtitle>
            <v-card-subtitle class="pt-0">
              {{ profile.mobile_number }} /
              {{ profile.bank_name }}
              {{ profile.account_number }}
            </v-card-subtitle>
            <v-card-actions>
              <v-btn
                :to="{ name: 'profile-editor', params: { id: profile.id } }"
              >
                {{ $t("modify") }}
              </v-btn>
              <v-btn>{{ $t("delete") }}</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
import { apiService } from "@/common/api.service";

export default {
  name: "Profiles",
  data() {
    return {
      profiles: []
    };
  },
  methods: {
    getProfiles() {
      let endpoint = "api/profiles/";
      apiService(endpoint).then(data => {
        this.profiles.push(...data);
      });
    }
  },
  created() {
    this.getProfiles();
  }
};
</script>
