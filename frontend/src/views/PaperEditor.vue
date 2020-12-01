<!-- eslint-disable -->
<template>
  <ValidationObserver ref="obs">
    <v-container>
      <template v-if="false">
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
      </template>
      <!-- need to support i18n -->
      <template v-if="is_expert">
        <v-divider></v-divider>
          <div class="caption">
            {{ $t("enforcement_rules") }}
            <span class="blue--text text--accent-4">&lt;{{$t("ve_updated_date")}}&gt;</span>
            <span class="float_right">(4쪽 중 제1쪽)</span>
          </div>
          <div class="text-h6 font-weight-bold" align="center">중개대상물 확인ㆍ설명서[Ⅰ] (주거용 건축물)</div>
          <v-row justify="center" align="center">
            <v-checkbox class="ve_checkbox" v-model="ve.paper_categories" label="단독주택" value=0></v-checkbox>
            <v-checkbox class="ve_checkbox" v-model="ve.paper_categories" label="공동주택" value=1></v-checkbox>
            <v-checkbox class="ve_checkbox" v-model="ve.paper_categories" label="매매·교환" value=2></v-checkbox>
            <v-checkbox class="ve_checkbox" v-model="ve.paper_categories" label="임대" value=3></v-checkbox>
          </v-row>
          <v-row no-gutters>
            <v-row no-gutters>
              <v-col cols="12">
                <v-card tile outlined color="grey lighten-1" align="center">
                  <v-card-text>
                    확인·설명 자료
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="2" class="d-flex border" align="center">
                  <span class="label"> 확인·설명 근거자료 등 </span>
              </v-col>
              <v-col class="d-flex flex-wrap border">
                  <v-checkbox class="ve_checkbox" v-model="ve.explanation_evidences" label="등기권리증" value=0 hideDetails="auto"></v-checkbox>
                  <v-checkbox class="ve_checkbox" v-model="ve.explanation_evidences" label="등기사항증명서" value=1 hideDetails="auto"></v-checkbox>
                  <v-checkbox class="ve_checkbox" v-model="ve.explanation_evidences" label="토지대장" value=2 hideDetails="auto"></v-checkbox>
                  <v-checkbox class="ve_checkbox" v-model="ve.explanation_evidences" label="건축물대장" value=3 hideDetails="auto"></v-checkbox>
                  <v-checkbox class="ve_checkbox" v-model="ve.explanation_evidences" label="지적도" value=4 hideDetails="auto"></v-checkbox>
                  <v-checkbox class="ve_checkbox" v-model="ve.explanation_evidences" label="임야도" value=5 hideDetails="auto"></v-checkbox>
                  <v-checkbox class="ve_checkbox" v-model="ve.explanation_evidences" label="토지이용계획확인서" value=6 hideDetails="auto"></v-checkbox>
                  <v-checkbox class="ve_checkbox" v-model="ve.explanation_evidences" label="그밖의자료" value=7 hideDetails="auto"></v-checkbox>
              </v-col>
            </v-row>
            <v-col cols="2" class="border" align="center">
              <span class="label"> 대상물건의 상태에 관한 자료요구 사항 </span>
            </v-col>
            <v-col cols="10" class="border">
              <v-textarea
                class="mt-4"
                label="자료요구 사항"
                placeholder="대상물건의 상태에 관한 자료요구 사항"
                outlined
                hide-details="auto"
              >
              </v-textarea>
            </v-col>
          </v-row>
          <v-row class="mt-4" no-gutters>
            <v-col class="grey lighten-1 border" cols="12" align="center">유의사항</v-col>
            <v-col class="border" cols="2" align="center">
              개업공인중개사의 확인·설명 의무
            </v-col>
            <v-col class="border" cols="10">
              개업공인중개사는 중개대상물에 관한 권리를 취득하려는 중개의뢰인에게 성실·정확하게 설명하고, 토지대장 등본, 등기사항증명서 등 설명의 근거자료를 제시해야 합니다.
            </v-col>
            <v-col class="border" cols="2" align="center">
              실제 거래가격 신고
            </v-col>
            <v-col class="border" cols="10">
              「부동산 거래신고 등에 관한 법률」 제3조 및 같은 법 시행령 별표 1 제1호마목에 따른 실제 거래가격은 매수인이 매수한 부동산을 양도하는 경우 「소득세법」 제97조제1항 및 제7항과 같은 법 시행령 제163조제11항제2호에 따라 취득 당시의 실제 거래가액으로 보아 양도차익이 계산될 수 있음을 유의하시기 바랍니다.
            </v-col>
          </v-row>
          <div class="text-subtitle font-weight-bold">1. 개업공인중개사 기본 확인사항</div>
          <div class="border pl-2 pr-2 mt-4">
            <div class="text-body font-weight-bold">
              ① 대상물건의 표시
            </div>
            <div class="border">
              <span class="ml-2 font-weight-bold">&lt;토지&gt;</span>
              <v-row no-gutters>
                <v-col class="d-flex flex-wrap">
                  <v-text-field class="d-flex ve-input" label="토지 소재지"></v-text-field>
                  <v-text-field class="d-flex ve-input" v-model="ve.land_area" label="토지 면적" type="Number" step="0.01" hide-details="auto"></v-text-field>
                  <v-text-field class="d-flex ve-input" v-model="ve.land_category" label="공부상지목" hide-details="auto"></v-text-field>
                  <v-text-field class="d-flex ve-input" v-model="ve.actual_land_category" label="실제 이용 상태" hide-details="auto"></v-text-field>
                </v-col>
              </v-row>
            </div>
            <div class="border">
              <span class="ml-2 font-weight-bold">&lt;건축물&gt;</span>
              <v-row no-gutters>
                <v-col class="d-flex flex-wrap">
                  <v-text-field class="d-flex ve-input" v-model="ve.net_area" type="Number" step="0.01" label="전용면적" hide-details="auto"></v-text-field>
                  <v-text-field class="d-flex ve-input" v-model="ve.land_share" label="대지지분" hide-details="auto"></v-text-field>
                  <v-text-field class="d-flex ve-input" v-model="ve.year_of_completion" label="준공년도(증개축년도)" hide-details="auto"></v-text-field>
                  <v-text-field class="d-flex ve-input" v-model="ve.building_category" label="건축물대장상 용도" hide-details="auto"></v-text-field>
                  <v-text-field class="d-flex ve-input" v-model="ve.actual_building_category" label="실제 용도" hide-details="auto"></v-text-field>
                  <v-text-field class="d-flex ve-input" v-model="ve.explanation_building_structure" label="구조" hide-details="auto"></v-text-field>
                  <v-text-field class="d-flex ve-input" v-model="ve.building_direction" label="방향" hide-details="auto"></v-text-field>
                  <v-text-field class="d-flex ve-input" v-model="ve.seismic_design" label="내진설계 적용여부" hide-details="auto"></v-text-field>
                  <v-text-field class="d-flex ve-input" v-model="ve.seismic_capacity" label="내진능력" hide-details="auto"></v-text-field>
                  <v-radio-group class="ve-input" label="건축물대장상위반건축물 여부" v-model="ve.legal_status" row mandatory>
                    <v-radio label="위반" :value="false"></v-radio>
                    <v-radio label="적법" :value="true"></v-radio>
                  </v-radio-group>
                  <v-text-field v-if="!ve.legal_status" class="d-flex ve-input" v-model="ve.matters_of_violation" label="위반내용" hide-details="auto"></v-text-field>
                </v-col>
              </v-row>
            </div>
            <div class="border pl-2 pr-2 mt-4">
              <div class="text-body font-weight-bold">
                ② 권리관계
              </div>
              <div class="border">
                <span class="ml-2 font-weight-bold">&lt;등기부기재사항&gt;</span>
                <v-row no-gutters>
                  <v-col class="d-flex flex-wrap">
                    <v-textarea class="d-flex ve-input" v-model="ve.land_ownership" label="토지 소유권에 관한 사항" hide-details="auto" auto-grow rows="2"></v-textarea>
                    <v-textarea class="d-flex ve-input" v-model="ve.building_ownership" label="건축물 소유권에 관한 사항" hide-details="auto" auto-grow rows="2"></v-textarea>
                    <v-textarea class="d-flex ve-input" v-model="ve.land_other" label="토지 소유권 외의 권리에 관한 사항" hide-details="auto" auto-grow rows="2"></v-textarea>
                    <v-textarea class="d-flex ve-input" v-model="ve.building_other" label="건축물 소유권의 권리에 관한 사항" hide-details="auto" auto-grow rows="2"></v-textarea>
                  </v-col>
                </v-row>
              </div>
              <div class="border">
                <span class="ml-2 font-weight-bold">&lt;민간임대등록여부&gt;</span>
                <v-radio-group class="d-flex ve-input" label="건축물대장상위반건축물 여부" v-model="ve.rental_housing_registration" row mandatory>
                  <v-radio label="장기일반민간임대주택" :value="0"></v-radio>
                  <v-radio label="공공지원민간임대주택" :value="1"></v-radio>
                  <v-radio label="단기민간임대주택" :value="2"></v-radio>
                  <v-radio label="해당 사항 없음" :value="3"></v-radio>
                </v-radio-group>
              </div>
            </div>
            <div class="border pl-2 pr-2 mt-4">
              <div class="text-body font-weight-bold">
                ③ 토지이용계획, 공법상 이용제한 및 거래규제에 관한 사항(토지)
              </div>
              <div class="border">
                <v-row no-gutters>
                  <v-col class="d-flex flex-wrap">
                    <v-text-field class="d-flex ve-input" v-model="ve.use_area" label="용도지역" hide-details="auto"></v-text-field>
                    <v-text-field class="d-flex ve-input" v-model="ve.use_district" label="용도지구" hide-details="auto"></v-text-field>
                    <v-text-field class="d-flex ve-input" v-model="ve.use_zone" label="용도구역" hide-details="auto"></v-text-field>
                    <v-text-field class="d-flex ve-input" v-model="ve.building_coverage_limit" type="Number" step="1" label="건페율 상한" hide-details="auto"></v-text-field>
                    <v-text-field class="d-flex ve-input" v-model="ve.floor_area_limit" type="Number" step="1" label="용적률 상한" hide-details="auto"></v-text-field>                  
                      <v-textarea class="d-flex ve-input" v-model="ve.planning_facilities" label="도시·군계획 시설" hide-details="auto" auto-grow rows="1"></v-textarea>
                      <v-checkbox class="d-flex ve-input" v-model="ve.permission_reposrt_zone" label="토지거래허가 신고구역"></v-checkbox>
                      <v-radio-group class="d-flex ve-input" label="투기지역 여부" v-model="ve.speculative_area" row mandatory>
                        <v-radio label="토지투기지역" :value="0"></v-radio>
                        <v-radio label="주택투기지역" :value="1"></v-radio>
                        <v-radio label="투기과열지구" :value="2"></v-radio>
                      </v-radio-group>
                      <v-textarea class="d-flex ve-input" v-model="ve.unit_planning_area_others" label="지구단위계획구역, 그 밖의 도시·군관리계획" hint="지구단위계획구역, 그 밖의 도시·군관리계획" hide-details="auto" auto-grow rows="1"></v-textarea>
                      <v-textarea class="d-flex ve-input" v-model="ve.other_use_restriction" label="그 밖의 이용제한 및 거래규제사항" hide-details="auto" auto-grow rows="1"></v-textarea>
                    </v-col>
                </v-row>
              </div>
            </div>
            <div class="border pl-2 pr-2 mt-4">
              <div class="text-body font-weight-bold">
                ④ 입지조건
              </div>
              <div class="border">
                <v-row no-gutters>
                  <v-col class="d-flex flex-wrap">
                    <div class="d-flex">
                      <v-text-field class="d-flex ve-input" v-model="ve.relative_with_roads" label="도로와의 관계" hide-details="auto"></v-text-field>
                      <v-radio-group class="ve-input" v-model="ve.is_paved_rode" row mandatory>
                        <v-radio label="포장" :value="true"></v-radio>
                        <v-radio label="비포장" :value="false"></v-radio>
                      </v-radio-group>
                      <v-radio-group v-model="ve.acessibility" label="접근성" row mandatory>
                        <v-radio label="용이함" :value="true"></v-radio>
                        <v-radio label="불편함" :value="false"></v-radio>
                      </v-radio-group>
                    </div>
                  </v-col>
                </v-row>
              </div>
            </div>
          </div>
      </template>
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
      options: [0,1,2],
      special_agreement: null,
      ve: {
        paper_categories: [],
        explanation_evidences: [],
        explanation_evidence_info: null,
        explanation_address: {
          old_address: null
        },
        land_area: null,
        land_category: null,
        actual_land_category: null,
        net_area: null,
        land_share: null,
        year_of_completion: null,
        building_category: null,
        actual_building_category: null,
        explanation_building_structure: null,
        building_direction: null,
        seismic_design: null,
        seismic_capacity: null,
        legal_status: true,
        matters_of_violation: null,
        land_ownership: null,
        building_ownership: null,
        land_other: null,
        building_other: null,
        rental_housing_registration: 4,
        use_area: null,
        use_district: null,
        use_zone: null,
        building_coverage_limit: null,
        floor_area_limit: null,
        planning_facilities: null,
        permission_report_zone: null,
        speculative_area: null,
        unit_planning_area_others: null,
        other_use_restriction: null,
        relative_with_roads: '(  m  ×  m ) 도로에 접합',
        is_paved_rode: null,
        acessibility: null,
        bus_stop: null,
        bus_by_foot: null,
        bus_time_required: null,
        subway_station: null,
        subway_by_foot: null,
        subway_time_required: null,
        parking_lot: null,
        parking_lot_info: null,
        elementary_school: null,
        elementary_school_by_foot: null,
        elementary_school_time_required: null,
        middle_school: null,
        middle_school_by_foot: null,
        middle_school_time_required: null,
        high_school: null,
        high_school_by_foot: null,
        high_school_time_required: null,
        department_store: null,
        department_store_by_foot: null,
        department_store_time_required: null,
        medical_center: null,
        medical_center_by_foot: null,
        medical_center_time_required: null,
        security_office: null,
        management: null,
        undesirable_facilities: null,
        undesirable_facilities_info: null,
        expected_transaction_price: null,
        land_prcie_recorded: null,
        building_price_recorded: null,
        acquisition_tax: null,
        special_tax: null,
        local_education_tax: null,
        water_damage_status: null,
        water_damage_location: null,
        water_capacity_status: null,
        water_capacity_location: null,
        electricity_supply_status: null,
        electricity_location: null,
        gas_supply_status: null,
        gas_supply_info: null,
        fire_alarm_detector: null,
        fire_alarm_detector_quantity: null,
        heating_supply_method: null,
        heating_status: null,
        heating_status_info: null,
        heating_type: null,
        heating_type_info: null,
        is_elevator: null,
        elevator_status: null,
        drainage_status: null,
        drainage_status_info: null,
        other_facilities: null,
        wall_crack_status: null,
        wall_crack_status_info: null,
        water_leak_status: null,
        water_leak_status_info: null,
        wall_paper_status: null,
        wall_paper_status_info: null,
        sunshine_status: null,
        sunshine_status_info: null,
        noise_status: null,
        vibration: null,
        comission: null,
        actual_expenses: null,
        payment_period: null,
        caculation_info: null
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
              options: self.options,
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
.v-label {
  margin-bottom: 0;
}

.label {
  margin: auto;
}
.ve_checkbox {
  margin: 4px !important;
}
.ve-input {
  margin-left: 8px;
  margin-right: 8px;
  margin-bottom: 4px;
}
.v-card__text {
  padding: 8px;
}
.col {
  word-break: break-all;
}
.border {
  border:solid 1px rgba(0, 0, 0 ,0.12)
}
</style>