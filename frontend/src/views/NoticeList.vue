<template>
  <v-container min-width="250">
    <v-row>
      <v-col v-for="notice in notices" :key="notice.id" cols="12" md="6" lg="4" xl="3">
        <v-card :to="{name: 'notice-detail', params: { id: notice.id } }">
          <v-card-subtitle class="py-1">
            {{ $t("onepaper") }}
            <span class="notice_date">{{ notice.created_at }}</span>
          </v-card-subtitle>
          <v-card-title class="py-1" style="border-bottom:1px solid lightgrey">
            <span>{{ notice.title }}</span>
          </v-card-title>
          <v-card-text class="py-1" v-html="filterImage(notice.body)"/>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { apiService } from "@/common/api_service"
import { applyValidation } from "@/common/common_api"

export default {
  name: "NoticeList",
  data() {
    return {
      isLoading: false,
      notices: [],
      next: null
    }
  },
  methods: {
    filterImage(text){
      return text.replace(/<img .*?>/g,"[그림]");
    },
    getNotices(){
      let endpoint = "/api/notices/";
      if(this.next) {
        endpoint = this.next;
      }
      this.isLoading = true;
      apiService(endpoint).then(data=>{
        if(data.count != undefined){
          this.notices.push(...data.results)
          this.next = data.next;
        } else {
          applyValidation(data)
        }
        this.isLoading = false;
      })
    }
  },
  created() {
    this.getNotices();
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