<template>
  <div>
    <v-form ref="form" v-model="valid" lazy-validation>
      <template v-if="step == 2 || validation_check">
        <div class="caption">
          {{ $t("enforcement_rules") }}
          <span class="blue--text text--accent-4"
            >&lt;{{ $t("ve_amendment_updated_date") }}&gt;</span
          >
          <span class="float-right">(4쪽 중 제1쪽)</span>
        </div>
        <div class="text-h6 font-weight-bold" align="center">
          중개대상물 확인ㆍ설명서[Ⅰ] (주거용 건축물)
        </div>
        <v-row justify="center" align="center">
          <v-checkbox
            class="ve_checkbox"
            v-model="ve.paper_categories"
            label="단독주택"
            :value="1"
            :readonly="readonly"
          ></v-checkbox>
          <v-checkbox
            class="ve_checkbox"
            v-model="ve.paper_categories"
            label="공동주택"
            :value="2"
            :readonly="readonly"
          ></v-checkbox>
          <v-checkbox
            class="ve_checkbox"
            v-model="ve.paper_categories"
            label="매매·교환"
            :value="3"
            :readonly="readonly"
          ></v-checkbox>
          <v-checkbox
            class="ve_checkbox"
            v-model="ve.paper_categories"
            label="임대"
            :value="4"
            :readonly="readonly"
          ></v-checkbox>
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
              <v-checkbox
                class="ve_checkbox"
                v-model="ve.explanation_evidences"
                label="등기권리증"
                :value="1"
                :readonly="readonly"
              ></v-checkbox>
              <v-checkbox
                class="ve_checkbox"
                v-model="ve.explanation_evidences"
                label="등기사항증명서"
                :value="2"
                :readonly="readonly"
              ></v-checkbox>
              <v-checkbox
                class="ve_checkbox"
                v-model="ve.explanation_evidences"
                label="토지대장"
                :value="3"
                :readonly="readonly"
              ></v-checkbox>
              <v-checkbox
                class="ve_checkbox"
                v-model="ve.explanation_evidences"
                label="건축물대장"
                :value="4"
                :readonly="readonly"
              ></v-checkbox>
              <v-checkbox
                class="ve_checkbox"
                v-model="ve.explanation_evidences"
                label="지적도"
                :value="5"
                :readonly="readonly"
              ></v-checkbox>
              <v-checkbox
                class="ve_checkbox"
                v-model="ve.explanation_evidences"
                label="임야도"
                :value="6"
                :readonly="readonly"
              ></v-checkbox>
              <v-checkbox
                class="ve_checkbox"
                v-model="ve.explanation_evidences"
                label="토지이용계획확인서"
                :value="7"
                :readonly="readonly"
              ></v-checkbox>
              <v-checkbox
                class="ve_checkbox"
                v-model="ve.explanation_evidences"
                label="그밖의자료"
                :value="99"
                :readonly="readonly"
              ></v-checkbox>
              <LazyTextField
                v-if="ve.explanation_evidences.includes(99)"
                class="d-flex ve-input"
                v-model="ve.explanation_evidence_info"
                prefix="("
                suffix=")"
                :readonly="readonly"
              ></LazyTextField>
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col cols="2" class="border" align="center">
              <span class="label"> 대상물건의 상태에 관한 자료요구 사항 </span>
            </v-col>
            <v-col cols="10" class="border">
              <LazyTextArea
                class="mt-4"
                v-model="ve.requesting_condition_info"
                label="자료요구 사항"
                placeholder="대상물건의 상태에 관한 자료요구 사항"
                outlined
                rows="2"
                auto-grow
                :readonly="readonly"
              ></LazyTextArea>
            </v-col>
          </v-row>
        </v-row>
        <v-row class="mt-4" no-gutters>
          <v-col class="grey lighten-1 border" cols="12" align="center">유의사항</v-col>
          <v-col class="border" cols="2" align="center">
            개업공인중개사의 확인·설명 의무
          </v-col>
          <v-col class="border" cols="10">
            개업공인중개사는 중개대상물에 관한 권리를 취득하려는 중개의뢰인에게 성실·정확하게
            설명하고, 토지대장 등본, 등기사항증명서 등 설명의 근거자료를 제시해야 합니다.
          </v-col>
          <v-col class="border" cols="2" align="center">
            실제 거래가격 신고
          </v-col>
          <v-col class="border" cols="10">
            「부동산 거래신고 등에 관한 법률」 제3조 및 같은 법 시행령 별표 1 제1호마목에 따른 실제
            거래가격은 매수인이 매수한 부동산을 양도하는 경우 「소득세법」 제97조제1항 및 제7항과
            같은 법 시행령 제163조제11항제2호에 따라 취득 당시의 실제 거래가액으로 보아 양도차익이
            계산될 수 있음을 유의하시기 바랍니다.
          </v-col>
        </v-row>
        <div class="text-subtitle font-weight-bold mt-4">
          Ⅰ. 개업공인중개사 기본 확인사항
        </div>
        <div class="border pl-2 pr-2 mt-4">
          <div class="text-body font-weight-bold">
            ① 대상물건의 표시
          </div>
          <div class="border">
            <div class="site-condition-label text-body-2 font-weight-bold">
              토지
            </div>
            <v-row no-gutters>
              <v-col class="d-flex flex-wrap">
                <v-col cols="12">
                  <AddressSearch
                    ref="ve.address"
                    :label="'소재지' + $t('search')"
                    :address.sync="ve.address"
                    :readonly="readonly"
                  ></AddressSearch>
                </v-col>
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.land_area"
                  label="토지 면적"
                  type="Number"
                  step="0.01"
                  :readonly="readonly"
                ></LazyTextField>
                <v-select
                  class="d-flex ve-input"
                  v-model="ve.ledger_land_category"
                  :items="$getConstList('LAND_CATEGORY_LIST')"
                  item-text="text"
                  item-value="value"
                  label="공부상지목"
                  :readonly="readonly"
                >
                  <template v-slot:selection="{ item }">{{ $t(item.text) }}</template>
                  <template v-slot:item="{ item }">{{ $t(item.text) }}</template>
                </v-select>
                <v-select
                  class="d-flex ve-input"
                  v-model="ve.actual_land_category"
                  :items="$getConstList('LAND_CATEGORY_LIST')"
                  item-text="text"
                  item-value="value"
                  label="실제 이용 상태"
                  :readonly="readonly"
                >
                  <template v-slot:selection="{ item }">{{ $t(item.text) }}</template>
                  <template v-slot:item="{ item }">{{ $t(item.text) }}</template>
                </v-select>
              </v-col>
            </v-row>
          </div>
          <div class="border">
            <div class="site-condition-label text-body-2 font-weight-bold">
              건축물
            </div>
            <v-row no-gutters>
              <v-col class="d-flex flex-wrap">
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.net_area"
                  type="Number"
                  step="0.01"
                  label="전용면적"
                  :readonly="readonly"
                ></LazyTextField>
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.land_share"
                  label="대지지분"
                  :readonly="readonly"
                ></LazyTextField>
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.year_of_completion"
                  label="준공년도(증개축년도)"
                  :readonly="readonly"
                ></LazyTextField>
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.ledger_building_category"
                  label="건축물대장상 용도"
                  :readonly="readonly"
                ></LazyTextField>
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.actual_building_category"
                  label="실제 용도"
                  :readonly="readonly"
                ></LazyTextField>
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.building_structure"
                  label="구조"
                  :readonly="readonly"
                ></LazyTextField>
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.building_direction"
                  label="방향"
                  :readonly="readonly"
                ></LazyTextField>
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.seismic_design"
                  label="내진설계 적용여부"
                  :readonly="readonly"
                ></LazyTextField>
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.seismic_capacity"
                  label="내진능력"
                  :readonly="readonly"
                ></LazyTextField>
                <v-radio-group
                  class="ve-input ve-radio-group"
                  label="건축물대장상위반건축물 여부"
                  v-model="ve.legal_status"
                  row
                  mandatory
                >
                  <v-radio label="위반" :value="false" :readonly="readonly"></v-radio>
                  <v-radio label="적법" :value="true" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  v-if="!ve.legal_status"
                  class="d-flex ve-input"
                  v-model="ve.matters_of_violation"
                  label="위반내용"
                  :readonly="readonly"
                ></LazyTextField>
              </v-col>
            </v-row>
          </div>
        </div>
        <div class="border pl-2 pr-2 mt-4">
          <div class="text-body font-weight-bold">
            ② 권리관계
          </div>
          <div class="border">
            <div class="site-condition-label text-body-2 font-weight-bold">
              등기부기재사항
            </div>
            <v-row no-gutters>
              <v-col class="d-flex flex-wrap">
                <LazyTextArea
                  class="d-flex ve-input"
                  v-model="ve.land_ownership"
                  label="토지 소유권에 관한 사항"
                  auto-grow
                  rows="2"
                  :readonly="readonly"
                ></LazyTextArea>
                <LazyTextArea
                  class="d-flex ve-input"
                  v-model="ve.building_ownership"
                  label="건축물 소유권에 관한 사항"
                  auto-grow
                  rows="2"
                  :readonly="readonly"
                ></LazyTextArea>
                <LazyTextArea
                  class="d-flex ve-input"
                  v-model="ve.land_other"
                  label="토지 소유권 외의 권리에 관한 사항"
                  auto-grow
                  rows="2"
                  :readonly="readonly"
                ></LazyTextArea>
                <LazyTextArea
                  class="d-flex ve-input"
                  v-model="ve.building_other"
                  label="건축물 소유권의 권리에 관한 사항"
                  auto-grow
                  rows="2"
                  :readonly="readonly"
                ></LazyTextArea>
              </v-col>
            </v-row>
          </div>
          <div class="border">
            <div class="site-condition-label text-body-2 font-weight-bold">
              민간임대등록여부
            </div>
            <v-radio-group
              class="d-flex ve-input ve-radio-group"
              label="민간임대 등록여부"
              v-model="ve.rental_housing_registration"
              row
              mandatory
            >
              <v-radio label="장기일반민간임대주택" :value="1" :readonly="readonly"></v-radio>
              <v-radio label="공공지원민간임대주택" :value="2" :readonly="readonly"></v-radio>
              <v-radio label="그 밖의 유형" :value="99" :readonly="readonly"></v-radio>
              <LazyTextField
                v-if="ve.rental_housing_registration == 99"
                class="d-flex ve-input"
                v-model="ve.rental_housing_registration_info"
                label="그 밖의 유형"
                :readonly="readonly"
              ></LazyTextField>
              <v-radio label="해당 사항 없음" :value="0" :readonly="readonly"></v-radio>
            </v-radio-group>
            <v-row no-gutters>
              <v-col class="d-flex flex-wrap">
                <LazyTextField
                  class="d-flex ve-input"
                  :disabled="ve.rental_housing_registration == 0"
                  v-model="ve.mandatory_lease_period"
                  type="Number"
                  step="1"
                  label="임대의무기간"
                  suffix="년"
                  :readonly="readonly"
                ></LazyTextField>
                <v-menu
                  :disabled="ve.rental_housing_registration == 0"
                  v-model="lease_initiation_date_dialog"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  min-width="auto"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      :disabled="ve.rental_housing_registration == 0"
                      v-model="ve.lease_initiation_date"
                      label="임대개시일"
                      prepend-icon="mdi-calendar"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="ve.lease_initiation_date"
                    @input="lease_initiation_date_dialog = false"
                    :locale="this.$i18n.locale"
                  ></v-date-picker>
                </v-menu>
                <NullRadioGroup
                  class=" ve-input ve-radio-group"
                  v-model="ve.right_to_lease_contract_renewal"
                  label="계약갱신요구권 행사여부"
                  row
                >
                  <v-radio
                    label="확인(확인서류 첨부)"
                    :value="true"
                    :readonly="readonly"
                  ></v-radio>

                  <v-radio label="미확인" :value="false" :readonly="readonly"></v-radio>
                  <template v-if="!(updated_at < '2021-12-31')">
                    <v-radio label="해당 없음" :value="null" :readonly="readonly"></v-radio>
                  </template>
                </NullRadioGroup>
                <template v-if="!(updated_at < '2021-12-31')">
                  <NullRadioGroup
                    class=" ve-input ve-radio-group"
                    v-model="ve.multi_family_housing_document"
                    label="다가구주택 확인서류 제출여부"
                    row
                  >
                    <v-radio
                      label="제출(확인서류 첨부)"
                      :value="true"
                      :readonly="readonly"
                    ></v-radio>
                    <v-radio label="미제출" :value="false" :readonly="readonly"></v-radio>
                    <v-radio label="해당 없음" :value="null" :readonly="readonly"></v-radio>
                  </NullRadioGroup>
                </template>
              </v-col>
            </v-row>
          </div>
        </div>
        <div class="border pl-2 pr-2 mt-4">
          <div class="text-body font-weight-bold">
            ③ 토지이용계획, 공법상 이용제한 및 거래규제에 관한 사항(토지)
          </div>
          <div class="border">
            <v-row no-gutters>
              <v-col class="d-flex flex-wrap">
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.use_area"
                  label="용도지역"
                  :readonly="readonly"
                ></LazyTextField>
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.use_district"
                  label="용도지구"
                  :readonly="readonly"
                ></LazyTextField>
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.use_zone"
                  label="용도구역"
                  :readonly="readonly"
                ></LazyTextField>
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.building_coverage_limit"
                  type="Number"
                  step="1"
                  label="건페율 상한"
                  suffix="%"
                  :readonly="readonly"
                ></LazyTextField>
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.floor_area_limit"
                  type="Number"
                  step="1"
                  label="용적률 상한"
                  suffix="%"
                  :readonly="readonly"
                ></LazyTextField>
                <LazyTextArea
                  class="d-flex ve-input"
                  v-model="ve.planning_facilities"
                  label="도시·군계획 시설"
                  auto-grow
                  rows="1"
                  :readonly="readonly"
                ></LazyTextArea>
                <v-checkbox
                  class="d-flex ve-input"
                  v-model="ve.permission_reposrt_zone"
                  label="토지거래허가 신고구역"
                  :readonly="readonly"
                ></v-checkbox>
                <v-radio-group
                  class="d-flex ve-input ve-radio-group"
                  label="투기지역 여부"
                  v-model="ve.speculative_area"
                  row
                >
                  <v-radio label="토지투기지역" :value="1" :readonly="readonly"></v-radio>
                  <v-radio label="주택투기지역" :value="2" :readonly="readonly"></v-radio>
                  <v-radio label="투기과열지구" :value="3" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextArea
                  class="d-flex ve-input"
                  v-model="ve.unit_planning_area_others"
                  label="지구단위계획구역, 그 밖의 도시·군관리계획"
                  hint="지구단위계획구역, 그 밖의 도시·군관리계획"
                  auto-grow
                  rows="1"
                  :readonly="readonly"
                ></LazyTextArea>
                <LazyTextArea
                  class="d-flex ve-input"
                  v-model="ve.other_use_restriction"
                  label="그 밖의 이용제한 및 거래규제사항"
                  auto-grow
                  rows="1"
                  :readonly="readonly"
                ></LazyTextArea>
              </v-col>
            </v-row>
          </div>
        </div>
      </template>
      <template v-if="step == 3 || validation_check">
        <div class="caption">
          <span class="float-right">(4쪽 중 제2쪽)</span>
        </div>
        <div class="border pl-2 pr-2 mt-4">
          <div class="text-body font-weight-bold">
            ④ 입지조건
          </div>
          <div class="border">
            <v-row no-gutters>
              <v-col class="d-flex flex-wrap">
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.relative_with_roads"
                  label="도로와의 관계"
                  suffix="도로에 접함"
                  :readonly="readonly"
                ></LazyTextField>
                <v-radio-group class="ve-input" v-model="ve.is_paved_rode" row mandatory>
                  <v-radio label="포장" :value="true" :readonly="readonly"></v-radio>
                  <v-radio label="비포장" :value="false" :readonly="readonly"></v-radio>
                </v-radio-group>
                <v-radio-group
                  class=" ve-input ve-radio-group"
                  v-model="ve.accessibility"
                  label="접근성"
                  row
                  mandatory
                >
                  <v-radio label="용이함" :value="true" :readonly="readonly"></v-radio>
                  <v-radio label="불편함" :value="false" :readonly="readonly"></v-radio>
                </v-radio-group>
              </v-col>
            </v-row>
          </div>
          <div class="border">
            <div class="site-condition-label text-body-2 font-weight-bold">
              대중교통
            </div>
            <v-row no-gutters>
              <v-col class="d-flex flex-wrap">
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.bus_stop"
                  label="버스 정류장"
                  suffix="정류장"
                  :readonly="readonly"
                ></LazyTextField>
                <v-radio-group
                  class="ve-input ve-radio-group"
                  v-model="ve.bus_by_foot"
                  label="소요시간"
                  row
                  mandatory
                >
                  <v-radio label="도보" :value="true" :readonly="readonly"></v-radio>
                  <v-radio label="차량" :value="false" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  class="d-flex ve-input site-condition-minute"
                  v-model="ve.bus_required_time"
                  type="Number"
                  prefix="약"
                  suffix="분"
                  :readonly="readonly"
                ></LazyTextField>

                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.subway_station"
                  label="지하철 역"
                  suffix="역"
                  :readonly="readonly"
                ></LazyTextField>
                <v-radio-group
                  class="ve-input ve-radio-group"
                  v-model="ve.subway_by_foot"
                  label="소요시간"
                  row
                >
                  <v-radio label="도보" :value="true" :readonly="readonly"></v-radio>
                  <v-radio label="차량" :value="false" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  class="d-flex ve-input site-condition-minute"
                  v-model="ve.subway_required_time"
                  type="Number"
                  prefix="약"
                  suffix="분"
                  :readonly="readonly"
                ></LazyTextField>
              </v-col>
            </v-row>
          </div>
          <div class="border">
            <v-row class="ml-2" no-gutters>
              <v-col class="d-flex flex-wrap">
                <v-radio-group v-model="ve.parking_lot" label="주차장" row mandatory>
                  <v-radio label="없음" :value="0" :readonly="readonly"></v-radio>
                  <v-radio label="전용주차시설" :value="1" :readonly="readonly"></v-radio>
                  <v-radio label="공동주차시설" :value="2" :readonly="readonly"></v-radio>
                  <v-radio label="그 밖의 주차시설" :value="99" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  v-if="ve.parking_lot == 99"
                  class="d-flex ve-input"
                  v-model="ve.parking_lot_info"
                  label="그 밖의 주차시설 상세정보"
                  :readonly="readonly"
                ></LazyTextField>
              </v-col>
            </v-row>
          </div>
          <div class="border">
            <div class="site-condition-label text-body-2 font-weight-bold">
              교육시설
            </div>
            <v-row no-gutters>
              <v-col class="d-flex flex-wrap">
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.elementary_school"
                  label="초등학교"
                  suffix="학교"
                  :readonly="readonly"
                ></LazyTextField>
                <v-radio-group
                  class="ve-input ve-radio-group"
                  v-model="ve.elementary_school_by_foot"
                  label="소요시간"
                  row
                  mandatory
                >
                  <v-radio label="도보" :value="true" :readonly="readonly"></v-radio>
                  <v-radio label="차량" :value="false" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  class="d-flex ve-input site-condition-minute"
                  v-model="ve.elementary_school_required_time"
                  type="Number"
                  prefix="약"
                  suffix="분"
                  :readonly="readonly"
                ></LazyTextField>

                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.middle_school"
                  label="중학교"
                  suffix="학교"
                  :readonly="readonly"
                ></LazyTextField>
                <v-radio-group
                  class="ve-input ve-radio-group"
                  v-model="ve.middle_school_by_foot"
                  label="소요시간"
                  row
                  mandatory
                >
                  <v-radio label="도보" :value="true" :readonly="readonly"></v-radio>
                  <v-radio label="차량" :value="false" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  class="d-flex ve-input site-condition-minute"
                  v-model="ve.middle_school_required_time"
                  type="Number"
                  prefix="약"
                  suffix="분"
                  :readonly="readonly"
                ></LazyTextField>

                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.high_school"
                  label="고등학교"
                  suffix="학교"
                  :readonly="readonly"
                ></LazyTextField>
                <v-radio-group
                  class="ve-input ve-radio-group"
                  v-model="ve.high_school_by_foot"
                  label="소요시간"
                  row
                  mandatory
                >
                  <v-radio label="도보" :value="true" :readonly="readonly"></v-radio>
                  <v-radio label="차량" :value="false" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  class="d-flex ve-input site-condition-minute"
                  v-model="ve.high_school_required_time"
                  type="Number"
                  prefix="약"
                  suffix="분"
                  :readonly="readonly"
                ></LazyTextField>
              </v-col>
            </v-row>
          </div>
          <div class="border">
            <div class="site-condition-label text-body-2 font-weight-bold">
              판매 및 의료시설
            </div>
            <v-row no-gutters>
              <v-col class="d-flex flex-wrap">
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.department_store"
                  label="백화점 및 할인매장"
                  :readonly="readonly"
                ></LazyTextField>
                <v-radio-group
                  class="ve-input ve-radio-group"
                  v-model="ve.department_store_by_foot"
                  label="소요시간"
                  row
                  mandatory
                >
                  <v-radio label="도보" :value="true" :readonly="readonly"></v-radio>
                  <v-radio label="차량" :value="false" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  class="d-flex ve-input site-condition-minute"
                  v-model="ve.department_store_required_time"
                  type="Number"
                  prefix="약"
                  suffix="분"
                  :readonly="readonly"
                ></LazyTextField>

                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.medical_center"
                  label="종합의료시설"
                  :readonly="readonly"
                ></LazyTextField>
                <v-radio-group
                  class="ve-input ve-radio-group"
                  v-model="ve.medical_center_by_foot"
                  label="소요시간"
                  row
                  mandatory
                >
                  <v-radio label="도보" :value="true" :readonly="readonly"></v-radio>
                  <v-radio label="차량" :value="false" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  class="d-flex ve-input site-condition-minute"
                  v-model="ve.medical_center_required_time"
                  type="Number"
                  prefix="약"
                  suffix="분"
                  :readonly="readonly"
                ></LazyTextField>
              </v-col>
            </v-row>
          </div>
        </div>
        <div class="border pl-2 pr-2 mt-4">
          <div class="text-body font-weight-bold">
            ⑤ 관리에 관한사항
          </div>
          <v-row no-gutters>
            <v-col class="d-flex flex-wrap">
              <v-radio-group
                class="ve-input ve-radio-group"
                v-model="ve.is_security_office"
                label="경비실"
                row
                mandatory
              >
                <v-radio label="있음" :value="true" :readonly="readonly"></v-radio>
                <v-radio label="없음" :value="false" :readonly="readonly"></v-radio>
              </v-radio-group>
              <v-radio-group
                class="ve-input ve-radio-group"
                v-model="ve.management"
                label="관리주체"
                row
                mandatory
              >
                <v-radio label="위탁관리" :value="1" :readonly="readonly"></v-radio>
                <v-radio label="자체관리" :value="2" :readonly="readonly"></v-radio>
                <v-radio label="그 밖의 유형" :value="99" :readonly="readonly"></v-radio>
              </v-radio-group>
            </v-col>
          </v-row>
        </div>
        <div class="border pl-2 pr-2 mt-4">
          <div class="text-body font-weight-bold">
            ⑥ 비선호시설(1km이내)
          </div>
          <v-row no-gutters>
            <v-col class="d-flex flex-wrap">
              <v-radio-group
                class="ve-input ve-radio-group"
                v-model="ve.undesirable_facilities"
                label="비선호시설"
                row
                mandatory
              >
                <v-radio label="없음" :value="false" :readonly="readonly"></v-radio>
                <v-radio label="있음" :value="true" :readonly="readonly"></v-radio>
              </v-radio-group>
              <LazyTextField
                v-if="ve.undesirable_facilities == true"
                class="d-flex ve-input"
                v-model="ve.undesirable_facilities_info"
                label="종류 및 위치"
                :readonly="readonly"
              ></LazyTextField>
            </v-col>
          </v-row>
        </div>
        <div class="border pl-2 pr-2 mt-4">
          <div class="text-body font-weight-bold">
            ⑦ 거래예정금액 등
          </div>
          <v-row no-gutters>
            <v-col class="d-flex flex-wrap">
              <LazyTextField
                class="d-flex ve-input"
                v-model="ve.expected_transaction_price"
                label="거래예정금액"
                type="Number"
                :readonly="readonly"
              ></LazyTextField>
              <LazyTextField
                class="d-flex ve-input"
                v-model="ve.land_price_recorded"
                label="개별공시지가(㎡당)"
                type="Number"
                :readonly="readonly"
              ></LazyTextField>
              <LazyTextField
                class="d-flex ve-input"
                v-model="ve.building_price_recorded"
                label="건물(주택)공시가격"
                type="Number"
                :readonly="readonly"
              ></LazyTextField>
            </v-col>
          </v-row>
        </div>
        <div class="border pl-2 pr-2 mt-4">
          <div class="text-body font-weight-bold">
            ⑧ 취득 시부담할 조세의 종류 및 세율
          </div>
          <v-row>
            <v-col cols="4">
              <LazyTextField
                v-model="ve.acquisition_tax"
                label="취득세"
                type="Number"
                step="0.01"
                suffix="%"
                :readonly="readonly"
              ></LazyTextField>
            </v-col>
            <v-col cols="4">
              <LazyTextField
                v-model="ve.special_tax"
                label="농어촌특별세"
                type="Number"
                step="0.01"
                suffix="%"
                :readonly="readonly"
              ></LazyTextField>
            </v-col>
            <v-col cols="4">
              <LazyTextField
                v-model="ve.local_education_tax"
                label="지방교육세"
                type="Number"
                step="0.01"
                suffix="%"
                :readonly="readonly"
              ></LazyTextField>
            </v-col>
          </v-row>
          <div class="text-caption">
            ※ 재산세는 6월 1일 기준 대상물건 소유자가 납세의무를 부담
          </div>
        </div>
      </template>
      <template v-if="step == 4 || validation_check">
        <div class="caption">
          <span class="float-right">(4쪽 중 제2쪽)</span>
        </div>
        <div class="text-subtitle font-weight-bold mt-4">
          Ⅱ. 개업공인중개사 세부 확인사항
        </div>
        <v-row no-gutters>
          <v-col cols="12">
            <LazyTextArea
              class="mt-4"
              v-model="ve.actual_legal_right_relationship"
              label="실제 권리관계 또는 공시되지 않은물건의 권리 사항"
              placeholder="실제 권리관계 또는 공시되지 않은물건의 권리 사항"
              outlined
              auto-grow
              rows="2"
              :readonly="readonly"
            ></LazyTextArea>
          </v-col>
        </v-row>
        <div class="border pl-2 pr-2 mt-4">
          <div class="text-body font-weight-bold">
            ⑩ 내부·외부 시설물의 상태 (건축물)
          </div>
          <div class="border">
            <v-row no-gutters>
              <v-col class="d-flex flex-wrap">
                <v-radio-group
                  class="d-flex ve-input ve-radio-group"
                  v-model="ve.water_damage_status"
                  label="수도 파손여부"
                  row
                  mandatory
                >
                  <v-radio label="없음" :value="false" :readonly="readonly"></v-radio>
                  <v-radio label="있음" :value="true" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  v-if="ve.water_damage_status == true"
                  class="d-flex ve-input"
                  v-model="ve.water_damage_status_info"
                  label="파손 위치"
                  :readonly="readonly"
                ></LazyTextField>
                <v-radio-group
                  class="d-flex ve-input ve-radio-group"
                  v-model="ve.water_capacity_status"
                  label="수도 용수량"
                  row
                  mandatory
                >
                  <v-radio label="정상" :value="true" :readonly="readonly"></v-radio>
                  <v-radio label="부족함" :value="false" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  v-if="ve.water_capacity_status == false"
                  class="d-flex ve-input"
                  v-model="ve.water_capacity_status_info"
                  label="부족한 위치"
                  :readonly="readonly"
                ></LazyTextField>
                <v-radio-group
                  class="d-flex ve-input ve-radio-group"
                  v-model="ve.electricity_supply_status"
                  label="전기 공급상태"
                  row
                  mandatory
                >
                  <v-radio label="정상" :value="true" :readonly="readonly"></v-radio>
                  <v-radio label="교체필요" :value="false" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  v-if="ve.electricity_supply_status == false"
                  class="d-flex ve-input"
                  v-model="ve.electricity_supply_status_info"
                  label="교체할 부분"
                  :readonly="readonly"
                ></LazyTextField>

                <v-radio-group
                  class="d-flex ve-input ve-radio-group"
                  v-model="ve.gas_supply_status"
                  label="가스(취사용) 공급방식"
                  row
                  mandatory
                >
                  <v-radio label="도시가스" :value="true" :readonly="readonly"></v-radio>
                  <v-radio label="그 밖의 방식" :value="false" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  v-if="ve.gas_supply_status == false"
                  class="d-flex ve-input"
                  v-model="ve.gas_supply_status_info"
                  label="위치"
                  :readonly="readonly"
                ></LazyTextField>
                <v-radio-group
                  class="d-flex ve-input ve-radio-group"
                  v-model="ve.is_fire_alarm_detector"
                  label="소방 단독경보형감지기"
                  row
                  mandatory
                >
                  <v-radio label="없음" :value="false" :readonly="readonly"></v-radio>
                  <v-radio label="있음" :value="true" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  v-if="ve.is_fire_alarm_detector == true"
                  class="d-flex ve-input"
                  v-model="ve.fire_alarm_detector_quantity"
                  type="Number"
                  label="수량"
                  suffix="개"
                  :readonly="readonly"
                ></LazyTextField>
                <div class="d-flex text-caption">
                  ※「화재예방, 소방시설 설치·유지 및 안전관리에 관한 법률」 제8조 및 같은 법 시행령
                  제13조에 따른 주택용 소방시설로서 아파트(주택으로 사용하는 층수가 5개층 이상인
                  주택을 말한다)를 제외한 주택의 경우만 작성합니다.
                </div>
                <v-radio-group
                  class="d-flex ve-input ve-radio-group"
                  v-model="ve.heating_supply_method"
                  label="난방 공급방식"
                  row
                  mandatory
                >
                  <v-radio label="중앙공급" :value="1" :readonly="readonly"></v-radio>
                  <v-radio label="개별공급" :value="2" :readonly="readonly"></v-radio>
                </v-radio-group>
                <v-radio-group
                  class="d-flex ve-input ve-radio-group"
                  v-model="ve.heating_status"
                  label="난방 시설작동"
                  row
                  mandatory
                >
                  <v-radio label="정상" :value="true" :readonly="readonly"></v-radio>
                  <v-radio label="수선필요" :value="false" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  v-if="ve.heating_status == false"
                  class="d-flex ve-input"
                  v-model="ve.heating_status_info"
                  label="상세정보"
                  :readonly="readonly"
                ></LazyTextField>
                <v-radio-group
                  class="d-flex ve-input ve-radio-group"
                  v-model="ve.heating_type"
                  label="난방 종류"
                  row
                  mandatory
                >
                  <v-radio label="도시가스" :value="1" :readonly="readonly"></v-radio>
                  <v-radio label="기름" :value="2" :readonly="readonly"></v-radio>
                  <v-radio label="프로판가스" :value="3" :readonly="readonly"></v-radio>
                  <v-radio label="연탄" :value="4" :readonly="readonly"></v-radio>
                  <v-radio label="그 밖의 종류" :value="99" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  v-if="ve.heating_type == 5"
                  class="d-flex ve-input"
                  v-model="ve.heating_type_info"
                  label="난방 종류 상세정보"
                  :readonly="readonly"
                ></LazyTextField>

                <v-radio-group
                  class="d-flex ve-input ve-radio-group"
                  v-model="ve.is_elevator"
                  label="승강기"
                  row
                  mandatory
                >
                  <v-radio label="있음" :value="true" :readonly="readonly"></v-radio>
                  <v-radio label="없음" :value="false" :readonly="readonly"></v-radio>
                </v-radio-group>
                <v-radio-group
                  v-if="ve.is_elevator"
                  class="d-flex ve-input"
                  v-model="ve.elevator_status"
                  label="승강기 상태"
                  row
                  mandatory
                >
                  <v-radio label="양호" :value="true" :readonly="readonly"></v-radio>
                  <v-radio label="불량" :value="false" :readonly="readonly"></v-radio>
                </v-radio-group>
                <v-radio-group
                  class="d-flex ve-input ve-radio-group"
                  v-model="ve.drainage_status"
                  label="배수"
                  row
                  mandatory
                >
                  <v-radio label="정상" :value="true" :readonly="readonly"></v-radio>
                  <v-radio label="수선필요" :value="false" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  v-if="ve.drainage_status == false"
                  class="d-flex ve-input"
                  v-model="ve.drainage_status_info"
                  label="상세정보"
                  :readonly="readonly"
                ></LazyTextField>
                <LazyTextField
                  class="ve-input"
                  v-model="ve.other_facilities"
                  label="그 밖의 시설물"
                  :readonly="readonly"
                ></LazyTextField>
              </v-col>
            </v-row>
          </div>
        </div>
        <div class="caption">
          <span class="float-right">(4쪽 중 제3쪽)</span>
        </div>
        <div class="border pl-2 pr-2 mt-4">
          <div class="text-body font-weight-bold">
            ⑪ 벽면 및 도배상태
          </div>
          <div class="border">
            <v-row no-gutters>
              <v-col class="d-flex flex-wrap">
                <v-radio-group
                  class="d-flex ve-input ve-radio-group"
                  v-model="ve.wall_crack_status"
                  label="벽면 균열"
                  row
                  mandatory
                >
                  <v-radio label="없음" :value="false" :readonly="readonly"></v-radio>
                  <v-radio label="있음" :value="true" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  v-if="ve.wall_crack_status == true"
                  class="d-flex ve-input"
                  v-model="ve.wall_crack_status_info"
                  label="위치"
                  :readonly="readonly"
                ></LazyTextField>
                <v-radio-group
                  class="d-flex ve-input ve-radio-group"
                  v-model="ve.water_leak_status"
                  label="벽면 누수"
                  row
                  mandatory
                >
                  <v-radio label="없음" :value="false" :readonly="readonly"></v-radio>
                  <v-radio label="있음" :value="true" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  v-if="ve.water_leak_status == true"
                  class="d-flex ve-input"
                  v-model="ve.water_leak_status_info"
                  label="위치"
                  :readonly="readonly"
                ></LazyTextField>
                <v-radio-group
                  v-if="!(updated_at < '2021-12-31')"
                  class="d-flex ve-input ve-radio-group"
                  v-model="ve.floor_surface_status"
                  label="바닥면"
                  row
                  mandatory
                >
                  <v-radio label="깨끗함" :value="2" :readonly="readonly"></v-radio>
                  <v-radio label="보통임" :value="1" :readonly="readonly"></v-radio>
                  <v-radio label="수리 필요" :value="0" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  v-if="ve.floor_surface_status === 0"
                  class="d-flex ve-input"
                  v-model="ve.floor_surface_status_info"
                  label="위치"
                  :readonly="readonly"
                ></LazyTextField>
                <v-radio-group
                  class="d-flex ve-input ve-radio-group"
                  v-model="ve.wall_paper_status"
                  label="도배"
                  row
                  mandatory
                >
                  <v-radio label="깨끗함" :value="2" :readonly="readonly"></v-radio>
                  <v-radio label="보통임" :value="1" :readonly="readonly"></v-radio>
                  <v-radio label="도배필요" :value="0" :readonly="readonly"></v-radio>
                </v-radio-group>
              </v-col>
            </v-row>
          </div>
        </div>
        <div class="border pl-2 pr-2 mt-4">
          <div class="text-body font-weight-bold">
            ⑫ 환경조건
          </div>
          <div class="border">
            <v-row>
              <v-col class="d-flex flex-wrap">
                <v-radio-group
                  class="d-flex ve-input ve-radio-group"
                  v-model="ve.sunshine_status"
                  label="일조량"
                  row
                  mandatory
                >
                  <v-radio label="풍부함" :value="2" :readonly="readonly"></v-radio>
                  <v-radio label="보통임" :value="1" :readonly="readonly"></v-radio>
                  <v-radio label="불충분" :value="0" :readonly="readonly"></v-radio>
                </v-radio-group>
                <LazyTextField
                  v-if="ve.sunshine_status == 0"
                  class="d-flex ve-input"
                  v-model="ve.sunshine_status_info"
                  label="불충분 이유"
                  :readonly="readonly"
                ></LazyTextField>
                <v-radio-group
                  class="d-flex ve-input ve-radio-group"
                  v-model="ve.noise_status"
                  label="소음"
                  row
                  mandatory
                >
                  <v-radio label="미미함" :value="2" :readonly="readonly"></v-radio>
                  <v-radio label="보통임" :value="1" :readonly="readonly"></v-radio>
                  <v-radio label="심한편임" :value="0" :readonly="readonly"></v-radio>
                </v-radio-group>
                <v-radio-group
                  class="d-flex ve-input ve-radio-group"
                  v-model="ve.vibration"
                  label="진동"
                  row
                  mandatory
                >
                  <v-radio label="미미함" :value="2" :readonly="readonly"></v-radio>
                  <v-radio label="보통임" :value="1" :readonly="readonly"></v-radio>
                  <v-radio label="심한편임" :value="0" :readonly="readonly"></v-radio>
                </v-radio-group>
              </v-col>
            </v-row>
          </div>
        </div>
        <div class="text-subtitle font-weight-bold mt-4">
          Ⅲ. 중개보수 등에 관한 사항
        </div>
        <div class="border pl-2 pr-2 mt-4">
          <div class="text-body font-weight-bold">
            ⑬ 중개보수 및 실비의 금액과 산출내역
          </div>
          <div class="border">
            <v-row no-gutters>
              <v-col class="d-flex flex-wrap">
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.comission"
                  type="Number"
                  label="중개보수"
                  :readonly="readonly"
                ></LazyTextField>
                <LazyTextField
                  class="d-flex ve-input"
                  v-model="ve.actual_expenses"
                  type="Number"
                  label="실비"
                  :readonly="readonly"
                ></LazyTextField>
                <LazyTextField
                  class="d-flex ve-input"
                  :value="parseInt(ve.comission) + parseInt(ve.actual_expenses)"
                  label="합계"
                  readonly
                ></LazyTextField>
                <LazyTextArea
                  class="d-flex ve-input"
                  v-model="ve.payment_period"
                  label="지급시기"
                  auto-grow
                  rows="1"
                  :readonly="readonly"
                ></LazyTextArea>
              </v-col>
            </v-row>
            <v-row no-gutters>
              <LazyTextArea
                class="ve-input"
                v-model="ve.calculation_info"
                label="중개보수 산출내역"
                auto-grow
                rows="3"
                :readonly="readonly"
              ></LazyTextArea>
            </v-row>
          </div>
        </div>
      </template>
    </v-form>
    <div>
      <slot name="footer"></slot>
    </div>
    <template v-if="step != 1">
      <div class="text-subtitle font-weight-bold mt-4 text-center">
        확인설명서 별지
      </div>
      <v-row no-gutters>
        <v-col cols="12">
          <LazyTextArea
            class="mt-4"
            v-model="ve.additional_info"
            label="확인설명서 별지 내용"
            placeholder="확인설명서 별지 내용"
            outlined
            auto-grow
            rows="2"
            :readonly="readonly"
          ></LazyTextArea>
        </v-col>
      </v-row>
    </template>
    <slot name="insurance"></slot>
  </div>
</template>

<script>
import NullRadioGroup from "@/components/NullRadioGroup";
export default {
  name: "VerifyingExplanationEditor",
  components: {
    NullRadioGroup
  },
  props: {
    ve: {
      type: Object,
      required: true
    },
    step: {
      type: Number,
      required: false
    },
    validation_check: {
      type: Boolean,
      required: true
    },
    readonly: {
      type: Boolean,
      required: false,
      default: false
    },
    updated_at: {
      type: Date,
      required: false
    }
  },
  data() {
    return {
      lease_initiation_date_dialog: false,
      valid: true
    };
  },
  watch: {
    step() {
      window.scrollTo(0, 0);
    }
  }
};
</script>

<style scoped>
legend {
  font-weight: bold;
}
.flex-text-verical-center {
  align-items: center;
}
.ve-radio-group legend:after {
  content: ":";
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
.label {
  margin: auto;
}
.col {
  word-break: break-all;
}
.border {
  border: solid 1px rgba(0, 0, 0, 0.12);
}
.site-condition-label {
  padding: 0px 8px 0px 8px;
  margin-top: 16px;
}
.site-condition-minute {
  max-width: 70px;
}
</style>
