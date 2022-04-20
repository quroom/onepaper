<template>
  <div>
    <v-row>
      <v-checkbox
        v-model="obj.online_visit"
        :label="$t('asking_online_visit')"
        width="120px"
      ></v-checkbox>
      <v-col cols="auto">
        <!-- FIXME comment out when support gwangju all location -->
        <LazyTextField
          :label="$t('ask_location')"
          value="광주광역시 북구 중흥동"
          outlined
          disabled
        ></LazyTextField>
        <!-- <ValidationProvider :name="$t('location')" rules="required" v-slot="{ errors }">
          <v-autocomplete
            class="dong"
            v-model="obj.location"
            :items="dongs"
            :loading="isLoading"
            :search-input.sync="search"
            clearable
            hide-selected
            hide-details="auto"
            item-text="name"
            item-value="name"
            :label="$t('location')"
            :placeholder="$t('ask_location')"
            :error-messages="errors"
            solo
            style="min-width:245px"
            :menu-props="menu_position"
          >
            <template v-slot:selection="{ item }">{{ item.name }}</template>
            <template v-slot:item="{ item }">{{ item.name }}</template>
          </v-autocomplete>
        </ValidationProvider> -->
      </v-col>
      <v-menu
        v-model="visit_menu"
        :close-on-content-click="false"
        :nudge-right="40"
        transition="scale-transition"
        offset-y
        min-width="290px"
      >
        <template v-slot:activator="{ on, attrs }">
          <ValidationProvider
            ref="visit_date"
            :name="$t('visit_date')"
            v-slot="{ errors }"
            rules="required"
          >
            <LazyTextField
              class="mt-4"
              v-model="obj.visit_date"
              :error-messages="errors"
              :label="$t('visit_date')"
              prepend-icon="event"
              v-bind="attrs"
              v-on="on"
              readonly
              style="width:150px"
            ></LazyTextField>
          </ValidationProvider>
        </template>
        <v-date-picker
          v-model="obj.visit_date"
          @input="visit_menu = false"
          :locale="this.$i18n.locale"
        ></v-date-picker>
      </v-menu>
      <v-menu
        v-model="moving_menu"
        :close-on-content-click="false"
        :nudge-right="40"
        transition="scale-transition"
        offset-y
        min-width="290px"
      >
        <template v-slot:activator="{ on, attrs }">
          <ValidationProvider
            ref="moving_date"
            :name="$t('moving_date')"
            v-slot="{ errors }"
            rules="required"
          >
            <LazyTextField
              class="mt-4"
              v-model="obj.moving_date"
              :error-messages="errors"
              :label="$t('moving_date')"
              prepend-icon="event"
              v-bind="attrs"
              v-on="on"
              readonly
              style="width:150px"
            ></LazyTextField>
          </ValidationProvider>
        </template>
        <v-date-picker
          v-model="obj.moving_date"
          @input="moving_menu = false"
          :locale="this.$i18n.locale"
        ></v-date-picker>
      </v-menu>
      <v-col cols="4" sm="auto">
        <ValidationProvider
          ref="item_category"
          :name="$t('item_category')"
          v-slot="{ errors }"
          rules="required"
        >
          <v-select
            id="v-item-category"
            v-model="obj.item_category"
            :error-messages="errors"
            :items="$getConstList('ITEM_CATEGORY_LIST')"
            item-text="text"
            item-value="value"
            :label="$t('item_category')"
            style="max-width:150px"
          >
            <template v-slot:selection="{ item }">{{ $t(item.text) }}</template>
            <template v-slot:item="{ item }">{{ $t(item.text) }}</template>
          </v-select>
        </ValidationProvider>
      </v-col>
      <v-col cols="4" sm="auto">
        <ValidationProvider
          ref="trade_category"
          :name="$t('trade_category')"
          v-slot="{ errors }"
          rules="required"
        >
          <v-select
            id="v-trade-category"
            v-model="obj.trade_category"
            :error-messages="errors"
            :items="$getConstList('TRADE_CATEGORY_LIST')"
            item-text="text"
            item-value="value"
            :label="$t('trade_category')"
            style="max-width:120px"
          >
            <template v-slot:selection="{ item }">{{ $t(item.text) }}</template>
            <template v-slot:item="{ item }">{{ $t(item.text) }}</template>
          </v-select>
        </ValidationProvider>
      </v-col>
      <v-col cols="auto">
        <ValidationProvider :name="$t('term_of_lease')" rules="required" v-slot="{ errors }">
          <v-text-field
            v-model="obj.term_of_lease"
            :label="$t('term_of_lease')"
            :placeholder="$t('term_of_lease')"
            :suffix="$t('months')"
            :error-messages="errors"
            style="max-width:120px"
          ></v-text-field>
        </ValidationProvider>
      </v-col>
      <template v-if="obj.trade_category == $getConstByName('TRADE_CATEGORY', 'rent')">
        <v-col
          v-for="(contract_field, index) in fields_names.contract_fields"
          cols="auto"
          :key="`index` + index"
        >
          <ValidationProvider
            v-slot="{ errors }"
            :ref="contract_field.name"
            :name="$t(contract_field.name)"
            :rules="`required|max_value:${contract_field.max_value}`"
          >
            <LazyTextField
              v-model="obj[contract_field.name]"
              :error-messages="errors"
              :label="$t(contract_field.name)"
              :suffix="$t('manwon')"
              :type="contract_field.type"
              required
              style="width:120px;"
            ></LazyTextField>
          </ValidationProvider>
        </v-col>
      </template>
      <template v-else>
        <template v-for="(contract_field, index) in fields_names.contract_fields">
          <v-col
            v-if="contract_field.name != 'monthly_fee'"
            cols="6"
            md="3"
            :key="`index` + index"
          >
            <ValidationProvider
              v-slot="{ errors }"
              :ref="contract_field.name"
              :name="$t(contract_field.name)"
              :rules="`required|max_value:${contract_field.max_value}`"
            >
              <LazyTextField
                :v-model="obj[contract_field.name]"
                :error-messages="errors"
                :label="$t(contract_field.name)"
                :suffix="$t('manwon')"
                :type="contract_field.type"
                required
              ></LazyTextField>
            </ValidationProvider>
          </v-col>
        </template>
      </template>
    </v-row>
    <LazyTextArea
      class="mt-4"
      v-model="obj.content"
      :label="`(${$t('optional')}) ${$t('detail_info')}`"
      :placeholder="$t('ask_listing_detail_info')"
      outlined
      rows="2"
      auto-grow
    ></LazyTextArea>
  </div>
