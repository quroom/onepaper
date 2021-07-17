<template>
  <div>
    <v-app-bar class="navigation" dark color="grey darken-3" dense hide-on-scroll fixed>
      <v-spacer />
      <v-btn-toggle tile group mandatory v-model="is_mine">
        <v-btn
          :value="false"
          text
          rounded
          @click="
            is_mine = false;
            getPapersWithOptions();
          "
        >
          <span> {{ $t("all_papers") }}</span>
          <v-icon>mdi-history</v-icon>
        </v-btn>
        <v-btn
          :value="true"
          text
          rounded
          @click="
            is_mine = true;
            getPapersWithOptions();
          "
        >
          <span> {{ $t("only_my_papers") }}</span>
          <v-icon>mdi-heart</v-icon>
        </v-btn>
      </v-btn-toggle>
      <v-menu v-model="menu" :close-on-content-click="false">
        <template v-slot:activator="{ on, attrs }">
          <v-btn text rounded v-bind="attrs" v-on="on">
            <v-icon>filter_list_alt</v-icon>
            <span>{{ $t("filter") }}</span>
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
                ></v-text-field
              ></v-col>
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
                <v-select
                  class="ve-input"
                  v-model="all_papers_options.status"
                  :items="STATUS_CATEGORY_LIST"
                  item-text="text"
                  item-value="value"
                  :label="`${$t('contract')} ${$t('status')}`"
                  style="width:80px"
                  @change="getPapersWithOptions()"
                ></v-select>
              </v-col>
              <v-col class="mt-0 mb-0" cols="auto">
                <v-text-field
                  class="search-text ve-input"
                  v-model="all_papers_options.bjdong"
                  :label="`${$t('bjdong')}`"
                  hide-details
                  dense
                  @keyup.enter="getPapersWithOptions()"
                ></v-text-field>
              </v-col>
            </template>
          </v-row>
          <v-card-actions>
            <v-btn color="red" dark @click="menu = false">
              {{ $t("cancel") }}
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
              dark
              @click="
                getPapersWithOptions();
                menu = false;
              "
            >
              <v-icon>search</v-icon>
              {{ $t("search") }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-menu>
      <v-spacer />
    </v-app-bar>
    <v-container>
      <div class="text-caption red--text pr-10">{{ $t("paper_subtitle") }}</div>
      <div v-if="papers.length == 0 && !isLoading" class="text-h6 text-center">
        {{ $t("no_paper") }}
      </div>
      <template v-else>
        <v-row>
          <template v-for="paper in papers">
            <PaperItem :paper="paper" :key="paper.id" />
          </template>
        </v-row>
        <v-row justify="center">
          <v-btn v-show="next" @click="getPapers" color="grey" dark>
            {{ $t("load_more") }}
          </v-btn>
        </v-row>
      </template>
      <v-row>
        <v-col class="text-right" cols="12">
          <v-btn :to="{ name: 'paper-editor' }" color="primary" dark>
            <v-icon>add</v-icon>
            {{ $t("create_paper") }}
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { apiService } from "@/common/api_service";
import { applyValidation } from "@/common/common_api";
import PaperItem from "@/components/PaperItem";
export default {
  name: "Home",
  components: {
    PaperItem
  },
  computed: {
    mine_or_all_list() {
      return [
        {
          text: `${this.$t("only_my_papers")}`,
          value: true
        },
        {
          text: `${this.$t("all_papers")}`,
          value: false
        }
      ];
    },
    ORDERING_LIST() {
      return [
        {
          text: `${this.$t("none")}`,
          value: ""
        },
        {
          text: `${this.$t("ascending")}`,
          value: "to_date"
        },
        {
          text: `${this.$t("descending")}`,
          value: "-to_date"
        }
      ];
    },
    STATUS_CATEGORY_LIST() {
      return [
        {
          text: `${this.$t("all")}`,
          value: ""
        },
        {
          text: `${this.$t("requesting")}`,
          value: this.$getConstByName("status_category", "requesting")
        },
        {
          text: `${this.$t("draft")}`,
          value: this.$getConstByName("status_category", "draft")
        },
        {
          text: `${this.$t("progress")}`,
          value: this.$getConstByName("status_category", "progress")
        },
        {
          text: `${this.$t("done")}`,
          value: this.$getConstByName("status_category", "done")
        }
      ];
    }
  },
  data() {
    return {
      papers: [],
      isLoading: true,
      options: {
        old_address: "",
        dong: "",
        ho: "",
        status: "",
        ordering: ""
      },
      all_papers_options: {
        status: "",
        bjdong: ""
      },
      hide: false,
      menu: false,
      requestUser: null,
      next: null,
      is_mine: true
    };
  },
  methods: {
    async getPapersWithOptions() {
      let endpoint = "/api/papers/";
      let is_first_option = false;
      if (this.is_mine) {
        Object.entries(this.options).forEach(function(entry) {
          const [key, value] = entry;
          if (value !== "") {
            if (is_first_option) {
              endpoint += `&${key}=${value}`;
            } else {
              endpoint += `?${key}=${value}`;
            }
            is_first_option = true;
          }
        });
      } else {
        endpoint = "/api/all-papers/";
        Object.entries(this.all_papers_options).forEach(function(entry) {
          const [key, value] = entry;
          if (value !== "") {
            if (is_first_option) {
              endpoint += `&${key}=${value}`;
            } else {
              endpoint += `?${key}=${value}`;
            }
            is_first_option = true;
          }
        });
      }
      this.isLoading = true;
      await apiService(endpoint).then((data) => {
        if (!data.count) {
          applyValidation(data);
        } else {
          this.papers = data.results;
          this.next = data.next;
        }
        this.isLoading = false;
      });
    },
    async getPapers() {
      let endpoint = "/api/papers/";
      if (this.next) {
        endpoint = this.next;
      }
      this.isLoading = true;
      await apiService(endpoint).then((data) => {
        if (data.count != undefined) {
          //#FIXME Add codes for user didn't write papers yet.
          if (data.count == 0) {
            apiService("/api/all-papers/").then((data) => {
              if (data.count != undefined) {
                this.papers.push(...data.results);
                this.isLoading = false;
                this.next = data.next;
                this.is_mine = false;
              } else {
                applyValidation(data);
              }
            });
          } else {
            this.papers.push(...data.results);
            this.isLoading = false;
            this.next = data.next;
          }
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
.card-title {
  width: 100%;
}
.search-text {
  width: 210px;
}
.ve-input {
  margin: 8px;
}
.navigation {
  top: 64px;
  z-index: 1;
}
@media (max-width: 960px) {
  .navigation {
    top: 56px;
    z-index: 1;
  }
  .container {
    max-width: 100%;
  }
}
.container {
  padding-top: 56px;
}
</style>
