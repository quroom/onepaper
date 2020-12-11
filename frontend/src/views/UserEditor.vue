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
            v-model="deleted_username"
            :label="`${$t('deleted')} ${$t('username')}`"
            hide-details="auto"
          ></LazyTextField>
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
          회원 아이디, 이메일, 성함이 정확히 일치해야 탈퇴 처리 되며, 작성된 프로필과 계약서가 없는 경우에만 계정 DB는 완전히 삭제됩니다. <br/>
          작성된 계약서가 있는 경우 계정은 더이상 이용할 수 없도록 처리되며, 데이터베이스를 향후 법적 분쟁 시 활용하기 위해 보존 됩니다. 보존되는 데이터는 본인에게만 제공되니 안심하셔도 됩니다.
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
    <div class="mt-4 text-h4 font-weight text-center">{{$t("edit_registor_info")}}</div>
    <LazyTextField
      class="mt-4"
      v-model="email"
      :label="$t('email')"
      hide-details="auto"
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
    <v-checkbox
      :label="$t('request_agent_account')"
      v-model="request_expert"
      >
    </v-checkbox>
    <v-btn
      style="float:right"
      class="primary"
      @click="submit"
    >
      {{ $t("submit") }}
    </v-btn>
  </v-container>
</template>

<script>
import { apiService } from "@/common/api.service";
import { applyValidation } from "@/common/common_api"

export default {
  name:"UserEditor",
  data() {
    return {
      id: null,
      email: null,
      name: null,
      birthday: null,
      request_expert: null,
      birthday_menu: false,
      dialog: false,
      deleted_username: '',
      deleted_email: '',
      deleted_name: ''
    }
  },
  methods: {
    submit() {
      let endpoint = `/api/user/${this.id}/`;
      let that = this;
      apiService(endpoint, "PUT", {
        email: this.email,
        name: this.name,
        birthday: this.birthday,
      }).then(data => {
        if(data.id != undefined){
          this.id = data.id;
          this.email = data.email;
          this.name = data.name;
          this.birthday = data.birthday;
          this.request_expert = data.request_expert;
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
        username: this.deleted_username,
        email: this.deleted_email,
        name: this.deleted_name
      }).then(data => {
        if(data['delete'] != undefined){
          alert(data['delete'])
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
          vm.request_expert = data.request_expert;
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