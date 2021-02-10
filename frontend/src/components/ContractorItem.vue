<template>
  <v-row no-gutters>
    <template v-for="(field, index) in fields">
      <template v-if="field.key != undefined && $get(contractor, field.key)">
        <v-col class="text-center font-weight-bold" :cols="label_cols ? label_cols.cols : '3' " :md="label_cols ? label_cols.md : '2'" :lg="label_cols ? label_cols.lg : '1'" :key="`name`+index">
          <v-card outlined tile>{{ $t(field.name) }}</v-card>
        </v-col>
        <v-col
          class="text-center"
          :cols="field.cols"
          :xs="field.xs"
          :md="field.md"
          :lg="field.lg"
          :key="`value-` + index"
        >
          <v-card outlined tile>{{ $get(contractor, field.key) }}</v-card>
        </v-col>
      </template>
      <template v-else-if="contractor[field.name]">
        <v-col class="text-center font-weight-bold" :cols="label_cols ? label_cols.cols : '3' " :md="label_cols ? label_cols.md : '2'" :lg="label_cols ? label_cols.lg : '1'" :key="`name`+index">
        <v-card outlined tile>{{ $t(field.name) }}</v-card>
        </v-col>
        <v-col
          class="text-center"
          :cols="field.cols"
          :xs="field.xs"
          :md="field.md"
          :lg="field.lg"
          :key="`value-` + index"
        >
          <v-card outlined tile>{{ contractor[field.name] }}</v-card>
        </v-col>
      </template>
    </template>
  </v-row>
</template>

<script>
export default {
  name: "ContractorItem",
  props: {
    contractor: {
      type: Object,
      required: true
    },
    fields: {
      type: Array,
      required: true
    },
    label_cols: {
      type: Object,
      required: false
    }
  },
}
</script>

<style scoped>

</style>