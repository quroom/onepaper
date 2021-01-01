<template>
  <v-chip-group>
    <DeleteAlert :id="this.id" :url="this.delete_url" :router_name="this.delete_router_name"></DeleteAlert>
    <v-spacer></v-spacer>
    <router-link :to="{name: this.editor_router_name, params: {id: this.id, readonly: false}}">
      <v-btn class="ma-1 auto" color="green" dark>
        {{$t('edit')}}
      </v-btn>
    </router-link>
  </v-chip-group>
</template>

<script>
import DeleteAlert from "@/components/DeleteAlert"
export default {
  name: "ActionItems",
  components: {
    DeleteAlert
  },
  props: {
    id: {
      type: [Number, String],
      required: true
    },
    delete_url: {
      type: [String],
      required: true
    },
    delete_router_name: {
      type: [String],
      required: true
    },
    editor_router_name: {
      type: [String],
      required: true
    }
  },
  data() {
    return {
    }    
  },
}
</script>