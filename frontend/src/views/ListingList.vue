<template>
  <div>
    <v-app-bar class="filter-bar" dark color="grey darken-3" dense fixed>
      <v-btn text rounded :to="{ name: 'listing-editor' }">
        <v-icon>add</v-icon>
      </v-btn>
      <v-spacer />
      <LazyTextField
        v-model="options.bjdong"
        class="filter-search"
        hide-details
        prepend-icon="search"
        single-line
        :label="`${$t('bjdong')}`"
        @keydown.enter="getListingsWithOptions"
      ></LazyTextField>
      <div v-if="!isAsking" id="v-filter">
        <v-menu v-model="menu" :close-on-content-click="false" offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn text rounded v-bind="attrs" v-on="on">
              <v-icon>filter_list_alt</v-icon>
            </v-btn>
          </template>
          <v-card>
            <v-row class="ma-auto" align="center">
              <v-col class="d-flex flex-wrap pt-0">
                <v-checkbox
                  class="ve-input"
                  v-model="options.only_vacancy"
                  :label="`${$t('only_vacancy')}`"
                  hide-details
                  @change="getListingsWithOptions()"
                ></v-checkbox>
              </v-col>
              <v-col class="d-flex flex-wrap pt-0">
                <v-select
                  class="ve-input"
                  v-model="options.is_mine"
                  :items="mine_or_all_list"
                  item-text="text"
                  item-value="value"
                  :label="`${$t('lookup_scope')}`"
                  hide-details
                  style="width:110px; max-width:110px"
                  @change="getListingsWithOptions()"
                ></v-select>
              </v-col>
              <v-col class="d-flex flex-wrap pt-0">
                <v-select
                  v-model="options.item_category"
                  :items="$getConstList('ITEM_CATEGORY_LIST')"
                  item-text="text"
                  item-value="value"
                  :label="$t('item_category')"
                  hide-details
                  multiple
                  style="width:130px; max-width:130px"
                >
                  <template v-slot:selection="{ item, index }">
                    <v-chip v-if="options.item_category.length === 1">
                      <span>{{ $t(item.text) }}</span>
                    </v-chip>
                    <span
                      v-else-if="index === options.item_category.length - 1"
                      class="grey--text text-caption"
                    >
                      (+{{ options.item_category.length }} others)
                    </span>
                  </template>
                  <template v-slot:item="{ item, attrs, on }">
                    <v-list-item v-on="on" v-bind="attrs" #default="{ active }">
                      <v-list-item-action class="ma-0">
                        <v-checkbox :ripple="false" :input-value="active"></v-checkbox>
                      </v-list-item-action>
                      <v-list-item-content>
                        <v-list-item-title>
                          <v-row class="ma-0" align="center">
                            {{ $t(item.text) }}
                          </v-row>
                        </v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </template>
                </v-select>
              </v-col>
              <v-col class="d-flex flex-wrap pt-0">
                <v-select
                  v-model="options.trade_category"
                  :items="$getConstList('TRADE_CATEGORY_LIST')"
                  item-text="text"
                  item-value="value"
                  :label="$t('trade_category')"
                  hide-details
                  multiple
                  style="width:100px; max-width:100px;"
                >
                  <template v-slot:selection="{ item, index }">
                    <v-chip v-if="options.trade_category.length === 1">
                      <span>{{ $t(item.text) }}</span>
                    </v-chip>
                    <span
                      v-else-if="index === options.trade_category.length - 1"
                      class="grey--text text-caption"
                    >
                      (+{{ options.trade_category.length }} others)
                    </span>
                  </template>
                  <template v-slot:item="{ item, attrs, on }">
                    <v-list-item v-on="on" v-bind="attrs" #default="{ active }">
                      <v-list-item-action class="ma-0">
                        <v-checkbox :ripple="false" :input-value="active"></v-checkbox>
                      </v-list-item-action>
                      <v-list-item-content>
                        <v-list-item-title>
                          <v-row class="ma-0" align="center">
                            {{ $t(item.text) }}
                          </v-row>
                        </v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </template>
                </v-select>
              </v-col>
              <v-col class="pt-6 pb-0" cols="12">
                <v-range-slider
                  v-if="isRent"
                  v-model="options.monthly_fee"
                  max="300"
                  min="0"
                  step="10"
                  class="align-center"
                  :label="$t('monthly_fee')"
                  thumb-size="32"
                  thumb-label="always"
                >
                  <template v-slot:thumb-label="props">
                    <template v-if="props.value < 300">
                      {{ props.value }}
                    </template>
                    <template v-else>
                      무한
                    </template>
                  </template>
                </v-range-slider>
              </v-col>
              <v-col class="py-0" cols="12">
                <v-range-slider
                  v-model="options.security_deposit"
                  max="25000"
                  min="0"
                  step="1000"
                  class="align-center"
                  :label="$t('security_deposit')"
                  thumb-size="32"
                  thumb-label="always"
                >
                  <template v-slot:thumb-label="props">
                    <template v-if="props.value < 25000">
                      {{ props.value }}
                    </template>
                    <template v-else>
                      무한
                    </template>
                  </template>
                </v-range-slider>
              </v-col>
              <v-col class="py-0" cols="12">
                <v-range-slider
                  v-model="options.maintenance_fee"
                  max="50"
                  min="0"
                  step="2"
                  class="align-center"
                  :label="$t('maintenance_fee')"
                  thumb-size="32"
                  thumb-label="always"
                >
                  <template v-slot:thumb-label="props">
                    <template v-if="props.value < 50">
                      {{ props.value }}
                    </template>
                    <template v-else>
                      무한
                    </template>
                  </template>
                </v-range-slider>
              </v-col>
            </v-row>
            <v-card-actions>
              <v-btn color="red" dark @click="menu = false">
                {{ $t("cancel") }}
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn
                dark
                @click="
                  getListingsWithOptions();
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
      <div class="text-caption red--text">{{ $t("listing_subtitle") }}</div>
      <div v-if="listings.length == 0 && !isLoading" class="text-h5 text-center">
        {{ $t("no_result") }}
      </div>
      <template v-else>
        <v-row>
          <template v-for="listing in listings">
            <ListingItem :listing="listing" :key="listing.id"></ListingItem>
          </template>
        </v-row>
        <v-row justify="center">
          <v-btn v-show="next" @click="getListings" color="grey" dark>
            {{ $t("load_more") }}
          </v-btn>
        </v-row>
      </template>
      <v-row height="100%" justify="end">
        <v-btn :to="{ name: 'listing-editor' }" color="primary" dark>
          <v-icon>add</v-icon>
          {{ $t("create") }}
        </v-btn>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { applyValidation } from "@/common/common_api";
