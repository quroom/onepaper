<template>
  <v-container>
    <v-row>
      <v-col
        cols="12"
        md="6"
        lg="4"
        xl="3"
        v-for="mandate in mandates"
        :key="mandate.id"
      >
        <v-card
          class="outlined tile"
          :to="{ name: 'mandates-editor', params: {id: mandate.id, readonly:false } }"
        >
          <v-card-title class="card-title pa-0 pl-4">
            {{mandate.address.old_address}}
          </v-card-title>
          <v-card-text>
            <div> {{$t("designator")}} : {{ mandate.designator.user.name }} </div>
            <div> {{$t("designee")}} : {{ mandate.designee.user.name }} </div>
          </v-card-text>

        </v-card>
      </v-col>
    </v-row>
    <router-link :to="{ name: 'mandates-editor', params: {readonly:false} }">
      <v-btn color="grey" dark fixed fab bottom right>
        <v-icon>add</v-icon>
      </v-btn>
    </router-link>
  </v-container>
</template>

<script>
import { apiService } from "@/common/api.service";

export default {
  name: "Mandates",
  data() {
    return {
      mandates:[]
    }
  },
  methods: {
    async getMandates(){
      let endpoint = "api/mandates/";
      await apiService(endpoint).then(data => {
        this.mandates.push(...data.results);
      })
    }
  },
  created(){
    this.getMandates();
  }
}
</script>

<style>

</style>