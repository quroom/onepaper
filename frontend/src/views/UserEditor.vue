<template>
  <v-container max-width="400px">
    <v-dialog v-model="dialog" max-width="400px">
      <template v-slot:activator="{ on }">
        <v-btn
          class="ma-1 auto"
          color="error"
          @click.prevent=""
          v-on.prevent="on">
          {{$t('delete_account')}}
        </v-btn>
      </template>
      <v-card>
        <v-card-title
          class="error headline"
          style="color:white;"
        >
          {{$t("delete_confirm")}}
        </v-card-title>
        <v-card-text>
          <LazyTextField
            v-model="deleted_email"
            :label="`${$t('deleted')} ${$t('user')} ${$t('email')}`"
            hide-details="auto"
          ></LazyTextField>
          <LazyTextField
            v-model="deleted_name"
            :label="`${$t('deleted')} ${$t('user')} ${$t('name')}`"
            hide-details="auto"
          ></LazyTextField>
        </v-card-text>
        <v-card-subtitle>
          {{$t("delete_profile_subtitle")}}
        </v-card-subtitle>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn
            color="green"
            dark
            @click="dialog=false;"
          >
            {{ $t("cancel") }}
          </v-btn>
        <v-spacer></v-spacer>
          <v-btn
            color="error"
            @click="dialog=false; deleteData();"
          >
            {{ $t("delete_account") }} {{ $t("confirm") }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-btn
      class="ma-1 auto"
      style="float:right"
      color="green"
      dark
      href="/accounts/password/change/"
    >
      {{$t('password_change')}}
    </v-btn>
    <div class="mt-4 text-h4 font-weight text-center">{{$t("edit_registor_info")}}</div>
    <LazyTextField
      class="mt-4"
      v-model="email"
      :label="$t('email')"
      hide-details="auto"
      disabled
    ></LazyTextField>
    <LazyTextField
      class="mt-4"
      v-model="name"
      :label="$t('name')"
      hide-details="auto"
    ></LazyTextField>
    <v-menu
      v-model="birthday_menu"
      :close-on-content-click="false"
      :nudge-right="40"
      transition="scale-transition"
      offset-y
      min-width="290px"
    >
      <template v-slot:activator="{ on, attrs }">
        <ValidationProvider ref="birthday"  :name="$t('birthday')" v-slot="{ errors }">
          <LazyTextField
            ref="birthday_input"
            class="mt-4"
            v-model="birthday"
            :error-messages="errors"
            :label="$t('birthday')"
            prepend-icon="event"
            v-bind="attrs"
            v-on="on"
            readonly
          ></LazyTextField>
        </ValidationProvider>
      </template>
      <v-date-picker
        v-model="birthday"
        @input="birthday_menu=false"
        :locale="this.$i18n.locale"
      ></v-date-picker>
    </v-menu>
    <v-row class="mt-4" justify="end">
      <v-btn class="primary" @click="submit">
        {{ $t("submit") }}
      </v-btn>
    </v-row>
  </v-container>
</template>

<script>
import { apiService } from "@/common/api_service";
import { applyValidation } from "@/common/common_api"

export default {
  name:"UserEditor",
  data() {
    return {
      id: null,
      email: null,
      name: null,
      birthday: null,
      birthday_menu: false,
      dialog: false,
      deleted_email: '',
      deleted_name: ''
    }
  },
  methods: {
    submit() {
      let endpoint = `/api/user/${this.id}/`;
      let that = this;
      apiService(endpoint, "PUT", {
        name: this.name,
        birthday: this.birthday,
      }).then(data => {
        if(data.id != undefined){
          this.id = data.id;
          this.email = data.email;
          this.name = data.name;
          this.birthday = data.birthday;
          alert(that.$i18n.t("request_success"))
        }
        else{
          applyValidation(data, that);
        }
      });
    },
    deleteData() {
      let endpoint = `/api/user/${this.id}/`;
      let that = this;
      apiService(endpoint, "DELETE", {
        email: this.deleted_email,
        name: this.deleted_name
      }).then(data => {
        if(data['user_delete'] != undefined){
          alert(data['user_delete'])
          window.location.href="/accounts/logout/"
        }
        else{
          applyValidation(data, that);
        }
      });
    },
  },
  async beforeRouteEnter(to, from, next){
    let endpoint = `/api/user/`;
    let data = await apiService(endpoint);
    if(data.id != undefined){
      return next(
        vm => {
          vm.id = data.id;
          vm.email = data.email;
          vm.name = data.name;
          vm.birthday = data.birthday;
        }
      )
    } else {
      applyValidation(data)
    }
  }
}
</script>

<style scoped>
  .container {
    max-width: 360px
  }

</style>