<template>
  <v-container>
    <v-row>
      <DeleteAlert v-if="id" :id="this.id" :url="`/api/profiles/${this.profile_id}/insurances/` router_name='profiles'/>
    </v-row>
    <v-text-field>

    </v-text-field>
  </v-container>
</template>

<script>
export default {
  name: "InsuranceEditor",
  props: {
    ActionItems,
    DeleteAlert
  }

}
</script>

<style>

</style>