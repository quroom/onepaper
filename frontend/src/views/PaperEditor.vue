<template>
  <ValidationObserver ref="obs">
    <div class="container my-5">
      <div class="mt-5">1. {{ $t("desc_realestate") }}</div>
      <v-row>
        <v-col cols="8" md="10">
          <ValidationProvider :name="$t('address')" rules="required" v-slot="{ errors, }">
            <v-text-field
              v-model="address"
              :error-messages="errors"
              :label="$t('address')"
              required
            ></v-text-field>
          </ValidationProvider>
        </v-col>
        <template v-for="(realestate_field_name, index) in fields_names.realestate_fields_name">
          <v-col cols="4" md="2" :key="`index`+index">
            <ValidationProvider
              :name="$t(realestate_field_name)"
              rules="required"
              v-slot="{ errors, }"
            >
              <v-text-field
                v-model="$data[''+realestate_field_name]"
                :error-messages="errors"
                :label="$t(realestate_field_name)"
                required
              ></v-text-field>
            </ValidationProvider>
          </v-col>
        </template>
        <v-col cols="4" md="2">
          <ValidationProvider :name="$t('realestate_type')" v-slot="{ errors, }" rules="required">          
            <v-select
              v-model="realestate_type"
              :error-messages="errors"
              :items="$getConst('REALESTATE_TYPE_LIST')"
              item-text="text"
              item-value="value"
              :label="$t('realestate_type')"
            >
              <template v-slot:selection="{ item }">{{ $t(item.text) }}</template>
              <template v-slot:item="{ item }">{{ $t(item.text) }}</template>
            </v-select>
          </ValidationProvider>
        </v-col>
      </v-row>
      <div class="mt-5">2. {{ $t("terms_and_conditions") }}</div>
      <div>{{ $t("terms_and_conditions_intro") }}</div>
      <v-row>
        <v-col cols="2">
          <ValidationProvider :name="$t('trade_type')" v-slot="{ errors, }" rules="required">
            <v-select
              v-model="trade_type"
              :error-messages="errors"
              :items="$getConst('TRADE_TYPE_LIST')"
              item-text="text"
              item-value="value"
              :label="$t('trade_type')"
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
              <ValidationProvider :name="$t('from_date')" v-slot="{ errors, }" rules="required">
                <v-text-field
                  v-model="from_date"
                  :error-messages="errors"
                  :label="$t('from_date')"
                  prepend-icon="event"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
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
              <ValidationProvider :name="$t('to_date')" v-slot="{ errors, }" rules="required">
                <v-text-field
                  v-model="to_date"
                  :error-messages="errors"
                  :label="$t('to_date')"
                  prepend-icon="event"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
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
        <template v-if="trade_type==$getConstByVal('TRADE_TYPE', 'rent')">
          <template v-for="(contract_field_name, index) in fields_names.contract_fields_name">
            <v-col cols="6" md="3" :key="`index`+index">
              <ValidationProvider
                v-slot="{ errors, }"
                :name="$t(contract_field_name)"
                rules="required"
              >
                <v-text-field
                  v-model="$data[''+contract_field_name]"
                  :error-messages="errors"
                  :label="$t(contract_field_name)+'('+$t('manwon')+')'"
                  required
                ></v-text-field>
              </ValidationProvider>
            </v-col>
          </template>
        </template>
        <template v-else>
          <template v-for="(contract_field_name, index) in fields_names.contract_fields_name">
            <v-col v-if="contract_field_name!='monthly_fee'" cols="6" md="3" :key="`index`+index">
              <ValidationProvider
                v-slot="{ errors, }"
                :name="$t(contract_field_name)"
                rules="required"
              >
                <v-text-field
                  v-model="$data[''+contract_field_name]"
                  :error-messages="errors"
                  :label="$t(contract_field_name)+'('+$t('manwon')+')'"
                  required
                ></v-text-field>
              </ValidationProvider>
            </v-col>
          </template>
        </template>
      </v-row>

      <div class="mt-5">3. {{ $t("contractor_info") }}</div>
      <div>{{ $t("contractor_info_intro") }}</div>
      <v-expansion-panels>
        <v-row no-gutters>
          <v-col v-if="is_expert" cols="12">
            <ValidationProvider
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
                <v-row>
                  <template v-for="(field_name, index) in fields_names.expert_fields_name">
                    <v-col class="text-center font-weight-bold" cols="2" md="2" :key="`name`+index">
                      <v-card outlined tile>{{ $t(field_name) }}</v-card>
                    </v-col>
                    <v-col
                      v-if="field_name==='name' || field_name==='birthday'"
                      class="text-center"
                      cols="4"
                      md="2"
                      :key="`value-`+index"
                    >
                      <v-card outlined tile>{{ expert.user[field_name]}}</v-card>
                    </v-col>
                    <v-col v-else-if="field_name==='registration_number' || field_name==='shop_name'" class="text-center" cols="4" md="2" :key="`value-`+index">
                      <v-card outlined tile>{{ expert.expert_profile[field_name]}}</v-card>
                    </v-col>
                    <v-col v-else class="text-center" cols="4" md="2" :key="`value-`+index">
                      <v-card outlined tile>{{ expert[field_name]}}</v-card>
                    </v-col>
                  </template>
                </v-row>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-col>
          <v-col v-if="!is_loading" cols="12">
            <ValidationProvider
              ref="seller"
              v-slot="{ errors }"
              :name="$t('landlord')"
              rules="required"
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
                >{{ item.user.name + '(' + $t('birthday') + ':' + item.user.birthday + ' / ' + $t('username') +':'+ item.user.username + ' / ' + $t('profile_name') + ':'+ item.profile_name + ")" }}</template>
                <template
                  v-slot:item="{ item }"
                >{{ item.user.name + '(' + $t('birthday') + ':' + item.user.birthday + ' / ' + $t('username') +':'+ item.user.username + ' / ' + $t('profile_name') + ':'+ item.profile_name + ")" }}</template>
              </v-autocomplete>
            </ValidationProvider>
            <v-expansion-panel v-if="seller">
              <v-expansion-panel-header>{{$t("landlord")}} {{$t("detail")}} {{$t("info")}}</v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-row>
                  <template v-for="(field_name, index) in fields_names.basic_profile_fields_name">
                    <v-col class="text-center font-weight-bold" cols="2" md="2" :key="`name`+index">
                      <v-card outlined tile>{{ $t(field_name) }}</v-card>
                    </v-col>
                    <v-col
                      v-if="field_name==='name' || field_name==='birthday'"
                      class="text-center"
                      cols="4"
                      md="2"
                      :key="`value-`+index"
                    >
                      <v-card outlined tile>{{ seller['user'][field_name]}}</v-card>
                    </v-col>
                    <v-col v-else class="text-center" cols="4" md="2" :key="`value-`+index">
                      <v-card outlined tile>{{ seller[field_name]}}</v-card>
                    </v-col>
                  </template>
                </v-row>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-col>
          <v-col v-if="!is_loading" class="mt-5" cols="12">
            <ValidationProvider
              ref="buyer"
              v-slot="{ errors }"
              :name="$t('tenant')"
              rules="required"
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
                >{{ item.user.name + '(' + $t('birthday') + ':' + item.user.birthday + ' / ' + $t('username') +':'+ item.user.username + ' / ' + $t('profile_name') + ':'+ item.profile_name + ")" }}</template>
                <template
                  v-slot:item="{ item }"
                >{{ item.user.name + '(' + $t('birthday') + ':' + item.user.birthday + ' / ' + $t('username') +':'+ item.user.username + ' / ' + $t('profile_name') + ':'+ item.profile_name + ")" }}</template>
              </v-autocomplete>
            </ValidationProvider>
            <v-expansion-panel v-if="buyer">
              <v-expansion-panel-header>{{$t("tenant")}} {{$t("detail")}} {{$t("info")}}</v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-row>
                  <template v-for="(field_name, index) in fields_names.basic_profile_fields_name">
                    <v-col class="text-center font-weight-bold" cols="2" md="2" :key="`name`+index">
                      <v-card outlined tile>
                        {{ $t(field_name) }}
                      </v-card>
                    </v-col>
                    <v-col
                      v-if="field_name==='name' || field_name==='birthday'"
                      class="text-center"
                      cols="4"
                      md="2"
                      :key="`value-` + index"
                    >
                      <v-card outlined tile>
                        {{ buyer["user"][field_name] }}
                      </v-card>
                    </v-col>
                    <v-col
                      v-else
                      class="text-center"
                      cols="4"
                      md="2"
                      :key="`value-` + index"
                    >
                      <v-card outlined tile>
                        {{ buyer[field_name] }}
                      </v-card>
                    </v-col>
                  </template>
                </v-row>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-col>
        </v-row>
      </v-expansion-panels>
      <div class="mt-5">4. {{ $t("special_agreement") }}</div>
      <v-textarea class="mt-2" v-model="special_agreement" auto-grow outlined>
      </v-textarea>
      <v-btn class="mr-4" @click="onSubmit()">submit</v-btn>
    </div>
  </ValidationObserver>
