<template>
  <v-container>
    <v-menu v-model="menu"
      :close-on-content-click="false"
      :nudge-width="200"
    >
      <template
        v-slot:activator="{ on, attrs }"
      >
        <v-btn color="primary" dark fixed fab middle right v-bind="attrs" v-on="on">
          <v-icon>filter_list_alt</v-icon>
        </v-btn>
      </template>
      <v-card>
          <v-list>
            <v-list-item>
              <v-select
                v-model="options.status"
                :items="STATUS_CATEGORY_LIST"
                item-text="text"
                item-value="value"
                :label="`${$t('contract')} ${$t('status')}`"
              >
              </v-select>
            </v-list-item>
            <v-list-item>
              <v-text-field
                class="ve-input"
                v-model="options.address"
                exact_correct_match

                :label="`${$t('address')}(${$t('partial_correct_match')})`"
                hide-details
                dense
              ></v-text-field>
            </v-list-item>
            <v-list-item>
              <v-text-field
                class="ve-input"
                v-model="options.dong"
                :label="`${$t('dong')}(${$t('exact_correct_match')})`"
                hide-details
                dense
              ></v-text-field>
              <v-text-field
                class="ve-input"
                v-model="options.ho"
                :label="`${$t('ho')}(${$t('exact_correct_match')})`"
                hide-details
                dense
              ></v-text-field>
            </v-list-item>
          </v-list>
          <v-card-actions>
            <v-btn
              color="green"
              dark
              @click="menu = false"
            >
              {{ $t('cancel') }}
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              @click="getPapersWithOptions(); menu=false;">
              <v-icon>search</v-icon>
              {{ $t('search') }}
            </v-btn>
          </v-card-actions>
        </v-card>
    </v-menu>
    <div v-if="papers.length == 0 && !isLoading" class="text-h5 text-center">
      {{$t("no_contents")}}
    </div>
    <template v-else>
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
import { applyValidation } from "@/common/common_api";
import Paper from "@/components/Paper"
export default {
  name: "Home",
  components: {
    Paper
  },
  data() {
    return {
      papers: [],
      isLoading: true,
      options: {
        address: '',
        dong: '',
        ho: '',
        status: ''
      },
      hide: false,
      menu: false,
      requestUser: null,
      next: null,
      STATUS_CATEGORY_LIST: [
        {
          text:`${this.$t('all')}`,
          value: ''
        },
        {
          text:`${this.$t('draft')}`,
          value: 0
        },
        {
          text:`${this.$t('progress')}`,
          value: 1
        },
        {
          text:`${this.$t('done')}`,
          value: 2
        }
      ]
    };
  },
  computed: {},
  methods: {
    async getPapersWithOptions(){
      let endpoint = "/api/papers/";
      let is_options = false;
      Object.entries(this.options).forEach(function(entry){
        const [key, value] = entry;
        if(value !== ''){
          if(is_options) {
            endpoint += `&${key}=${value}`
          } else {
            endpoint += `?${key}=${value}`
          }
          is_options = true;
        }
      })
      this.isLoading = true;
      await apiService(endpoint).then(data => {
        if(data.count != undefined){
          this.papers = data.results
          this.isLoading = false;
          this.next = data.next;
        } else {
          applyValidation(data);
        }
      });
    },
    async getPapers() {
      const that = this;
      let endpoint = "/api/papers/";
      if(this.next) {
        endpoint = this.next;
      }
      this.isLoading = true;
      await apiService(endpoint).then(data => {
        if(data.count != undefined){
          this.papers.push(...data.results);
          this.isLoading = false;
          this.next = data.next;
        } else {
          applyValidation(data);
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