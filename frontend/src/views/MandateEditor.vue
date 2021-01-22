<template>
  <v-container v-if="!isLoading">
    <v-dialog content-class="signature-dialog" v-model="signature_dialog" eager>
        <v-card>
          <VueSignaturePad
            class="signature-pad"
            ref="signaturePad"
            :customStyle="{ border: 'black 2px solid' }"
            :options="{
              minWidth: 3,
              maxWidth: 3,
              penColor: 'red'
            }"
          />
          <v-card-title class="justify-center">
            {{ $t("please_sign") }}
          </v-card-title>
          <v-card-actions>
            <v-btn color="blue darken-1" text @click="signature_dialog = false">{{
              $t("close")
            }}</v-btn>
            <v-btn color="blue darken-1" text @click="$refs.signaturePad.clearSignature();">{{
              `${$t("signature")} ${$t("clear")}`
            }}</v-btn>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="submit()">{{
              $t("mandate_paper") + ' ' + $t("submit")
            }}</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <template v-if="id&&isAuthor&&!designator_signature_url">
        <v-chip-group>
          <DeleteAlert v-if="!readonly" :id="id" url="/api/mandates/" router_name="mandates" />
          <v-spacer></v-spacer>
          <v-btn v-if="readonly" class="ma-1 auto" color="green" dark @click="readonly_flag=false">
            {{ $t("edit") }}
          </v-btn>
          <v-btn v-else class="ma-1 auto" dark @click="readonly_flag=true">
            {{ $t("read_mode") }}
          </v-btn>
        </v-chip-group>
      </template>
      <div class="mt-3">1. {{ $t("desc_realestate") }} {{ $t("and") }} {{ $t("mandate") }} {{ $t("period") }}</div>
      <ValidationObserver ref="mandate_obs">
        <v-row>
          <v-col cols="12" sm="9">
            <AddressSearch
            ref_name="address"
            :readonly="readonly"
            :label="$t('mandate')+' '+$t('realestate')+' '+$t('address') + $t('search')"
            :address.sync="address"
            ></AddressSearch>
          </v-col>
          <v-col cols="12" sm="3">
            <v-menu
              v-model="period_menu"
              :disabled="readonly"
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
                    :label="$t('mandate') + $t('period')"
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
                @change="period_menu=false"
                :locale="this.$i18n.locale"
                range
              ></v-date-picker>
            </v-menu>
          </v-col>
        </v-row>
      
      <div class="mt-3">2. {{ $t("designator") }} {{ $t("and") }} {{ $t("designee") }} {{ $t("info") }}</div>
        <v-expansion-panels
          v-model="panels"
          multiple
        >
          <v-row>
            <v-col cols="12" md="6">
              <ValidationProvider
                v-if="id?isAuthor:true"
                ref="designator"
                v-slot="{ errors }"
                rules="required"
                :name="$t('designator')">
                <v-autocomplete
                  v-if="readonly==false"
                  v-model="designator"
                  :error-messages="errors"
                  :filter="customFilter"
                  :items="allowed_profiles"
                  item-text="name"
                  item-value="id"
                  return-object
                  :label="$t('designator')"
                  :placeholder="$t('quick_trade_user')+ ' ' + $t('select')"
                >
                  <template v-slot:selection="{ item }"
                  >{{ item.user.username + ' (#' + item.id + ' / ' + item.user.name + ' / ' + item.mobile_number + ")" }}</template>
                  <template v-slot:item="{ item }"
                  >{{ item.user.username + ' (#' + item.id + ' / ' + item.user.name + ' / ' + item.mobile_number + ")" }}</template>
                </v-autocomplete>
              </ValidationProvider>
              <v-expansion-panel v-if="designator">
                <v-expansion-panel-header>{{$t("designator")}} {{$t("detail")}} {{$t("info") }} {{`(${designator.user.username})`}}</v-expansion-panel-header>
                <v-expansion-panel-content>
                  <ContractorItem :contractor="designator" :fields="basic_profile_fields" :label_cols="label_cols"></ContractorItem>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-col>

            <v-col cols="12" md="6">
              <ValidationProvider
                v-if="id?isAuthor:true"
                ref="designee"
                rules="required"
                v-slot="{ errors }"
                :name="$t('designee')"
              >
                <v-autocomplete
                  v-if="readonly==false"
                  v-model="designee"
                  :error-messages="errors"
                  :filter="customFilter"
                  :items="allowed_profiles"
                  item-text="name"
                  item-value="id"
                  return-object
                  :label="$t('designee')"
                  :placeholder="$t('quick_trade_user')+ ' ' + $t('select')"
                >
                  <template v-slot:selection="{ item }"
                  >{{ item.user.username + ' (#' + item.id + ' / ' + item.user.name + ' / ' + ' / ' + item.mobile_number + ")" }}</template>
                  <template v-slot:item="{ item }"
                  >{{ item.user.username + ' (#' + item.id + ' / ' + item.user.name + ' / ' + ' / ' + item.mobile_number + ")" }}</template>
                </v-autocomplete>
              </ValidationProvider>
              <v-expansion-panel v-if="designee">
                <v-expansion-panel-header>{{$t("designee")}} {{$t("detail")}} {{$t("info")}} {{`(${designee.user.username})`}}</v-expansion-panel-header>
                <v-expansion-panel-content>
                  <ContractorItem :contractor="designee" :fields="basic_profile_fields" :label_cols="label_cols"></ContractorItem>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-col>
          </v-row>
        </v-expansion-panels>
        <div class="mt-3">4. {{$t("mandate_paper")}} {{ $t("content") }}</div>
        <ValidationProvider
          ref="content"
          v-slot="{ errors }"
          :name="$t('special_agreement')"
          rules="required"
        >
          <quill-editor
            ref="myQuillEditor"
            v-model="content"
            :options="editorOption"
            :disabled="readonly"
          />
          <div class="v-messages theme--light error--text" role="alert">
            <div class="v-messages__wrapper">
              <div class="v-messages__message">{{ errors[0] }}</div>
            </div>
          </div>
        </ValidationProvider>
        <div class="mt-3" align="end">
          <template v-if="designator_signature_url">
            <a v-bind:href="designator_signature_url" target="_blank">
              <img class="signature-img" :src="designator_signature_url" />
            </a>
          </template>
          ({{ $t("designator") }} {{ $t("signature") }})
        </div>
      </ValidationObserver>
      <v-row v-if="!designator_signature_url" justify="end">
        <v-btn
          v-if="isDesignator"
          class="mt-3"
          @click="open()"
          color="primary"
          dark
        >
          <v-icon>create</v-icon>
          {{ $t("signature_and_submit") }}
        </v-btn>
        <v-btn
          v-else-if="!id||!readonly"
          class="mt-3"
          @click="submit()"
          color="primary"
          dark
        >
          <v-icon>create</v-icon>
          {{ $t("submit") }}
        </v-btn>        
        <ValidationProvider ref="signature-button" v-slot="{ errors }">
                <v-input :error-messages="errors"></v-input>
        </ValidationProvider>
      </v-row>
  </v-container>
