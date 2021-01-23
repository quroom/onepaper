<template>
  <v-container>
    <v-treeview
      activatable
      open-all
      :items="tree_items"
    >

    </v-treeview>
  </v-container>
</template>

<script>
// import { apiService } from "@/common/api_service";
export default {
  name: "ManualList",
  data() {
    return {
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
                { id: 211, name: `${this.$t('add_quick_trade_user')}`,},
                { id: 212, name: `${this.$t('add_quick_trader_link')}`,},
              ]}
          ]
        }
      ]
    }
  }
}
</script>

<style>

</style>