<template>
  <v-container>
    <v-row>
      <v-col class="d-flex">
        <v-treeview
          activatable
          open-all
          :items="tree_items"
          @update:active="loadPage"
        >

        </v-treeview>
    </v-col>
      <v-col v-if="!!active_node" class="d-flex">
        {{active_node}}
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// import { apiService } from "@/common/api_service";
export default {
  name: "ManualList",
  data() {
    return {
      active_node: [],
      tree_items: [
        {
          id: 1,
          name: this.$t('paper'),
          children: [
            {
              id: 11, name: `${this.$t('create_paper')}`, children: [
                { id: 111, name: `${this.$t('quick_trade_user')}`,},
                { id: 112, name: `${this.$t('manual_input')}`}
              ]
            }
          ],
        },
        {
          id: 2,
          name: this.$t('profile'),
          children: [
            { 
              id: 21, name: `${this.$t('profile')} ${this.$t('manage')}`, children: [
                { id: 212, name: `${this.$t('add_quick_trader_link')}`,},
                { id: 211, name: `${this.$t('add_quick_trade_user')}`,},
              ]}
          ]
        }
      ]
    }
  },
  methods: {
    loadPage(value){
      console.log(value)
    }
  }
}
</script>

<style>

</style>