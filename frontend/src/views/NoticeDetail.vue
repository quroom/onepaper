<template>
  <v-container>
    <v-row v-if="notice" justify="center">
      <v-card>
        <v-card-subtitle class="py-1">
          {{ $t("onepaper") }}
          <span class="notice_date">{{ notice.created_at }}</span>
        </v-card-subtitle>
        <v-card-title class="py-1" style="border-bottom:1px solid lightgrey"> {{ notice.title }} </v-card-title>
        <v-card-text  class="py-1" v-html="notice.body"/>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
import { apiService } from "@/common/api_service";
import { applyValidation } from "@/common/common_api"

export default {
  name: "NoticeDetail",
  props: {
    id: {
      type: [Number, String],
      required: true
    }
  },
  data() {
    return {
      notice: null
    }
  },
  methods: {
    async getNoticeData(){
      let endpoint = `/api/notices/${this.id}/`;
      let data = await apiService(endpoint);
      if(data.id != undefined){
        this.notice = data;
      } else {
        applyValidation(data)
      }
    }
  },
  created(){
    this.getNoticeData();
  }
}
</script>

<style scoped>
  .notice_date {
    display: inline-block;
    position: absolute;
    right: 8px;
  }
</style>