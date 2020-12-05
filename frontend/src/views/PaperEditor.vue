<!-- eslint-disable -->
<template>
  <ValidationObserver ref="obs">
    <v-container>
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
        <v-dialog v-model="paper_load_dialog" height="90%" max-width="90%">
          <v-data-table
            v-model="selected_paper"
            :headers="paper_headers"
            :items="papers"
            item-key="id"
          >
            <template
              v-slot:[`item.trade_category`]="{ item }">
              {{$getConstI18("TRADE_CATEGORY", item.trade_category)}}
            </template>
            <template v-slot:[`item.select`]="{ item }">
              <v-btn class="primary" @click="loadPaper(item)"> {{$t("select")}} </v-btn>
            </template>
          </v-data-table>
        </v-dialog>
        <v-btn class="success float_right" @click="getPaperList()">
          {{ $t("paper") + ' ' + $t("load") }}
        </v-btn>
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
                rules="required"
                v-slot="{ errors }"
              >
                <v-select
                  v-if="realestate_field.type=='select'"
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
                  v-else
                  v-model="$data[''+realestate_field.name]"
                  :error-messages="errors"
                  :label="$t(realestate_field.name)"
                  required
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
                rules="required"
              >
                <LazyTextField
                  v-model="$data[''+contract_field.name]"
                  :error-messages="errors"
                  :label="$t(contract_field.name)+'('+$t('manwon')+')'"
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
                  rules="required"
                >
                  <LazyTextField
                    v-model="$data[''+contract_field.name]"
                    :error-messages="errors"
                    :label="$t(contract_field.name)+'('+$t('manwon')+')'"
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
        <v-expansion-panels>
          <v-row no-gutters>
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
                  :items="my_profiles"
                  item-text="name"
                  item-value="id"
                  return-object
                  :label="$t('realestate_agency')"
                  :placeholder="$t('realestate_agency')+' '+$t('search')"
                >
                  <template v-slot:selection="{ item }">
                    {{ item.expert_profile.shop_name + ':' + item.user.name}}
                  </template>
                  <template v-slot:item="{ item }">
                    {{ item.expert_profile.shop_name + ':' + item.user.name}}
                  </template>
                </v-autocomplete>
              </ValidationProvider>
              <v-expansion-panel v-if="expert">
                <v-expansion-panel-header>{{$t("realestate_agency")}} {{$t("detail")}} {{$t("info")}}</v-expansion-panel-header>
                <v-expansion-panel-content>
                  <Contractor :contractor="expert" :fields="fields_names.expert_profile_fields"></Contractor>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-col>
            <v-col v-if="!isLoading" cols="12">
              <ValidationProvider
                ref="seller"
                v-slot="{ errors }"
                :name="$t('landlord')"
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
                  :label="$t('landlord')"
                  :placeholder="$t('landlord')+' '+$t('search')"
                >
                  <template
                    v-slot:selection="{ item }"
                  >{{ item.user.username + '(' + item.user.name + ' / ' + item.user.birthday +")" }}</template>
                  <template
                    v-slot:item="{ item }"
                  >{{ item.user.username + '(' + item.user.name + ' / ' + item.user.birthday +")" }}</template>
                </v-autocomplete>
              </ValidationProvider>
              <v-expansion-panel v-if="seller">
                <v-expansion-panel-header>{{$t("landlord")}} {{$t("detail")}} {{$t("info")}}</v-expansion-panel-header>
                <v-expansion-panel-content>
                  <Contractor :contractor="seller" :fields="fields_names.basic_profile_fields"></Contractor>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-col>
            <v-col v-if="!isLoading" class="mt-3" cols="12">
              <ValidationProvider
                ref="buyer"
                v-slot="{ errors }"
                :name="$t('tenant')"
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
                  :label="$t('tenant')"
                  :placeholder="$t('tenant')+' '+$t('search')"
                >
                  <template
                    v-slot:selection="{ item }"
                  >{{ item.user.username + '(' + item.user.name + ' / ' + item.user.birthday +")" }}</template>
                  <template
                    v-slot:item="{ item }"
                  >{{ item.user.username + '(' + item.user.name + ' / ' + item.user.birthday +")" }}</template>
                </v-autocomplete>
              </ValidationProvider>
              <v-expansion-panel v-if="buyer">
                <v-expansion-panel-header>{{$t("tenant")}} {{$t("detail")}} {{$t("info")}}</v-expansion-panel-header>
                <v-expansion-panel-content>
                  <Contractor :contractor="buyer" :fields="fields_names.basic_profile_fields"></Contractor>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-col>
          </v-row>
        </v-expansion-panels>
        <div class="mt-3">4. {{ $t("special_agreement") }}</div>
        <quill-editor
          ref="myQuillEditor"
          v-model="special_agreement"
          :options="editorOption"
        />
      </template>
      <v-divider class="ma-4"></v-divider>
      <!-- need to support i18n -->
      <VerifyingExplanationEditor ref="verifying_explanation" v-if="is_expert" :ve.sync="ve" :step="step" :validation_check.sync="validation_check"></VerifyingExplanationEditor>
      <v-row class="mt-4" no-gutters v-if="step==max_step && is_expert ">
        <v-col class="contractor-title text-center font-weight-bold" cols="12">
          <v-card outlined tile color="blue lighten-4">
            {{ $t("realestate_agency") }}
          </v-card>
        </v-col>
        <v-col v-if="expert" cols="12">
          <Contractor :contractor="expert" :fields="fields_names.expert_profile_fields"></Contractor>
        </v-col>
        <template v-if="seller">
          <v-col class="contractor-title text-center font-weight-bold" cols="12">
            <v-card outlined tile color="blue lighten-4">
              {{ $t("landlord") }}
            </v-card>
          </v-col>
          <v-col cols="12">
            <Contractor :contractor="seller" :fields="fields_names.basic_profile_fields"></Contractor>
          </v-col>
        </template>
        <template v-if="buyer">
          <v-col class="contractor-title text-center font-weight-bold" cols="12">
            <v-card outlined tile color="blue lighten-4">
              {{ $t("tenant") }}
            </v-card>
          </v-col>
          <v-col cols="12">
            <Contractor :contractor="buyer" :fields="fields_names.basic_profile_fields"></Contractor>
          </v-col>
        </template>
      </v-row>
      <template v-if="is_expert">
        <v-btn class="mt-3" style="float:left" v-if="step!=1" dark @click="backStep()">{{$t("back")}}</v-btn>
        <v-spacer></v-spacer>
        <v-btn class="mt-3" style="float:right" color="green" v-if="step!=max_step" dark @click="nextStep()">{{$t("next")}}</v-btn>
        <v-btn v-if="step==max_step" class="mt-3 float_right primary" @click="onSubmit()">{{$t('submit')}}</v-btn>
      </template>
      <v-btn v-else class="mt-3 float_right primary" @click="onSubmit()">{{$t('submit')}}</v-btn>
    </v-container>
  </ValidationObserver>
