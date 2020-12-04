<template>
  <v-container>
    <div v-if="papers.length == 0 && !isLoading" class="text-h5 text-center">
      {{$t("no_contract")}}
    </div>
    <v-row v-else>
      <template v-for="paper in papers">
        <Paper :requestUser="requestUser" :paper="paper" :key="paper.id"/>
      </template>
    </v-row>
    <router-link :to="{ name: 'paper-editor' }">
      <v-btn color="grey" dark fixed fab bottom right>
        <v-icon>add</v-icon>
      </v-btn>
    </router-link>
  </v-container>
</template>

<script>
import { apiService } from "@/common/api.service";
import Paper from "@/components/Paper"
export default {
  name: "Home",
  components: {
    Paper
  },
  data() {
    return {
      papers: [],
      requestUser: null
    };
  },
  computed: {},
  methods: {
    async getPapers() {
      let endpoint = "api/paper-list/";
      this.isLoading = true;
      await apiService(endpoint).then(data => {
        this.papers.push(...data.results);
        this.isLoading = false;
      });
    }
  },
  created() {
    this.getPapers();
    this.requestUser = window.localStorage.getItem("username");
  }
};
</script>
<style scoped>
.author-name-position {
  float:right;
}
.author-name-font {
  font-weight: bold !important;
  color: #dc3545;
}
.card-title {
  width: 100%;
}
</style>