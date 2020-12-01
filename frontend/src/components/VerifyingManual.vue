<template>
  <v-container>
    <table
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
            <span class="blue--text text--accent-4">&lt;개정 2020. 10. 27.&gt;</span>
          </div>
        </td>
        <td class="caption" style="border:0;" width="128" colspan="4" valign="bottom" align="right" >
          <div>(4쪽 중 제1쪽)</div>
        </td>
      </tr>
      <tr>
        <td style="border:0;" colspan="18" valign="top" align="center">
          <b style="font-size: 16pt">중개대상물 확인 · 설명서[Ⅰ] (주거용 건축물)</b>
        </td>
      </tr>
      <tr>
        <td style="border:0;" colspan="18">
          <div align="center">
            <b>(    ［］단독주택［］공동주택［］매매·교환［］임대    )</b>
          </div>
        </td>
      </tr>
      <tr>
        <td style="border-top:0;" colspan="18">
          
        </td>
      </tr>
      <tr>
        <td class="border-trb" width="102" colspan="3" rowspan="2">
          <div>확인·설명 자료</div>
        </td>
        <td width="92" colspan="2">
          <div>확인·설명 근거자료 등</div>
        </td>
        <td class="border-tbl" width="444" colspan="13">
          <div>
            ［］등기권리증［］등기사항증명서［］토지대장［
            ］건축물대장 ［］지적도 <br/>［］임야도 ［
            ］토지이용계획확인서 ［］그 밖의 자료( )
          </div>
        </td>
      </tr>
      <tr>
        <td width="92" colspan="2">
          <div>
            대상물건의 상태에 관한 자료요구 사항
          </div>
        </td>
        <td class="border-tbl" width="444" colspan="13">
          <div>
            {{ explanation_evidence_info }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18">
          <div>
            
          </div>
        </td>
      </tr>
      <tr class="grey">
        <td style="border-width: 1px 0px 1px 0px;" width="800" colspan="18">
          <div align="center">유의사항</div>
        </td>
      </tr>
      <tr>
        <td class="border-trb" width="102" colspan="3">
          <div>개업공인중개사의 확인·설명 의무</div>
        </td>
        <td class="border-tbl" width="536" colspan="15">
          <div>
            개업공인중개사는 중개대상물에 관한 권리를 취득하려는
            중개의뢰인에게 성실·정확하게 설명하고, 토지대장 등본,
            등기사항증명서 등 설명의 근거자료를 제시해야 합니다.
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-trb" width="102" colspan="3">
          <div>실제 거래가격 신고</div>
        </td>
        <td class="border-tbl" width="536" colspan="15">
          <div>
            「부동산 거래신고 등에 관한 법률」 제3조 및 같은 법
            시행령 별표 1 제1호마목에 따른 실제 거래가격은 매수인이 매수한
            부동산을 양도하는 경우 「소득세법」 제97조제1항 및 제7항과
            같은 법 시행령 제163조제11항제2호에 따라 취득 당시의 실제
            거래가액으로 보아 양도차익이 계산될 수 있음을 유의하시기
            바랍니다.
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18" valign="bottom">
          <div>
            <br/>
            <b>Ⅰ</b><b>. </b><b>개업공인중개사 기본 확인사항</b>
          </div>
        </td>
      </tr>
      <tr>
        <td class="label border-trb" width="75" rowspan="9">
          <div>① 대상물건의 표시</div>
        </td>
        <td class="label" width="70" colspan="3" rowspan="3">
          <div>토지</div>
        </td>
        <td class="label border-tbl" width="93" colspan="2">
          <div>소재지</div>
        </td>
        <td class="border-tbl" width="401" colspan="12">
          <div>
            {{ address.old_address }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="2" rowspan="2">
          <div>면적(㎡)</div>
        </td>
        <td width="110" colspan="2" rowspan="2">
          <div>
            {{ land_area }}
          </div>
        </td>
        <td class="label" width="55" colspan="2" rowspan="2">
          <div>지목</div>
        </td>
        <td class="label" width="98" colspan="3">
          <div>공부상 지목</div>
        </td>
        <td class="border-tbl" width="137" colspan="5">
          <div>
            {{ land_category }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="98" colspan="3">
          <div>실제 이용 상태</div>
        </td>
        <td class="border-tbl" width="137" colspan="5">
          <div>
            {{ actual_land_category }}
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
          <div>
            {{ net_area }}
          </div>
        </td>
        <td class="label" width="98" colspan="3">
          <div>대지지분(㎡)</div>
        </td>
        <td class="border-tbl" width="137" colspan="5">
          <div>
            {{ land_share }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="2" rowspan="2">
          <div>준공년도 (증개축년도)</div>
        </td>
        <td width="110" colspan="2" rowspan="2">
          <div>
            {{ year_of_completion }}
          </div>
        </td>
        <td class="label" width="55" colspan="2" rowspan="2">
          <div>용도</div>
        </td>
        <td class="label" width="98" colspan="3">
          <div>건축물대장상 용도</div>
        </td>
        <td class="border-tbl" width="137" colspan="5">
          <div>
            {{ building_category }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="98" colspan="3">
          <div>실제 용도</div>
        </td>
        <td class="border-tbl" width="137" colspan="5">
          <div>
            {{ actual_building_category }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="2">
          <div>구조</div>
        </td>
        <td width="110" colspan="2">
          <div>
            {{ building_category }}
          </div>
        </td>
        <td class="label" width="153" colspan="5">
          <div>방향</div>
        </td>
        <td class="border-tbl" width="137" colspan="5">
          <div>
            {{ building_direction }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="2">
          <div>내진설계 적용여부</div>
        </td>
        <td width="110" colspan="2">
          <div>
            {{ seismic_design }}
          </div>
        </td>
        <td class="label" width="153" colspan="5">
          <div>내진능력</div>
        </td>
        <td class="border-tbl" width="137" colspan="5">
          <div>
            {{ seismic_capacity }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="2">
          <div>건축물대장상 위반건축물 여부</div>
        </td>
        <td width="110" colspan="2">
          <div>［{{ legal_status?'':'√' }}］위반［{{ legal_status?'√':'' }}］적법</div>
        </td>
        <td class="label" width="55" colspan="2">
          <div>위반내용</div>
        </td>
        <td class="border-tbl" width="235" colspan="8">
          <div>
            {{ matters_of_violation }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18">
          <div>
            
          </div>
        </td>
      </tr>
      <tr>
        <td class="label border-trb" width="75" rowspan="4">
          <div>② 권리관계</div>
        </td>
        <td class="label" width="70" colspan="3" rowspan="3">
          <div>등기부 기재사항</div>
        </td>
        <td class="label" width="258" colspan="6">
          <div>소유권에 관한 사항</div>
        </td>
        <td class="label border-tbl" width="235" colspan="8">
          <div>소유권 외의 권리사항</div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="2">
          <div>토지</div>
        </td>
        <td width="165" colspan="4">
          <div>
            {{ land_ownership }}
          </div>
        </td>
        <td class="label" width="75">
          <div>토지</div>
        </td>
        <td class="border-tbl" width="160" colspan="7">
          <div>
            {{ land_other }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="2">
          <div>건축물</div>
        </td>
        <td class="border-tbl" width="165" colspan="4">
          <div>
            {{ building_ownership }}
          </div>
        </td>
        <td class="label" width="75">
          <div>건축물</div>
        </td>
        <td class="border-tbl" width="160" colspan="7">
          <div>
            {{ building_other }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="70" colspan="3">
          <div>민간임대 등록여부</div>
        </td>
        <td class="border-tbl" width="494" colspan="14">
          <div>
            ［ {{ rental_housing_registration==0 ? '√' : '' }} ］장기일반민간임대주택 ［ {{ rental_housing_registration==1 ? '√' : '' }} ］공공지원민간임대주택 
            ［ {{ rental_housing_registration==2 ? '√' : '' }} ］단기민간임대주택 ［ {{ rental_housing_registration==3 ? '√' : '' }} ］해당 사항 없음
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18">
          <div>
            
          </div>
        </td>
      </tr>
      <tr>
        <td class="label border-trb" width="75" rowspan="6">
          <div>
            ③ 토지이용계획, 공법상 이용제한 및 거래규제에 관한
            사항(토지)
          </div>
        </td>
        <td class="label" width="70" colspan="3" rowspan="3">
          <div>지역·지구</div>
        </td>
        <td class="label" width="93" colspan="2">
          <div>용도지역</div>
        </td>
        <td width="240" colspan="5">
          <div>
            {{ use_area }}
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
            {{ use_district }}
          </div>
        </td>
        <td width="79" colspan="5" rowspan="2">
          <div>{{ building_coverage_limit }}%</div>
        </td>
        <td class="border-tbl" width="81" colspan="2" rowspan="2">
          <div>{{ floor_area_limit }}%</div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="2">
          <div>용도구역</div>
        </td>
        <td class="border-tbl" width="240" colspan="5">
          <div>
            {{ use_zone }}
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="70" colspan="3" rowspan="2">
          <div>도시·군계획 시설</div>
        </td>
        <td width="123" colspan="3" rowspan="2">
          <div>
            {{ planning_facilities }}
          </div>
        </td>
        <td class="label" width="80">
          <div>허가·신고 구역 여부</div>
        </td>
        <td class="border-tbl" width="290" colspan="10">
          <div>
            
            ［］토지거래허가구역
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="80">
          <div>투기지역 여부</div>
        </td>
        <td class="border-tbl" width="290" colspan="10">
          <div>
            
            ［］토지투기지역［］주택투기지역［］투기과열지구
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="163" colspan="5">
          <div>지구단위계획구역, 그 밖의 도시·군관리계획</div>
        </td>
        <td width="133" colspan="3">
          <div>
            
          </div>
        </td>
        <td class="label" width="115" colspan="3">
          <div>그 밖의 이용제한 및 거래규제사항</div>
        </td>
        <td class="border-tbl" width="153" colspan="6">
          <div>
            
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18">
          <div>
            
          </div>
        </td>
      </tr>
      <tr>
        <td style="border:0" width="800" colspan="18" valign="bottom" align="right">
          <div>210mm×297mm[백상지(80g/㎡) 또는 중질지(80g/㎡)</div>
        </td>
      </tr>
      <tr height="0">
        <td width="75"></td>
        <td width="24"></td>
        <td width="3"></td>
        <td width="43"></td>
        <td width="50"></td>
        <td width="43"></td>
        <td width="30"></td>
        <td width="80"></td>
        <td width="23"></td>
        <td width="32"></td>
        <td width="75"></td>
        <td width="7"></td>
        <td width="16"></td>
        <td width="9"></td>
        <td width="24"></td>
        <td width="23"></td>
        <td width="20"></td>
        <td width="61"></td>
      </tr>
    </table>
    <div>
      
      <br clear="all" />
      
    </div>
    <table
      style="border-collapse:collapse"
      class="a4 MsoNormalTable"
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
          <div>④ 입지조건</div>
        </td>
        <td width="77" colspan="3">
          <div>
            도로와의 관계
          </div>
        </td>
        <td width="241" colspan="10">
          <div>
            
            ( m × m )도로에 접함 ［］포장 ［］비포장
          </div>
        </td>
        <td class="label" width="84" colspan="2">
          <div>접근성</div>
        </td>
        <td class="border-tbl" width="160">
          <div>［］용이함 ［］불편함</div>
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
            
            ( ) 정류장, 소요시간: (［］도보 ［］차량) 약 분
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="67" colspan="2">
          <div>지하철</div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            
            ( ) 역, 소요시간: (［］도보 ［］차량) 약 분
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="77" colspan="3">
          <div>주차장</div>
        </td>
        <td class="border-tbl" width="486" colspan="14">
          <div>
            ［］없음 ［］전용주차시설 ［］공동주차시설 ［］그
            밖의 주차시설 ( )
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
            
            ( ) 학교, 소요시간: (［］도보 ［］차량) 약 분
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="67" colspan="2">
          <div>중학교</div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            
            ( ) 학교, 소요시간: (［］도보 ［］차량) 약 분
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="67" colspan="2">
          <div>고등학교</div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            
            ( ) 학교, 소요시간: (［］도보 ［］차량) 약 분
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="77" colspan="3" rowspan="2">
          <div>판매 및 의료시설</div>
        </td>
        <td class="label" width="67" colspan="2">
          <div>백화점 및 할인매장</div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            
            ( ), 소요시간: (［］도보 ［］차량) 약 분
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="67" colspan="2">
          <div>종합의료시설</div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            
            ( ), 소요시간: (［］도보 ［］차량) 약 분
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18">
          <div>
            
          </div>
        </td>
      </tr>
      <tr>
        <td class="label border-trb"  width="75" colspan="2">
          <div>⑤ 관리에 관한사항</div>
        </td>
        <td class="label" width="85" colspan="3">
          <div>경비실</div>
        </td>
        <td width="136" colspan="3">
          <div>［］있음 ［］없음</div>
        </td>
        <td class="label" width="64" colspan="3">
          <div>관리주체</div>
        </td>
        <td class="border-tbl" width="278" colspan="7">
          <div>［］위탁관리 ［］자체관리 ［］그 밖의 유형</div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18">
          <div>
            
          </div>
        </td>
      </tr>
      <tr>
        <td class="label border-trb"  width="159" colspan="5">
          <div>⑥ 비선호시설(1km이내)</div>
        </td>
        <td class="border-tbl" width="478" colspan="13">
          <div>
            
            ［］없음 ［］있음 (종류 및 위치: )
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18">
          <div>
            
          </div>
        </td>
      </tr>
      <tr>
        <td class="label border-trb"  width="109" colspan="3" rowspan="2">
          <div>⑦ 거래예정금액 등</div>
        </td>
        <td class="label" width="122" colspan="4">
          <div>거래예정금액</div>
        </td>
        <td class="border-tbl" width="407" colspan="11">
          <div>
            
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="122" colspan="4">
          <div>개별공시지가(㎡당)</div>
        </td>
        <td width="160" colspan="6">
          <div>
            
          </div>
        </td>
        <td class="label" width="85" colspan="3">
          <div>건물(주택) 공시가격</div>
        </td>
        <td class="border-tbl" width="162" colspan="2">
          <div>
            
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18">
          <div>
            
          </div>
        </td>
      </tr>
      <tr>
        <td class="label border-trb" width="109" colspan="3" rowspan="2">
          <div>⑧ 취득 시 부담할 조세의 종류 및 세율</div>
        </td>
        <td class="label" width="50" colspan="2">
          <div>취득세</div>
        </td>
        <td width="72" colspan="2">
          <div>%</div>
        </td>
        <td class="label" width="74" colspan="2">
          <div>농어촌특별세</div>
        </td>
        <td width="85" colspan="4">
          <div>%</div>
        </td>
        <td class="label" width="85" colspan="3">
          <div>지방교육세</div>
        </td>
        <td class="border-tbl" width="162" colspan="2">
          <div>%</div>
        </td>
      </tr>
      <tr>
        <td class="border-tbl" width="529" colspan="15">
          <div>
            ※ 재산세는 6월 1일 기준 대상물건 소유자가 납세의무를
            부담
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18">
          <div>
            
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18" valign="bottom">
          <div>
            <b>Ⅱ</b><b>. </b><b>개업공인중개사 세부 확인사항</b>
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18" valign="top">
          <div>
            ⑨ 실제 권리관계 또는 공시되지 않은 물건의 권리 사항
            
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18">
          <div>
            
          </div>
        </td>
      </tr>
      <tr>
        <td class="label border-tb" width="71" rowspan="10">
          <div>⑩ 내부·외부 시설물의 상태 (건축물)</div>
        </td>
        <td class="label" width="81" colspan="4" rowspan="2">
          <div>수도</div>
        </td>
        <td width="67" colspan="2">
          <div>파손 여부</div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            
            ［］없음 ［］있음 (위치: )
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="67" colspan="2">
          <div>용수량</div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            
            ［］정상 ［］부족함 (위치: )
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
            
            ［］정상 ［］교체 필요 (교체할 부분: )
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
            
            ［］도시가스 ［］그 밖의 방식 ( )
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="81" colspan="4">
          <div>소방</div>
        </td>
        <td class="label" width="67" colspan="2">
          <div>단독경보형 감지기</div>
        </td>
        <td width="127" colspan="4">
          <div>
            
            ［］없음

            
            ［］있음(수량: 개)
          </div>
        </td>
        <td class="border-tbl caption" width="292" colspan="8">
          <div>                
            ※「화재예방, 소방시설 설치 · 유지 및 안전관리에 관한 법률」
            제8조 및 같은 법 시행령 제13조에 따른 주택용 소방시설로서
            아파트(주택으로 사용하는 층수가 5개층 이상인 주택을 말한다)를
            제외한 주택의 경우만 작성합니다.
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="81" colspan="4" rowspan="2">
          <div>난방방식 및 연료공급</div>
        </td>
        <td class="label" width="67" colspan="2">
          <div>공급방식</div>
        </td>
        <td width="157" colspan="6">
          <div>
            
            ［］중앙공급 ［］개별공급
          </div>
        </td>
        <td class="label" width="52" colspan="4">
          <div>시설작동</div>
        </td>
        <td class="border-tbl" width="210" colspan="3">
          <div>［］정상［］수선 필요 ( )</div>
        </td>
      </tr>
      <tr>
        <td class="label" width="67" colspan="2">
          <div>종류</div>
        </td>
        <td class="border-tbl" width="419" colspan="12">
          <div>
            
            ［］도시가스 ［］기름 ［］프로판가스 ［］연탄 ［］그 밖의
            종류 ( )
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="81" colspan="4">
          <div>승강기</div>
        </td>
        <td class="border-tbl" width="486" colspan="14">
          <div>
            
            ［］있음 (［］양호 ［］불량) ［］없음
          </div>
        </td>
      </tr>
      <tr>
        <td class="label border-tbl" width="81" colspan="4">
          <div>배수</div>
        </td>
        <td class="border-tbl" width="486" colspan="14">
          <div>
            
            ［］정상 ［］수선 필요 ( )
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tbl" width="81" colspan="4">
          <div>그 밖의 시설물</div>
        </td>
        <td class="border-tbl" width="486" colspan="14">
          <div>
            
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="18" valign="bottom">
          <div>
            
          </div>
        </td>
      </tr>
      <tr height="0">
        <td width="71"></td>
        <td width="4"></td>
        <td width="34"></td>
        <td width="43"></td>
        <td width="8"></td>
        <td width="59"></td>
        <td width="13"></td>
        <td width="64"></td>
        <td width="10"></td>
        <td width="41"></td>
        <td width="14"></td>
        <td width="16"></td>
        <td width="15"></td>
        <td width="3"></td>
        <td width="35"></td>
        <td width="48"></td>
        <td width="2"></td>
        <td width="160"></td>
      </tr>
    </table>
    <div>
      
      <br clear="all" />
      
    </div>
    <table
      style="border-collapse:collapse"
      class="a4 MsoNormalTable"
      cellspacing="0"
      cellpadding="0"
      width="800"
    >
      <tr>
        <td class="caption" style="border:0" width="278" colspan="12" valign="bottom" align="right">
          <div>(4쪽 중 제3쪽)</div>
        </td>
      </tr>
      <tr>
        <td class="label border-trb" width="71" colspan="2" rowspan="3">
          <div>
            ⑪ 벽면 및 
            도배상태
          </div>
        </td>
        <td class="label" width="89" colspan="1" rowspan="2">
          <div>벽면</div>
        </td>
        <td class="label" width="56" colspan="2">
          <div>균열</div>
        </td>
        <td class="border-tbl" width="422" colspan="6">
          <div>
            
            ［］없음 ［］있음 (위치: )
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="56" colspan="2">
          <div>누수</div>
        </td>
        <td class="border-tbl" width="422" colspan="6">
          <div>
            
            ［］없음 ［］있음 (위치: )
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="89" colspan="1">
          <div>도배</div>
        </td>
        <td class="border-tbl" width="478" colspan="8">
          <div>
            
            ［］깨끗함 ［］보통임 ［］도배 필요
          </div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="12">
          <div>
            
          </div>
        </td>
      </tr>
      <tr>
        <td class="label border-trb" width="71" colspan="2" rowspan="2">
          <div>⑫ 환경 조건</div>
        </td>
        <td class="label" width="89" colspan="1">
          <div>일조량</div>
        </td>
        <td class="border-tbl" width="478" colspan="8">
          <div>
            
            ［］풍부함 ［］보통임 ［］불충분 (이유: )
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="69" colspan="1">
          <div>소음</div>
        </td>
        <td width="239" colspan="6">
          <div>
            
            ［］미미함 ［］보통임 ［］심한 편임
          </div>
        </td>
        <td class="label" width="45" colspan="1">
          <div>진동</div>
        </td>
        <td class="border-tbl" width="214" colspan="2">
          <div>［］미미함 ［］보통임 ［］심한 편임</div>
        </td>
      </tr>
      <tr>
        <td class="border-tb" width="800" colspan="12">
          <div>
            
          </div>
        </td>
      </tr>
      <tr>
        <td class="label border-tb" width="800" colspan="12" valign="bottom">
          <div><b>Ⅲ</b><b>. </b><b>중개보수 등에 관한 사항</b></div>
        </td>
      </tr>
      <tr>
        <td class="label border-trb" width="71" colspan="2" rowspan="4">
          <div>⑬ 중개보수 및 실비의 금액과 산출내역</div>
        </td>
        <td class="label" width="93" colspan="3">
          <div>중개보수</div>
        </td>
        <td width="219" colspan="4">
          <div>
            
          </div>
        </td>
        <td class="border-tbl" width="255" colspan="3" rowspan="4">
          <div>
            &lt;산출내역&gt; 
            <br/><br/>
            중개보수:
            <br/><br/>
            실 비:
            <br/><br/>
            ※ 중개보수는 시·도 조례로 정한 요율에 따르거나, 시·도
            조례로 정한 요율한도에서 중개의뢰인과 개업공인중개사가 서로
            협의하여 결정하도록 한 요율에 따르며 부가가치세는 별도로
            부과될 수 있습니다.
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="3">
          <div>실비</div>
        </td>
        <td width="219" colspan="4">
          <div>
            
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="3">
          <div>계</div>
        </td>
        <td width="219" colspan="4">
          <div>
            
          </div>
        </td>
      </tr>
      <tr>
        <td class="label" width="93" colspan="3">
          <div>지급시기</div>
        </td>
        <td width="219" colspan="4">
          <div>
            
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
              공인중개사법」 제25조제3항 및 제30조제5항에 따라
            거래당사자는 개업공인중개사로부터 위 중개대상물에 관한
            확인·설명 및 손해배상책임의 보장에 관한 설명을 듣고, 같은 법
            시행령 제21조제3항에 따른 본 확인·설명서와 같은 법 시행령
            제24조제2항에 따른 손해배상책임 보장 증명서류(사본 또는
            전자문서)를 수령합니다.
            <br/>
          </div>
          <div align="right">
            년 월 일
          </div>
        </td>
      </tr>
    </table>
  </v-container>
</template>

<script>
export default {
  name: "VerifyingExplanation",
  props: {
    obj: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      paper_categories: null,
      explanation_evidences: null,
      explanation_evidence_info: null,
      address: {
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
      building_structure: null,
      building_direction: null,
      seismic_design: null,
      seismic_capacity: null,
      legal_status: true,
      matters_of_violation: null,
      land_ownership: null,
      building_ownership: null,
      land_other: null,
      building_other: null,
      rental_housing_registration: null,
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
      relative_with_roads: null,
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
    }
  }
}
</script>

<style>

</style>