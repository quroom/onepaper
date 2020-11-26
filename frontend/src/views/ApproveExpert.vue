<template>
  <v-container>
    <div class="text-h6 text-center ma-2">{{ $t("realestate_agency") }} {{ $t("approve") }}</div>
    <v-data-table
      v-model="selected_profiles"
      :headers="headers"
      :items="profiles"
      item-key="id"
      show-expand
      single-expand
      show-select
    >
      <template v-slot:top>
        <v-chip-group>
          <v-btn
            color="error"
            :label="$t('deny')"
            class="pa-3 btn"
            @click="denyProfiles()"
          > {{$t("select")}} {{$t("deny")}} </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            :label="$t('approve')"
            class="pa-3 btn"
            @click="approveProfile(item, true)"
          > {{$t("select")}} {{$t("approve")}}
          </v-btn>
        </v-chip-group>
      </template>
      <template v-slot:[`item.status`]="{item}">
        {{ $getConstI18("expert_status", item.status) }}
      </template>
      <template v-slot:[`item.approve`]="{ item }">
        <v-btn
          v-if="item.status != $getConstByName('expert_status', 'approved') && item.status != $getConstByName('expert_status', 'closed')"
          color="primary"
          :label="$t('approve')"
          class="pa-3 btn"
          @click="approveProfile(item)"
        > {{$t("approve")}}
        </v-btn>
      </template>
      <template v-slot:expanded-item="{headers, item}">
        <td :colspan="headers.length">
          <div class="mt-5 row sp-details">
            <v-col class="d-flex child-flex" cols="6" xl="3">
              <div class="absolute_text"> {{ $t("registration_certificate") }} </div>
              <a v-bind:href="item.registration_certificate" target="_blank">
                <img class="img" :src="item.registration_certificate" aspect-ratio="1" />
              </a>
            </v-col>
            <v-col class="d-flex child-flex" cols="6" xl="3">
              <div class="absolute_text"> {{ $t("agency_license") }} </div>
              <a v-bind:href="item.agency_license" target="_blank">
                <img class="img" :src="item.agency_license" aspect-ratio="1" />
              </a>
            </v-col>
            <v-col class="d-flex child-flex" cols="6" xl="3">
              <div class="absolute_text"> {{ $t("garantee_insurance") }} </div>
              <a v-bind:href="item.garantee_insurance" target="_blank">
                <img class="img" :src="item.garantee_insurance" aspect-ratio="1" />
              </a>
            </v-col>
            <v-col class="d-flex child-flex" cols="6" xl="3">
              <div class="absolute_text"> {{ $t("stamp") }} </div>
              <a v-bind:href="item.stamp" target="_blank">
                <img class="img" :src="item.stamp" aspect-ratio="1" />
              </a>
            </v-col>
          </div>
        </td>
      </template>
    </v-data-table>
    <v-row no-gutters>
      <v-col class="text-right">
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { apiService } from "@/common/api.service";

export default {
  name: "ApproveExpert",
  data() {
    return {
      headers: [{
        text: `${this.$i18n.t("updated_at")}`,
        align: 'start',
        value: 'updated_at'
      },
      {
        text: `${this.$i18n.t("username")}`,
        align: 'start',
        value: 'username'
      },
      {
        text: `${this.$i18n.t("name")}`,
        align: 'start',
        value: 'name'
      },
      {
        text: `${this.$i18n.t("birthday")}`,
        align: 'start',
        value: 'birthday'
      },
      {
        text: `${this.$i18n.t("registration_number")}`,
        align: 'start',
        value: 'registration_number'
      },
      {
        text: `${this.$i18n.t("shop_name")}`,
        align: 'start',
        value: 'shop_name'
      },
      {
        text: `${this.$i18n.t("status")}`,
        align: 'start',
        value: 'status',
        filterable: true
      },
      { 
        text: `${this.$i18n.t("approve")}`,
        value: 'approve',
        sortable: false 
      },
      ],
      profiles: [],
      selected_profiles: [],
      new_profiles: [],
      item: null,
      dialog: false,
    }
  },
  methods: {
    getProfiles() {
      let endpoint = `/api/approve-experts/`
      apiService(endpoint).then(data => {
        this.profiles=data.results;
      })
    },
    approveProfile(item, is_list) {
      this.new_profiles = [];
      if(is_list == true){
        for(var i=0; i<this.selected_profiles.length; i++){
          this.new_profiles.push(this.selected_profiles[i].id)
        }
      } else {
        this.new_profiles.push(item.id);
      }
      let data = {
        "profiles" : this.new_profiles
      }
      let endpoint = `/api/approve-experts/`
      apiService(endpoint, "PUT", data).then(data => {
        if(data.length == undefined) {
          this.profiles=data.results;
          alert(this.$i18n.t("request_success"))
        } else {
          alert(data)
        }
      })
    },
    denyProfiles() {
      let selected_profile_list = []
      for(var i=0; i<this.selected_profiles.length; i++){
        selected_profile_list.push(this.selected_profiles[i].id)
      }
      let data = {
        "profiles" : selected_profile_list
      }

      let endpoint = `/api/approve-experts/`
      apiService(endpoint, "DELETE", data).then(data => {
        console.log(data.length)
        if(data.length == undefined) {
          this.profiles=data.results;
          alert(this.$i18n.t("request_success"))
          this.selected_profile_list = []
        } else {
          alert(data)
        }
      })
    }
  },
  created() {
    this.getProfiles();
  }
}
</script>

<style>
</style>