</template>

<script>
import { apiService } from "@/common/api_service";
import { applyValidation } from "@/common/common_api";

export default {
  name: "AskListing",
  props: {
    obj: {
      type: Object,
      required: true
    },
    fields_names: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      visit_menu: false,
      moving_menu: false,
      dongs: [],
      isLoading: false,
      search: null
    };
  },
  watch: {
    search(val) {
      if (!val) {
        return;
      }
      let endpoint = "/api/dongs/";
      // Items have already been loaded
      if (this.dongs.length > 0) return;

      // Items have already been requested
      if (this.isLoading) return;

      this.isLoading = true;
      return apiService(endpoint).then((data) => {
        if (data.length != undefined) {
          this.dongs = data;
        } else {
          applyValidation(data);
        }
        this.isLoading = false;
      });

      // this.fetchEntriesDebounced();
    }
  },
  computed: {
    menu_position() {
      // default properties copied from the vuetify-autocomplete docs
      let defaultProps = {
        closeOnClick: false,
        closeOnContentClick: false,
        disableKeys: true,
        openOnClick: false,
        maxHeight: 304
      };

      if (this.$vuetify.breakpoint.xsOnly) {
        defaultProps.maxHeight = 130;
      }
      return defaultProps;
    }
  },
  // methods: {
  //   fetchEntriesDebounced() {
  //     // cancel pending call
  //     clearTimeout(this._timerId);

  //     // delay new call 500ms
  //     this._timerId = setTimeout(() => {
  //       let endpoint = "/api/dongs/";
  //       // Items have already been loaded
  //       if (this.dongs.length > 0) return;

  //       // Items have already been requested
  //       if (this.isLoading) return;

  //       this.isLoading = true;
  //       return apiService(endpoint).then((data) => {
  //         if (data.length != undefined) {
  //           this.dongs = data;
  //         } else {
  //           applyValidation(data);
  //         }
  //         this.isLoading = false;
  //       });
  //     }, 500);
  //   }
  // },
  created() {
    let endpoint = "/api/dongs/";
    this.isLoading = true;
    return apiService(endpoint).then((data) => {
      if (data.length != undefined) {
        this.dongs = data;
      } else {
        applyValidation(data);
      }
      this.isLoading = false;
    });
  }
};
</script>

<style scoped>
::v-deep .dong .v-select__selections input {
  width: 1px !important;
  min-width: 1px !important;
}
</style>