</template>

<script>
import { apiService } from "@/common/api.service";
import i18n from "@/plugins/i18n";
import { ValidationProvider, ValidationObserver } from "vee-validate";

export default {
  name: "PaperEditor",
  props: {
    id: {
      type: [Number, String],
      required: false
    }
  },
  components: {
    ValidationProvider,
    ValidationObserver
  },
  computed: {
  },
  data() {
    return {
      requestUser: null,
      is_loading: false,
      is_expert: false,
      my_profiles: [],
      allowed_profiles: [],
      fields_names: {
        realestate_fields_name: [
          "room_name",
          "land_type",
          "lot_area",
          "building_structure",
          "building_type",
          "building_area"
        ],
        contract_fields_name: [
          "security_deposit",
          "monthly_fee",
          "maintenance_fee",
          "down_payment"
        ],
        basic_profile_fields_name: [
          "name",
          "birthday",
          "mobile_number",
          "address",
          "bank_name",
          "account_number"
        ],
        expert_fields_name: [
          "name",
          "birthday",
          "bank_name",
          "account_number",
          "registration_number",
          "shop_name",
          "address"
        ]
      },
      from_date_menu: false,
      to_date_menu: false,
      land_type: "대",
      lot_area: null,
      building_structure: null,
      building_type: null,
      building_area: null,
      trade_type: null,
      address: null,
      room_name: null,
      down_payment: null,
      security_deposit: null,
      maintenance_fee: null,
      monthly_fee: null,
      from_date: null,
      to_date: null,
      realestate_type: null,
      contractors: [

      ],
      expert: null,
      seller: null,
      buyer: null,
      special_agreement: null
    };
  },
  methods: {
    remove (item, type) {
      const index = this[type].indexOf(item)
      if (index >= 0) this[type].splice(index, 1)
    },
    contractorChanged(datas, type) {
      for(var data of datas){
        console.log(data, type)
      }
    },
    getAuthedProfiles() {
      let endpoint = `/api/allowed-profiles/`;
      this.is_loading = true;
      this.test = true
      apiService(endpoint).then(data => {
        this.allowed_profiles = data;
        this.is_loading = false;
      });
    },
    getMyProfiles() {
      let endpoint = `/api/profiles/`;
      apiService(endpoint).then(data => {
        this.my_profiles = data;
        this.is_expert = true;
      });
    },
    customFilter(item, queryText) {  
      const name = item.user.name.toLowerCase();
      const username = item.user.username.toLowerCase();
      const profile_name = item.profile_name.toLowerCase();
      const shop_name = item.expert_profile === null ? "" : item.expert_profile.shop_name.toLowerCase();
      const searchText = queryText.toLowerCase();
            
      return (
        name.indexOf(searchText) > -1 ||
        username.indexOf(searchText) > -1 ||
        shop_name.indexOf(searchText) > -1 ||
        profile_name.indexOf(searchText) > -1
      );
    },
    combine_contractors(){
      if(this.expert) {
        this.contractors.push({
          "profile": this.expert.id, "paper":null, "group":this.$getConstByVal("CONTRACTOR_TYPE", "expert")
        })
      }
      if(this.seller) {
        this.contractors.push({
          "profile": this.seller.id, "paper":null, "group":this.$getConstByVal("CONTRACTOR_TYPE", "seller")
        })
      }
      if(this.buyer) {
        this.contractors.push({
          "profile": this.buyer.id, "paper":null, "group":this.$getConstByVal("CONTRACTOR_TYPE", "buyer")
        })
      }
    },
    onSubmit() {
      const self = this;
      this.$refs.obs.validate().then(function(v) {
        if (v == true) {
          self.contractors = [];
          console.log("validation true");
          self.combine_contractors();
          let endpoint = "/api/papers/";
          let method = "POST";
          if (self.id !== undefined) {
            endpoint += `${self.id}/`;
            method = "PUT";
          }
          try {
            apiService(endpoint, method, {
              land_type: self.land_type,
              lot_area: self.lot_area,
              building_structure: self.building_structure,
              building_type: self.building_type,
              building_area: self.building_area,
              trade_type: self.trade_type,
              address: self.address,
              room_name: self.room_name,
              down_payment: self.down_payment,
              security_deposit: self.security_deposit,
              maintenance_fee: self.maintenance_fee,
              monthly_fee: self.monthly_fee,
              from_date: self.from_date,
              to_date: self.to_date,
              title: self.title,
              realestate_type: self.realestate_type,
              paper_contractors: self.contractors,
              special_agreement: self.special_agreement
            }).then(data => {
              if (data.id) {
                self.$router.push({
                  name: "paper",
                  params: { id: data.id }
                });
              } else {
                Object.keys(data).forEach(function(key) {
                  self.$refs[key].applyResult({
                    errors: data[key],
                    valid: false,
                    failedRules: {}
                  });
                });
              }
            });
          } catch (err) {
            console.log(err);
          }
        } else console.log("validation error");
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
            if(contractor.group==vm.$getConstByVal("CONTRACTOR_TYPE", "expert")){
              (vm.expert = contractor.profile)
            }else if(contractor.group==vm.$getConstByVal("CONTRACTOR_TYPE", "seller")){
              (vm.seller = contractor.profile)
            }else {
              (vm.buyer = contractor.profile)
            }
          }
          (vm.land_type = data.land_type),
          (vm.lot_area = data.lot_area),
          (vm.building_structure = data.building_structure),
          (vm.building_type = data.building_type),
          (vm.building_area = data.building_area),
          (vm.trade_type = data.trade_type),
          (vm.address = data.address),
          (vm.room_name = data.room_name),
          (vm.deposit = data.deposit),
          (vm.down_payment = data.monthly_fee),
          (vm.security_deposit = data.security_deposit),
          (vm.maintenance_fee = data.maintenance_fee),
          (vm.monthly_fee = data.monthly_fee),
          (vm.from_date = data.from_date),
          (vm.to_date = data.to_date),
          (vm.realestate_type = data.realestate_type),
          (vm.special_agreement = data.special_agreement),
          (vm.contractors = data.paper_contractors),
          (vm.status = data.status)
        }
      );
    } else {
      return next();
    }
  },
  created() {    
    
    document.title = i18n.t("create_paper_title");
    this.requestUser = window.localStorage.getItem("username");
    this.getAuthedProfiles();
    if (window.localStorage.getItem("is_expert") == "true") {
      this.getMyProfiles();
    }
  }
};
</script>