</template>

<script>
import { apiService } from "@/common/api.service";
import { applyValidation } from "@/common/common_api";
import AddressSearch from "@/components/AddressSearch";
import Contractor from "@/components/Contractor";
import VerifyingExplanationEditor from "@/components/VerifyingExplanationEditor";
import 'quill/dist/quill.core.css';
import 'quill/dist/quill.snow.css';
import 'quill/dist/quill.bubble.css';
import { quillEditor } from 'vue-quill-editor';

export default {
  name: "PaperEditor",
  props: {
    id: {
      type: [Number, String],
      required: false
    }
  },
  components: {
    AddressSearch,
    Contractor,
    quillEditor,
    VerifyingExplanationEditor
  },
  computed: {
    percent() {
      return (this.step-1)*100/(this.max_step-1)
    }
  },
  data() {
    return {
      requestUser: null,
      paper_load_dialog: false,
      papers: [],
      selected_paper: [],
      isLoading: false,
      is_expert: false,
      my_profiles: [],
      allowed_profiles: [],
      validation_check: false,
      step:1,
      max_step:4,
      fields_names: {
        realestate_fields: [
          {
            name: "land_category",
            type: "select"
          },
          { 
            name: "lot_area",
            type: "Number",
            step: "0.01"
          },
          {
            name: "building_structure",
            tyep: "String"
          },
          {
            name: "building_category",
            type: "select"
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
            type: "Number"
          },
          {
            name: "monthly_fee",
            type: "Number"
          },
          {
            name: "maintenance_fee",
            type: "Number"
          },
          {
            name: "down_payment",
            type: "Number"
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
        { name: "bank_name"
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
        { name: "bank_name"
          , cols:"9", sm:"3", md:"2"}, 
        { name: "account_number"
          , cols:"9", sm:"3", md:"2"}
        ]
      },
      from_date_menu: false,
      to_date_menu: false,
      land_category: 7,
      lot_area: null,
      building_structure: null,
      building_category: 80,
      building_area: null,
      trade_category: null,
      address: {
        old_address: null,
        dong: '',
        ho: '',
      },
      down_payment: null,
      security_deposit: null,
      maintenance_fee: null,
      monthly_fee: null,
      from_date: null,
      to_date: null,
      realestate_category: 0,
      contractors: [

      ],
      expert: null,
      seller: null,
      buyer: null,
      options: [0,1,2],
      special_agreement: null,
      ve: {
        paper_categories: [],
        explanation_evidences: [],
        explanation_evidence_info: '',
        address: {
          old_address: null,
          dong: '',
          ho: '',
        },
        land_area: 0,
        land_category: 7,
        actual_land_category: 7,
        net_area: 0,
        land_share: '',
        year_of_completion: 1995,
        building_category: 80,
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
        rental_housing_registration: 3,
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
        relative_with_roads: '(  m  ×  m )',
        is_paved_rode: true,
        accessibility: true,
        bus_stop: "",
        bus_by_foot: true,
        bus_time_required: 5,
        subway_station: "",
        subway_by_foot: null,
        subway_time_required: null,
        parking_lot: 0,
        parking_lot_info: '',
        elementary_school: '',
        elementary_school_by_foot: true,
        elementary_school_time_required: 10,
        middle_school: '',
        middle_school_by_foot: true,
        middle_school_time_required: 10,
        high_school: '',
        high_school_by_foot: true,
        high_school_time_required: 10,
        department_store: '',
        department_store_by_foot: false,
        department_store_time_required: 10,
        medical_center: '',
        medical_center_by_foot: false,
        medical_center_time_required: 10,
        is_security_office: false,
        management: 1,
        undesirable_facilities: false,
        undesirable_facilities_info: '',
        expected_transaction_price: null,
        land_prcie_recorded: null,
        building_price_recorded: null,
        acquisition_tax: null,
        special_tax: null,
        local_education_tax: null,
        water_damage_status: true,
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
        wall_crack_status: true,
        wall_crack_status_info: '',
        water_leak_status: true,
        water_leak_status_info: '',
        wall_paper_status: 'null',
        wall_paper_status_info: '',
        sunshine_status: 'null',
        sunshine_status_info: '',
        noise_status: 'null',
        vibration: true,
        comission: 2000000,
        actual_expenses: 50000,
        payment_period: '',
        calculation_info: '<산출내역> \n\n중개보수: \n실    비: \n※ 중개보수는 시ㆍ도 조례로 정한 요율에 따르거나, 시ㆍ도 조례로 정한 요율한도에서 중개의뢰인과 개업공인중개사가 서로 협의하여 결정하도록 한 요율에 따르며 부가가치세는 별도로 부과될 수 있습니다.'
      },
      editorOption: {
        modules: {
          toolbar: {
            container: [
              ['bold', 'underline', {'list': 'ordered'}, { 'size': ['small', false, 'large', 'huge'] }],
              ['image', 'link', 'video']
            ],
            handlers: {
              'image': () => {
                let self = this;
                var input = document.createElement("input");
                input.setAttribute("type", "file");
                input.click();
                input.onchange = () => {
                    const file = input.files[0];
                    if(file.size > 512000){
                      alert(self.$t("image_file_size_error"))
                      return;
                    }
                    const file_count = self.$refs.myQuillEditor.$el.getElementsByTagName("img").length
                    if(file_count >= 2){
                      alert(self.$t("image_file_count_error"))
                      return;
                    }
                    if (/^image\//.test(file.type)) {
                        const getBase64 = (file) => new Promise(function (resolve, reject) {
                            let reader = new FileReader();
                            reader.readAsDataURL(file);
                            reader.onload = () => resolve(reader.result)
                            reader.onerror = (error) => reject('Error: ', error);
                        })

                        const range = self.$refs.myQuillEditor.quill.getSelection();
                        getBase64(file).then((result) => {
                          let encoded = result;
                          self.$refs.myQuillEditor.quill.insertEmbed(range.index, "image", encoded);
                        })
                        .catch(e => alert(e))
                        
                    } else {
                        alert(self.$t("image_file_type_error"));
                    }
                };
              }
            }
          }
        },
        placeholder: this.$t("insert_special_agreement")
      },
      paper_headers: [
        {
          text: "",
          value: "id",
          align: "start",
          sortable: true,
          visibility: "hidden"
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
    remove (item, type) {
      const index = this[type].indexOf(item)
      if (index >= 0) this[type].splice(index, 1)
    },
    getAllowedProfiles() {
      let endpoint = `/api/allowed-profiles/`;
      this.isLoading = true;
      apiService(endpoint).then(data => {
        this.allowed_profiles = data;
        this.isLoading = false;
      });
    },
    getMyProfiles() {
      let endpoint = `/api/profiles/`;
      apiService(endpoint).then(data => {
        this.my_profiles = data;
        this.is_expert = true;
      });
    },
    getPaperList() {
      this.papers = [];
      this.paper_load_dialog = true;
      this.isLoading = true;
      let endpoint = `/api/paper-list/`;
      apiService(endpoint).then(data => {
        this.papers.push(...data.results);
        this.isLoading = false;
      })
    },
    loadPaper(item) {
      let self = this;
      let endpoint = `/api/papers/${item.id}/`;
      self.contractors = []
      apiService(endpoint).then(data => {
        for(const contractor_index in data.paper_contractors) {
          var contractor = data.paper_contractors[contractor_index]
          console.log(contractor.profile.user.username)
          console.log(self.requestUser)
          if(contractor.profile.user.username==self.requestUser){
            self.contractors.push(contractor)
            self.$data[self.$getConst("contractor_category", contractor.group)]=contractor.profile
          }
        }
        self.land_category = data.land_category;
        self.lot_area = data.lot_area;
        self.building_structure = data.building_structure;
        self.building_category = data.building_category;
        self.building_area = data.building_area;
        self.trade_category = data.trade_category;
        self.address = data.address;
        self.deposit = data.deposit;
        self.down_payment = data.down_payment;
        self.security_deposit = data.security_deposit;
        self.maintenance_fee = data.maintenance_fee;
        self.monthly_fee = data.monthly_fee;
        self.from_date = data.from_date;
        self.to_date = data.to_date;
        self.realestate_category = data.realestate_category;
        self.special_agreement = data.special_agreement;
        if(data.verifying_explanation != null) {
          self.ve = data.verifying_explanation;
        }
        self.paper_load_dialog = false;
      })
    },    
    nextStep(){
      const self = this;
      this.$refs.verifying_explanation.$refs.form.validate()
      this.$refs.obs.validate().then(function(v) {
        if (v == true) {
          self.step +=1;
        } else {
          self.$vuetify.goTo(self.$el.querySelector(".v-messages.error--text:first-of-type"), {offset:100})
        }
      })
    },
    backStep(){
      this.validation_check = false;
      this.step -=1;
    },
    customFilter(item, queryText) {
      const name = item.user.name.toLowerCase();
      const username = item.user.username.toLowerCase();
      const birthday = item.user.birthday.toLowerCase();
      const shop_name = item.expert_profile == null ? "" : item.expert_profile.shop_name.toLowerCase();
      const searchText = queryText.toLowerCase();
            
      return (
        name.indexOf(searchText) > -1 ||
        username.indexOf(searchText) > -1 ||
        shop_name.indexOf(searchText) > -1 ||
        birthday.indexOf(searchText) > -1
      );
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
    onSubmit() {
      const self = this;
      this.validation_check = true
      this.$refs.obs.validate().then(function(v) {
        if (v == true) {
          let endpoint = "/api/papers/";
          let method = "POST";
          if (self.id !== undefined) {
            endpoint += `${self.id}/`;
            method = "PUT";
          }
          self.updateContractors();
          try {
            apiService(endpoint, method, {
              land_category: self.land_category,
              lot_area: self.lot_area,
              building_structure: self.building_structure,
              building_category: self.building_category,
              building_area: self.building_area,
              trade_category: self.trade_category,
              address: {
                old_address: self.address.old_address ,
                new_address: self.address.new_address,
                sigunguCd: self.address.sigunguCd,
                bjdongCd: self.address.bjdongCd,
                bun: self.address.bun,
                ji:  self.address.ji,
                dong: self.address.dong,
                ho: self.address.ho,
              },
              down_payment: self.down_payment,
              security_deposit: self.security_deposit,
              maintenance_fee: self.maintenance_fee,
              monthly_fee: self.monthly_fee,
              from_date: self.from_date,
              to_date: self.to_date,
              title: self.title,
              realestate_category: self.realestate_category,
              paper_contractors: self.contractors,
              options: self.options,
              special_agreement: self.special_agreement,
              verifying_explanation: self.ve
            }).then(data => {
              if (data.id) {
                alert(self.$i18n.t("request_success"))
                self.$router.push({
                  name: "paper",
                  params: { id: data.id }
                });
              } else {
                applyValidation(data, self);
                self.$nextTick(() => {
                    self.$vuetify.goTo(self.$el.querySelector(".v-messages.error--text:first-of-type"), {offset:100})
                    alert(self.$i18n.t("error"))
                    return;
                });
              }
            });
          } catch (err) {
            alert(err);
          }
        }
      });
    }
  },
  async beforeRouteEnter(to, from, next) {
    if (to.params.id !== undefined) {
      let endpoint = `/api/papers/${to.params.id}/`;
      let data = await apiService(endpoint);
      return next(
        vm => {
          for(const contractor_index in data.paper_contractors) {
            var contractor = data.paper_contractors[contractor_index]
            if(contractor.group==vm.$getConstByName("CONTRACTOR_CATEGORY", "expert")){
              (vm.expert = contractor.profile)
            }else if(contractor.group==vm.$getConstByName("CONTRACTOR_CATEGORY", "seller")){
              (vm.seller = contractor.profile)
            }else {
              (vm.buyer = contractor.profile)
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
          console.log(data.verifying_explanation)
          if(data.verifying_explanation != null) {
            vm.ve = data.verifying_explanation;
          }
        }
      );
    } else {
      return next();
    }
  },
  created() {
    document.title = this.$i18n.t("create_paper_title");
    this.requestUser = window.localStorage.getItem("username");
    this.getAllowedProfiles();
    if (window.localStorage.getItem("is_expert") == "true") {
      this.getMyProfiles();
    }
  }
};
</script>
<style scoped>
</style>