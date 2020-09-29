<template>
  <v-container class="my-5">
    <v-row>
      <v-col cols="12">
        <v-text-field class="profile_name" v-model="profile_name" :label="$t('profile_name')"></v-text-field>
      </v-col>
      <template v-if="is_expert">
        <v-col cols="4" md="2">
          <v-text-field v-model="registration_number" :label="$t('registration_number')"></v-text-field>
        </v-col>
        <v-col cols="4" md="2">
          <v-text-field v-model="shop_name" :label="$t('shop_name')"></v-text-field>
        </v-col>
        <v-col cols="8">
          <v-text-field v-model="shop_address" :label="$t('shop_address')"></v-text-field>
        </v-col>
      </template>
      <template v-else>
      </template>
        <v-col cols="4" md="2">
          <v-text-field v-model="name" :label="$t('name')"></v-text-field>
        </v-col>
        <v-col cols="4" md="2">
          <v-text-field v-model="birthday" :label="$t('birthday')"></v-text-field>
        </v-col>
        <v-col v-if="!is_expert" cols="8">
          <v-text-field v-model="address" :label="$t('address')"></v-text-field>
        </v-col>
        <v-col cols="4" md="2">
          <v-text-field v-model="mobile_number" :label="$t('mobile_number')"></v-text-field>
        </v-col>
        <v-col cols="4" md="2">
          <v-text-field v-model="bank_name" :label="$t('bank_name')"></v-text-field>
        </v-col>
        <v-col cols="4" md="2">
          <v-text-field v-model="account_number" :label="$t('account_number')"></v-text-field>
        </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { apiService } from "@/common/api.service";

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
      name: null,
      birthday: null,
      profile_name: null,
      mobile_number: null,
      address: null,
      bank_name: null,
      account_number: null,
      registration_number: null,
      shop_name: null,
      shop_address: null
    };
  },
  async beforeRouteEnter(to, from, next) {
    console.log(to.params.id)
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
          (vm.registration_number = data.registration_number),
          (vm.shop_name = data.shop_name),
          (vm.shop_address = data.shop_address)
        )
      );
    }
  },
  created() {
    if (window.localStorage.getItem("is_expert") == "true") {
      this.is_expert = true;
    }
  }
};
</script>

<style>
  .profile_name {
    width: 400px;
  }
</style>
