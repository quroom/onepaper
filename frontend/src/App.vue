<template>
  <v-app app>
    <Navbar class="navbar" :is_staff="is_staff" />
    <v-main>
      <router-view :has_profile.sync="has_profile" />
    </v-main>
  </v-app>
</template>

<script>
import Navbar from "./components/Navbar";
import { applyValidation } from "@/common/common_api"
import { apiService } from "@/common/api.service";

export default {
  name: "App",
  components: {
    Navbar
  },
  data: () => ({
    is_staff: false,
    link_dialog: false,
    has_profile: true
  }),
  watch: {
    has_profile() {
      if (this.has_profile == false && this.is_staff == false) {
        console.log("profile", this.has_profile)
        if (this.$router.name != "profile-editor") {
          alert(this.$i18n.t("no_profile_cant_use_service"));
          this.$router.push({ name: "profile-editor" });
        }
      }
    },
    $route(to) {
      console.log(this)
      if (this.has_profile == false && this.is_staff == false) {
        console.log("route_profile", this.has_profile)
        if (to.name != "profile-editor") {
          alert(this.$i18n.t("no_profile_cant_use_service"));
          this.$router.push({ name: "profile-editor" });
        }
      }
    }
  },
  methods: {
    async setUserInfo() {
      const data = await apiService("/api/user/");
      if(data.id == undefined){
        applyValidation(data, this)
      }
      console.log("update_has_profile", data["has_profile"])
      window.localStorage.setItem("username", data["username"]);
      window.localStorage.setItem("name", data["name"]);
      window.localStorage.setItem("birthday", data["birthday"]);
      window.localStorage.setItem("is_expert", data["is_expert"]);
      window.localStorage.setItem("request_expert", data["request_expert"]);
      this.has_profile = data["has_profile"];
      this.is_staff = data["is_staff"];
      // if (this.has_profile == false && this.is_staff == false) {
      //   if (this.$route.name != "profile-editor") {
      //     alert(this.$i18n.t("no_profile_cant_use_service"));
      //     this.$router.push({ name: "profile-editor" });
      //   }
      // }
    }
  },
  created() {
    this.setUserInfo();
    this.isLoading = false;
  }
};
</script>
<style>
/* Chrome, Safari, Edge, Opera */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
-webkit-appearance: none;
margin: 0;
}

/* Firefox */
input[type=number] {
-moz-appearance: textfield;
}
a {
  text-decoration: none !important;
}
a:hover {
  text-decoration: none;
}
.float_right {
  float: right;
}

@media print {
  .navbar {
    display: none;
  }
}
</style>