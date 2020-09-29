<template>
  <div class="home">
    <v-container class="my-5">
      <v-row>
        <v-col
          cols="12"
          md="6"
          lg="4"
          xl="3"
          v-for="paper in papers"
          :key="paper.id"
        >
          <v-card
            class="outlined tile"
            :to="{ name: 'paper', params: { id: paper.id } }"
          >
            <div class="text-body-2" style="float:right">
              {{ $t("last") }}{{ $t("updated_at") }} : {{ paper.updated_at}}
            </div>
            <v-card-title class="ma-1">
              {{ paper.room_name }}
              {{ $getConstI18("trade_type", paper.trade_type) }}
            </v-card-title>
            <v-card-subtitle style="float:right">
              {{ $t("author") }}: <span class="author-name"> {{ paper.author }} </span>
            </v-card-subtitle>
            <v-card-text>
              <div>
                {{ paper.address }}
              </div>
              <span>
                {{ $getConstI18("realestate_type", paper.realestate_type) }}
              </span>
              <span v-if="paper.trade_type == $getConstByVal('trade_type', 'rent')">
                보{{ paper.security_deposit }}/월 {{paper.monthly_fee}}
              </span>
              <span v-else-if="paper.trade_type == $getConstByVal('trade_type', 'depositloan')">
              </span>
              <span v-else-if="paper.trade_type == $getConstByVal('trade_type', 'trade')">
              </span>
              <span v-else-if="paper.trade_type == $getConstByVal('trade_type', 'exchange')">
              </span>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <router-link :to="{ name: 'paper-editor' }">
        <v-btn color="grey" dark absolute fab mid right>
          <v-icon>add</v-icon>
        </v-btn>
      </router-link>
    </v-container>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service";

export default {
  name: "Home",
  data() {
    return {
      papers: []
    };
  },
  methods: {
    getPapers() {
      let endpoint = "api/papers/";
      apiService(endpoint).then(data => {
        this.papers.push(...data.results);
      });
    }
  },
  created() {
    this.getPapers();
  }
};
</script>
<style>
  .author-name {
    font-weight:bold !important;
    color : #DC3545
  }
</style>