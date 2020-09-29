<template>
  <v-app>
    <NavbarComponent />
    <router-view />
  </v-app>
</template>

<script>
import NavbarComponent from "./components/Navbar.vue";
import { apiService } from "@/common/api.service";

export default {
  name: "App",
  components: {
    NavbarComponent
  },
  data: () => ({
    //
  }),
  methods: {
    async setUserInfo() {
      const data = await apiService("/api/user/");
      const requestUser = data["username"];
      const is_expert = data["is_expert"]
      window.localStorage.setItem("username", requestUser);
      window.localStorage.setItem("is_expert", is_expert);
    }
  },
  created() {
    this.setUserInfo();
  }
};
</script>
