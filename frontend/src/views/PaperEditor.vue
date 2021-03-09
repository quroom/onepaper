<template>
  <ValidationObserver ref="obs">
    <v-container>
      <v-row>
        <v-col cols="12" class="text-right">
          <v-btn dark @click="getPaperList()">
            {{ $t("paper") + ' ' + $t("load") }}
          </v-btn>
        </v-col>
      </v-row>
      <div class="mt-4 text-h4 font-weight-bold text-center">{{ `${$t('realestate')} ${$getConstI18('TRADE_CATEGORY', trade_category)} ${$t('contract')}` }}</div>
      <div class="text-caption red--text"> {{ $t("paper_subtitle") }} </div>
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
      <template v-if="step==1 || validation_check">
        <v-dialog v-if="dialog_category=='paper'" v-model="load_dialog" height="90%" max-width="90%">
          <v-data-table
            :headers="paper_headers"
            :items="papers"
            item-key="id"
            :server-items-length="items_length"
            @update:page="updatePagination"
          >
            <template
              v-slot:[`item.trade_category`]="{ item }">
              {{$getConstI18("TRADE_CATEGORY", item.trade_category)}}
            </template>
            <template v-slot:[`item.select`]="{ item }">
              <v-btn dark @click="loadPaper(item)"> {{$t("select")}} </v-btn>
            </template>
          </v-data-table>
        </v-dialog>
        <v-dialog v-else-if="dialog_category=='profile'" v-model="load_dialog" height="90%" max-width="90%">
          <v-card>
            <v-card-text>
                <v-row>
                  <v-col cols="8">
                    <LazyTextField
                      v-model="search.email"
                      :label="$t('email')"
                      @keyup.enter="searchProfile()"
                    ></LazyTextField>
                  </v-col>
                  <v-col cols="4">
                    <LazyTextField
                      v-model="search.mobile_number"
                      :label="$t('mobile_number')"
                      @keyup.enter="searchProfile()"
                    >
                      <template
                        v-slot:append-outer
                      >
                        <v-btn @click="searchProfile()">
                          {{ $t("search") }}
                        </v-btn>
                    </template>
                    </LazyTextField>
                  </v-col>
                </v-row>
                <v-data-table
                  :headers="open_profile_headers"
                  :items="searched_profiles"
                  item-key="usenrame"
                  :server-items-length="items_length"
                  @update:page="updatePagination"
                >
                  <template v-slot:[`item.select`]="{ item }">
                    <v-btn class="primary" @click="loadProfile(item)"> {{$t("select")}} </v-btn>
                  </template>
                </v-data-table>
            </v-card-text>
          </v-card>
        </v-dialog>
        <div class="mt-3">1. {{ $t("desc_realestate") }}</div>
        <v-row>
          <v-col cols="8">
          <AddressSearch
            ref_name="address"
            :label="$t('address') + $t('search')"
            outlined
            :address.sync="address"
          ></AddressSearch>
          </v-col>
          <v-col cols="2">
            <LazyTextField
              v-model="address.dong"
              :label="$t('dong')"
            ></LazyTextField>
          </v-col>
          <v-col cols="2">
            <LazyTextField
              v-model="address.ho"
              :label="$t('ho')"
              hide-details="auto"
            ></LazyTextField>
          </v-col>
        </v-row>
        <v-row>
          <template v-for="(realestate_field, index) in fields_names.realestate_fields">
            <v-col cols="4" md="2" :key="`index`+index">
              <ValidationProvider
                :ref="realestate_field.name"
                :name="$t(realestate_field.name)"
                :rules="`${realestate_field.required != false ? 'required' :''}`"
                v-slot="{ errors }"
              >
                <v-select
                  v-if="realestate_field.type == 'Select'"
                  v-model="$data[''+realestate_field.name]"
                  :error-messages="errors"
                  :items="$getConstList(realestate_field.name+'_LIST')"
                  item-text="text"
                  item-value="value"
                  :label="$t(realestate_field.name)"
                >
                  <template v-slot:selection="{ item }">{{ $t(item.text) }}</template>
                  <template v-slot:item="{ item }">{{ $t(item.text) }}</template>
                </v-select>
                <LazyTextField
                  v-else-if="realestate_field.type=='Number'"
                  v-model="$data[''+realestate_field.name]"
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
                  v-model="$data[''+realestate_field.name]"
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
        <div class="mt-3">2. {{ $t("terms_and_conditions") }}</div>
        <div>{{ $t("terms_and_conditions_intro") }}</div>
        <v-row>
          <v-col cols="2">
            <ValidationProvider ref="trade_category" :name="$t('trade_category')" v-slot="{ errors }" rules="required">
              <v-select
                v-model="trade_category"
                :error-messages="errors"
                :items="$getConstList('TRADE_CATEGORY_LIST')"
                item-text="text"
                item-value="value"
                :label="$t('trade_category')"
              >
                <template v-slot:selection="{ item }">{{ $t(item.text) }}</template>
                <template v-slot:item="{ item }">{{ $t(item.text) }}</template>
              </v-select>
            </ValidationProvider>
          </v-col>
          <v-col cols="5" md="3">
            <v-menu
              v-model="from_date_menu"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              min-width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <ValidationProvider ref="from_date"  :name="$t('from_date')" v-slot="{ errors }" rules="required">
                  <LazyTextField
                    v-model="from_date"
                    :error-messages="errors"
                    :label="$t('from_date')"
                    prepend-icon="event"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                  ></LazyTextField>
                </ValidationProvider>
              </template>
              <v-date-picker
                v-model="from_date"
                @input="from_date_menu=false"
                :locale="this.$i18n.locale"
              ></v-date-picker>
            </v-menu>
          </v-col>
          <v-col cols="5" md="3">
            <v-menu
              v-model="to_date_menu"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              offset-y
              min-width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <ValidationProvider ref="to_date" :name="$t('to_date')" v-slot="{ errors }" rules="required">
                  <LazyTextField
                    v-model="to_date"
                    :error-messages="errors"
                    :label="$t('to_date')"
                    prepend-icon="event"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                  ></LazyTextField>
                </ValidationProvider>
              </template>
              <v-date-picker
                v-model="to_date"
                @input="to_date_menu=false"
                :locale="this.$i18n.locale"
              ></v-date-picker>
            </v-menu>
          </v-col>
        </v-row>
        <v-row>
          <template v-if="trade_category==$getConstByName('TRADE_CATEGORY', 'rent')">
            <v-col v-for="(contract_field, index) in fields_names.contract_fields" cols="6" md="3" :key="`index`+index">
              <ValidationProvider
                v-slot="{ errors }"
                :ref="contract_field.name"
                :name="$t(contract_field.name)"
                :rules="`required|max_value:${contract_field.max_value}`"
              >
                <LazyTextField
                  v-model="$data[''+contract_field.name]"
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
              <v-col v-if="contract_field.name!='monthly_fee'" cols="6" md="3" :key="`index`+index">
                <ValidationProvider
                  v-slot="{ errors }"
                  :ref="contract_field.name"
                  :name="$t(contract_field.name)"
                  :rules="`required|max_value:${contract_field.max_value}`"
                >
                  <LazyTextField
                    v-model="$data[''+contract_field.name]"
                    :error-messages="errors"
                    :label="$t(contract_field.name)+'('+$t('won')+')'"
                    :type="contract_field.type"
                    required
                  ></LazyTextField>
                </ValidationProvider>
              </v-col>
            </template>
          </template>
        </v-row>
        <div class="mt-3">3. {{ $t("contractor_info") }}</div>
        <div>{{ $t("contractor_info_intro") }}</div>
        <v-expansion-panels
          v-model="panels"
          :readonly="true"
          multiple>
          <v-row no-gutters>
            <v-col v-if="!isLoading" cols="12">
              <ValidationProvider
                ref="seller"
                v-slot="{ errors }"
                :name="$t('seller')"
              >
                <v-autocomplete
                  v-model="seller"
                  :error-messages="errors"
                  :filter="customFilter"
                  :items="allowed_profiles"
                  item-text="name"
                  item-value="id"
                  return-object
                  class="mt-2"
                  :label="$t('seller')"
                  :placeholder="$t('quick_trade_user')+' '+$t('select')"
                >
                  <template
                    v-slot:selection="{ }"
                  >{{ seller.user.email + ' (' + seller.user.name + ' / ' + seller.mobile_number + ")" }}</template>
                  <template
                    v-slot:item="{ item }"
                  >{{ item.user.email + ' (' + item.user.name + ' / ' + item.mobile_number + ")" }}</template>
                  <template v-slot:append-outer>
                    <v-btn @click.stop="loadSearchDialog('seller')"> {{ $t("manual_search") }} </v-btn>
                  </template>
                </v-autocomplete>
              </ValidationProvider>
              <v-expansion-panel v-if="seller">
                <v-expansion-panel-header>{{$t("seller")}} {{$t("detail")}} {{$t("info")}} ({{seller.user.email}})</v-expansion-panel-header>
                <v-expansion-panel-content>
                  <ContractorItem :profile="seller" :fields="fields_names.basic_profile_fields"></ContractorItem>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-col>
            <v-col v-if="!isLoading" class="mt-3" cols="12">
              <ValidationProvider
                ref="buyer"
                v-slot="{ errors }"
                :name="$t('buyer')"
              >
                <v-autocomplete
                  v-model="buyer"
                  :error-messages="errors"
                  :filter="customFilter"
                  :items="allowed_profiles"
                  item-text="name"
                  item-value="id"
                  class="mt-2"
                  return-object
                  :label="$t('buyer')"
                  :placeholder="$t('quick_trade_user')+' '+$t('select')"
                >
                  <template v-slot:selection="{ item }"
                  >{{ item.user.email + ' (' + item.user.name + ' / ' + item.mobile_number + ")" }}</template>
                  <template v-slot:item="{ item }"
                  >{{ item.user.email + ' (' + item.user.name + ' / ' + item.mobile_number + ")" }}</template>
                  <template v-slot:append-outer>
                    <v-btn @click.stop="loadSearchDialog('buyer')"> {{ $t("manual_search") }} </v-btn>
                  </template>
                </v-autocomplete>
              </ValidationProvider>
              <v-expansion-panel v-if="buyer">
                <v-expansion-panel-header>{{$t("buyer")}} {{$t("detail")}} {{$t("info")}} ({{buyer.user.email}})</v-expansion-panel-header>
                <v-expansion-panel-content>
                  <ContractorItem :profile="buyer" :fields="fields_names.basic_profile_fields"></ContractorItem>
                </v-expansion-panel-content>
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
                  :placeholder="$t('realestate_agency')+' '+$t('select')"
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
                <v-expansion-panel-header>{{$t("realestate_agency")}} {{$t("detail")}} {{$t("info")}} ({{expert.user.email}})</v-expansion-panel-header>
                <v-expansion-panel-content>
                  <ContractorItem :profile="expert" :fields="fields_names.expert_profile_fields"></ContractorItem>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-col>
          </v-row>
        </v-expansion-panels>
        <div class="mt-3">4. {{ $t("special_agreement") }}</div>
        <ValidationProvider
          ref="special_agreement"
          v-slot="{ errors }"
          :name="$t('special_agreement')"
          rules="required"
        >
          <quill-editor
            ref="myQuillEditor"
            v-model="special_agreement"
            :options="editorOption"
            :disabled="quill_disabled"
          />
          <div class="v-messages theme--light error--text" role="alert">
            <div class="v-messages__wrapper">
              <div class="v-messages__message">{{ errors[0] }}</div>
            </div>
          </div>
        </ValidationProvider>
      </template>
      <v-divider class="ma-4"></v-divider>
      <!--#FIXME need to support i18n -->
      <VerifyingExplanationEditor ref="verifying_explanation" v-if="is_expert" :ve.sync="ve" :step="step" :validation_check.sync="validation_check"></VerifyingExplanationEditor>
      <v-row class="mt-4" no-gutters v-if="step==max_step && is_expert ">
        <template v-if="seller">
          <v-col class="contractor-title text-center font-weight-bold" cols="12">
            <v-card outlined tile color="blue lighten-4">
              {{ $t("seller") }}
            </v-card>
          </v-col>
          <v-col cols="12">
            <ContractorItem :profile="seller" :fields="fields_names.basic_profile_fields"></ContractorItem>
          </v-col>
        </template>
        <template v-if="buyer">
          <v-col class="contractor-title text-center font-weight-bold" cols="12">
            <v-card outlined tile color="blue lighten-4">
              {{ $t("buyer") }}
            </v-card>
          </v-col>
          <v-col cols="12">
            <ContractorItem :profile="buyer" :fields="fields_names.basic_profile_fields"></ContractorItem>
          </v-col>
        </template>
        <v-col class="contractor-title text-center font-weight-bold" cols="12">
          <v-card outlined tile color="blue lighten-4">
            {{ $t("realestate_agency") }}
          </v-card>
        </v-col>
        <v-col v-if="expert" cols="12">
          <ContractorItem :profile="expert" :fields="fields_names.expert_profile_fields"></ContractorItem>
        </v-col>
      </v-row>
      <template v-if="is_expert">
        <v-row>
          <v-btn class="mt-3" style="float:left" v-if="step!=1" dark @click="backStep()">{{$t("back")}}</v-btn>
          <v-spacer></v-spacer>
          <v-btn class="mt-3" style="float:right" color="green" v-if="step!=max_step" dark @click="nextStep()">{{$t("next")}}</v-btn>
          <v-btn v-if="step==max_step" class="mt-3 float_right primary" @click="onSubmit()"> {{$t('submit')}} </v-btn>
        </v-row>
      </template>
      <v-row v-else>
        <v-col cols="12" class="text-right">
          <v-btn class="primary" @click="onSubmit()">{{$t('submit')}}</v-btn>
        </v-col>
      </v-row>
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
      return (this.step-1)*100/(this.max_step-1)
    },
  },
  data() {
    return {
      dialog_category: 'paper',
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
      items_length: 0,
      items_per_page: 2,
      quill_disabled: true,
      from_date_menu: false,
      to_date_menu: false,
      panels: [0,1,2],
      land_category: 7,
      lot_area: null,
      building_structure: '',
      building_category: 80,
      building_area: null,
      trade_category: 0,
      address: {
        old_address: null,
        dong: '',
        ho: '',
      },
      down_payment: 0,
      security_deposit: 0,
      maintenance_fee: 0,
      monthly_fee: 0,
      from_date: null,
      to_date: null,
      realestate_category: 0,
      contractors: [

      ],
      expert: null,
      seller: null,
      buyer: null,
      options: [1,2,3],
      special_agreement: '<p><strong>제1조(입주 전 수리) </strong>임대인과 임차인은 임차주택의 수리가 필요한 시설물 및 비용부담에 관하여 다음과 같이 합의한다.</p><p><strong>제2조(임차주택의 사용·관리·수선) </strong>① 임차인은 임대인의 동의 없이 임차주택의 구조변경 및 전대나 임차권 양도를 할 수 없으며, 임대차 목적인 주거 이외의 용도로 사용할 수 없다.</p><p>② 임대인은 계약 존속 중 임차주택을 사용·수익에 필요한 상태로 유지하여야 하고, 임차인은 임대인이 임차주택의 보존에 필요한 행위를 하는 때 이를 거절하지 못한다.</p><p>③ 임대인과 임차인은 계약 존속 중에 발생하는 임차주택의 수리 및 비용부담에 관하여 다음과 같이 합의한다. 다만, 합의되지 아니한 기타 수선비용에 관한 부담은 민법, 판례 기타 관습에 따른다.</p><p>④ 임차인이 임대인의 부담에 속하는 수선비용을 지출한 때에는 임대인에게 그 상환을 청구할 수 있다.</p><p><strong>제3조(계약의 해제)</strong> 임차인이 임대인에게 중도금(중도금이 없을 때는 잔금)을 지급하기 전까지, 임대인은 계약금의 배액을 상환하고, 임차인은 계약금을 포기하고 이 계약을 해제할 수 있다.</p><p><strong>제4조(채무불이행과 손해배상</strong>) 당사자 일방이 채무를 이행하지 아니하는 때에는 상대방은 상당한 기간을 정하여 그 이행을 최고하고 계약을 해제할 수 있으며, 그로 인한 손해배상을 청구할 수 있다. 다만, 채무자가 미리 이행하지 아니할 의사를 표시한 경우의 계약해제는 최고를 요하지 아니한다.</p><p><strong>제5조(계약의 해지)</strong> ① 임차인은 본인의 과실 없이 임차주택의 일부가 멸실 기타 사유로 인하여 임대차의 목적대로 사용할 수 없는 경우에는 계약을 해지할 수 있다.</p><p>② 임대인은 임차인이 2기의 차임액에 달하도록 연체하거나, 제2조 제1항을 위반한 경우 계약을 해지할 수 있다.</p><p><strong>제6조(계약의 종료) </strong>임대차계약이 종료된 경우에 임차인은 임차주택을 원래의 상태로 복구하여 임대인에게 반환하고, 이와 동시에 임대인은 보증금을 임차인에게 반환하여야 한다. 다만, 시설물의 노후화나 통상 생길 수 있는 파손 등은 임차인의 원상복구의무에 포함되지 아니한다.</p><p><strong>제7조(비용의 정산) </strong>① 임차인은 계약종료 시 공과금과 관리비를 정산하여야 한다.</p><p>② 임차인은 이미 납부한 관리비 중 장기수선충당금을 소유자에게 반환 청구할 수 있다. 다만, 관리사무소 등 관리주체가 장기수선충당금을 정산하는 경우에는 그 관리주체에게 청구할 수 있다.</p><br/>',
      search: {
        email: "",
        mobile_number: ""
      },
      search_contractor_category: null,
      searched_profiles: [],
      ve: {
        paper_categories: [],
        explanation_evidences: [],
        explanation_evidence_info: '',
        address: {
          old_address: '',
          dong: '',
          ho: '',
        },
        land_area: null,
        ledger_land_category: 7,
        actual_land_category: 7,
        net_area: null,
        land_share: '',
        year_of_completion: null,
        ledger_building_category: 80,
        actual_building_category: 80,
        building_structure: '',
        building_direction: '남향  (기준:  )',
        seismic_design: '해당사항없음',
        seismic_capacity: '해당사항없음',
        legal_status: true,
        matters_of_violation: '',
        land_ownership: '',
        building_ownership: '',
        land_other: '',
        building_other: '',
        rental_housing_registration: 0,
        rental_housing_registration_info: '',
        mandatory_lease_period: null,
        lease_initiation_date: null,
        right_to_lease_contract_renewal: null,
        use_area: '',
        use_district: '',
        use_zone: '',
        building_coverage_limit: null,
        floor_area_limit: null,
        planning_facilities: '',
        permission_report_zone: '',
        speculative_area: null,
        unit_planning_area_others: '',
        other_use_restriction: '',
        relative_with_roads: '( m × m ) ',
        is_paved_rode: true,
        accessibility: true,
        bus_stop: '',
        bus_by_foot: true,
        bus_required_time: 5,
        subway_station: '',
        subway_by_foot: null,
        subway_required_time: null,
        parking_lot: 0,
        parking_lot_info: '',
        elementary_school: '',
        elementary_school_by_foot: true,
        elementary_school_required_time: 10,
        middle_school: '',
        middle_school_by_foot: true,
        middle_school_required_time: 10,
        high_school: '',
        high_school_by_foot: true,
        high_school_required_time: 10,
        department_store: '',
        department_store_by_foot: false,
        department_store_required_time: 10,
        medical_center: '',
        medical_center_by_foot: false,
        medical_center_required_time: 10,
        is_security_office: false,
        management: 2,
        undesirable_facilities: false,
        undesirable_facilities_info: '',
        expected_transaction_price: null,
        land_prcie_recorded: null,
        building_price_recorded: null,
        acquisition_tax: null,
        special_tax: null,
        local_education_tax: null,
        actual_legal_right_relationship: '',
        water_damage_status: false,
        water_damage_status_info: '',
        water_capacity_status: true,
        water_capacity_status_info: '',
        electricity_supply_status: true,
        electricity_supply_status_info: '',
        gas_supply_status: true,
        gas_supply_status_info: '',
        is_fire_alarm_detector: false,
        fire_alarm_detector_quantity: null,
        heating_supply_method: 1,
        heating_status: true,
        heating_status_info: '',
        heating_type: 0,
        heating_type_info: '',
        is_elevator: false,
        elevator_status: null,
        drainage_status: true,
        drainage_status_info: '',
        other_facilities: '',
        wall_crack_status: false,
        wall_crack_status_info: '',
        water_leak_status: false,
        water_leak_status_info: '',
        wall_paper_status: 'null',
        wall_paper_status_info: '',
        sunshine_status: 'null',
        sunshine_status_info: '',
        noise_status: 'null',
        vibration: true,
        comission: 0,
        actual_expenses: 0,
        payment_period: '',
        calculation_info: '<산출내역> \n\n중개보수: \n실    비: \n※ 중개보수는 시ㆍ도 조례로 정한 요율에 따르거나, 시ㆍ도 조례로 정한 요율한도에서 중개의뢰인과 개업공인중개사가 서로 협의하여 결정하도록 한 요율에 따르며 부가가치세는 별도로 부과될 수 있습니다.'
      },
      fields_names: {
        realestate_fields: [
          {
            name: "land_category",
            type: "Select"
          },
          { 
            name: "lot_area",
            type: "Number",
            step: "0.01"
          },
          {
            name: "building_structure",
            tyep: "String",
            required: false
          },
          {
            name: "building_category",
            type: "Select"
          },
          {
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
          },
        ],
        basic_profile_fields: [
        { name: "address"
          , key: "address.old_address"
          , cols:"9", md:"10", lg:"11" },
        { name: "name"
          , key: "user.name"
          , cols:"9", sm:"3", md:"2"},
        { name: "birthday"
          , key: "user.birthday"
          , cols:"9", sm:"3", md:"2"}, 
        { name: "mobile_number"
          , cols:"9", sm:"3", md:"2"}, 
        { name: "bank_name",
          const_name: "bank_category"
          , cols:"9", sm:"3", md:"2"}, 
        { name: "account_number"
          , cols:"9", sm:"3", md:"2"}
        ],
        expert_profile_fields: [
        { name: "registration_number"
          , key: "expert_profile.registration_number"
          , cols:"9", md:"10", lg:"4"},
        { name: "shop_name"
          , key: "expert_profile.shop_name"
          , cols:"9", md:"10", lg:"6"},
        { name: "address"
          , key: "address.old_address"
          , cols:"9", md:"10", lg:"11" },
        { name: "name"
          , key: "user.name"
          , cols:"9", sm:"3", md:"2"},
        { name: "birthday"
          , key: "user.birthday"
          , cols:"9", sm:"3", md:"2"}, 
        { name: "mobile_number"
          , cols:"9", sm:"3", md:"2"}, 
        { name: "bank_name",
          const_name: "bank_category"
          , cols:"9", sm:"3", md:"2"}, 
        { name: "account_number"
          , cols:"9", sm:"3", md:"2"}
        ]
      },
      editorOption: {
        modules: {
          toolbar: {
            container: [
              [{ 'size': ['small', false, 'large', 'huge'] }, 'bold', 'underline', ],
              [{'list': 'ordered'}, { 'align': []},],
              ['image', 'link']
            ],
            handlers: {
              'image': () => {
                let that = this;
                var input = document.createElement("input");
                input.setAttribute('accept', 'image/png, image/jpeg, image/bmp');
                input.setAttribute("type", "file");
                input.click();
                input.onchange = () => {
                    const file = input.files[0];
                    const max_size = 1024*1024
                    const max_count = 2
                    if (/^image\/(jpe?g|png|bmp)$/.test(file.type)) {
                      if(file.size > max_size){
                        alert(that.$t("image_file_size_error", [max_size/1024]))
                        return;
                      }
                      const file_count = that.$refs.myQuillEditor.$el.getElementsByTagName("img").length
                      if(file_count >= max_count){
                        alert(that.$t("image_file_count_error", [max_count]))
                        return;
                      }
                      const getBase64 = (file) => new Promise(function (resolve, reject) {
                          let reader = new FileReader();
                          reader.readAsDataURL(file);
                          reader.onload = () => resolve(reader.result)
                          reader.onerror = (error) => reject('Error: ', error);
                      })
                      const range = that.$refs.myQuillEditor.quill.getSelection();
                      getBase64(file).then((result) => {
                        let encoded = result;
                        that.$refs.myQuillEditor.quill.insertEmbed(range.index, "image", encoded);
                      })
                      .catch(e => alert(e))
                    } else {
                      alert(that.$t("image_file_type_error"));
                    }
                };
              }
            }
          }
        },
        placeholder: this.$t("insert_special_agreement")
      },
      open_profile_headers: [
        {
          text: `${this.$i18n.t("number")}`,
          value: "id",
          align: "start",
          sortable: true,
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
      ]
    };
  },
  methods: {
    backStep(){
      this.validation_check = false;
      this.step -=1;
    },
    customFilter(item, queryText) {
      const name = item.user.name.toLowerCase();
      const email = item.user.email.toLowerCase();
      const mobile_number = item.mobile_number.toLowerCase();
      const shop_name = item.expert_profile == null ? "" : item.expert_profile.shop_name.toLowerCase();
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
      apiService(endpoint).then(data => {
        if(data.length != undefined){
            this.allowed_profiles = data;
        } else {
          applyValidation(data)
        }
        this.isLoading = false;
      });
    },
    getExpertProfiles() {
      let endpoint = `/api/expert-profiles/`;
      apiService(endpoint).then(data => {
        if(data.length != undefined){
          this.expert_profiles = data;
        } else {
          applyValidation(data)
        }
      });
    },
    getPaperList() {
      this.papers = [];
      this.dialog_category = 'paper';
      this.load_dialog = true;
      this.isLoading = true;
      let endpoint = `/api/papers/`;
      apiService(endpoint).then(data => {
        if(data != undefined) {
          this.items_length = data.count;
          this.papers.push(...data.results);
        }
        this.isLoading = false;
      })
    },
    input_change() {
      this.$delete(this.allowed_profiles)
    },
    loadPaper(item) {
      let that = this;
      let endpoint = `/api/papers/${item.id}/load/`;
      that.quill_disabled = true;
      that.contractors = []
      that.load_dialog = false;
      apiService(endpoint).then(data => {
        if(data.id != undefined) {
          for(const contractor_index in data.paper_contractors) {
            var contractor = data.paper_contractors[contractor_index]
            if(contractor.profile.user.email==that.requestUser){
              that.contractors.push(contractor)
              that.$data[that.$getConst("contractor_category", contractor.group)]=contractor.profile
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
          that.from_date = data.from_date;
          that.to_date = data.to_date;
          that.realestate_category = data.realestate_category;
          that.special_agreement = data.special_agreement;
          if(data.verifying_explanation != null) {
            that.ve = data.verifying_explanation;
          }
          that.$nextTick(()=>{
            that.quill_disabled = false;
          })
        } else {
          applyValidation(data)
        }
      })
    },
    loadProfile(item) {
      this[this.search_contractor_category] = item;
      this.load_dialog = false;
    },
    loadSearchDialog(contractor_category){
      this.search_contractor_category = contractor_category;
      this.dialog_category = 'profile';
      this.load_dialog = true;
      this.items_length = 0;
    },
    nextStep(){
      const that = this;
      this.$refs.verifying_explanation.$refs.form.validate()
      this.$refs.obs.validate().then(function(v) {
        if (v == true) {
          that.step +=1;
        } else {
          that.$vuetify.goTo(that.$el.querySelector(".v-messages.error--text"), {offset:100})
        }
      })
    },
    onSubmit() {
      const that = this;
      // FIXME: This will be used later when we check validation for VerifyingExplanation.
      // this.validation_check = true
      // This code makes reflow. So we need to make anotehr code to check validation.
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
            from_date: that.from_date,
            to_date: that.to_date,
            title: that.title,
            realestate_category: that.realestate_category,
            paper_contractors: that.contractors,
            options: that.options,
            special_agreement: that.special_agreement,
          }
            if(that.is_expert){
              data.verifying_explanation = that.ve;
            }
          try {
            apiService(endpoint, method, data).then(data => {
              if (data.id != undefined) {
                alert(that.$i18n.t("request_success"))
                that.$router.push({
                  name: "paper-detail",
                  params: { id: data.id }
                });
              } else {
                var flag = applyValidation(data, that);
                if(!flag){
                  that.$nextTick(() => {
                    try {
                      that.$vuetify.goTo(that.$el.querySelector(".v-messages.error--text"), {offset:100})
                      alert(that.$i18n.t("error"))
                      return;
                    } catch (error) {
                      alert(`${that.$i18n.t("error")} : ${JSON.stringify(data)}`)
                    }
                  });
                }
              }
            });
          } catch (err) {
            alert(err);
          }
        }
      });
    },
    searchProfile(){
      let endpoint = "/api/open-profiles/"
      let is_first_option = false;
      Object.entries(this.search).forEach(function(entry){
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
      apiService(endpoint).then(data => {
        if(!data.count){
          applyValidation(data)
        } else {
          this.searched_profiles = data.results;
          this.items_length = data.count;
        }
      })
    },
    remove (item, type) {
      const index = this[type].indexOf(item)
      if (index >= 0) this[type].splice(index, 1)
    },
    updateContractors(){
      const local_contractor_list = ["expert", "seller", "buyer"]
      for(const index in local_contractor_list){
        let matched = false;
        const local_group_name = local_contractor_list[index]
        const local_group_constant = this.$getConstByName("CONTRACTOR_CATEGORY", local_group_name)

        if(this[local_group_name] != null){
          for(const index in this.contractors){
            if(this.contractors[index].group == local_group_constant){
              this.contractors[index].profile = this[local_group_name].id;
              matched = true;
            }
          }
          if(matched == false){
            this.contractors.push({
              "profile": this[local_group_name].id, "paper":this.id ? this.id : null, "group": local_group_constant
            })
          }
        } else {
          for(const index in this.contractors){
            if(this.contractors[index].group == local_group_constant){
              this.contractors[index].paper = null;
              this.contractors[index].profile = this.contractors[index].profile.id
            }
          }
        }
      }
    },
    updatePagination (pagination) {
      let endpoint = `/api/papers/?page=${pagination}`
      if(this.dialog_category == 'profile'){
        endpoint = `/api/open-profiles/?page=${pagination}`+`&name=${this.search.name}`+`&mobile_number=${this.search.mobile_number}`
      }

      apiService(endpoint).then(data => {
        if(data != undefined) {
          if (this.dialog_category == 'paper') {
            this.papers = data.results;
          } else {
            this.searched_profiles = data.results;
          }
          this.items_length = data.count;
        } else {
          applyValidation(data)
        }
      })
    }
  },
  async beforeRouteEnter(to, from, next) {
    if (to.params.id !== undefined) {
      let endpoint = `/api/papers/${to.params.id}/`;
      let data = await apiService(endpoint);
      if(data.id) {
        return next(
          vm => {
            for(const contractor_index in data.paper_contractors) {
              var contractor = data.paper_contractors[contractor_index]
              if(contractor.group==vm.$getConstByName("CONTRACTOR_CATEGORY", "expert")){
                vm.expert = contractor.profile;
              }else if(contractor.group==vm.$getConstByName("CONTRACTOR_CATEGORY", "seller")){
                vm.seller = contractor.profile;
              }else {
                vm.buyer = contractor.profile
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
            vm.from_date = data.from_date;
            vm.to_date = data.to_date;
            vm.realestate_category = data.realestate_category;
            vm.special_agreement = data.special_agreement;
            vm.contractors = data.paper_contractors;
            vm.status = data.status;
            if(data.verifying_explanation != null) {
              vm.ve = data.verifying_explanation;
            }
          }
        );
      } else {
        applyValidation(data)
      }
    } else {
      return next();
    }
  },
  created() {
    document.title = this.$i18n.t("create_paper");
    this.requestUser = window.localStorage.getItem("email");
    this.getAllowedProfiles();
    this.is_expert = window.localStorage.getItem("user_category") == "expert" ? true : false;
    if(this.is_expert){
      this.getExpertProfiles();
    }
    this.$nextTick(()=>{
      this.quill_disabled=false;
    })
  }
};
</script>
<style scoped>
</style>