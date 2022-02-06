<template>
  <div class="ve mt-2 pa-0">
    <table
      border="1"
      style="border-collapse:collapse;"
      class="a4 MsoNormalTable"
      cellspacing="0"
      cellpadding="0"
      width="800"
    >
      <tr>
        <td class="caption" style="border:0;" width="510" colspan="14" valign="top">
          <div>
            ■ 공인중개사법 시행규칙 [별지 제20호서식]
            <span class="blue--text text--accent-4"
              >&lt;{{ $t("ve_amendment_updated_date", { updated_at: "2021.1. 12." }) }}&gt;</span
            >
          </div>
        </td>
        <td
          class="caption"
          style="border:0;"
          width="128"
          colspan="4"
          valign="bottom"
          align="right"
        >
          <div>(4쪽 중 제1쪽)</div>
        </td>
      </tr>
      <tr>
        <td class="ve-title" style="border:0;" colspan="18" valign="top" align="center">
          <b style="font-size: 16pt">중개대상물 확인 · 설명서[Ⅰ] (주거용 건축물)</b>
        </td>
      </tr>
      <tr>
        <td style="border:0;" colspan="18">
          <div align="center">
            <b style="font-size: 12pt"
              >( [ {{ ve.paper_categories.includes(1) ? "√" : "" }} ]단독주택[
              {{ ve.paper_categories.includes(2) ? "√" : "" }} ]공동주택[
              {{ ve.paper_categories.includes(3) ? "√" : "" }} ]매매·교환[
              {{ ve.paper_categories.includes(4) ? "√" : "" }} ]임대 )</b
            >
          </div>
        </td>
      </tr>
      <tr>
        <td style="border-top:0;" colspan="18"></td>
      </tr>
      <tr>
        <td class="border-trb" width="102" colspan="3" rowspan="2">
          <div align="center">
            확인·설명 <br />
            자료
          </div>
        </td>
        <td width="92" colspan="2">
          <div class="label">
            확인·설명 <br />
            근거자료 등
          </div>
        </td>
        <td class="border-tbl" width="444" colspan="13">
          <div>
            [ {{ ve.explanation_evidences.includes(1) ? "√" : "" }} ]등기권리증[
            {{ ve.explanation_evidences.includes(2) ? "√" : "" }} ]등기사항증명서[
            {{ ve.explanation_evidences.includes(3) ? "√" : "" }} ]토지대장[
            {{ ve.explanation_evidences.includes(4) ? "√" : "" }} ]건축물대장 [
            {{ ve.explanation_evidences.includes(5) ? "√" : "" }} ]지적도 <br />[
            {{ ve.explanation_evidences.includes(6) ? "√" : "" }} ]임야도 [
            {{ ve.explanation_evidences.includes(7) ? "√" : "" }} ]토지이용계획확인서 [
            {{ ve.explanation_evidences.includes(99) ? "√" : "" }} ]그 밖의 자료({{
              ve.explanation_evidence_info
            }})
          </div>
        </td>
      </tr>
      <tr>
        <td width="92" colspan="2">
          <div class="label">
            대상물건의 <br />
            상태에 관한 <br />
            자료요구 사항
          </div>
        </td>
        <td class="border-tbl" width="444" colspan="13">
          <div>
            {{ ve.requesting_condition_info }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb pt-2" width="800" colspan="18">
          <div
            style="padding:0px; border-color:#535353; border-style:solid; border-bottom-width: 4px;"
          ></div>
        </td>
      </tr>
      <tr class="grey">
        <td style="border-width: 1px 0px 1px 0px;" width="800" colspan="18">
          <div align="center">유의사항</div>
        </td>
      </tr>
      <tr>
        <td class="border-trb" width="152" colspan="3">
          <div class="label">
            개업공인중개사의 <br />
            확인·설명 의무
          </div>
        </td>
        <td class="border-tbl" width="536" colspan="15">
          <div>
            개업공인중개사는 중개대상물에 관한 권리를 취득하려는 중개의뢰인에게 성실·정확하게
            설명하고, 토지대장 등본, 등기사항증명서 등 설명의 근거자료를 제시해야 합니다.
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-trb" width="152" colspan="3">
          <div class="label">
            실제 거래가격 <br />
            신고
          </div>
        </td>
        <td class="border-tbl" width="536" colspan="15">
          <div>
            「부동산 거래신고 등에 관한 법률」 제3조 및 같은 법 시행령 별표 1 제1호마목에 따른 실제
            거래가격은 매수인이 매수한 부동산을 양도하는 경우 「소득세법」 제97조제1항 및 제7항과
            같은 법 시행령 제163조제11항제2호에 따라 취득 당시의 실제 거래가액으로 보아 양도차익이
            계산될 수 있음을 유의하시기 바랍니다.
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="21" valign="bottom">
          <div class="mt-1"><b>Ⅰ</b><b>. </b><b>개업공인중개사 기본 확인사항</b></div>
        </td>
      </tr>
      <tr>
        <td class="label border-trb" width="75" rowspan="9">
          <div class="label">①대상물건의<br />표시</div>
        </td>
        <td class="label" width="70" colspan="3" rowspan="3">
          <div>토지</div>
        </td>
        <td class="label border-tbl" width="93" colspan="2">
          <div>소재지</div>
        </td>
        <td class="border-tbl" width="401" colspan="12">
          <div>
            {{ ve.address.old_address }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="2" rowspan="2">
          <div>면적(㎡)</div>
        </td>
        <td width="110" colspan="3" rowspan="2">
          <div>{{ ve.land_area }}㎡</div>
        </td>
        <td class="label" width="55" colspan="1" rowspan="2">
          <div>지목</div>
        </td>
        <td class="label" width="98" colspan="3">
          <div>공부상 지목</div>
        </td>
        <td class="border-tbl" width="137" colspan="5">
          <div>
            {{ $getConstI18("LAND_CATEGORY", ve.ledger_land_category) }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="98" colspan="3">
          <div>실제 이용 상태</div>
        </td>
        <td class="border-tbl" width="137" colspan="5">
          <div>
            {{ $getConstI18("LAND_CATEGORY", ve.actual_land_category) }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="70" colspan="3" rowspan="6">
          <div>건축물</div>
        </td>
        <td class="label" width="93" colspan="2">
          <div>전용면적(㎡)</div>
        </td>
        <td width="165" colspan="4">
          <div>{{ ve.net_area }}㎡</div>
        </td>
        <td class="label" width="98" colspan="3">
          <div>대지지분(㎡)</div>
        </td>
        <td class="border-tbl" width="137" colspan="5">
          <div>
            {{ ve.land_share }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="2" rowspan="2">
          <div>준공년도<br />(증개축년도)</div>
        </td>
        <td width="110" colspan="3" rowspan="2">
          <div>{{ ve.year_of_completion }}년</div>
        </td>
        <td class="label" width="55" colspan="1" rowspan="2">
          <div>용도</div>
        </td>
        <td class="label" width="98" colspan="3">
          <div>건축물대장상 용도</div>
        </td>
        <td class="border-tbl" width="137" colspan="5">
          <div>
            {{ ve.ledger_building_category }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="98" colspan="3">
          <div>실제 용도</div>
        </td>
        <td class="border-tbl" width="137" colspan="5">
          <div>
            {{ ve.actual_building_category }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="2">
          <div>구조</div>
        </td>
        <td width="110" colspan="3">
          <div>
            {{ ve.building_structure }}
          </div>
        </td>
        <td class="label" width="153" colspan="4">
          <div>방향</div>
        </td>
        <td class="border-tbl" width="137" colspan="5">
          <div>
            {{ ve.building_direction }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="2">
          <div>내진설계 적용여부</div>
        </td>
        <td width="110" colspan="3">
          <div>
            {{ ve.seismic_design }}
          </div>
        </td>
        <td class="label" width="153" colspan="4">
          <div>내진능력</div>
        </td>
        <td class="border-tbl" width="137" colspan="5">
          <div>
            {{ ve.seismic_capacity }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="2">
          <div>
            건축물대장상 <br />
            위반건축물 여부
          </div>
        </td>
        <td width="110" colspan="3">
          <div>
            [ {{ ve.legal_status ? "" : "√" }} ]위반[ {{ ve.legal_status ? "√" : "" }} ]적법
          </div>
        </td>
        <td class="label" width="55" colspan="1">
          <div>위반내용</div>
        </td>
        <td class="border-tbl" width="235" colspan="8">
          <div>
            {{ ve.matters_of_violation }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="20">
          <div></div>
        </td>
      </tr>
      <tr>
        <td class="label border-trb" width="75" rowspan="7">
          <div>②권리관계</div>
        </td>
        <td class="label" width="70" colspan="3" rowspan="3">
          <div>등기부<br />기재사항</div>
        </td>
        <td class="label" width="258" colspan="6">
          <div>소유권에 관한 사항</div>
        </td>
        <td class="label border-tbl" width="235" colspan="9">
          <div>소유권 외의 권리사항</div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="2">
          <div>토지</div>
        </td>
        <td width="165" colspan="4">
          <div>
            {{ ve.land_ownership }}
          </div>
        </td>
        <td class="label" width="75">
          <div>토지</div>
        </td>
        <td class="border-tbl" width="160" colspan="8">
          <div>
            {{ ve.land_other }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="2">
          <div>건축물</div>
        </td>
        <td class="border-tbl" width="165" colspan="4">
          <div>
            {{ ve.building_ownership }}
          </div>
        </td>
        <td class="label" width="75">
          <div>건축물</div>
        </td>
        <td class="border-tbl" width="160" colspan="8">
          <div>
            {{ ve.building_other }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="70" colspan="2" rowspan="3">
          <div>
            민간<br />임대<br />
            등록<br />여부
          </div>
        </td>
        <td class="label" width="35" rowspan="2">
          <div>등록</div>
        </td>
        <td class="border-tbl" width="495" colspan="15">
          <div>
            [ {{ ve.rental_housing_registration == 1 ? "√" : "" }} ]장기일반민간임대주택 [
            {{ ve.rental_housing_registration == 2 ? "√" : "" }} ]공공지원민간임대주택 <br />
            [ {{ ve.rental_housing_registration == 99 ? "√" : "" }} ] 그 밖의 유형 ({{
              ve.rental_housing_registration == 99 ? ve.rental_housing_registration_info : ""
            }})
          </div>
        </td>
      </tr>
      <tr>
        <td colspan="2">
          <div>임대의무기간</div>
        </td>
        <td class="border-tbl" colspan="4">
          <div>
            {{
              `${
                ve.rental_housing_registration != 0 ? ve.mandatory_lease_period + $t("year") : ""
              }`
            }}
          </div>
        </td>
        <td colspan="2">
          <div>임대개시일</div>
        </td>
        <td class="border-tbl" colspan="7">
          <div>
            {{ `${ve.rental_housing_registration != 0 ? ve.lease_initiation_date : ""}` }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="35">
          <div>미등록</div>
        </td>
        <td class="border-tbl" width="495" colspan="15">
          <div>[ {{ ve.rental_housing_registration == 0 ? "√" : "" }} ]해당사항 없음</div>
        </td>
      </tr>
      <tr>
        <td class="label" width="70" colspan="3">
          <div>계약갱신<br />요구권<br />행사 여부</div>
        </td>
        <td class="border-tbl" width="495" colspan="15">
          <div>
            [ {{ is_right_to_lease_contract_renewal_true }} ] 확인(확인서류 첨부) [
            {{ is_right_to_lease_contract_renewal_false }} ] 미확인
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18">
          <div></div>
        </td>
      </tr>
      <tr>
        <td class="label border-trb" width="75" rowspan="6">
          <div>
            ③토지이용<br />
            계획, <br />
            공법상 이용<br />제한 및 거래<br />규제에 관한<br />사항(토지)
          </div>
        </td>
        <td class="label" width="70" colspan="3" rowspan="3">
          <div>지역 · 지구</div>
        </td>
        <td class="label" width="93" colspan="2">
          <div>용도지역</div>
        </td>
        <td width="240" colspan="5">
          <div>
            {{ ve.use_area }}
          </div>
        </td>
        <td class="label" width="79" colspan="5">
          <div>건폐율 상한</div>
        </td>
        <td class="label border-tbl" width="81" colspan="2">
          <div>용적률 상한</div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="2">
          <div>용도지구</div>
        </td>
        <td width="240" colspan="5">
          <div>
            {{ ve.use_district }}
          </div>
        </td>
        <td class="text-right pr-1" width="79" colspan="5" rowspan="2">
          <div>{{ ve.building_coverage_limit }}%</div>
        </td>
        <td class="border-tbl text-right pr-1" width="81" colspan="2" rowspan="2">
          <div>{{ ve.floor_area_limit }}%</div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="2">
          <div>용도구역</div>
        </td>
        <td class="border-tbl" width="240" colspan="5">
          <div>
            {{ ve.use_zone }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="70" colspan="3" rowspan="2">
          <div>
            도시 · 군계획<br />
            시설
          </div>
        </td>
        <td width="123" colspan="3" rowspan="2">
          <div>
            {{ ve.planning_facilities }}
          </div>
        </td>
        <td class="label" width="80">
          <div>
            허가·신고<br />
            구역 여부
          </div>
        </td>
        <td class="border-tbl" width="290" colspan="10">
          <div>[ {{ ve.permission_report_zone ? "√" : "" }} ]토지거래허가구역</div>
        </td>
      </tr>
      <tr>
        <td class="label" width="80">
          <div>투기지역 여부</div>
        </td>
        <td class="border-tbl" width="290" colspan="10">
          <div>
            [ {{ ve.speculative_area == 1 ? "√" : "" }} ]토지투기지역[
            {{ ve.speculative_area == 2 ? "√" : "" }} ]주택투기지역[
            {{ ve.speculative_area == 3 ? "√" : "" }} ]투기과열지구
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="163" colspan="5">
          <div>
            지구단위계획구역,<br />
            그 밖의 도시·군관리계획
          </div>
        </td>
        <td width="133" colspan="3">
          <div>
            {{ ve.unit_planning_area_others }}
          </div>
        </td>
        <td class="label" width="115" colspan="3">
          <div>
            그 밖의 이용제한 및<br />
            거래규제사항
          </div>
        </td>
        <td class="border-tbl" width="153" colspan="6">
          <div>
            {{ ve.other_use_restriction }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18">
          <div></div>
        </td>
      </tr>
      <tr>
        <td style="border:0" width="800" colspan="18" valign="bottom" align="right">
          <div>210mm×297mm[백상지(80g/㎡) 또는 중질지(80g/㎡)</div>
        </td>
      </tr>
      <tr height="0">
        <td style="border:0" width="75"></td>
        <td style="border:0" width="24"></td>
        <td style="border:0" width="3"></td>
        <td style="border:0" width="43"></td>
        <td style="border:0" width="50"></td>
        <td style="border:0" width="43"></td>
        <td style="border:0" width="30"></td>
        <td style="border:0" width="80"></td>
        <td style="border:0" width="23"></td>
        <td style="border:0" width="32"></td>
        <td style="border:0" width="75"></td>
        <td style="border:0" width="7"></td>
        <td style="border:0" width="16"></td>
        <td style="border:0" width="9"></td>
        <td style="border:0" width="24"></td>
        <td style="border:0" width="23"></td>
        <td style="border:0" width="20"></td>
        <td style="border:0" width="61"></td>
      </tr>
    </table>

    <div class="page-divide">
      <br clear="all" />
    </div>
    <table
      border="1"
      style="border-collapse:collapse"
      class="page2 a4 MsoNormalTable"
      cellspacing="0"
      cellpadding="0"
      width="800"
    >
      <tr>
        <td style="border:0" width="247" colspan="18" valign="bottom" align="right">
          <div>(4쪽 중 제2쪽)</div>
        </td>
      </tr>
      <tr>
        <td class="label border-trb" width="75" colspan="2" rowspan="9">
          <div>④입지조건</div>
        </td>
        <td class="label" width="77" colspan="3">
          <div>
            도로와의 관계
          </div>
        </td>
        <td width="241" colspan="10">
          <div>
            {{ ve.relative_with_roads }}도로에 접함 [ {{ ve.is_paved_rode ? "√" : "" }} ]포장 [
            {{ ve.is_paved_rode ? "" : "√" }} ]비포장
          </div>
        </td>
        <td class="label" width="84" colspan="2">
          <div>접근성</div>
        </td>
        <td class="border-tbl text-center" width="160">
          <div>
            [ {{ ve.accessibility ? "√" : "" }} ]용이함 [ {{ ve.accessiblity ? "√" : "" }} ]불편함
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="77" colspan="3" rowspan="2">
          <div>대중교통</div>
        </td>
        <td class="label" width="67" colspan="2">
          <div>버스</div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            ({{ ve.bus_stop }}) 정류장, 소요시간: ([ {{ ve.bus_by_foot ? "√" : "" }} ]도보 [
            {{ ve.bus_by_foot ? "" : "√" }} ]차량) 약 {{ ve.bus_required_time }}분
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="67" colspan="2">
          <div>지하철</div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            ({{ ve.subway_station }}) 역, 소요시간: ([ {{ ve.subway_by_foot == true ? "√" : "" }} ]
            도보 [ {{ ve.subway_by_foot == false ? "√" : "" }} ]차량) 약
            {{ ve.subway_required_time }}분
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="77" colspan="3">
          <div>주차장</div>
        </td>
        <td class="border-tbl" width="486" colspan="14">
          <div>
            [ {{ ve.parking_lot == 0 ? "√" : "" }} ]없음 [
            {{ ve.parking_lot == 1 ? "√" : "" }} ]전용주차시설 [
            {{ ve.parking_lot == 2 ? "√" : "" }} ]공동주차시설 [
            {{ ve.parking_lot == 3 ? "√" : "" }} ]그 밖의 주차시설 (
            {{ ve.parking_lot == 99 ? ve.parking_lot_info : "" }} )
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="77" colspan="3" rowspan="3">
          <div>교육시설</div>
        </td>
        <td class="label" width="67" colspan="2">
          <div>초등학교</div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            ({{ ve.elementary_school }}) 학교, 소요시간: ([
            {{ ve.elementary_school_by_foot ? "√" : "" }} ]도보 [
            {{ ve.elementary_school_by_foot ? "" : "√" }} ]차량) 약
            {{ ve.elementary_school_required_time }}분
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="67" colspan="2">
          <div>중학교</div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            ({{ ve.middle_school }}) 학교, 소요시간: ([
            {{ ve.middle_school_by_foot ? "√" : "" }} ]도보 [
            {{ ve.middle_school_by_foot ? "" : "√" }} ]차량) 약
            {{ ve.middle_school_required_time }}분
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="67" colspan="2">
          <div>고등학교</div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            ({{ ve.high_school }}) 학교, 소요시간: ([ {{ ve.high_school_by_foot ? "√" : "" }} ]도보
            [ {{ ve.high_school_by_foot ? "" : "√" }} ]차량) 약
            {{ ve.high_school_required_time }}분
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="77" colspan="3" rowspan="2">
          <div>
            판매 및<br />
            의료시설
          </div>
        </td>
        <td class="label" width="67" colspan="2">
          <div>
            백화점 및<br />
            할인매장
          </div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            ({{ ve.department_store }}), 소요시간: ([
            {{ ve.department_store_by_foot ? "√" : "" }} ]도보 [
            {{ ve.department_store_by_foot ? "" : "√" }} ]차량) 약
            {{ ve.department_store_required_time }}분
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="67" colspan="2">
          <div>종합의료시설</div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            ({{ ve.medical_center }}), 소요시간: ([
            {{ ve.medical_center_by_foot ? "√" : "" }} ]도보 [
            {{ ve.medical_center_by_foot ? "" : "√" }} ]차량) 약
            {{ ve.medical_center_required_time }}분
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18">
          <div></div>
        </td>
      </tr>
      <tr>
        <td class="label border-trb" width="75" colspan="2">
          <div>
            ⑤관리에<br />
            관한사항
          </div>
        </td>
        <td class="label" width="85" colspan="3">
          <div>경비실</div>
        </td>
        <td width="136" colspan="3">
          <div>
            [ {{ ve.is_security_office ? "√" : "" }} ]있음 [
            {{ ve.is_security_office ? "" : "√" }} ]없음
          </div>
        </td>
        <td class="label" width="64" colspan="3">
          <div>관리주체</div>
        </td>
        <td class="border-tbl" width="278" colspan="7">
          <div>
            [ {{ ve.management == 1 ? "√" : "" }} ]위탁관리 [
            {{ ve.management == 2 ? "√" : "" }} ]자체관리 [
            {{ ve.management == 99 ? "√" : "" }} ]그 밖의 유형
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18">
          <div></div>
        </td>
      </tr>
      <tr>
        <td class="border-trb" width="159" colspan="5">
          <div>⑥비선호시설(1km이내)</div>
        </td>
        <td class="border-tbl" width="478" colspan="13">
          <div>
            [ {{ ve.undesirable_facilities ? "" : "√" }} ]없음 [
            {{ ve.undesirable_facilities ? "√" : "" }} ]있음 (종류 및 위치:
            {{ ve.undesirable_facilities ? ve.undesirable_facilities_info : "" }})
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18">
          <div></div>
        </td>
      </tr>
      <tr>
        <td class="label border-trb" width="109" colspan="3" rowspan="2">
          <div>⑦거래예정금액 등</div>
        </td>
        <td class="label" width="122" colspan="4">
          <div>거래예정금액</div>
        </td>
        <td class="border-tbl" width="407" colspan="11">
          <div>
            {{ ve.expected_transaction_price }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="122" colspan="4">
          <div>개별공시지가(㎡당)</div>
        </td>
        <td width="160" colspan="6">
          <div>
            {{ ve.land_prcie_recorded }}
          </div>
        </td>
        <td class="label" width="85" colspan="3">
          <div>
            건물(주택)<br />
            공시가격
          </div>
        </td>
        <td class="border-tbl" width="162" colspan="2">
          <div>
            {{ ve.building_price_recorded }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18">
          <div></div>
        </td>
      </tr>
      <tr>
        <td class="label border-trb" width="109" colspan="3" rowspan="2">
          <div>
            ⑧취득 시 부담할 <br />
            조세의 종류 및 세율
          </div>
        </td>
        <td class="label" width="50" colspan="2">
          <div>취득세</div>
        </td>
        <td class="text-right pr-1" width="72" colspan="2">
          <div>{{ ve.acquisition_tax }}%</div>
        </td>
        <td class="label" width="74" colspan="2">
          <div>농어촌특별세</div>
        </td>
        <td class="text-right pr-1" width="85" colspan="4">
          <div>{{ ve.special_tax }}%</div>
        </td>
        <td class="label" width="85" colspan="3">
          <div>지방교육세</div>
        </td>
        <td class="border-tbl text-right pr-1" width="162" colspan="2">
          <div>{{ ve.local_education_tax }}%</div>
        </td>
      </tr>
      <tr>
        <td class="border-tbl" width="529" colspan="15">
          <div>
            ※ 재산세는 6월 1일 기준 대상물건 소유자가 납세의무를 부담
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18">
          <div></div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18" valign="bottom">
          <div><b>Ⅱ</b><b>. </b><b>개업공인중개사 세부 확인사항</b></div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18" valign="top">
          <div style="height:110px">⑨ 실제 권리관계 또는 공시되지 않은 물건의 권리 사항<br /></div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18">
          <div></div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="71" rowspan="10">
          <div>⑩ 내부 ·<br />외부 시설물<br />의 상태 <br />(건축물)</div>
        </td>
        <td class="label" width="81" colspan="4" rowspan="2">
          <div>수도</div>
        </td>
        <td class="label" width="67" colspan="2">
          <div>파손 여부</div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            [ {{ ve.water_damage_status ? "" : "√" }} ]없음 [
            {{ ve.water_damage_status ? "√" : "" }} ]있음 (위치:
            {{ ve.water_damage_status ? ve.water_damage_status_info : "" }})
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="67" colspan="2">
          <div>용수량</div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            [ {{ ve.water_capacity_status ? "√" : "" }} ]정상 [
            {{ ve.water_capacity_status ? "" : "√" }} ]부족함 (위치:
            {{ ve.water_capacity_status ? "" : ve.water_capacity_status_info }})
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="81" colspan="4">
          <div>전기</div>
        </td>
        <td class="label" width="67" colspan="2">
          <div>공급상태</div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            [ {{ ve.electricity_supply_status ? "√" : "" }} ]정상 [
            {{ ve.electricity_supply_status ? "" : "√" }} ]교체 필요 (교체할 부분:
            {{ ve.electricity_supply_status_info }})
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="81" colspan="4">
          <div>가스(취사용)</div>
        </td>
        <td class="label" width="67" colspan="2">
          <div>공급방식</div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            [ {{ ve.gas_supply_status ? "√" : "" }} ]도시가스 [
            {{ ve.gas_supply_status ? "" : "√" }} ]그 밖의 방식 ({{
              ve.gas_supply_status ? "" : ve.gas_supply_status_info
            }})
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="81" colspan="4">
          <div>소방</div>
        </td>
        <td class="label" width="67" colspan="2">
          <div>
            단독경보형 <br />
            감지기
          </div>
        </td>
        <td width="127" colspan="4">
          <div>
            [ {{ ve.is_fire_alarm_detector ? "" : "√" }} ]없음
            <br />
            [ {{ ve.is_fire_alarm_detector ? "√" : "" }} ]있음(수량:
            {{ ve.is_fire_alarm_detector ? ve.fire_alarm_detector_quantity : "" }}개)
          </div>
        </td>
        <td class="border-tbl caption" width="292" colspan="8">
          <div>
            ※「화재예방, 소방시설 설치 · 유지 및 안전관리에 관한 법률」 제8조 및 같은 법 시행령
            제13조에 따른 주택용 소방시설로서 아파트(주택으로 사용하는 층수가 5개층 이상인 주택을
            말한다)를 제외한 주택의 경우만 작성합니다.
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="81" colspan="4" rowspan="2">
          <div>
            난방방식 및<br />
            연료공급
          </div>
        </td>
        <td class="label" width="67" colspan="2">
          <div>공급방식</div>
        </td>
        <td width="157" colspan="6">
          <div>
            [ {{ ve.heating_supply_method == 1 ? "√" : "" }} ]중앙공급 [
            {{ ve.heating_supply_method == 2 ? "√" : "" }} ]개별공급
          </div>
        </td>
        <td class="label" width="52" colspan="4">
          <div>시설작동</div>
        </td>
        <td class="border-tbl" width="210" colspan="3">
          <div>
            [ {{ ve.heating_status ? "√" : "" }} ]정상[ {{ ve.heating_status ? "" : "√" }} ]수선
            필요 ({{ ve.heating_status ? "" : ve.heating_status_info }})
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="67" colspan="2">
          <div>종류</div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            [ {{ ve.heating_type == 1 ? "√" : "" }} ]도시가스 [
            {{ ve.heating_type == 2 ? "√" : "" }} ]기름 [
            {{ ve.heating_type == 3 ? "√" : "" }} ]프로판가스 [
            {{ ve.heating_type == 4 ? "√" : "" }} ]연탄 [
            {{ ve.heating_type == 99 ? "√" : "" }} ]그 밖의 종류 ({{
              ve.heating_type == 99 ? ve.heating_type_info : ""
            }})
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="81" colspan="4">
          <div>승강기</div>
        </td>
        <td class="border-tbl" width="486" colspan="14">
          <div>
            [ {{ ve.is_elevator ? "√" : "" }} ]있음 ([
            {{ ve.is_elevator ? (ve.elevator_status ? "√" : "") : "" }} ]양호 [
            {{ ve.is_elevator ? (ve.elevator_status ? "" : "√") : "" }} ]불량) [
            {{ ve.is_elevator ? "" : "√" }} ]없음
          </div>
        </td>
      </tr>
      <tr>
        <td class="label border-tbl" width="81" colspan="4">
          <div>배수</div>
        </td>
        <td class="border-tbl" width="486" colspan="14">
          <div>
            [ {{ ve.drainage_status ? "√" : "" }} ]정상 [ {{ ve.drainage_status ? "" : "√" }} ]수선
            필요 ( {{ ve.drainage_status ? "" : ve.drainage_status_info }} )
          </div>
        </td>
      </tr>
      <tr>
        <td class="label border-tbl" width="81" colspan="4">
          <div>그 밖의 시설물</div>
        </td>
        <td class="border-tbl" width="486" colspan="14">
          <div>
            {{ ve.other_facilities }}
          </div>
        </td>
      </tr>
      <tr height="0">
        <td style="border:0" width="71"></td>
        <td style="border:0" width="4"></td>
        <td style="border:0" width="34"></td>
        <td style="border:0" width="43"></td>
        <td style="border:0" width="8"></td>
        <td style="border:0" width="59"></td>
        <td style="border:0" width="13"></td>
        <td style="border:0" width="64"></td>
        <td style="border:0" width="10"></td>
        <td style="border:0" width="41"></td>
        <td style="border:0" width="14"></td>
        <td style="border:0" width="16"></td>
        <td style="border:0" width="15"></td>
        <td style="border:0" width="3"></td>
        <td style="border:0" width="35"></td>
        <td style="border:0" width="48"></td>
        <td style="border:0" width="2"></td>
        <td style="border:0" width="160"></td>
      </tr>
    </table>

    <div class="page-divide">
      <br clear="all" />
    </div>
    <div class="a4">
      <table
        border="1"
        style="border-collapse:collapse"
        class="MsoNormalTable"
        cellspacing="0"
        cellpadding="0"
        width="800"
      >
        <tr>
          <td
            class="caption"
            style="border:0"
            width="278"
            colspan="12"
            valign="bottom"
            align="right"
          >
            <div>(4쪽 중 제3쪽)</div>
          </td>
        </tr>
        <tr>
          <td class="label border-trb" width="71" colspan="2" rowspan="3">
            <div>
              ⑪ 벽면 및<br />
              도배상태
            </div>
          </td>
          <td class="label" width="89" colspan="2" rowspan="2">
            <div>벽면</div>
          </td>
          <td class="label" width="56" colspan="2">
            <div>균열</div>
          </td>
          <td class="border-tbl" width="422" colspan="6">
            <div>
              [ {{ ve.wall_crack_status ? "" : "√" }} ]없음 [
              {{ ve.wall_crack_status ? "√" : "" }} ]있음 (위치:
              {{ ve.wall_crack_status ? ve.wall_crack_status_info : "" }})
            </div>
          </td>
        </tr>
        <tr>
          <td class="label" width="56" colspan="2">
            <div>누수</div>
          </td>
          <td class="border-tbl" width="422" colspan="6">
            <div>
              [ {{ ve.water_leak_status ? "" : "√" }} ]없음 [
              {{ ve.water_leak_status ? "√" : "" }} ]있음 (위치:
              {{ ve.water_leak ? ve.water_leak_status_info : "" }})
            </div>
          </td>
        </tr>
        <tr>
          <td class="label" width="89" colspan="2">
            <div>도배</div>
          </td>
          <td class="border-tbl" width="478" colspan="8">
            <div>
              [ {{ ve.wall_paper_status == 2 ? "√" : "" }} ]깨끗함 [
              {{ ve.wall_paper_status == 1 ? "√" : "" }} ]보통임 [
              {{ ve.wall_paper_status == 0 ? "√" : "" }} ]도배 필요
            </div>
          </td>
        </tr>
        <tr>
          <td class="border-tb" width="800" colspan="12">
            <div></div>
          </td>
        </tr>
        <tr>
          <td class="label border-trb" width="71" colspan="2" rowspan="2">
            <div>⑫ 환경 <br />조건</div>
          </td>
          <td class="label" width="89" colspan="2">
            <div>일조량</div>
          </td>
          <td class="border-tbl" width="478" colspan="8">
            <div>
              [ {{ ve.sunshine_status == 2 ? "√" : "" }} ]풍부함 [
              {{ ve.sunshine_status == 1 ? "√" : "" }} ]보통임 [
              {{ ve.sunshine_status == 0 ? "√" : "" }} ]불충분 (이유:
              {{ ve.sunshine_status == false ? ve.sunshine_status_info : "" }})
            </div>
          </td>
        </tr>
        <tr>
          <td class="label" width="69" colspan="2">
            <div>소음</div>
          </td>
          <td width="239" colspan="6">
            <div>
              [ {{ ve.noise_status == 2 ? "√" : "" }} ]미미함 [
              {{ ve.noise_status == 1 ? "√" : "" }} ]보통임 [
              {{ ve.noise_status == 0 ? "√" : "" }} ]심한 편임
            </div>
          </td>
          <td class="label" width="45" colspan="1">
            <div>진동</div>
          </td>
          <td class="border-tbl" width="214" colspan="2">
            <div>
              [ {{ ve.vibration == 2 ? "√" : "" }} ]미미함 [
              {{ ve.vibration == 1 ? "√" : "" }} ]보통임 [ {{ ve.vibration == 0 ? "√" : "" }} ]심한
              편임
            </div>
          </td>
        </tr>
        <tr>
          <td class="border-tb" width="800" colspan="12">
            <div></div>
          </td>
        </tr>
        <tr>
          <td class="border-tb" width="800" colspan="12" valign="bottom">
            <div><b>Ⅲ</b><b>. </b><b>중개보수 등에 관한 사항</b></div>
          </td>
        </tr>
        <tr>
          <td class="label border-trb" width="71" colspan="2" rowspan="4">
            <div>⑬ 중개보수 <br />및 실비의 <br />금액과 <br />산출내역</div>
          </td>
          <td class="label" width="93" colspan="3">
            <div>중개보수</div>
          </td>
          <td width="219" colspan="4">
            <div>
              {{ `${ve.comission}${$t("won")}` }}
            </div>
          </td>
          <td class="border-tbl" width="255" colspan="3" rowspan="4">
            <div style="white-space: pre-line">
              {{ `${ve.calculation_info}` }}
            </div>
          </td>
        </tr>
        <tr>
          <td class="label" width="93" colspan="3">
            <div>실비</div>
          </td>
          <td width="219" colspan="4">
            <div>
              {{ `${ve.actual_expenses}${$t("won")}` }}
            </div>
          </td>
        </tr>
        <tr>
          <td class="label" width="93" colspan="3">
            <div>계</div>
          </td>
          <td width="219" colspan="4">
            <div>
              {{ `${ve.comission + ve.actual_expenses}${$t("won")}` }}
            </div>
          </td>
        </tr>
        <tr>
          <td class="label" width="93" colspan="3">
            <div>지급시기</div>
          </td>
          <td width="219" colspan="4">
            <div>
              {{ ve.payment_period }}
            </div>
          </td>
        </tr>
        <tr>
          <td class="border-tb" width="800" colspan="12">
            <div><s> </s></div>
          </td>
        </tr>
        <tr>
          <td class="border-tb" width="800" colspan="12">
            <div>
              「공인중개사법」 제25조제3항 및 제30조제5항에 따라 거래당사자는 개업공인중개사로부터
              위 중개대상물에 관한 확인·설명 및 손해배상책임의 보장에 관한 설명을 듣고, 같은 법
              시행령 제21조제3항에 따른 본 확인·설명서와 같은 법 시행령 제24조제2항에 따른
              손해배상책임 보장 증명서류(사본 또는 전자문서)를 수령합니다.
              <br />
            </div>
            <div class="created_date" align="right">{{ year }}년 {{ month }}월 {{ day }}일</div>
          </td>
        </tr>
        <tr class="contractor">
          <td class="label border-tb" width="63" rowspan="2">
            <div>매도인<br />(임대인)</div>
          </td>
          <td class="label" width="82" colspan="2">
            <div>주소</div>
          </td>
          <td width="215" colspan="4">
            <div>
              {{
                `${$get(seller, "profile.address.new_address")}${
                  $get(seller, "profile.address.dong")
                    ? ", " + $get(seller, "profile.address.dong") + $t("dong")
                    : ""
                }${
                  $get(seller, "profile.address.dong")
                    ? $get(seller, "profile.address.ho")
                      ? $get(seller, "profile.address.ho") + $t("ho")
                      : ""
                    : $get(seller, "profile.address.ho")
                    ? ", " + $get(seller, "profile.address.ho") + $t("ho")
                    : ""
                }`
              }}
            </div>
          </td>
          <td class="label" width="68" colspan="4">
            <div>성명</div>
          </td>
          <td class="text-right border-tb" width="211" valign="bottom">
            <div>
              <img
                v-if="isSellerSigned"
                class="signature-img"
                :src="$get(seller, 'explanation_signature.image')"
              />
              <img v-else class="signature-img" :src="SellerMandateSrc" />
              <span style="float:left">{{ `${$get(seller, "profile.user.name")}` }}</span>
              (서명 또는 날인)
            </div>
          </td>
        </tr>
        <tr class="contractor">
          <td class="label" width="82" colspan="2">
            <div>생년월일</div>
          </td>
          <td width="215" colspan="4">
            <div>{{ `${$get(seller, "profile.user.birthday")}` }}</div>
          </td>
          <td class="label" width="68" colspan="4">
            <div>전화번호</div>
          </td>
          <td class="border-tb" width="211" valign="bottom">
            <div>{{ `${$get(seller, "profile.mobile_number")}` }}</div>
          </td>
        </tr>
        <tr class="contractor">
          <td class="label border-tb" width="63" rowspan="2">
            <div>매수인<br />(임차인)</div>
          </td>
          <td class="label" width="82" colspan="2">
            <div>주소</div>
          </td>
          <td width="215" colspan="4">
            <div>
              {{
                `${$get(buyer, "profile.address.new_address")}${
                  $get(buyer, "profile.address.dong")
                    ? ", " + $get(buyer, "profile.address.dong") + $t("dong")
                    : ""
                }${
                  $get(buyer, "profile.address.dong")
                    ? $get(buyer, "profile.address.ho")
                      ? $get(buyer, "profile.address.ho") + $t("ho")
                      : ""
                    : $get(buyer, "profile.address.ho")
                    ? ", " + $get(buyer, "profile.address.ho") + $t("ho")
                    : ""
                }`
              }}
            </div>
          </td>
          <td class="label" width="68" colspan="4">
            <div>성명</div>
          </td>
          <td class="text-right border-tb" width="211" valign="bottom">
            <div>
              <img
                v-if="isBuyerSigned"
                class="signature-img"
                :src="$get(buyer, 'explanation_signature.image')"
              />
              <img v-else class="signature-img" :src="BuyerMandateSrc" />
              <span style="float:left">{{ `${$get(buyer, "profile.user.name")}` }}</span>
              (서명 또는 날인)
            </div>
          </td>
        </tr>
        <tr class="contractor">
          <td class="label" width="82" colspan="2">
            <div>생년월일</div>
          </td>
          <td width="215" colspan="4">
            <div>{{ `${$get(buyer, "profile.user.birthday")}` }}</div>
          </td>
          <td class="label" width="68" colspan="4">
            <div>전화번호</div>
          </td>
          <td class="border-tb" width="211" valign="bottom">
            <div>{{ `${$get(buyer, "profile.mobile_number")}` }}</div>
          </td>
        </tr>
        <tr class="contractor">
          <td class="label border-tb" width="63" rowspan="3">
            <div>개업<br />공인중개사</div>
          </td>
          <td class="label" width="82" colspan="2">
            <div>등록번호</div>
          </td>
          <td width="215" colspan="4">
            <div>
              {{ `${$get(expert, "profile.expert_profile.registration_number")}` }}
            </div>
          </td>
          <td class="label" width="68" colspan="4">
            <div>성명(대표자)</div>
          </td>
          <td class="text-right border-tb" width="211" valign="bottom">
            <div>
              <img
                v-if="isExpertSigned"
                class="signature-img"
                :src="$get(expert, 'explanation_signature.image')"
              />
              <img
                v-if="isExpertSigned"
                class="stamp-img"
                :src="$get(expert, 'profile.expert_profile.stamp')"
              />
              <span style="float:left">{{ `${$get(expert, "profile.user.name")}` }}</span>
              (서명 및 날인)
            </div>
          </td>
        </tr>
        <tr class="contractor">
          <td class="label" width="82" colspan="2">
            <div>사무소 명칭</div>
          </td>
          <td width="215" colspan="4">
            <div>
              {{ `${$get(expert, "profile.expert_profile.shop_name")}` }}
            </div>
          </td>
          <td class="label" width="68" colspan="4">
            <div>소속<br />공인중개사</div>
          </td>
          <td class="text-right border-tb" width="211" valign="bottom">
            <div>(서명 및 날인)</div>
          </td>
        </tr>
        <tr class="contractor">
          <td class="label" width="82" colspan="2">
            <div>사무소 소재지</div>
          </td>
          <td width="215" colspan="4">
            <div>
              {{
                `${$get(expert, "profile.address.new_address")}${
                  $get(expert, "profile.address.dong")
                    ? ", " + $get(expert, "profile.address.dong") + $t("dong")
                    : ""
                }${
                  $get(expert, "profile.address.dong")
                    ? $get(expert, "profile.address.ho")
                      ? $get(expert, "profile.address.ho") +
                        ($get(expert, "profile.expert_profile.is_shown_ho") ? $t("ho") : "")
                      : ""
                    : $get(expert, "profile.address.ho")
                    ? ", " +
                      $get(expert, "profile.address.ho") +
                      ($get(expert, "profile.expert_profile.is_shown_ho") ? $t("ho") : "")
                    : ""
                }`
              }}
            </div>
          </td>
          <td class="label" width="68" colspan="4">
            <div>전화번호</div>
          </td>
          <td class="border-tb" width="211" valign="bottom">
            <div>{{ `${$get(expert, "profile.mobile_number")}` }}</div>
          </td>
        </tr>
        <tr class="contractor">
          <td class="label border-tb" width="63" rowspan="3">
            <div>개업<br />공인중개사</div>
          </td>
          <td class="label" width="82" colspan="2">
            <div>등록번호</div>
          </td>
          <td width="215" colspan="4">
            <div></div>
          </td>
          <td class="label" width="68" colspan="4">
            <div>성명(대표자)</div>
          </td>
          <td class="text-right border-tb" width="211" valign="bottom">
            <div>(서명 및 날인)</div>
          </td>
        </tr>
        <tr class="contractor">
          <td class="label" width="82" colspan="2">
            <div>사무소 명칭</div>
          </td>
          <td width="215" colspan="4">
            <div></div>
          </td>
          <td class="label" width="68" colspan="4">
            <div>소속<br />공인중개사</div>
          </td>
          <td class="text-right border-tb" width="211" valign="bottom">
            <div>(서명 및 날인)</div>
          </td>
        </tr>
        <tr class="contractor">
          <td class="label" width="82" colspan="2">
            <div>사무소 소재지</div>
          </td>
          <td width="215" colspan="4">
            <div></div>
          </td>
          <td class="label" width="68" colspan="4">
            <div>전화번호</div>
          </td>
          <td class="border-tb" width="211" valign="bottom">
            <div></div>
          </td>
        </tr>
        <tr height="0">
          <td style="border:0" width="70"></td>
          <td style="border:0" width="8"></td>
          <td style="border:0" width="80"></td>
          <td style="border:0" width="15"></td>
          <td style="border:0" width="26"></td>
          <td style="border:0" width="54"></td>
          <td style="border:0" width="144"></td>
          <td style="border:0" width="19"></td>
          <td style="border:0" width="4"></td>
          <td style="border:0" width="41"></td>
          <td style="border:0" width="4"></td>
          <td style="border:0" width="203"></td>
        </tr>
      </table>
    </div>
    <div style="width:790px; margin:auto; overflow:auto;">
      <slot name="footer"></slot>
    </div>
    <template v-if="ve.additional_info">
      <div class="page-divide"></div>
      <div class="text-center font-weight-bold" style="font-size:16px;">
        확인설명서 별지
      </div>
      <div class="label" style="border:1px solid #ccc;">
        <div>
          {{ ve.additional_info }}
        </div>
      </div>
    </template>
    <template v-if="ve.insurance.image">
      <div class="page-divide"></div>
      <div class="a4">
        <div class="text-center font-weight-bold">
          {{ $t("garantee_insurance") }}
        </div>
        <v-row justify="center">
          <img :src="ve.insurance.image" style="max-width:800px;" />
        </v-row>
      </div>
    </template>
  </div>
</template>

<script>
export default {
  name: "VerifyingExplanation",
  props: {
    paper: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      ve: null
    };
  },
  computed: {
    is_right_to_lease_contract_renewal_true() {
      return this.ve.rental_housing_registration != 0 &&
        this.ve.right_to_lease_contract_renewal == true
        ? "√"
        : "";
    },
    is_right_to_lease_contract_renewal_false() {
      return this.ve.rental_housing_registration != 0 &&
        this.ve.right_to_lease_contract_renewal == false
        ? "√"
        : "";
    },
    year() {
      return this.paper.updated_at.split("-")[0];
    },
    month() {
      return this.paper.updated_at.split("-")[1];
    },
    day() {
      return this.paper.updated_at.split("-")[2].split(" ")[0];
    },
    seller: function() {
      return this.paper.paper_contractors.find(
        (item) => item.group == this.$getConstByName("CONTRACTOR_CATEGORY", "seller")
      );
    },
    buyer: function() {
      return this.paper.paper_contractors.find(
        (item) => item.group == this.$getConstByName("CONTRACTOR_CATEGORY", "buyer")
      );
    },
    expert: function() {
      return this.paper.paper_contractors.find(
        (item) => item.group == this.$getConstByName("CONTRACTOR_CATEGORY", "expert")
      );
    },
    isSellerSigned: function() {
      return this.seller
        ? this.seller.explanation_signature &&
            this.paper.updated_at <= this.seller.explanation_signature.updated_at
        : undefined;
    },
    isBuyerSigned: function() {
      return this.buyer
        ? this.buyer.explanation_signature &&
            this.paper.updated_at <= this.buyer.explanation_signature.updated_at
        : undefined;
    },
    isExpertSigned: function() {
      return this.expert
        ? this.expert.explanation_signature &&
            this.paper.updated_at <= this.expert.explanation_signature.updated_at
        : undefined;
    },
    SellerMandateSrc: function() {
      if (this.paper.mandates && this.seller) {
        const matched_profile = this.paper.mandates.find(
          (item) => item.designator.user.email == this.seller.profile.user.email
        );
        if (matched_profile) {
          return matched_profile.designator_signature;
        }
      }
      return "";
    },
    BuyerMandateSrc: function() {
      if (this.paper.mandates && this.buyer) {
        const matched_profile = this.paper.mandates.find(
          (item) => item.designator.user.email == this.buyer.profile.user.email
        );
        if (matched_profile) {
          return matched_profile.designator_signature;
        }
      }
      return "";
    }
  },
  created() {
    this.ve = this.paper.verifying_explanation;
  }
};
</script>

<style scoped>
.created_date {
  margin-right: 80px;
}
.contractor td {
  height: 60px;
  vertical-align: middle;
}
.contractor td div {
  position: relative;
}
.label {
  text-align: center;
}
.ve {
  min-width: 790px;
}
.page2 .label {
  padding: 3.8px 0px 3.8px 0px;
}
table {
  width: 790px;
  border-width: 0px;
  margin: auto;
  margin-top: 30px;
}
div {
  padding: 2.5px 0px 2.5px 1px;
  word-spacing: 2px;
  font-size: 14px;
  letter-spacing: 1px;
  line-height: 1.4;
}
.border-tb {
  border-width: 1px 0px 1px 0px;
}
.border-trb {
  border-width: 1px 1px 1px 0px;
}
.border-tbl {
  border-width: 1px 0px 1px 1px;
}
.signature-img {
  height: 40px;
  z-index: 1;
  right: 0px;
  top: -7px;
  position: absolute;
}
.stamp-img {
  height: 40px;
  z-index: 1;
  right: 80px;
  top: -17px;
  position: absolute;
}
</style>
