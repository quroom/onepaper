<template>
  <v-app>
    <Navbar />
    <router-view />
  </v-app>
</template>

<script>
import Navbar from "./components/Navbar.vue";
import { apiService } from "@/common/api.service";

export default {
  name: "App",
  components: {
    Navbar
  },
  data: () => ({
    //
  }),
  methods: {
    async setUserInfo() {
      const data = await apiService("/api/user/");
      window.localStorage.setItem("username", data["username"]);
      window.localStorage.setItem("is_expert", data["is_expert"]);
      window.localStorage.setItem("request_expert", data["request_expert"]);
    }
  },
  created() {
    this.setUserInfo();
  }
};
</script>
