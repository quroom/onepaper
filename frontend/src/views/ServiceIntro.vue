<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12">
        <v-card class="elevation-0 transparent">
          <v-card-title primary-title class="layout justify-center">
            <div class="text-h3 text-center font-weight-bold">ONEPAPER</div>
          </v-card-title>
          <v-card-text>
            <div class="text-h6 text-center">
              원페이퍼는 기술 서비스를 통해 당신의 시간과 위험을 줄이는데 가치를 두고 있습니다.
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="4">
        <v-card class="elevation-0 transparent">
          <v-card-text class="text-center">
            <v-icon x-large class="blue--text text--lighten-2">flash_on</v-icon>
          </v-card-text>
          <v-card-title primary-title class="layout justify-center">
            <div class="text-h5 text-center">신속성</div>
          </v-card-title>
          <v-card-text>
            계약서 아직도 손으로 번거롭게 작성하고 계시나요?
            썼던 내용 또 쓰고 계세요? 이제는 한번 쓴 내용은 불러와서 계약서 작성해보세요.
            휴대폰, PC만 있으면 언제 어디서든 계약서를 작성할 수 있답니다.
            <br/>당신과 타인의 거리를 좁혀드리겟습니다.
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card class="elevation-0 transparent">
          <v-card-text class="text-center">
            <v-icon x-large class="blue--text text--lighten-2">hourglass_full</v-icon>
          </v-card-text>
          <v-card-title primary-title class="layout justify-center">
            <div class="text-h5 text-center">영속성</div>
          </v-card-title>
          <v-card-text>
            계약서 분실을 더이상 걱정할 필요없습니다. 언제 어디서든 당신의 계약서를 확인하세요.
            휴대폰, PC로 작성한 계약 데이터는 서비스 기간동안 AWS RDS에 안전하게 저장됩니다.
            <br/>당신의 계약서를 영구히 보존해보세요.
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card class="elevation-0 transparent">
          <v-card-text class="text-center">
            <v-icon x-large class="blue--text text--lighten-2">share</v-icon>
          </v-card-text>
          <v-card-title primary-title class="layout justify-center">
            <div class="text-h5 text-center">공유</div>
          </v-card-title>
          <v-card-text>
            계약서를 어떻게 작성하는지 자신이 없으세요?
            내가 쓴 계약서가 잘 작성되었는지 걱정 되시나요?
            당신이 작성한 계약서를 공유하고, 친구가 작성한 계약서를 공유받으세요.
            그리고 잘 작성된 계약서를 참고해보세요. 
            <br/>더 나은 계약서를 작성할 수 있을거에요.
          </v-card-text>
        </v-card>
      </v-col>
      <v-btn class="blue lighten-2 mt-5" dark large :to="{name:'manuals'}">
          이용방법 알아보기
      </v-btn>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "ServiceIntro"
}
</script>

<style>

</style>