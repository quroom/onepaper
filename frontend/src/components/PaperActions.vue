<template>
  <div class="paper-actions">    
    <router-link
      :to="{name: 'paper-editor', params: {id: id}}"
    >
      <v-btn color="green" dark>
        {{$t('edit')}}
      </v-btn>
    </router-link>
    <v-btn color="error" @click="deletePaper">
      {{$t('delete')}}
    </v-btn>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service";

export default {
  name: "PaperActions",
  props: {
    id: {
      type: [Number, String],
      required: true
    }
  },
  methods: {
    async deletePaper() {
      let endpoint = `/api/peprs/${this.id}/`;
      try {
        await apiService(endpoint, "DELETE");
        this.$router.push("/");
      }catch (err) {
        alert(err);
      }
    }
  }
}
</script>