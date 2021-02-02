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
            {{$t("service_intro_title")}}
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
            <div class="text-h5 text-center">{{$t("quickness")}}</div>
          </v-card-title>
          <v-card-text v-html='$t("service_intro_text1")'>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card class="elevation-0 transparent">
          <v-card-text class="text-center">
            <v-icon x-large class="blue--text text--lighten-2">hourglass_full</v-icon>
          </v-card-text>
          <v-card-title primary-title class="layout justify-center">
            <div class="text-h5 text-center">{{$t("permanence")}}</div>
          </v-card-title>
          <v-card-text v-html='$t("service_intro_text2")'>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card class="elevation-0 transparent">
          <v-card-text class="text-center">
            <v-icon x-large class="blue--text text--lighten-2">share</v-icon>
          </v-card-text>
          <v-card-title primary-title class="layout justify-center">
            <div class="text-h5 text-center">{{$t("share")}}</div>
          </v-card-title>
          <v-card-text v-html='$t("service_intro_text3")'>
          </v-card-text>
        </v-card>
      </v-col>
      <v-btn class="blue lighten-2 mt-5" dark large :to="{name:'manuals'}">
          {{$t("learn_how_to_use")}}
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