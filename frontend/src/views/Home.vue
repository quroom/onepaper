<template>
  <v-container>
    <RightMenu v-model="menu"
      :close-on-content-click="false"
    >
      <template
        v-slot:activator="{ on, attrs }"
      >
        <v-btn dark fixed fab small right v-bind="attrs" v-on="on">
          <v-icon>filter_list_alt</v-icon>
        </v-btn>
      </template>
      <v-card>
        <v-row class="ma-auto" align="center" no-gutters>
          <v-col class="mt-0 mb-0" cols="auto">
            <v-select
              class="ve-input"
              v-model="is_mine"
              :items="mine_or_all_list"
              item-text="text"
              item-value="value"
              :label="`${$t('lookup_scope')}`"
              style="width:110px"
              @change="getPapersWithOptions()"
            ></v-select>
          </v-col>
          <template v-if="is_mine">
            <v-col class="mt-0 mb-0" cols="auto">
              <v-select
                class="ve-input"
                v-model="options.status"
                :items="STATUS_CATEGORY_LIST"
                item-text="text"
                item-value="value"
                :label="`${$t('contract')} ${$t('status')}`"
                style="width:80px"
                @change="getPapersWithOptions()"
              ></v-select>
            </v-col>
            <v-col class="mt-0 mb-0" cols="auto">
              <v-select
                class="ve-input"
                v-model="options.ordering"
                :items="ORDERING_LIST"
                item-text="text"
                item-value="value"
                :label="`${$t('to_date')} ${$t('ordering')}`"
                style="width:80px"
                @change="getPapersWithOptions()"
              ></v-select>
            </v-col>
            <v-col class="mt-0 mb-0" cols="auto">
                <v-text-field
                  class="search-text ve-input"
                  v-model="options.old_address"
                  :label="`${$t('address')}(${$t('partial_correct_match')})`"
                  hide-details
                  dense
                  @keyup.enter="getPapersWithOptions()"
                ></v-text-field>
              </v-col>
            <v-col class="mt-0 mb-0" cols="auto">
                <v-text-field
                  class="search-text ve-input"
                  v-model="options.dong"
                  :label="`${$t('dong')}(${$t('exact_correct_match')})`"
                  hide-details
                  dense
                  @keyup.enter="getPapersWithOptions()"
                ></v-text-field></v-col>
            <v-col class="mt-0 mb-0" cols="auto">
                <v-text-field
                  class="search-text ve-input"
                  v-model="options.ho"
                  :label="`${$t('ho')}(${$t('exact_correct_match')})`"
                  hide-details
                  dense
                  @keyup.enter="getPapersWithOptions()"
                ></v-text-field>
            </v-col>
          </template>
          <template v-else>
            <v-col class="mt-0 mb-0" cols="auto">
              <v-text-field
                class="search-text ve-input"
                v-model="all_papers_options.bjdong"
                :label="`${$t('bjdong')}(${$t('exact_correct_match')})`"
                hide-details
                dense
                @keyup.enter="getPapersWithOptions()"
              ></v-text-field>
            </v-col>
          </template>
        </v-row>
        <v-card-actions>
          <v-btn
            color="red"
            dark
            @click="menu = false"
          >
            {{ $t('cancel') }}
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            dark
            @click="getPapersWithOptions(); menu=false;">
            <v-icon>search</v-icon>
            {{ $t('search') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </RightMenu>
    <div class="text-caption red--text">{{ $t("paper_subtitle") }}</div>
    <div v-if="papers.length == 0 && !isLoading" class="text-h5 text-center">
      {{$t("no_paper")}}
    </div>
    <template v-else>
      <v-row>
        <template v-for="paper in papers">
          <PaperItem :requestUser="requestUser" :paper="paper" :key="paper.id"/>
        </template>
      </v-row>
      <v-row justify="center">
        <v-btn
          v-show="next"
          @click="getPapers"
          color="grey"
          dark
        >
          {{$t("load_more")}}
        </v-btn>
      </v-row>
    </template>
    <v-row>
      <v-col class="text-right" cols="12">
        <v-btn :to="{ name: 'paper-editor' }" color="primary" dark>
          <v-icon>add</v-icon>
          {{$t("create_paper")}}
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { apiService } from "@/common/api_service";
import { applyValidation } from "@/common/common_api";
import PaperItem from "@/components/PaperItem"
export default {
  name: "Home",
  components: {
    PaperItem
  },
  data() {
    return {
      papers: [],
      isLoading: true,
      options: {
        old_address: '',
        dong: '',
        ho: '',
        status: '',
        ordering: ''
      },
      all_papers_options: {
        bjdong: '',
      },
      hide: false,
      menu: false,
      requestUser: null,
      next: null,
      is_mine: true,
      mine_or_all_list: [
        {
          text: `${this.$t('only_my_papers')}`,
          value: true
        },
        {
          text: `${this.$t('all_papers')}`,
          value: false
        }
      ],
      ORDERING_LIST: [
        {
          text: `${this.$t('none')}`,
          value: ''
        },
        {
          text: `${this.$t('ascending')}`,
          value: 'to_date'
        },
        {
          text: `${this.$t('descending')}`,
          value: '-to_date'
        },
      ],
      STATUS_CATEGORY_LIST: [
        {
          text:`${this.$t('all')}`,
          value: ''
        },
        {
          text:`${this.$t('requesting')}`,
          value: this.$getConstByName('status_category', 'requesting')
        },
        {
          text:`${this.$t('draft')}`,
          value: this.$getConstByName('status_category', 'draft')
        },
        {
          text:`${this.$t('progress')}`,
          value: this.$getConstByName('status_category', 'progress')
        },
        {
          text:`${this.$t('done')}`,
          value: this.$getConstByName('status_category', 'done')
        }
      ]
    };
  },
  computed: {},
  methods: {
    async getPapersWithOptions(){
      let endpoint = "/api/papers/";
      let is_first_option = false;
      if(this.is_mine){
        Object.entries(this.options).forEach(function(entry){
          const [key, value] = entry;
          if(value !== ''){
            if(is_first_option) {
              endpoint += `&${key}=${value}`
            } else {
              endpoint += `?${key}=${value}`
            }
            is_first_option = true;
          }
        })
      } else {
        Object.entries(this.all_papers_options).forEach(function(entry){
          const [key, value] = entry;
          endpoint = "/api/all-papers/"
          if(value !== ''){
            if(is_first_option) {
              endpoint += `&${key}=${value}`
            } else {
              endpoint += `?${key}=${value}`
            }
            is_first_option = true;
          }
        })
      }
      this.isLoading = true;
      await apiService(endpoint).then(data => {
        if(!data.count){
          applyValidation(data);
        } else {
          this.papers = data.results
          this.next = data.next;
        }
        this.isLoading = false;
      });
    },
    async getPapers() {
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
    this.requestUser = window.localStorage.getItem("email");
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
.search-text {
  width: 230px;
}
.ve-input {
  margin: 8px;
}
</style>