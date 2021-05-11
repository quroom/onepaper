<template>
  <v-container>
    <div class="text-caption red--text">
      {{ $t("quick_trade_user_list_subtitle") }}
    </div>
    <div class="text-h6 text-center ma-2">
      {{ $t("quick_trade_user_list") }}
    </div>
    <v-data-table
      v-model="selected_users"
      :headers="headers"
      :items="allowed_users"
      item-key="email"
      show-select
      :server-items-length="items_length"
      @update:page="updatePagination"
      :items-per-page="items_per_page"
    >
      <template v-slot:top>
        <v-row>
          <v-col cols="12">
            <LazyTextField
              v-on:keyup.enter="addUser"
              ref="email_text"
              :label="$t('email')"
              outlined
              v-model="new_user.email"
            >
              <template v-slot:append-outer>
                <v-btn color="primary" :label="$t('add_user')" class="pa-3 btn" @click="addUser">
                  {{ $t("add_user") }}
                </v-btn>
              </template>
            </LazyTextField>
          </v-col>
        </v-row>
      </template>
    </v-data-table>
    <v-row no-gutters>
      <v-col class="text-right">
        <DeleteAlert :callback="deleteUser"></DeleteAlert>
        <!-- <v-btn
        color="error"
        :label="$t('delete')"
        class="pa-3 btn"
        @click="deleteUser"
      > {{$t("user")}} {{$t("delete")}} </v-btn> -->
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { apiService } from "@/common/api_service";
import { applyValidation } from "@/common/common_api";
import DeleteAlert from "@/components/DeleteAlert";

export default {
  name: "AllowedUserEditor",
  components: {
    DeleteAlert
  },
  props: {
    id: {
      type: [Number, String],
      required: true
    }
  },
  data() {
    return {
      allowed_users: [],
      selected_users: [],
      items_length: 0,
      items_per_page: 10,
      next: null,
      new_user: {
        name: null,
        email: null
      },
      headers: [
        {
          text: `${this.$i18n.t("allow")} ${this.$i18n.t("email")}`,
          align: "start",
          sortable: true,
          value: "email"
        },
        {
          text: `${this.$i18n.t("name")}`,
          align: "start",
          value: "name"
        }
      ]
    };
  },
  methods: {
    updatePagination(pagination) {
      let endpoint = `/api/profiles/${this.id}/allowed-users/?page=${pagination}`;
      apiService(endpoint).then((data) => {
        if (!data.count) {
          applyValidation(data);
        } else {
          this.items_length = data.count;
          this.allowed_users = data.results;
        }
      });
    },
    getUsers() {
      let endpoint = `/api/profiles/${this.id}/allowed-users/`;
      apiService(endpoint).then((data) => {
        if (!data.count) {
          applyValidation(data);
        } else {
          this.items_length = data.count;
          this.allowed_users = data.results;
        }
      });
    },
    addUser() {
      let data = {
        allowed_users: this.new_user
      };
      let endpoint = `/api/profiles/${this.id}/allowed-users/`;
      apiService(endpoint, "POST", data).then((data) => {
        if (!data.count) {
          applyValidation(data);
        } else {
          this.items_length = data.count;
          this.allowed_users = data.results;
          alert(this.$i18n.t("request_success"));
        }
        this.new_user = { name: null, email: null };
      });
    },
    async deleteUser() {
      const that = this;
      let selected_user_list = [];
      for (var i = 0; i < this.selected_users.length; i++) {
        selected_user_list.push(this.selected_users[i].email);
      }

      let data = {
        allowed_users: selected_user_list
      };

      let endpoint = `/api/profiles/${this.id}/allowed-users/`;
      await apiService(endpoint, "DELETE", data).then((data) => {
        console.log("delete");
        if (data == undefined) {
          alert(that.$i18n.t("delete_success"));
          for (var i = 0; i < that.selected_users.length; i++) {
            that.$delete(that.allowed_users, that.allowed_users.indexOf(that.selected_users[i]));
          }
        } else {
          applyValidation(data);
        }
        this.selected_users = [];
      });
    }
  },
  created() {
    this.getUsers();
  }
};
</script>

<style></style>
