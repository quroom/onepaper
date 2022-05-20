<template>
  <v-container>
    <v-row justify="center" no-gutters>
      <v-radio-group hide-details="auto" row v-model="is_ask_move_in" @change="updatePage">
        <v-radio :label="$t('ask_move_in')" :value="true"></v-radio>
        <v-radio :label="$t('ask')" :value="false"></v-radio>
      </v-radio-group>
    </v-row>
    <LazyTextField
      v-if="is_expert"
      v-model="search"
      append-icon="mdi-magnify"
      hide-details="auto"
      :label="`${$t('location')}`"
      prepend-icon="search"
    ></LazyTextField>
    <v-data-table
      v-if="is_ask_move_in"
      :headers="ask_move_in_headers"
      :items="listingvisits"
      item-key="id"
      :server-items-length="items_length"
      :page.sync="page_num"
      @update:page="updatePagination"
      :disable-sort="true"
      :footer-props="{
        'items-per-page-options': [10]
      }"
    >
      <template #[`footer.prepend`]>
        <v-spacer />
      </template>
      <template v-for="header in ask_move_in_headers" v-slot:[`item.${header.value}`]="{ item }">
        <template v-if="header.value == 'title'">
          {{ item.listing.title }}
        </template>
        <template v-if="header.value == 'room_name'">
          {{ item.listing_item ? item.listing_item.room_name : "-" }}
        </template>

        <template v-else-if="header.value == 'number'">
          <router-link
            :key="header.value"
            :to="{
              name: 'listing-detail',
              params: { id: item.listing.id }
            }"
            >{{ item.listing.id }}
          </router-link>
        </template>
        <template v-else-if="['trade_category', 'item_category'].includes(header.value)">
          {{ $getConstI18(header.value, item.listing[header.value]) }}
        </template>
        <template v-else-if="['security_deposit', 'maintenance_fee'].includes(header.value)">
          {{ item.listing_item ? item.listing_item[header.value] : item.listing[header.value] }}
        </template>
        <template v-else-if="header.value == 'monthly_fee'">
          <template
            v-if="item.listing.trade_category == $getConstByName('trade_category', 'rent')"
          >
            {{
              item.listing_item ? item.listing_item[header.value] : item.listing[header.value]
            }}</template
          >
          <template v-else>-</template>
        </template>
        <template v-else>
          {{ item[header.value] }}
        </template>
      </template>
    </v-data-table>
    <v-data-table
      v-else
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
      :disable-items-per-page="true"
      :footer-props="{
        'items-per-page-options': [10]
      }"
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
      <template v-slot:expanded-item="{ item }">
        <td class="px-0" :colspan="headers.length">
          <v-row>
            <DeleteAlert
              v-if="$store.state.user.email === item.author"
              :id="item.id"
              :callback="deleteAskListing"
          /></v-row>
          <v-divider class="my-1"></v-divider>
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
              <v-card v-else-if="'online_visit' === key" outlined tile class="pa-1">
                {{ item[key] == true ? "O" : "X" }}
              </v-card>
              <v-card v-else outlined tile class="pa-1">{{ value }}</v-card>
            </v-col>
          </v-row>
        </td>
      </template>
      <template #[`footer.prepend`]>
        <v-spacer />
      </template>
    </v-data-table>
    <v-row v-if="!is_ask_move_in">
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
      ask_move_in_headers: [
        {
          text: `${this.$i18n.t("listing_title")}`,
          align: "start",
          value: "title"
        },
        {
          text: `${this.$i18n.t("number")}`,
          align: "start",
          value: "number"
        },
        {
          text: `${this.$i18n.t("mobile_number")}`,
          align: "start",
          value: "mobile_number"
        },
        {
          text: `${this.$i18n.t("room_name")}`,
          align: "start",
          value: "room_name"
        },
        {
          text: `${this.$i18n.t("item_category")}`,
          align: "start",
          value: "item_category"
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
      is_ask_move_in: true,
      search: "",
      asklistings: [],
      listingvisits: [],
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
      if (this.is_ask_move_in) {
        this.getListingVisits();
      } else {
        this.getAskListings();
      }
    }
  },
  methods: {
    updatePage() {
      this.search = "";
      this.page_num = 1;
      if (this.is_ask_move_in) {
        this.getListingVisits();
      } else {
        this.getAskListings();
      }
    },
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
    getListingVisits() {
      let endpoint = `/api/listingvisits/?page=${this.page_num}`;
      if (this.search) {
        endpoint += `&location=${this.search}`;
      }
      apiService(endpoint).then((data) => {
        if (data.count != undefined) {
          this.listingvisits = data.results;
          this.items_length = data.count;
        } else if (data.count == 0) {
          this.listingvisits = [];
        } else {
          applyValidation(data);
        }
      });
    },
    updatePagination(pagination) {
      this.page_num = pagination;
      let endpoint = `/api/asklistings/?page=${this.page_num}`;

      if (this.is_ask_move_in) {
        endpoint = `/api/listingvisits/?page=${this.page_num}`;
      }
      if (this.search) {
        endpoint += `&location=${this.search}`;
      }
      apiService(endpoint).then((data) => {
        if (data != undefined) {
          if (this.is_ask_move_in) {
            this.listingvisits = data.results;
          } else {
            this.asklistings = data.results;
          }
          this.items_length = data.count;
        } else {
          applyValidation(data);
          this.asklistings = [];
          this.listingvisits = [];
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
    if (this.is_ask_move_in) {
      this.getListingVisits();
    } else {
      this.getAskListings();
    }
    this.is_expert = this.$store.state.user_category == "expert" ? true : false;
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
::v-deep .v-data-table__mobile-row {
  min-height: 24px !important;
}
</style>
