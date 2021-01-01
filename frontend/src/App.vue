<template>
  <v-app app>
    <NavbarItem v-if="!isLoading" class="navbar" :is_staff="is_staff"/>
    <v-main>
      <router-view v-if="!isLoading" :has_profile.sync="has_profile" />
    </v-main>
  </v-app>
</template>

<script>
import NavbarItem from "./components/NavbarItem";
import { applyValidation } from "@/common/common_api"
import { apiService } from "@/common/api.service";

export default {
  name: "App",
  components: {
    NavbarItem
  },
  data: () => ({
    isLoading: true,
    is_staff: false,
    link_dialog: false,
    has_profile: true
  }),
  watch: {
    has_profile() {
      if (this.has_profile == false && this.is_staff == false) {
        if (this.$router.name != "profile-editor" && this.$router.name != "profiles" && this.$router.name != "user-editor") {
          alert(this.$i18n.t("no_profile_cant_use_service"));
          this.$router.push({ name: "profile-editor" });
        }
      }
    },
    $route(to) {
      if (this.has_profile == false && this.is_staff == false) {
        if (to.name != "profile-editor" && to.name != "profiles" && to.name != "user-editor") {
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
      window.localStorage.setItem("username", data["username"]);
      window.localStorage.setItem("name", data["name"]);
      window.localStorage.setItem("birthday", data["birthday"]);
      window.localStorage.setItem("is_expert", data["is_expert"]);
      this.has_profile = data["has_profile"];
      this.is_staff = data["is_staff"];
      this.isLoading = false;
    }
  },
  created() {
    this.setUserInfo();
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

.signature-dialog {
  width: 50vh !important;
  min-width: 280px !important;
  max-width: 560px !important;
}

.signature-pad {
  width: 50vh !important;
  min-width: 280px;
  max-width: 560px;
  height: 25vh !important;
  min-height: 140px;
  max-height: 280px;
}
</style>