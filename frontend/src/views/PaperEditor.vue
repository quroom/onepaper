<template>
  <ValidationObserver ref="obs">
    <v-container>
      <v-dialog v-model="paper_load_dialog" height="90%" max-width="90%">
        <v-data-table
          v-model="selected_paper"
          :headers="paper_headers"
          :items="papers"
          item-key="id"
        >
          <template
            v-slot:[`item.trade_type`]="{ item }">
            {{$getConstI18("TRADE_TYPE", item.trade_type)}}
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
          ref="address"
          :label="$t('address') + $t('search')"
          :address.sync="address"
        ></AddressSearch>
        </v-col>
        <v-col cols="2">
          <v-text-field
            v-model="address.dong"
            :label="$t('dong')"
            outlined
            hide-details="auto"
          ></v-text-field>
        </v-col>
        <v-col cols="2">
          <v-text-field
            v-model="address.ho"
            :label="$t('ho')"
            outlined
            hide-details="auto"
          ></v-text-field>
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
              <v-text-field
                v-else
                v-model="$data[''+realestate_field.name]"
                :error-messages="errors"
                :label="$t(realestate_field.name)"
                required
                :type="realestate_field.type"
                :step="realestate_field.step"
              >
              </v-text-field>
            </ValidationProvider>
          </v-col>
        </template>
      </v-row>
      <div class="mt-3">2. {{ $t("terms_and_conditions") }}</div>
      <div>{{ $t("terms_and_conditions_intro") }}</div>
      <v-row>
        <v-col cols="2">
          <ValidationProvider ref="trade_type" :name="$t('trade_type')" v-slot="{ errors }" rules="required">
            <v-select
              v-model="trade_type"
              :error-messages="errors"
              :items="$getConstList('TRADE_TYPE_LIST')"
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
              <ValidationProvider ref="from_date"  :name="$t('from_date')" v-slot="{ errors }" rules="required">
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
              <ValidationProvider ref="to_date" :name="$t('to_date')" v-slot="{ errors }" rules="required">
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
        <template v-if="trade_type==$getConstByName('TRADE_TYPE', 'rent')">
          <v-col v-for="(contract_field, index) in fields_names.contract_fields" cols="6" md="3" :key="`index`+index">
            <ValidationProvider
              v-slot="{ errors }"
              :ref="contract_field.name"
              :name="$t(contract_field.name)"
              rules="required"
            >
              <v-text-field
                v-model="$data[''+contract_field.name]"
                :error-messages="errors"
                :label="$t(contract_field.name)+'('+$t('manwon')+')'"
                :type="contract_field.type"
                required
              ></v-text-field>
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
                <v-text-field
                  v-model="$data[''+contract_field.name]"
                  :error-messages="errors"
                  :label="$t(contract_field.name)+'('+$t('manwon')+')'"
                  :type="contract_field.type"
                  required
                ></v-text-field>
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
      <v-btn class="mt-3 float_right primary" @click="onSubmit()">{{$t('submit')}}</v-btn>
    </v-container>
  </ValidationObserver>
</template>

<script>
import { apiService } from "@/common/api.service";
import Contractor from "@/components/Contractor";
import AddressSearch from "@/components/AddressSearch";
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
import { quillEditor } from 'vue-quill-editor'

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
    quillEditor
  },
  computed: {
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
      fields_names: {
        realestate_fields: [
          {
            name: "land_type",
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
            name: "building_type",
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
      land_type: 7,
      lot_area: null,
      building_structure: null,
      building_type: 80,
      building_area: null,
      trade_type: null,
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
      realestate_type: 0,
      contractors: [

      ],
      expert: null,
      seller: null,
      buyer: null,
      special_agreement: null,
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
                // Listen upload local image and save to server
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
                    // file type is only image.
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
          text: `${this.$i18n.t("trade_type")}`,
          value: "trade_type"
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
            self.$data[self.$getConst("contractor_type", contractor.group)]=contractor.profile
          }
        }
        self.land_type = data.land_type;
        self.lot_area = data.lot_area;
        self.building_structure = data.building_structure;
        self.building_type = data.building_type;
        self.building_area = data.building_area;
        self.trade_type = data.trade_type;
        self.address = data.address;
        self.deposit = data.deposit;
        self.down_payment = data.down_payment;
        self.security_deposit = data.security_deposit;
        self.maintenance_fee = data.maintenance_fee;
        self.monthly_fee = data.monthly_fee;
        self.from_date = data.from_date;
        self.to_date = data.to_date;
        self.realestate_type = data.realestate_type;
        self.special_agreement = data.special_agreement;
        self.paper_load_dialog = false;
      })
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
        const local_group_constant = this.$getConstByName("CONTRACTOR_TYPE", local_group_name)
        
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
              land_type: self.land_type,
              lot_area: self.lot_area,
              building_structure: self.building_structure,
              building_type: self.building_type,
              building_area: self.building_area,
              trade_type: self.trade_type,
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
              realestate_type: self.realestate_type,
              paper_contractors: self.contractors,
              special_agreement: self.special_agreement
            }).then(data => {
              if (data.id) {
                alert(self.$i18n.t("request_success"))
                self.$router.push({
                  name: "paper",
                  params: { id: data.id }
                });
              } else {
                Object.keys(data).forEach(function(key) {
                  if(key=="detail") {
                    alert(data[key]);
                    return;
                  }
                  const ref = self.$refs[key].length == undefined ? self.$refs[key] : self.$refs[key][0];
                  ref.applyResult({
                    errors: data[key],
                    valid: false,
                    failedRules: {}
                  });
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
            if(contractor.group==vm.$getConstByName("CONTRACTOR_TYPE", "expert")){
              (vm.expert = contractor.profile)
            }else if(contractor.group==vm.$getConstByName("CONTRACTOR_TYPE", "seller")){
              (vm.seller = contractor.profile)
            }else {
              (vm.buyer = contractor.profile)
            }
          }
          vm.land_type = data.land_type;
          vm.lot_area = data.lot_area;
          vm.building_structure = data.building_structure;
          vm.building_type = data.building_type;
          vm.building_area = data.building_area;
          vm.trade_type = data.trade_type;
          vm.address = data.address;
          vm.deposit = data.deposit;
          vm.down_payment = data.down_payment;
          vm.security_deposit = data.security_deposit;
          vm.maintenance_fee = data.maintenance_fee;
          vm.monthly_fee = data.monthly_fee;
          vm.from_date = data.from_date;
          vm.to_date = data.to_date;
          vm.realestate_type = data.realestate_type;
          vm.special_agreement = data.special_agreement;
          vm.contractors = data.paper_contractors;
          vm.status = data.statu;
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
<style>
.float_right {
  float: right;
}
.ql-container {
    font-size: 16px;
}
.truncate {
  max-width: 1px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>