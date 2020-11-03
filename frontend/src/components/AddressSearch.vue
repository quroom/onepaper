<template>
  <v-row align="center">
    <v-col cols="8">
      <ValidationProvider mode="passive" :name="$t('address')" rules="required" v-slot="{ errors }">
        <v-text-field
          v-model="address_local"
          :label="label"
          outlined
          hide-details="auto"
          readonly
          required
          :error-messages="errors"
          @click="dialog=true;"
          data-vv-validate-on="none"
        >
        </v-text-field>
      </ValidationProvider>
    </v-col>
    <v-col cols="4">
      <ValidationProvider :name="$t('room_name')" v-slot="{ errors }">
        <v-text-field
          v-model="room_name_local"
          :label="$t('room_name')"
          outlined
          hide-details="auto"
          :error-messages="errors"
          v-on:change="updateText"
        ></v-text-field>
      </ValidationProvider>
    </v-col>
    <v-dialog v-model="dialog">
      <v-card>
        <v-card-text class="pt-5">
          <vue-daum-postcode :key=key @complete="address_objects = $event; onSubmitAddress();"/>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>

import { ValidationProvider } from "vee-validate";

export default {
  name: "AddressSearch",
  components: {
    ValidationProvider
  },
  props: {
    label: {
      type: String,
      required: true
    },
    address: {
      type: String,
      required: false
    },
    room_name: {
      type: String,
      required: false
    }
  },
  watch: { 
    address: function(newVal, oldVal) { // watch it
      this.address_local = this.address
      console.log('Prop changed: ', newVal, ' | was: ', oldVal)
    },
    room_name: function(newVal, oldVal) { // watch it
      this.room_name_local = this.room_name
      console.log('Prop changed: ', newVal, ' | was: ', oldVal)
    }
  },
  data() {
    return {
      dialog:false,
      key:0,
      address_local: null,
      address_objects:null,
      room_name_local: null,
    }
  },
  methods: {
    updateText(){
      this.$emit('update:room_name_local', this.room_name_local)
    },
    onSubmitAddress() {
      this.address_local = this.address_objects.address + ' ' + this.address_objects.buildingName;
      this.$emit('update:address_objects', this.address_objects)
      this.dialog = false
      this.key+=1
    }
  } 
}
</script>

<style>
.vue-daum-postcode-container {
  width: 100% !important;
  height: 444px !important;
}
</style>