import { apiService } from "@/common/api_service";
import ListingItem from "@/components/ListingItem";
import Constants from "@/plugins/Constants";

export default {
  name: "ListingList",
  components: {
    ListingItem
  },
  computed: {
    mine_or_all_list() {
      return [
        {
          text: `${this.$t("only_my_listings")}`,
          value: true
        },
        {
          text: `${this.$t("all_listings")}`,
          value: false
        }
      ];
    },
    isRent: function() {
      if (this.options.trade_category.length === 0) {
        return true;
      } else if (this.options.trade_category.includes(1)) {
        return true;
      }
      return false;
    }
  },
  watch: {
    options: {
      handler: function(val) {
        this.options.bjdong = "";
        localStorage.setItem("listing_options", JSON.stringify(val));
      },
      deep: true
    }
  },
  data() {
    return {
      options: {
        is_mine: false,
        bjdong: "",
        security_deposit: [0, Constants.MAX_SECURITY_DEPOSIT_FILTER],
        monthly_fee: [0, Constants.MAX_MONTHLY_FEE_FILTER],
        maintenance_fee: [0, Constants.MAX_MAINTENANCE_FEE_FILTER],
        trade_category: [],
        item_category: [],
        online_visit: false,
        only_vacancy: false
      },
      isAsking: false,
      isLoading: true,
      listings: [],
      next: null,
      menu: false
    };
  },
  methods: {
    async getListings() {
      let endpoint = "api/listings/";
      if (this.next) {
        endpoint = this.next;
      }
      this.isLoading = true;
      await apiService(endpoint).then((data) => {
        if (data.count != undefined) {
          this.next = data.next;
          this.listings.push(...data.results);
          this.isLoading = false;
        } else {
          applyValidation(data);
        }
      });
    },
    async getListingsWithOptions() {
      let endpoint = "/api/listings/";
      let is_first_option = false;

      Object.entries(this.options).forEach(function(entry) {
        const [key, value] = entry;
        if (["security_deposit", "monthly_fee", "maintenance_fee"].includes(key)) {
          if (value.length === 0) {
            return;
          } else {
            if (value[0] === 0 && value[1] === Constants[`MAX_${key.toUpperCase()}_FILTER`]) {
              return;
            } else {
              if (value[0] !== 0) {
                if (is_first_option) {
                  endpoint += `&min_${key}=${value[0]}`;
                } else {
                  endpoint += `?min_${key}=${value[0]}`;
                }
                is_first_option = true;
              }
              if (value[1] !== Constants[`MAX_${key.toUpperCase()}_FILTER`]) {
                if (is_first_option) {
                  endpoint += `&max_${key}=${value[1]}`;
                } else {
                  endpoint += `?max_${key}=${value[1]}`;
                }
                is_first_option = true;
              }
            }
          }
        } else {
          if (value === null || value === false || value === "") {
            return;
          }
          if (["trade_category", "item_category"].includes(key)) {
            if (value.length === 0) {
              return;
            }
          }
          if (is_first_option) {
            endpoint += `&${key}=${value}`;
          } else {
            endpoint += `?${key}=${value}`;
          }
          is_first_option = true;
        }
      });
      this.isLoading = true;
      await apiService(endpoint).then((data) => {
        if (!data.count) {
          this.listings = [];
          applyValidation(data);
        } else {
          this.listings = data.results;
          this.next = data.next;
        }
        this.isLoading = false;
      });
    }
  },
  created() {
    if (JSON.parse(localStorage.getItem("listing_options"))) {
      this._options = JSON.parse(localStorage.getItem("listing_options"));
      for (let key of Object.keys(this.options)) {
        if (this._options[key] === undefined) {
          this._options[key] = this.options[key];
        }
      }
      this.options = this._options;
      this.getListingsWithOptions();
    } else {
      this.getListings();
    }
  }
};
</script>

<style scoped>
.filter-bar {
  top: 64px !important;
  z-index: 2 !important;
}
.container {
  padding-top: 56px;
}
.filter-search {
  max-width: 140px;
}
@media (max-width: 960px) {
  .filter-bar {
    top: 56px !important;
    z-index: 2 !important;
  }
  .v-progress-linear {
    top: 54px !important;
  }
  .container {
    max-width: 100%;
  }
}
</style>
