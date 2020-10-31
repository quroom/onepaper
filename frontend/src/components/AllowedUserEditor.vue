<template>
  <v-container>
    <div class="text-h6 text-center ma-2"> {{ $t("allow_user_list") }} </div>    
    <v-data-table
      v-model="selected_users"
      :headers="headers"
      :items="allowed_users"
      item-key="username"
      show-select
    >
    <template v-slot:top>
      <v-row>
        <v-col>
          <v-text-field v-on:keyup.enter="addUser" ref="username_text" :label="$t('username')" outlined v-model="new_user">
            <template v-slot:append-outer>
              <v-btn
                color="primary"
                :label="$t('add_user')"
                class="pa-3 btn"
                @click="addUser"
              > {{$t("add_user")}} </v-btn>
            </template>
          </v-text-field>
        </v-col>
      </v-row>
    </template>
    </v-data-table>
    <v-row no-gutters>
      <v-col class="text-right">
        <v-btn
        color="error"
        :label="$t('delete')"
        class="pa-3 btn"
        @click="deleteUser"
      > {{$t("user")}} {{$t("delete")}} </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { apiService } from "@/common/api.service";
import i18n from "@/plugins/i18n";

export default {
  name: "AllowedUserEditor",
  props: {
    id: {
      type: [Number, String],
      required: true
    }
  },
  data() {
    return {
      headers: [{
        text: `${i18n.t("allow")} ${i18n.t("username")}`,
        align: 'start',
        sortable: true,
        value: 'username'
      }],
      allowed_users: [],
      selected_users: [],
      new_user: null,
      new_users: []
    }
  },
  methods: {
    getUsers() {
      let endpoint = `/api/profiles/${this.id}/allowed-users/`
      apiService(endpoint).then(data => {
        this.allowed_users = data.allowed_users;
      })
    },
    addUser() {
      this.new_users.push(this.new_user)
      let data = {
        "allowed_users" : this.new_users
      }
      
      let endpoint = `/api/profiles/${this.id}/allowed-users/`
      apiService(endpoint, "POST", data).then(data => {
        if(data.id) {
          alert(this.$i18n.t("request_success"))
          this.allowed_users = data.allowed_users;          
        } else {
          alert(data)
        }
        this.new_user = "";
        this.new_users = [];
      })
    },
    deleteUser() {
      let selected_user_list = []
      for(var i=0; i<this.selected_users.length; i++){
        selected_user_list.push(this.selected_users[i].username)
      }

      let data = {
        "allowed_users" : selected_user_list
      }

      let endpoint = `/api/profiles/${this.id}/allowed-users/`
      apiService(endpoint, "DELETE", data).then(data => {
        if(data.id) {
          alert(this.$i18n.t("request_success"))
          this.allowed_users = data.allowed_users;          
        } else {
          alert(data)
        }
        this.selected_users = []
      })
    }
  },
  created() {
    this.getUsers();
  }
}
</script>

<style>
</style>