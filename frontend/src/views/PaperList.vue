<template>
  <div>
    <v-app-bar class="filter-bar" dark color="grey darken-3" dense fixed>
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
      <v-spacer />
      <div id="v-filter">
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
                  <v-switch
                    class="switch"
                    v-model="options.is_hidden"
                    :label="$t('hide')"
                    :false-value="0"
                    :true-value="1"
                    @change="getPapersWithOptions()"
                  >
                  </v-switch>
                </v-col>
                <v-col class="mt-0 mb-0" cols="auto">
                  <v-text-field
                    class="search-text ve-input"
                    v-model="options.old_address"
                    :label="`${$t('old_address')}(${$t('partial_correct_match')})`"
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
      </div>
    </v-app-bar>
    <v-container>
      <div class="text-caption blue--text">{{ $t("paper_subtitle") }}</div>
      <v-row
        v-if="!$store.state.has_profile"
        justify="center"
        class="font-weight-bold red--text ma-auto"
      >
        {{ $t("before_create_contract") }},
        <v-btn
          id="v-create-profile"
          class="mx-1"
          :to="{ name: 'profile-editor' }"
          color="error"
          x-small
          >{{ $t("create_profile") }}</v-btn
        >
        {{ $t("mandatory") }}
      </v-row>
      <div v-else-if="papers.length == 0 && !isLoading" class="text-h6 text-center">
        {{ $t("no_result") }}
      </div>
      <div :id="this.is_mine && this.papers.length ? 'v-paper-list' : ''">
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
      </div>
      <v-row>
        <v-col class="text-right" cols="12">
          <v-btn id="v-create-paper" :to="{ name: 'paper-editor' }" color="primary" dark>
            <v-icon>add</v-icon>
            {{ $t("create_paper") }}
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
    <CustomTour name="papers" :steps="steps" :options="tourOptions" :callbacks="tourCallbacks" />
  </div>
</template>

<script>
import { apiService } from "@/common/api_service";
import { applyValidation } from "@/common/common_api";
import PaperItem from "@/components/PaperItem";
export default {
  name: "PaperList",
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
      var status_category_list = [
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
        },
        {
          text: `${this.$t("denied")}`,
          value: this.$getConstByName("status_category", "denied")
        }
      ];
      if (this.options.is_hidden == false) {
        return status_category_list;
      } else {
        for (var i = 1; i <= 3; i++) {
          this.$delete(status_category_list, 1);
        }
        return status_category_list;
      }
    },
    steps() {
      return [
        {
          target: "#v-navbar",
          content: `${this.$t("start_tour")}`
        },
        {
          target: "#v-create-profile",
          content: `${this.$t("tour_if_don_have_profile")}`,
          offset: -150,
          disabledButtons: {
            buttonNext: true
          }
        },
        {
          target: "#v-home",
          content: `${this.$t("tour_home_menu")}`,
          params: {
            highlight: false
          }
        },
        {
          target: "#v-menu",
          content: `${this.$t("tour_toggle_menu")}`
        },
        {
          target: "#v-help",
          content: `${this.$t("tour_help_menu")}`
        },
        {
          target: "#v-filter",
          content: `${this.$t("tour_filter")}`
        },
        {
          target: "#v-paper-list",
          content: `${this.$t("tour_paper_list")}`,
          params: {
            enableScrolling: false
          }
        },
        {
          target: "#v-create-paper",
          content: `${this.$t("tour_create_paper_button_click")}`
        }
      ];
    }
  },
  data() {
    return {
      papers: [],
      isLoading: true,
      options: {
        dong: "",
        ho: "",
        is_hidden: 0,
        status: "",
        old_address: "",
        ordering: ""
      },
      all_papers_options: {
        status: "",
        bjdong: ""
      },
      menu: false,
      next: null,
      is_mine: true,
      is_tour_on: true,
      tourCallbacks: {
        onPreviousStep: this.previousStepTour,
        onNextStep: this.nextStepTour
      },
      tourOptions: {
        highlight: true,
        stopOnTargetNotFound: false,
        useKeyboardNavigation: false
      }
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
          this.papers = [];
          applyValidation(data);
        } else {
          this.papers = data.results;
          this.next = data.next;
        }
        this.isLoading = false;
      });
    },
    async getPapers() {
      let endpoint = "/api/papers/?is_hidden=0";
      if (this.next) {
        endpoint = this.next;
      }
      this.isLoading = true;
      await apiService(endpoint).then((data) => {
        if (data.count != undefined) {
          this.papers.push(...data.results);
          this.isLoading = false;
          this.next = data.next;
        } else {
          applyValidation(data);
        }
      });
    },
    manageStep() {
      if (this.$store.state.has_profile) {
        this.$tours["papers"].currentstep += 1;
      }
    },
    nextStepTour(currentStep) {
      for (var i = currentStep + 1; i < this.steps.length; i++) {
        const target_element = document.querySelector(this.steps[i].target);
        if (target_element) {
          if (i != currentStep + 1) {
            const tour = this.$tours["papers"];
            this.$nextTick(() => {
              tour.currentStep = i;
            });
          }
          break;
        }
      }
    },
    previousStepTour(currentStep) {
      for (var i = currentStep - 1; i > -1; i--) {
        const target_element = document.querySelector(this.steps[i].target);
        if (target_element) {
          if (i != currentStep - 1) {
            const tour = this.$tours["papers"];
            this.$nextTick(() => {
              tour.currentStep = i;
            });
          }
          break;
        }
      }
    }
  },
  destroyed() {
    this.$tours["papers"].stop();
  },
  mounted() {
    this.getPapers();
    if (this.$store.state.user_setting.is_tour_on && this.$store.state.user_category === "user") {
      this.$tours["papers"].start();
    }
  }
};
</script>
<style scoped>
.filter-bar {
  top: 64px !important;
  z-index: 1;
}
.container {
  padding-top: 56px;
}
.card-title {
  width: 100%;
}
.search-text {
  width: 210px;
}
.ve-input {
  margin: 8px;
}
/* switch label style change */
.switch /deep/ .v-input__slot {
  position: relative !important;
}
.switch /deep/ .v-label {
  position: absolute !important;
  top: -20px !important;
  right: 0px !important;
  left: 0px !important;
}
@media (max-width: 960px) {
  .filter-bar {
    top: 56px !important;
    z-index: 1;
  }
  .v-progress-linear {
    top: 54px !important;
  }
  .container {
    max-width: 100%;
  }
}
</style>
