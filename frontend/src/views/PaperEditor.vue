<template>
  <ValidationObserver ref="obs">
    <v-container class="paper-edit-container">
      <div class="text-caption red--text">{{ $t("paper_subtitle") }}</div>
      <v-row>
        <v-spacer></v-spacer>
        <v-btn dark @click="getPaperList()">
          {{ $t("paper") + " " + $t("load") }}
        </v-btn>
      </v-row>
      <v-progress-linear
        v-if="is_expert"
        :value="percent"
        color="amber"
        height="25"
        fixed
        top
        style="top:62px"
      >
        <strong>{{ Math.ceil(percent) }}%</strong>
      </v-progress-linear>
      <template v-if="step == 1 || validation_check">
        <v-row>
          <v-col id="v-create-paper" cols="12">
            <ValidationProvider
              v-slot="{ errors }"
              ref="title"
              :name="`${$t('title')}`"
              :rules="`required|max:25`"
            >
              <v-text-field
                class="ma-auto"
                v-model="title"
                :error-messages="errors"
                :label="`${$t('paper')} ${$t('title')}`"
                type="String"
                required
                style="max-width:400px"
              ></v-text-field>
            </ValidationProvider>
          </v-col>
        </v-row>
        <v-dialog v-model="load_dialog" height="90%" max-width="90%">
          <v-data-table
            v-if="dialog_category == 'paper'"
            :headers="paper_headers"
            :items="papers"
            item-key="id"
            :server-items-length="items_length"
            @update:page="updatePagination"
            :page="paper_pagination"
          >
            <template v-slot:[`item.trade_category`]="{ item }">
              {{ $getConstI18("TRADE_CATEGORY", item.trade_category) }}
            </template>
            <template v-slot:[`item.select`]="{ item }">
              <v-btn dark @click="loadPaper(item)"> {{ $t("select") }} </v-btn>
            </template>
          </v-data-table>
          <v-card v-else-if="dialog_category == 'profile'" class="pa-2">
            <v-card-text>
              <v-row id="v-profile-input">
                <v-col cols="12" sm="7">
                  <LazyTextField
                    v-model="search.email"
                    :label="$t('email')"
                    @keyup.enter="searchProfile()"
                  ></LazyTextField>
                </v-col>
                <v-col cols="12" sm="5">
                  <LazyTextField
                    v-model="search.mobile_number"
                    :label="$t('mobile_number')"
                    @keyup.enter="searchProfile()"
                  >
                    <template v-slot:append-outer>
                      <v-btn id="v-search" @click="searchProfile()">
                        {{ $t("search") }}
                      </v-btn>
                    </template>
                  </LazyTextField>
                </v-col>
              </v-row>
              <v-data-table
                id="v-profile-select"
                :headers="open_profile_headers"
                :items="searched_profiles"
                item-key="usenrame"
                :server-items-length="items_length"
                @update:page="updatePagination"
                :page="profile_pagination"
              >
                <template v-slot:[`item.select`]="{ item }">
                  <v-btn class="primary" @click="loadProfile(item)">
                    {{ $t("select") }}
                  </v-btn>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-dialog>
        <div id="v-desc-realestate">
          <div class="mt-3">1. {{ $t("desc_realestate") }}</div>
          <v-row>
            <v-col cols="12" sm="8">
              <AddressSearch
                id="v-address"
                ref_name="address"
                :label="$t('address') + $t('search')"
                outlined
                :address.sync="address"
              ></AddressSearch>
            </v-col>
            <v-col cols="6" sm="2">
              <LazyTextField
                v-model="address.dong"
                :label="$t('dong')"
                outlined
                hide-details="auto"
              ></LazyTextField>
            </v-col>
            <span id="v-dong-ho"></span>
            <v-col cols="6" sm="2">
              <LazyTextField
                v-model="address.ho"
                :label="$t('ho')"
                outlined
                hide-details="auto"
              ></LazyTextField>
            </v-col>
            <template v-for="(realestate_field, index) in fields_names.realestate_fields">
              <v-col :id="realestate_field.id" cols="4" md="2" :key="`index` + index">
                <ValidationProvider
                  :ref="realestate_field.name"
                  :name="$t(realestate_field.name)"
                  :rules="`${realestate_field.required != false ? 'required' : ''}`"
                  v-slot="{ errors }"
                >
                  <v-select
                    v-if="realestate_field.type == 'Select'"
                    v-model="$data['' + realestate_field.name]"
                    :error-messages="errors"
                    :items="$getConstList(realestate_field.name + '_LIST')"
                    item-text="text"
                    item-value="value"
                    :label="$t(realestate_field.name)"
                  >
                    <template v-slot:selection="{ item }">{{ $t(item.text) }}</template>
                    <template v-slot:item="{ item }">{{ $t(item.text) }}</template>
                  </v-select>
                  <LazyTextField
                    v-else-if="realestate_field.type == 'Number'"
                    v-model="$data['' + realestate_field.name]"
                    :error-messages="errors"
                    :label="$t(realestate_field.name)"
                    required
                    :type="realestate_field.type"
                    :step="realestate_field.step"
                    suffix="㎡"
                  >
                  </LazyTextField>
                  <LazyTextField
                    v-else
                    v-model="$data['' + realestate_field.name]"
                    :error-messages="errors"
                    :label="$t(realestate_field.name)"
                    :required="realestate_field.required != false"
                    :type="realestate_field.type"
                    :step="realestate_field.step"
                  >
                  </LazyTextField>
                </ValidationProvider>
              </v-col>
            </template>
          </v-row>
        </div>
        <div id="v-terms-and-conditions">
          <div class="mt-3">2. {{ $t("terms_and_conditions") }}</div>
          <div>{{ $t("terms_and_conditions_intro") }}</div>
          <v-row>
            <v-col cols="4" sm="auto">
              <ValidationProvider
                ref="trade_category"
                :name="$t('trade_category')"
                v-slot="{ errors }"
                rules="required"
              >
                <v-select
                  id="v-trade-category"
                  v-model="trade_category"
                  :error-messages="errors"
                  :items="$getConstList('TRADE_CATEGORY_LIST')"
                  item-text="text"
                  item-value="value"
                  :label="$t('trade_category')"
                  style="max-width:150px"
                >
                  <template v-slot:selection="{ item }">{{ $t(item.text) }}</template>
                  <template v-slot:item="{ item }">{{ $t(item.text) }}</template>
                </v-select>
              </ValidationProvider>
            </v-col>
            <v-col cols="8" sm="auto">
              <v-menu
                v-model="period_menu"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <ValidationProvider
                    ref="period"
                    v-slot="{ errors }"
                    rules="required"
                    :name="$t('period')"
                  >
                    <LazyTextField
                      v-model="period"
                      :label="$t('term_of_lease')"
                      prepend-icon="event"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                      :error-messages="errors"
                    ></LazyTextField>
                  </ValidationProvider>
                </template>
                <v-date-picker
                  v-model="period"
                  @change="period_menu = false"
                  :locale="this.$i18n.locale"
                  range
                ></v-date-picker>
              </v-menu>
            </v-col>
            <template v-if="trade_category == $getConstByName('TRADE_CATEGORY', 'rent')">
              <v-col
                v-for="(contract_field, index) in fields_names.contract_fields"
                cols="6"
                sm="auto"
                :key="`index` + index"
              >
                <ValidationProvider
                  v-slot="{ errors }"
                  :ref="contract_field.name"
                  :name="$t(contract_field.name)"
                  :rules="`required|max_value:${contract_field.max_value}`"
                >
                  <LazyTextField
                    v-model="$data['' + contract_field.name]"
                    :error-messages="errors"
                    :label="$t(contract_field.name)"
                    :suffix="$t('won')"
                    :type="contract_field.type"
                    required
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
                      v-model="$data['' + contract_field.name]"
                      :error-messages="errors"
                      :label="$t(contract_field.name) + '(' + $t('won') + ')'"
                      :type="contract_field.type"
                      required
                    ></LazyTextField>
                  </ValidationProvider>
                </v-col>
              </template>
            </template>
          </v-row>
          <p
            v-if="period.length >= 2 && period[0] && period[1]"
            class="my-1"
            v-html="
              $t('terms_and_conditions_period', {
                from_year: period[0].split('-')[0],
                from_month: period[0].split('-')[1],
                from_day: period[0].split('-')[2],
                to_year: period[1].split('-')[0],
                to_month: period[1].split('-')[1],
                to_day: period[1].split('-')[2]
              })
            "
          ></p>
          <p
            v-else
            class="my-1"
            v-html="
              $t('terms_and_conditions_period', {
                from_year: '__',
                from_month: '__',
                from_day: '__',
                to_year: '__',
                to_month: '__',
                to_day: '__'
              })
            "
          ></p>
        </div>
        <div id="v-contract-details" class="pt-4">
          <ValidationProvider
            ref="contract_details"
            v-slot="{ errors }"
            :name="$t('contract_details')"
            rules="required"
          >
            <quill-editor
              class="v-quill-editor"
              ref="myQuillEditor"
              v-model="contract_details"
              :options="editorOption"
              :disabled="quill_disabled"
            />
            <div class="v-messages theme--light error--text" role="alert">
              <div class="v-messages__wrapper">
                <div class="v-messages__message">{{ errors[0] }}</div>
              </div>
            </div>
          </ValidationProvider>
        </div>
        <div id="v-contractor-info">
          <div class="mt-3">3. {{ $t("contractor_info") }}</div>
          <div>{{ $t("contractor_info_intro") }}</div>
        </div>
        <v-radio-group
          id="v-is-landlord"
          v-if="!is_expert"
          v-model="is_landlord"
          row
          @change="is_landlord ? selectLandlordOrTenant(true) : selectLandlordOrTenant(false)"
        >
          <template v-slot:label>
            <div>
              <strong>{{ $t("landlord_or_tenant") }}</strong>
            </div>
          </template>
          <v-row>
            <v-radio :label="this.$t('landlord')" :value="true"></v-radio>
            <v-radio :label="this.$t('tenant')" :value="false"></v-radio>
          </v-row>
        </v-radio-group>
        <v-expansion-panels :value="panels" multiple>
          <v-row no-gutters>
            <v-col cols="12">
              <ValidationProvider ref="seller" v-slot="{ errors }" :name="$t('seller')">
                <v-autocomplete
                  class="mt-2"
                  v-model="seller"
                  clearable
                  :error-messages="errors"
                  :filter="customFilter"
                  :items="allowed_profiles"
                  item-text="name"
                  item-value="id"
                  return-object
                  :label="$t('seller')"
                  :placeholder="$t('quick_trade_user') + ' ' + $t('select')"
                >
                  <template v-slot:selection="{}">{{
                    seller.user.name + "/" + seller.mobile_number
                  }}</template>
                  <template v-slot:item="{ item }">{{
                    item.user.name + "/" + item.mobile_number
                  }}</template>
                  <template v-if="is_expert || !is_landlord" v-slot:append-outer>
                    <v-btn id="v-profile-search" @click.stop="loadSearchDialog('seller')">
                      {{ $t("manual_search") }}
                    </v-btn>
                  </template>
                </v-autocomplete>
              </ValidationProvider>
              <v-expansion-panel v-if="seller">
                <template>
                  <v-expansion-panel-header
                    >{{ $t("seller") }} {{ $t("detail") }} {{ $t("info") }} ({{
                      seller.user.email
                    }})</v-expansion-panel-header
                  >
                  <v-expansion-panel-content>
                    <ContractorItem
                      :profile="seller"
                      :fields="fields_names.basic_profile_fields"
                    ></ContractorItem>
                  </v-expansion-panel-content>
                </template>
              </v-expansion-panel>
            </v-col>
            <v-col class="mt-3" cols="12">
              <ValidationProvider ref="buyer" v-slot="{ errors }" :name="$t('buyer')">
                <v-autocomplete
                  class="mt-2"
                  v-model="buyer"
                  clearable
                  :error-messages="errors"
                  :filter="customFilter"
                  :items="allowed_profiles"
                  item-text="name"
                  item-value="id"
                  return-object
                  :label="$t('buyer')"
                  :placeholder="$t('quick_trade_user') + ' ' + $t('select')"
                >
                  <template v-slot:selection="{}">{{
                    buyer.user.name + " / " + buyer.mobile_number
                  }}</template>
                  <template v-slot:item="{ item }">{{
                    item.user.name + " / " + item.mobile_number
                  }}</template>
                  <template v-if="is_expert || is_landlord" v-slot:append-outer>
                    <v-btn id="v-profile-search" @click.stop="loadSearchDialog('buyer')">
                      {{ $t("manual_search") }}
                    </v-btn>
                  </template>
                </v-autocomplete>
              </ValidationProvider>
              <v-expansion-panel v-if="buyer">
                <template>
                  <v-expansion-panel-header
                    >{{ $t("buyer") }} {{ $t("detail") }} {{ $t("info") }} ({{
                      buyer.user.email
                    }})</v-expansion-panel-header
                  >
                  <v-expansion-panel-content>
                    <ContractorItem
                      :profile="buyer"
                      :fields="fields_names.basic_profile_fields"
                    ></ContractorItem>
                  </v-expansion-panel-content>
                </template>
              </v-expansion-panel>
            </v-col>
            <v-col v-if="is_expert" cols="12">
              <ValidationProvider
                ref="expert"
                v-slot="{ errors }"
                :name="$t('realestate_agency')"
                rules="required"
              >
                <v-autocomplete
                  class="mt-2"
                  v-model="expert"
                  :error-messages="errors"
                  :filter="customFilter"
                  :items="expert_profiles"
                  item-text="name"
                  item-value="id"
                  return-object
                  :label="$t('realestate_agency')"
                  :placeholder="$t('realestate_agency') + ' ' + $t('select')"
                >
                  <template v-slot:selection="{ item }">
                    {{ item.expert_profile.shop_name + ` (#${item.id} / ${item.user.name})` }}
                  </template>
                  <template v-slot:item="{ item }">
                    {{ item.expert_profile.shop_name + ` (#${item.id} / ${item.user.name})` }}
                  </template>
                </v-autocomplete>
              </ValidationProvider>
              <v-expansion-panel v-if="expert">
                <template>
                  <v-expansion-panel-header
                    >{{ $t("realestate_agency") }} {{ $t("detail") }} {{ $t("info") }} ({{
                      expert.user.email
                    }})</v-expansion-panel-header
                  >
                  <v-expansion-panel-content>
                    <ContractorItem
                      :profile="expert"
                      :fields="fields_names.expert_profile_fields"
                    ></ContractorItem>
                  </v-expansion-panel-content>
                </template>
              </v-expansion-panel>
            </v-col>
          </v-row>
        </v-expansion-panels>
      </template>
      <v-divider class="ma-4"></v-divider>
      <!--#FIXME need to support i18n -->
      <template v-if="is_expert && expert">
        <VerifyingExplanationEditor
          ref="verifying_explanation"
          :ve.sync="ve"
          :step="step"
          :validation_check.sync="validation_check"
        >
          <template v-slot:footer>
            <v-row class="mt-4" no-gutters v-if="step == max_step">
              <template v-if="seller">
                <v-col class="contractor-title text-center font-weight-bold" cols="12">
                  <v-card outlined tile color="blue lighten-4">
                    {{ $t("seller") }}
                  </v-card>
                </v-col>
                <v-col cols="12">
                  <ContractorItem
                    :profile="seller"
                    :fields="fields_names.basic_profile_fields"
                  ></ContractorItem>
                </v-col>
              </template>
              <template v-if="buyer">
                <v-col class="contractor-title text-center font-weight-bold" cols="12">
                  <v-card outlined tile color="blue lighten-4">
                    {{ $t("buyer") }}
                  </v-card>
                </v-col>
                <v-col cols="12">
                  <ContractorItem
                    :profile="buyer"
                    :fields="fields_names.basic_profile_fields"
                  ></ContractorItem>
                </v-col>
              </template>
              <v-col class="contractor-title text-center font-weight-bold" cols="12">
                <v-card outlined tile color="blue lighten-4">
                  {{ $t("realestate_agency") }}
                </v-card>
              </v-col>
              <v-col v-if="expert" cols="12">
                <ContractorItem
                  :profile="expert"
                  :fields="fields_names.expert_profile_fields"
                ></ContractorItem>
              </v-col>
            </v-row>
          </template>
          <template
            v-if="expert.expert_profile.insurance.image && step == max_step"
            v-slot:insurance
          >
            <div class="text-center font-weight-bold">
              {{ $t("garantee_insurance") }}
            </div>
            <v-row justify="center">
              <img
                :src="expert.expert_profile.insurance.image"
                aspect-ratio="1"
                style="width:100%"
              />
            </v-row>
          </template>
        </VerifyingExplanationEditor>
        <v-row v-if="expert.expert_profile.insurance.image">
          <v-btn v-if="step != 1" class="mt-3" @click="backStep()">{{ $t("back") }}</v-btn>
          <v-spacer></v-spacer>
          <v-btn
            v-if="step != max_step"
            class="mt-3 float-right white--text"
            color="green"
            @click="nextStep()"
            >{{ $t("next") }}</v-btn
          >
          <v-btn
            v-if="step == max_step"
            class="mt-3 float-right primary white--text"
            @click="submit()"
          >
            {{ $t("submit") }}
          </v-btn>
        </v-row>
        <template v-else>
          <div class="text-right red--text">
            {{ $t("please_available_garantee_insurance") }}
          </div>
          <v-row class="mt-3" justify="end">
            <v-btn
              class="primary"
              dark
              :to="{ name: 'profile-editor', params: { id: expert.id } }"
            >
              {{ `${$t("add_garantee_insurance")}` }}
            </v-btn>
          </v-row>
        </template>
      </template>
      <v-row v-else>
        <v-col cols="12" class="text-right">
          <v-btn id="v-submit" class="primary" @click="submit()">{{ $t("submit") }}</v-btn>
        </v-col>
      </v-row>
      <CustomTour
        name="paper-editor"
        :steps="steps"
        :options="tourOptions"
        :callbacks="tourCallbacks"
      />
    </v-container>
  </ValidationObserver>
