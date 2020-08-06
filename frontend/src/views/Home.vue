<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.svg" />
    <Paper msg="Welcome to Your Vue.js App" />
  </div>
</template>

<script>
// @ is an alias to /src
import Paper from "@/components/Paper.vue";

export default {
  name: "Home",
  components: {
    Paper
  }
};
</script>
