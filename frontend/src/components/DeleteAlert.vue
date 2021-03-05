<template>
  <v-dialog v-model="dialog" max-width="400px">
      <template v-slot:activator="{ on }">
        <v-btn 
          class="ma-1 auto no-print"
          color="error"
          @click.prevent=""
          v-on.prevent="on">
          {{$t('delete')}}
        </v-btn>
      </template>
      <v-card>
        <v-card-title
          class="error headline"
          style="color:white;"
        >
          {{$t("delete_confirm")}}
        </v-card-title>
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
            {{ $t("delete") }} {{ $t("confirm") }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>

<script>

import { applyValidation } from "@/common/common_api";
import { apiService } from "@/common/api_service";

export default {
  name: "DeleteAlert",
  props: {
    url: { type: String },
    id: { type: [Number, String] },
    router_name: { type: String },
    callback: { type: Function }
  },
  data() {
    return {
      dialog: false
    }
  },
  methods: {
    async deleteData() {
      const that = this;
      if(this.callback == undefined) {
        try {
          let endpoint = this.url+`${this.id}/`;
          await apiService(endpoint, "DELETE").then(data => {
            if(data == undefined){
              alert(this.$i18n.t("delete_success"));
              this.$router.push({name:this.router_name}); 
            }
            else{
              applyValidation(data, that);
            }
          });
        } catch(err) {
          alert(err);
        }
      } else {
        this.callback()
      }
    }
  }
}
</script>

<style>

</style>