</template>

<script>
import { apiService } from "@/common/api_service";
import { applyValidation } from "@/common/common_api";
import ContractorItem from "@/components/ContractorItem";
import VerifyingExplanationEditor from "@/components/VerifyingExplanationEditor";

export default {
  name: "PaperEditor",
  props: {
    id: {
      type: [Number, String],
      required: false
    }
  },
  components: {
    ContractorItem,
    VerifyingExplanationEditor
  },
  computed: {
    percent() {
      return ((this.step - 1) * 100) / (this.max_step - 1);
    },
    steps() {
      return [
        /*The reason , offset is -100 , is scoll up app-bar hide vue-tour box.*/
        {
          target: "#v-create-paper",
          content: `${this.$t("tour_create_paper")}`,
          duration: 10,
          offset: -60
        },
        {
          target: "#v-create-paper",
          content: `${this.$t("tour_create_paper_title")}`,
          duration: 10,
          offset: -60
        },
        {
          target: "#v-desc-realestate",
          content: `${this.$t("tour_desc_relesate")}`,
          duration: 10,
          offset: -60
        },
        {
          target: "#v-address",
          content: `(${this.$t("mandatory")})<br/>${this.$t("tour_paper_address")}`,
          duration: 10,
          offset: -60
        },
        {
          target: "#v-dong-ho",
          content: `(${this.$t("optional")})<br/>${this.$t("tour_paper_dong_ho")}`,
          params: {
            highlight: false
          },
          duration: 10,
          offset: -60
        },
        {
          target: "#v-land-category",
          content: `(${this.$t("mandatory")})<br/>${this.$t("tour_land_category")}`,
          duration: 10,
          offset: -60
        },
        {
          target: "#v-lot-area",
          content: `(${this.$t("mandatory")})<br/>${this.$t("tour_lot_area")}`,
          duration: 10,
          offset: -60
        },
        {
          target: "#v-buildling-structure",
          content: `(${this.$t("mandatory")})<br/>${this.$t("tour_buildling_structure")}`,
          duration: 10,
          offset: -60
        },
        {
          target: "#v-buildling-category",
          content: `(${this.$t("mandatory")})<br/>${this.$t("tour_buildling_category")}`,
          duration: 10,
          offset: -60
        },
        {
          target: "#v-buildling-area",
          content: `(${this.$t("mandatory")})<br/>${this.$t("tour_buildling_area")}`,
          duration: 10,
          offset: -60
        },
        {
          target: "#v-terms-and-conditions",
          content: `(${this.$t("mandatory")})<br/>${this.$t("tour_terms_and_conditions")}`,
          duration: 10,
          offset: -60
        },
        {
          target: "#v-contract-details",
          content: `(${this.$t("mandatory")})<br/>${this.$t("tour_contract_details")}`,
          duration: 10,
          offset: -230,
          params: {
            placement: "top"
          }
        },
        {
          target: "#v-contractor-info",
          content: `(${this.$t("mandatory")})<br/>${this.$t("tour_contractor_info")}`,
          duration: 10,
          offset: -60
        },
        {
          target: "#v-is-landlord",
          content: `${this.$t("tour_select_landlord_tenant")}`,
          duration: 10,
          offset: -60
        },
        {
          target: "#v-profile-search",
          content: `(${this.$t("mandatory")})<br/>${this.$t("tour_profile_search")}`,
          duration: 10,
          offset: -60
        },
        {
          target: "#v-profile-input",
          content: `(${this.$t("mandatory")})<br/>${this.$t("tour_profile_input")}`,
          disabledButtons: {
            buttonNext: true,
            buttonPrevious: true
          }
        },
        {
          target: "#v-profile-select",
          content: `(${this.$t("mandatory")})<br/>${this.$t("tour_profile_select")}`,
          params: {
            enableScrolling: false
          },
          disabledButtons: {
            buttonNext: true
          }
        },
        {
          target: "#v-submit",
          content: `${this.$t("tour_submit")}`,
          offset: -60
        }
      ];
    }
  },
  data() {
    return {
      dialog_category: "paper",
      paper_pagination: 1,
      profile_pagination: 1,
      requestUser: null,
      load_dialog: false,
      isLoading: false,
      is_expert: false,
      papers: [],
      expert_profiles: [],
      allowed_profiles: [],
      validation_check: false,
      step: 1,
      max_step: 4,
      is_landlord: true,
      items_length: 0,
      items_per_page: 2,
      quill_disabled: true,
      period_menu: false,
      from_date_menu: false,
      to_date_menu: false,
      panels: [0, 1, 2],
      title: "",
      land_category: 7,
      lot_area: null,
      building_structure: "",
      building_category: 80,
      building_area: null,
      trade_category: 1,
      address: {
        old_address: null,
        dong: "",
        ho: ""
      },
      down_payment: 0,
      security_deposit: 0,
      maintenance_fee: 0,
      monthly_fee: 0,
      period: [],
      from_date: null,
      to_date: null,
      realestate_category: 0,
      contractors: [],
      expert: null,
      seller: null,
      buyer: null,
      options: [],
      contract_details:
        "<p>제 3조 (<strong>용도변경 및 전대 등</strong>) 임차인은 임대인의 동의없이 위 부동산의 용도나 구조를 변경하거나 전대․임차권 양도 또는 담보제공을 하지 못하며 임대차 목적 이외의 용도로 사용할 수 없다.</p>\
        <p>제 4조 (<strong>계약의 해지</strong>) 임차인이 제3조를 위반하였을 때 임대인은 즉시 본 계약을 해지 할 수 있다.</p>\
        <p>제 5조 (<strong>계약의 종료</strong>) 임대차계약이 종료된 경우에 임차인은 위 부동산을 원상으로 회복하여 임대인에게 반환한다. 이러한 경우 임대인은 보증금을 임차인에게 반환하고, 연체 차임 및 관리비 또는 손해배상금이 있을 때는 이들을 제하고 그 잔액을 반환한다.</p>\
        <p>제 6조 (<strong>계약의 해제</strong>) 임차인이 임대인에게 중도금(중도금이 없을 때는 잔금)을 지불하기 전까지, 임대인은 계약금의 배액을 상환하고, 임차인은 계약금을 포기하고 본 계약을 해제할 수 있다.</p>\
        <p>제 7조 (<strong>채무불이행과 손해배상</strong>) 임대인 또는 임차인이 본 계약상의 내용에 대하여 불이행이 있을 경우 그 상대방은 불이행한 자에 대하여 서면으로 최고하고 계약을 해제 할 수 있다. 그리고 계약 당사자는 계약해제에 따른 손해배상을 각각 상대방에 대하여 청구할 수 있으며, 손해배상에 대하여 별도의 약정이 없는 한 계약금을 손해배상의 기준으로 본다. </p>\
        <p><br/>[<strong>특약사항</strong>]<br/></p>",
      search: {
        email: "",
        mobile_number: ""
      },
      search_contractor_category: null,
      searched_profiles: [],
      ve: {
        paper_categories: [],
        explanation_evidences: [],
        explanation_evidence_info: "",
        address: {
          old_address: "",
          dong: "",
          ho: ""
        },
        land_area: null,
        ledger_land_category: 7,
        actual_land_category: 7,
        net_area: null,
        land_share: "",
        year_of_completion: null,
        ledger_building_category: "주택",
        actual_building_category: "주택",
        building_structure: "",
        building_direction: "남향  (기준:  )",
        seismic_design: "해당사항없음",
        seismic_capacity: "해당사항없음",
        legal_status: true,
        matters_of_violation: "",
        land_ownership: "",
        building_ownership: "",
        land_other: "",
        building_other: "",
        rental_housing_registration: 0,
        rental_housing_registration_info: "",
        mandatory_lease_period: null,
        lease_initiation_date: null,
        right_to_lease_contract_renewal: null,
        use_area: "",
        use_district: "",
        use_zone: "",
        building_coverage_limit: null,
        floor_area_limit: null,
        planning_facilities: "",
        permission_report_zone: "",
        speculative_area: null,
        unit_planning_area_others: "",
        other_use_restriction: "",
        relative_with_roads: "( m × m ) ",
        is_paved_rode: true,
        accessibility: true,
        bus_stop: "",
        bus_by_foot: true,
        bus_required_time: 5,
        subway_station: "",
        subway_by_foot: null,
        subway_required_time: null,
        parking_lot: 0,
        parking_lot_info: "",
        elementary_school: "",
        elementary_school_by_foot: true,
        elementary_school_required_time: 10,
        middle_school: "",
        middle_school_by_foot: true,
        middle_school_required_time: 10,
        high_school: "",
        high_school_by_foot: true,
        high_school_required_time: 10,
        department_store: "",
        department_store_by_foot: false,
        department_store_required_time: 10,
        medical_center: "",
        medical_center_by_foot: false,
        medical_center_required_time: 10,
        is_security_office: false,
        management: 2,
        undesirable_facilities: false,
        undesirable_facilities_info: "",
        expected_transaction_price: null,
        land_prcie_recorded: null,
        building_price_recorded: null,
        acquisition_tax: null,
        special_tax: null,
        local_education_tax: null,
        actual_legal_right_relationship: "",
        water_damage_status: false,
        water_damage_status_info: "",
        water_capacity_status: true,
        water_capacity_status_info: "",
        electricity_supply_status: true,
        electricity_supply_status_info: "",
        gas_supply_status: true,
        gas_supply_status_info: "",
        is_fire_alarm_detector: false,
        fire_alarm_detector_quantity: null,
        heating_supply_method: 2,
        heating_status: true,
        heating_status_info: "",
        heating_type: 0,
        heating_type_info: "",
        is_elevator: false,
        elevator_status: null,
        drainage_status: true,
        drainage_status_info: "",
        other_facilities: "",
        wall_crack_status: false,
        wall_crack_status_info: "",
        water_leak_status: false,
        water_leak_status_info: "",
        wall_paper_status: 1,
        wall_paper_status_info: "",
        sunshine_status: 1,
        sunshine_status_info: "",
        noise_status: 1,
        vibration: 1,
        comission: 0,
        actual_expenses: 0,
        payment_period: "",
        calculation_info:
          "<산출내역> \n\n중개보수: \n실    비: \n※ 중개보수는 시ㆍ도 조례로 정한 요율에 따르거나, 시ㆍ도 조례로 정한 요율한도에서 중개의뢰인과 개업공인중개사가 서로 협의하여 결정하도록 한 요율에 따르며 부가가치세는 별도로 부과될 수 있습니다."
      },
      fields_names: {
        realestate_fields: [
          {
            id: "v-land-category",
            name: "land_category",
            type: "Select"
          },
          {
            id: "v-lot-area",
            name: "lot_area",
            type: "Number",
            step: "0.01"
          },
          {
            id: "v-buildling-structure",
            name: "building_structure",
            type: "String"
          },
          {
            id: "v-buildling-category",
            name: "building_category",
            type: "Select"
          },
          {
            id: "v-buildling-area",
            name: "building_area",
            type: "Number",
            step: "0.01"
          }
        ],
        contract_fields: [
          {
            name: "security_deposit",
            type: "Number",
            max_value: 999999999999
          },
          {
            name: "monthly_fee",
            type: "Number",
            max_value: 999999999
          },
          {
            name: "maintenance_fee",
            type: "Number",
            max_value: 999999999
          },
          {
            name: "down_payment",
            type: "Number",
            max_value: 999999999999
          }
        ],
        basic_profile_fields: [
          {
            name: "address",
            key: "full_address",
            is_computed: true,
            cols: "9",
            md: "10",
            lg: "11"
          },
          { name: "name", key: "user.name", cols: "9", sm: "3", md: "2" },
          {
            name: "birthday",
            key: "user.birthday",
            cols: "9",
            sm: "3",
            md: "2"
          },
          { name: "mobile_number", cols: "9", sm: "3", md: "2" },
          {
            name: "bank_name",
            const_name: "bank_category",
            cols: "9",
            sm: "3",
            md: "2"
          },
          { name: "account_number", cols: "9", sm: "3", md: "2" }
        ],
        expert_profile_fields: [
          {
            name: "registration_number",
            key: "expert_profile.registration_number",
            cols: "9",
            md: "10",
            lg: "4"
          },
          {
            name: "shop_name",
            key: "expert_profile.shop_name",
            cols: "9",
            md: "10",
            lg: "6"
          },
          {
            name: "address",
            key: "full_address",
            is_computed: true,
            cols: "9",
            md: "10",
            lg: "11"
          },
          { name: "name", key: "user.name", cols: "9", sm: "3", md: "2" },
          {
            name: "birthday",
            key: "user.birthday",
            cols: "9",
            sm: "3",
            md: "2"
          },
          { name: "mobile_number", cols: "9", sm: "3", md: "2" },
          {
            name: "bank_name",
            const_name: "bank_category",
            cols: "9",
            sm: "3",
            md: "2"
          },
          { name: "account_number", cols: "9", sm: "3", md: "2" }
        ]
      },
      editorOption: {
        modules: {
          toolbar: {
            container: [
              { size: ["small", false, "large", "huge"] },
              "bold",
              "italic",
              "underline",
              { color: [] },
              { background: [] },
              { align: [] },
              "link"
            ],
            handlers: {
              image: () => {
                let that = this;
                var input = document.createElement("input");
                input.setAttribute("accept", "image/png, image/jpeg, image/bmp");
                input.setAttribute("type", "file");
                input.click();
                input.onchange = () => {
                  const file = input.files[0];
                  const max_size = 1024 * 1024;
                  const max_count = 2;
                  if (/^image\/(jpe?g|png|bmp)$/.test(file.type)) {
                    if (file.size > max_size) {
                      alert(that.$t("image_file_size_error", [max_size / 1024]));
                      return;
                    }
                    const file_count = that.$refs.myQuillEditor.$el.getElementsByTagName("img")
                      .length;
                    if (file_count >= max_count) {
                      alert(that.$t("image_file_count_error", [max_count]));
                      return;
                    }
                    const getBase64 = (file) =>
                      new Promise(function(resolve, reject) {
                        let reader = new FileReader();
                        reader.readAsDataURL(file);
                        reader.onload = () => resolve(reader.result);
                        reader.onerror = (error) => reject("Error: ", error);
                      });
                    const range = that.$refs.myQuillEditor.quill.getSelection();
                    getBase64(file)
                      .then((result) => {
                        let encoded = result;
                        that.$refs.myQuillEditor.quill.insertEmbed(range.index, "image", encoded);
                      })
                      .catch((e) => alert(e));
                  } else {
                    alert(that.$t("image_file_type_error"));
                  }
                };
              }
            }
          }
        },
        placeholder: this.$t("insert_contract_details")
      },
      open_profile_headers: [
        {
          text: `${this.$i18n.t("number")}`,
          value: "id",
          align: "start",
          sortable: true
        },
        {
          text: `${this.$i18n.t("email")}`,
          value: "user.email"
        },
        {
          text: `${this.$i18n.t("name")}`,
          value: "user.name"
        },
        {
          text: `${this.$i18n.t("mobile_number")}`,
          value: "mobile_number"
        },
        {
          text: "",
          value: "select"
        }
      ],
      paper_headers: [
        {
          text: `${this.$i18n.t("number")}`,
          value: "id",
          align: "start",
          sortable: true
        },
        {
          text: `${this.$i18n.t("author")}`,
          value: "author"
        },
        {
          text: `${this.$i18n.t("trade_category")}`,
          value: "trade_category"
        },
        {
          text: `${this.$i18n.t("address")}`,
          value: "address.old_address"
        },
        {
          text: `${this.$i18n.t("dong")}`,
          value: "address.dong"
        },
        {
          text: `${this.$i18n.t("ho")}`,
          value: "address.ho"
        },
        {
          text: "",
          value: "select"
        }
      ],
      tourCallbacks: {
        onPreviousStep: this.previousStepTour,
        onNextStep: this.nextStepTour
      },
      tourOptions: {
        highlight: true,
        stopOnTargetNotFound: false,
        useKeyboardNavigation: false
      },
      tourPreivousStepForDialog: 0
    };
  },
  watch: {
    load_dialog(visible) {
      if (
        this.$store.state.user_setting.is_tour_on &&
        this.$store.state.user_category === "user"
      ) {
        this.tourPreivousStepForDialog = this.$tours["paper-editor"].currentStep;
        if (!visible) {
          this.$tours["paper-editor"].currentStep = this.tourPreivousStepForDialog;
          if (this.dialog_category == "profile") {
            this.$nextTick(() => {
              this.$tours["paper-editor"].currentStep = this.steps.findIndex(
                (item) => item.target == "#v-profile-search"
              );
            });
          }
        }
      }
    }
  },
  methods: {
    backStep() {
      this.validation_check = false;
      this.step -= 1;
    },
    customFilter(item, queryText) {
      const name = item.user.name.toLowerCase();
      const email = item.user.email.toLowerCase();
      const mobile_number = item.mobile_number.toLowerCase();
      const shop_name =
        item.expert_profile == null ? "" : item.expert_profile.shop_name.toLowerCase();
      const searchText = queryText.toLowerCase();

      return (
        name.indexOf(searchText) > -1 ||
        email.indexOf(searchText) > -1 ||
        mobile_number.indexOf(searchText) > -1 ||
        mobile_number.replaceAll("-", "").indexOf(searchText) > -1 ||
        shop_name.indexOf(searchText) > -1
      );
    },
    getAllowedProfiles() {
      let endpoint = `/api/allowed-profiles/`;
      this.isLoading = true;
      return apiService(endpoint).then((data) => {
        if (data.length != undefined) {
          this.allowed_profiles = data;
        } else {
          applyValidation(data);
        }
        this.isLoading = false;
      });
    },
    getExpertProfiles() {
      let endpoint = `/api/expert-profiles/`;
      apiService(endpoint).then((data) => {
        if (data.length != undefined) {
          this.expert_profiles = data;
          this.expert = data[0];
        } else {
          applyValidation(data);
        }
      });
    },
    getPaperList() {
      this.papers = [];
      this.dialog_category = "paper";
      this.load_dialog = true;
      this.isLoading = true;
      let endpoint = `/api/papers/?page=${this.paper_pagination}`;
      apiService(endpoint).then((data) => {
        if (data != undefined) {
          this.items_length = data.count;
          this.papers.push(...data.results);
        }
        this.isLoading = false;
      });
    },
    input_change() {
      this.$delete(this.allowed_profiles);
    },
    loadPaper(item) {
      let that = this;
      let endpoint = `/api/papers/${item.id}/load/`;
      that.quill_disabled = true;
      that.contractors = [];
      that.load_dialog = false;
      apiService(endpoint).then((data) => {
        if (data.id != undefined) {
          for (const contractor_index in data.paper_contractors) {
            var contractor = data.paper_contractors[contractor_index];
            if (contractor.profile.user.email == that.requestUser) {
              that.contractors.push(contractor);
              that.$data[that.$getConst("contractor_category", contractor.group)] =
                contractor.profile;
            }
          }
          that.land_category = data.land_category;
          that.lot_area = data.lot_area;
          that.building_structure = data.building_structure;
          that.building_category = data.building_category;
          that.building_area = data.building_area;
          that.trade_category = data.trade_category;
          that.address = data.address;
          that.deposit = data.deposit;
          that.down_payment = data.down_payment;
          that.security_deposit = data.security_deposit;
          that.maintenance_fee = data.maintenance_fee;
          that.monthly_fee = data.monthly_fee;
          that.period = [];
          that.period.push(data.from_date);
          that.period.push(data.to_date);
          that.realestate_category = data.realestate_category;
          that.contract_details = data.contract_details;
          that.title = data.title;
          if (data.verifying_explanation != null) {
            that.ve = data.verifying_explanation;
          }
          that.$nextTick(() => {
            that.quill_disabled = false;
          });
        } else {
          applyValidation(data);
        }
      });
    },
    loadProfile(item) {
      this[this.search_contractor_category] = item;
      this.load_dialog = false;
    },
    loadSearchDialog(contractor_category) {
      this.load_dialog = true;
      this.search_contractor_category = contractor_category;
      this.dialog_category = "profile";
      this.items_length = 0;
      if (
        this.$store.state.user_setting.is_tour_on &&
        this.$store.state.user_category === "user"
      ) {
        this.$nextTick(() => {
          this.$tours["paper-editor"].currentStep = this.steps.findIndex(
            (item) => item.target == "#v-profile-input"
          );
        });
      }
    },
    nextStep() {
      const that = this;
      this.$refs.verifying_explanation.$refs.form.validate();
      this.$refs.obs.validate().then(function(v) {
        if (v == true) {
          that.step += 1;
        } else {
          that.$vuetify.goTo(that.$el.querySelector(".v-messages.error--text"), { offset: 100 });
        }
      });
    },
    nextStepTour(currentStep) {
      this.$nextTick(() => {
        const tour = this.$tours["paper-editor"];
        const profileSearchIndex = tour.steps.findIndex(
          (item) => item.target == "#v-profile-search"
        );
        if (profileSearchIndex == currentStep) {
          tour.currentStep = tour.steps.findIndex((item) => item.target == "#v-submit");
        }
      });
    },
    previousStepTour(currentStep) {
      this.$nextTick(() => {
        const tour = this.$tours["paper-editor"];
        const submitIndex = tour.steps.findIndex((item) => item.target == "#v-submit");
        if (submitIndex == currentStep) {
          tour.currentStep = tour.steps.findIndex((item) => item.target == "#v-profile-search");
        }
      });
    },
    submit() {
      const that = this;
      // FIXME: This will be used later when we check validation for VerifyingExplanation.
      // this.validation_check = true
      // This code makes reflow. So we need to make anotehr code to check validation.
      console.log("submit");
      this.$refs.obs.validate().then(function(v) {
        if (v == true) {
          let endpoint = "/api/papers/";
          let method = "POST";
          if (that.id !== undefined) {
            endpoint += `${that.id}/`;
            method = "PUT";
          }
          that.updateContractors();
          let data = {
            land_category: that.land_category,
            lot_area: that.lot_area,
            building_structure: that.building_structure,
            building_category: that.building_category,
            building_area: that.building_area,
            trade_category: that.trade_category,
            address: that.address,
            down_payment: that.down_payment,
            security_deposit: that.security_deposit,
            maintenance_fee: that.maintenance_fee,
            monthly_fee: that.monthly_fee,
            from_date: that.period[0],
            title: that.title,
            to_date: that.period[1],
            realestate_category: that.realestate_category,
            paper_contractors: that.contractors,
            options: that.options,
            contract_details: that.contract_details
          };
          if (that.is_expert) {
            data.verifying_explanation = that.ve;
            data.verifying_explanation["insurance"] = that.expert.expert_profile.insurance.id;
          }
          try {
            apiService(endpoint, method, data).then((data) => {
              if (data.id != undefined) {
                alert(that.$i18n.t("request_success"));
                that.$router.push({
                  name: "paper-detail",
                  params: { id: data.id }
                });
              } else {
                var flag = applyValidation(data, that);
                if (!flag) {
                  that.$nextTick(() => {
                    try {
                      that.$vuetify.goTo(that.$el.querySelector(".v-messages.error--text"), {
                        offset: 100
                      });
                      alert(that.$i18n.t("error"));
                      return;
                    } catch (error) {
                      alert(`${that.$i18n.t("error")} : ${JSON.stringify(data)}`);
                    }
                  });
                }
              }
            });
          } catch (err) {
            alert(err);
          }
        } else {
          that.$vuetify.goTo(that.$el.querySelector(".v-messages.error--text"), { offset: 100 });
        }
      });
    },
    searchProfile() {
      let endpoint = `/api/open-profiles/?page=${this.profile_pagination}`;
      Object.entries(this.search).forEach(function(entry) {
        const [key, value] = entry;
        if (value !== "") {
          endpoint += `&${key}=${value}`;
        }
      });
      apiService(endpoint).then((data) => {
        if (!data.count) {
          applyValidation(data);
        } else {
          this.searched_profiles = data.results;
          this.items_length = data.count;
          if (
            this.$store.state.user_setting.is_tour_on &&
            this.$store.state.user_category === "user"
          ) {
            this.$nextTick(() => {
              this.$tours["paper-editor"].currentStep = this.steps.findIndex(
                (item) => item.target == "#v-profile-select"
              );
            });
          }
        }
      });
    },
    remove(item, type) {
      const index = this[type].indexOf(item);
      if (index >= 0) this[type].splice(index, 1);
    },
    updateContractors() {
      const local_contractor_list = ["expert", "seller", "buyer"];
      for (const index in local_contractor_list) {
        let matched = false;
        const local_group_name = local_contractor_list[index];
        const local_group_constant = this.$getConstByName("CONTRACTOR_CATEGORY", local_group_name);

        if (this[local_group_name] != null) {
          for (const index in this.contractors) {
            if (this.contractors[index].group == local_group_constant) {
              this.contractors[index].profile = this[local_group_name].id;
              matched = true;
            }
          }
          if (matched == false) {
            this.contractors.push({
              profile: this[local_group_name].id,
              paper: this.id ? this.id : null,
              group: local_group_constant
            });
          }
        } else {
          for (const index in this.contractors) {
            if (this.contractors[index].group == local_group_constant) {
              this.contractors[index].paper = null;
              this.contractors[index].profile = this.contractors[index].profile.id;
            }
          }
        }
      }
    },
    selectLandlordOrTenant(is_landlord) {
      this.load_dialog = false;
      if (is_landlord) {
        this.is_landlord = true;
        if (this.buyer) {
          this.buyer = this.buyer.user.email == this.requestUser ? null : this.buyer;
        }
        this.seller = this.allowed_profiles.find(
          (profile) => profile.user.email == this.requestUser
        );
      } else {
        this.is_landlord = false;
        if (this.seller) {
          this.seller = this.seller.user.email == this.requestUser ? null : this.seller;
        }
        this.buyer = this.allowed_profiles.find(
          (profile) => profile.user.email == this.requestUser
        );
      }
    },
    updatePagination(pagination) {
      let endpoint = ``;
      if (this.dialog_category == "paper") {
        endpoint = `/api/papers/?page=${pagination}`;
        this.paper_pagination = pagination;
      } else {
        endpoint =
          `/api/open-profiles/?page=${pagination}` +
          `&name=${this.search.name}` +
          `&mobile_number=${this.search.mobile_number}`;
        this.profile_pagination = pagination;
      }

      apiService(endpoint).then((data) => {
        if (data != undefined) {
          if (this.dialog_category == "paper") {
            this.papers = data.results;
          } else {
            this.searched_profiles = data.results;
          }
          this.items_length = data.count;
        } else {
          applyValidation(data);
        }
      });
    }
  },
  async beforeRouteEnter(to, from, next) {
    if (to.params.id !== undefined) {
      let endpoint = `/api/papers/${to.params.id}/`;
      let data = await apiService(endpoint);
      if (data.id) {
        return next((vm) => {
          for (const contractor_index in data.paper_contractors) {
            var contractor = data.paper_contractors[contractor_index];
            if (contractor.group == vm.$getConstByName("CONTRACTOR_CATEGORY", "expert")) {
              vm.expert = contractor.profile;
            } else if (contractor.group == vm.$getConstByName("CONTRACTOR_CATEGORY", "seller")) {
              vm.seller = contractor.profile;
            } else {
              vm.buyer = contractor.profile;
            }
          }
          vm.land_category = data.land_category;
          vm.lot_area = data.lot_area;
          vm.building_structure = data.building_structure;
          vm.building_category = data.building_category;
          vm.building_area = data.building_area;
          vm.trade_category = data.trade_category;
          vm.address = data.address;
          vm.deposit = data.deposit;
          vm.down_payment = data.down_payment;
          vm.security_deposit = data.security_deposit;
          vm.maintenance_fee = data.maintenance_fee;
          vm.monthly_fee = data.monthly_fee;
          vm.period.push(data.from_date);
          vm.period.push(data.to_date);
          vm.from_date = data.from_date;
          vm.title = data.title;
          vm.to_date = data.to_date;
          vm.realestate_category = data.realestate_category;
          vm.contract_details = data.contract_details;
          vm.contractors = data.paper_contractors;
          vm.status = data.status;
          if (data.verifying_explanation != null) {
            vm.ve = data.verifying_explanation;
          }
        });
      } else {
        applyValidation(data);
      }
    } else if (to.params.contract_details !== undefined) {
      return next((vm) => {
        vm.contract_details = to.params.contract_details;
      });
    } else {
      return next();
    }
  },
  created() {
    const that = this;
    document.title = this.$i18n.t("create_paper");
    this.requestUser = this.$store.state.user.email;
    this.is_expert = this.$store.state.user_category == "expert" ? true : false;
    this.getAllowedProfiles().then(() => {
      if (!this.is_expert) {
        that.selectLandlordOrTenant(that.is_landlord);
      }
    });
    if (this.is_expert) {
      this.getExpertProfiles();
    }
    this.$nextTick(() => {
      this.quill_disabled = false;
    });
  },
  destroyed() {
    this.$tours["paper-editor"].stop();
  },
  mounted() {
    if (this.$store.state.user_setting.is_tour_on && this.$store.state.user_category === "user") {
      this.$tours["paper-editor"].start();
    }
  }
};
</script>
<style scoped>
@media (max-width: 960px) {
  .v-progress-linear {
    top: 54px !important;
  }
}
.row > .col,
.row > [class*="col-"] {
  padding-top: 0px;
}
</style>