</template>

<script>
import { apiService, apiService_formData } from "@/common/api_service";
import { applyValidation } from "@/common/common_api";
import AddressSearch from "@/components/AddressSearch";
import ContractorItem from "@/components/ContractorItem";
import DeleteAlert from "@/components/DeleteAlert";
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
import { quillEditor } from 'vue-quill-editor'

export default {
  name: "MandateEditor",
  components: {
    AddressSearch,
    ContractorItem,
    quillEditor,
    DeleteAlert
  },
  data() {
    return {
      id: null,
      readonly_flag: true,
      isLoading: false,
      allowed_profiles: [],
      designator: null,
      designee: null,
      signature_dialog: false,
      period_menu: false,
      period: [],
      designator_signature: null,
      designator_signature_url: null,
      address: {
        old_address: null,
        new_address: null,
        sigunguCd: null,
        bjdongCd: null,
        bun: null,
        ji: null,
        dong: '',
        ho: '',
      },
      panels: [0, 1],
      content: "제1조 상기 위임인은 수임인에게 부동산 기본정보에 기재된 거래 대상 부동산의 계약에 관한 사무를 위임한다.<br>제2조 상기 위임인은 거래계약체결 상대방에게 위임사실을 알리기 위하여 위임장 사본을 제공한다.",
      label_cols: {cols: "3", md:"2", lg: "2"},
      basic_profile_fields: [
        { name: "address"
          , key: "address.old_address"
          , cols:"9", md:"10", lg:"10"},
        { name: "name"
          , key: "user.name"
          , cols:"9", md:"4", lg:"4"},
        { name: "birthday"
          , key: "user.birthday"
          , cols:"9", md:"4", lg:"4"},
        { name: "mobile_number"
          , cols:"9", md:"4", lg:"4"},
        { name: "bank_name"
          , cols:"9", md:"4", lg:"4"},
        { name: "account_number"
          , cols:"9", md:"4"}
      ],
      editorOption: {
        modules: {
          toolbar: {
            container: [
              ['bold', 'underline', {'list': 'ordered'}, { 'size': ['small', false, 'large', 'huge'] }],
            ],
          }
        },
        placeholder: this.$t("detail") + " " + this.$t("content")
      },
    }
  },
  computed: {
    isAuthor() {
      return this.author === this.requestUser;
    },
    isDesignator() {
      return this.designator ? this.designator.user.username === this.requestUser : false;
    },
    readonly() {
      return this.id != null ? this.readonly_flag : false;
    }
  },
  methods: {
    getAllowedProfiles() {
      let endpoint = `/api/allowed-profiles/`;
      this.isLoading = true;
      apiService(endpoint).then(data => {
        if(data.length != undefined) {
          this.allowed_profiles = data;
          this.isLoading = false;
        } else {
          applyValidation(data)
        }
      });
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
    async submit() {
      const that = this;
      const { isEmpty, data } = await that.$refs.signaturePad.saveSignature();
      if (this.isDesignator&&isEmpty) {
        alert(this.$i18n.t("signature_empty_warning"))
        return;
      }
      this.$refs.mandate_obs.validate().then(function (v) {
        if (v == true) {
          const formData = new FormData()
          formData.append("designator", that.designator.id);
          formData.append("designee", that.designee.id);
          formData.append("content", that.content);
          if(that.isDesignator){
            formData.append("designator_signature", data);
          }
          if (that.period.length > 0) {
            formData.append("from_date", that.period[0]);
            formData.append("to_date", that.period[1]);
          }
          if (that.address) {
            formData.append("address.old_address", that.address.old_address);
            formData.append("address.new_address", that.address.new_address);
            formData.append("address.sigunguCd", that.address.sigunguCd);
            formData.append("address.bjdongCd", that.address.bjdongCd);
            formData.append("address.bun", that.address.bun);
            formData.append("address.ji", that.address.ji);
          }
          let endpoint = "/api/mandates/";
          let method = "POST";

          if (that.id != undefined) {
            endpoint += `${that.id}/`;
            method = "PATCH";
          }
          apiService_formData(endpoint, method, formData).then((data) => {
            if (data.id != undefined) {
              alert(that.$i18n.t("request_success"));
              that.$router.push({
                name: "mandates"
              });
            } else {
              applyValidation(data, that);
            }
          });
        }
        that.signature_dialog = false;
      })
    },
    open() {
      this.signature_dialog = true;
      this.$nextTick(() => {
        this.$refs.signaturePad.resizeCanvas();
      });
    }
  },  
  async beforeRouteEnter(to, from, next){
    if (to.params.id !== undefined){
      let endpoint = `/api/mandates/${to.params.id}/`;
      let data = await apiService(endpoint);
      if(data.id != undefined) {
        return next(
          vm => {
            vm.id = data.id;
            vm.author = data.author;
            vm.designator = data.designator;
            vm.designee = data.designee;
            vm.address = data.address;
            vm.designator_signature_url = data.designator_signature;
            vm.content = data.content;
            vm.period.push(data.from_date)
            vm.period.push(data.to_date)
          }
        ) 
      } else {
        applyValidation(data)
      }
    } else {
      return next();
    }
  },
  created() {
    this.requestUser = window.localStorage.getItem("username");
    this.getAllowedProfiles();
  }
}
</script>
<style>
</style>
<style scoped>
.signature-img {
  height: 40px;
  left: 95px;
  z-index: 1;
  position: relative;
  cursor: pointer;
}
</style>