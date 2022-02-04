<template>
  <v-container>
    <div class="text-caption red--text">{{ $t("mandate_subtitle") }}</div>
    <div v-if="mandates.length == 0 && !isLoading" class="text-h5 text-center">
      {{ $t("no_mandate") }}
    </div>
    <template v-else>
      <v-row>
        <v-col cols="12" md="6" lg="4" xl="3" v-for="mandate in mandates" :key="mandate.id">
          <v-card
            class="outlined tile"
            :to="{
              name: 'mandate-detail',
              params: { id: mandate.id }
            }"
          >
            <v-chip class="ma-1">{{ mandate.id }}</v-chip>
            <v-chip v-if="mandate.designator_signature == ''" class="ma-1">{{
              $t("progress")
            }}</v-chip>
            <v-chip v-else class="ma-1" color="primary">{{ $t("signature") + $t("done") }}</v-chip>
            <v-card-title class="card-title pa-0 pl-4">
              {{ mandate.address.old_address }}
            </v-card-title>
            <v-card-text>
              <div>{{ mandate.from_date }} ~ {{ mandate.to_date }}</div>
              <div>{{ $t("designator") }} : {{ mandate.designator.user.name }}</div>
              <div>{{ $t("designee") }} : {{ mandate.designee.user.name }}</div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-btn v-show="next" @click="getMandates" color="grey" dark>
          {{ $t("load_more") }}
        </v-btn>
      </v-row>
    </template>
    <v-row height="100%" justify="end">
      <v-btn :to="{ name: 'mandates-editor' }" color="primary" dark>
        <v-icon>add</v-icon>
        {{ $t("create_mandate") }}
      </v-btn>
    </v-row>
  </v-container>
</template>

<script>
import { applyValidation } from "@/common/common_api";
import { apiService } from "@/common/api_service";

export default {
  name: "Mandates",
  data() {
    return {
      isLoading: true,
      mandates: [],
      next: null
    };
  },
  methods: {
    async getMandates() {
      let endpoint = "api/mandates/";
      if (this.next) {
        endpoint = this.next;
      }
      this.isLoading = true;
      await apiService(endpoint).then((data) => {
        if (data.count != undefined) {
          this.next = data.next;
          this.mandates.push(...data.results);
          this.isLoading = false;
        } else {
          applyValidation(data);
        }
      });
    }
  },
  created() {
    this.getMandates();
  }
};
</script>

<style></style>
