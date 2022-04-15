<template>
  <v-container>
    <LazyTextField
      v-model="search"
      append-icon="mdi-magnify"
      single-line
      hide-details
      :label="`${$t('location')}`"
      prepend-icon="search"
    ></LazyTextField>
    <v-data-table
      :headers="isMobile ? mobile_headers : headers"
      :items="asklistings"
      item-key="id"
      :server-items-length="items_length"
      :page.sync="page_num"
      @update:page="updatePagination"
      :disable-sort="true"
      show-expand
      single-expand
      :mobile-breakpoint="mobile_breakpoint - 200"
    >
      <template v-slot:[`item.trade_category`]="{ item }">
        {{ $getConstI18("trade_category", item.trade_category) }}
      </template>
      <template v-slot:[`item.item_category`]="{ item }">
        {{ $getConstI18("item_category", item.item_category) }}
      </template>
      <template v-slot:[`item.online_visit`]="{ item }">
        {{ item.online_visit == true ? "O" : "X" }}
      </template>
      <template v-slot:[`item.short_lease`]="{ item }">
        {{ item.short_lease == true ? "O" : "X" }}
      </template>
      <template v-slot:expanded-item="{ item }">
        <DeleteAlert
          v-if="$store.state.user.email === item.author"
          :id="item.id"
          :callback="deleteAskListing"
        />
        <td class="px-0" :colspan="headers.length">
          <v-row no-gutters>
            <v-col cols="auto" v-for="(value, key) in item" :key="key">
              <v-card elevation="2" color="grey lighten-2" outlined tile class="pa-1">
                {{ $t(key) }}
              </v-card>
              <v-card
                v-if="['item_category', 'trade_category'].indexOf(key) > -1"
                outlined
                tile
                class="pa-1"
              >
                {{ $getConstI18(key, item[key]) }}</v-card
              >
              <v-card
                v-else-if="['online_visit', 'short_lease'].indexOf(key) > -1"
                outlined
                tile
                class="pa-1"
              >
                {{ item[key] == true ? "O" : "X" }}
              </v-card>
              <v-card v-else outlined tile class="pa-1">{{ value }}</v-card>
            </v-col>
          </v-row>
        </td>
      </template>
    </v-data-table>
    <v-row>
      <v-col class="text-right" cols="12">
        <v-btn
          :to="{ name: 'listing-editor', params: { default_is_asking: true } }"
          color="primary"
          dark
        >
          <v-icon>add</v-icon>
          {{ $t("create") }}
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { apiService } from "@/common/api_service";
import { applyValidation } from "@/common/common_api";

import DeleteAlert from "@/components/DeleteAlert";
export default {
  name: "AskListingList",
  components: {
    DeleteAlert
  },
  computed: {
    isMobile() {
      return this.$vuetify.breakpoint.width < this.mobile_breakpoint;
    }
  },
  data() {
    return {
      headers: [
        {
          text: `${this.$i18n.t("mobile_number")}`,
          align: "start",
          value: "mobile_number"
        },
        {
          text: `${this.$i18n.t("location")}`,
          align: "start",
          value: "location"
        },
        {
          text: `${this.$i18n.t("item_category")}`,
          align: "start",
          value: "item_category"
        },
        {
          text: `${this.$i18n.t("trade_category")}`,
          align: "start",
          value: "trade_category"
        },
        {
          text: `${this.$i18n.t("period")}`,
          align: "start",
          value: "term_of_lease"
        },
        {
          text: `${this.$i18n.t("security_deposit")}`,
          align: "start",
          value: "security_deposit"
        },
        {
          text: `${this.$i18n.t("monthly_fee")}`,
          align: "start",
          value: "monthly_fee"
        },
        {
          text: `${this.$i18n.t("maintenance_fee")}`,
          align: "start",
          value: "maintenance_fee"
        }
      ],
      mobile_headers: [
        {
          text: `${this.$i18n.t("mobile_number")}`,
          align: "start",
          value: "mobile_number"
        },
        {
          text: `${this.$i18n.t("location")}`,
          align: "start",
          value: "location"
        },
        {
          text: `${this.$i18n.t("item_category")}`,
          align: "start",
          value: "item_category"
        },
        {
          text: `${this.$i18n.t("security_deposit")}`,
          align: "start",
          value: "security_deposit"
        },
        {
          text: `${this.$i18n.t("monthly_fee")}`,
          align: "start",
          value: "monthly_fee"
        }
      ],
      search: "",
      asklistings: [],
      items_length: null,
      page_num: 1,
      pagination: {},
      mobile_breakpoint: 620
    };
  },
  watch: {
    search() {
      if (this.page_num != 1) {
        this.page_num = 1;
        return;
      }
      this.getAskListings();
    }
  },
  methods: {
    getAskListings() {
      let endpoint = `/api/asklistings/?page=${this.page_num}`;
      if (this.search) {
        endpoint += `&location=${this.search}`;
      }
      apiService(endpoint).then((data) => {
        if (data.count != undefined) {
          this.asklistings = data.results;
          this.items_length = data.count;
        } else if (data.count == 0) {
          this.asklistings = [];
        } else {
          applyValidation(data);
        }
      });
    },
    updatePagination(pagination) {
      this.page_num = pagination;
      let endpoint = `/api/asklistings/?page=${this.page_num}`;
      if (this.search) {
        endpoint += `&location=${this.search}`;
      }
      apiService(endpoint).then((data) => {
        if (data != undefined) {
          this.asklistings = data.results;
          this.items_length = data.count;
        } else {
          applyValidation(data);
          this.asklistings = [];
        }
      });
    },
    async deleteAskListing(id) {
      console.log(id);
      let endpoint = `/api/asklistings/${id}/`;
      await apiService(endpoint, "DELETE").then((data) => {
        if (data == undefined) {
          alert(this.$i18n.t("delete_success"));
          this.$delete(
            this.asklistings,
            this.asklistings.findIndex((item) => item.id === id)
          );
        } else {
          applyValidation(data);
        }
      });
    }
  },
  created() {
    this.getAskListings();
  }
};
</script>

<style scoped>
::v-deep .v-data-table > .v-data-table__wrapper > table > tbody > tr > td,
::v-deep .v-data-table > .v-data-table__wrapper > table > tbody > tr > th,
::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > td,
::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th,
::v-deep .v-data-table > .v-data-table__wrapper > table > tfoot > tr > td,
::v-deep .v-data-table > .v-data-table__wrapper > table > tfoot > tr > th {
  padding-left: 8px !important;
  padding-right: 8px !important;
}
</style>
