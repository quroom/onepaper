<template>
  <v-container>
    <div v-if="papers.length == 0 && !isLoading" class="text-h5 text-center">
      {{$t("no_contract")}}
    </div>
    <template v-else>
      <v-menu v-model="menu"
        :close-on-content-click="false"
        :nudge-width="200"
      >
        <template
          v-slot:activator="{ on, attrs }"
        >
          <v-btn color="grey" dark fixed fab middle right v-bind="attrs" v-on="on">
            <v-icon>filter_list_alt</v-icon>
          </v-btn>
        </template>
        <v-card>
            <v-list>
              <v-list-item>
                <v-text-field
                  class="ve-input"
                  :label="$t('address')"
                  hide-details
                  dense
                ></v-text-field>
              </v-list-item>
              <v-list-item>
                <v-text-field
                  class="ve-input"
                  :label="$t('ho')"
                  hide-details
                  dense
                ></v-text-field>
              </v-list-item>
              <v-list-item>
                <v-checkbox class="ve-input" v-model="hide" :label="$t('hidden') + $t('paper')" hide-details dense></v-checkbox>
              </v-list-item>
            </v-list>
            <v-list>
              <v-list-item>
                <v-list-item-action>
                  
      
                </v-list-item-action>
              </v-list-item>
            </v-list>
            <v-card-actions>
              <v-btn icon>
                <v-icon>search</v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
      </v-menu>
      <v-row>
        <template v-for="paper in papers">
          <Paper :requestUser="requestUser" :paper="paper" :key="paper.id"/>
        </template>
      </v-row>
      <v-row justify="center">
        <v-btn
          v-show="next"
          @click="getPapers"
          color="primary"
        >
          {{$t("load_more")}}
        </v-btn>
      </v-row>
    </template>
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
      options: {
        group: null,
        hide: false,
        status: 0,
        address: null,
        dong: null,
        ho: null,
      },
      hide: false,
      menu: false,
      requestUser: null,
      next: null
    };
  },
  computed: {},
  methods: {
    async getPapers() {
      let endpoint = "/api/papers/";
      if(this.next) {
        endpoint = this.next;
      }
      this.isLoading = true;
      await apiService(endpoint).then(data => {
        this.papers.push(...data.results);
        this.isLoading = false;
        if (data.next) {
          this.next = data.next;
        } else {
          this.next = null
        }
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
.ve-input {
  margin-left: 8px;
  margin-right: 8px;
  margin-bottom: 4px;
}
</style>