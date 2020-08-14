<template>
  <div class="home">
    <v-container class="my-5">
      <v-row>
        <v-col class="xs12 sm6 md4 lg3" v-for="n in 20" :key="n">
          <v-card class="pa-2 outlined tile">
            {{$getConst('ITEM_TYPE', 1)}}
          </v-card>
        </v-col>
      </v-row>
      <v-btn color="grey" dark absolute fab mid right>
        <v-icon>add</v-icon>
      </v-btn>
    </v-container>
  </div>
</template>

<script>
// @ is an alias to /src
export default {
  name: "Home",
  components: {}
};
</script>
