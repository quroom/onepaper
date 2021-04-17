<template>
  <v-app app>
    <NavbarItem class="no-print root_tag" v-if="!isLoading" :user_category="user_category"/>
    <v-main class="root_tag">
      <router-view v-if="!isLoading" :has_profile.sync="has_profile" />
    </v-main>
    <Footer class="no-print root_tag"/>
  </v-app>
</template>

<script>
import NavbarItem from "./components/NavbarItem";
import Footer from "./components/Footer";
import { applyValidation } from "@/common/common_api"
import { apiService } from "@/common/api_service";

export default {
  name: "App",
  components: {
    NavbarItem,
    Footer
  },
  data: () => ({
    isLoading: true,
    link_dialog: false,
    has_profile: true,
/* user_category: user(general_user), expert, staff */
    user_category: 'user'
  }),
  computed: {
    is_staff(){
      return this.user_category == 'staff';
    }
  },
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
      window.localStorage.setItem("email", data["email"]);
      window.localStorage.setItem("name", data["name"]);
      window.localStorage.setItem("birthday", data["birthday"]);
      this.has_profile = data["has_profile"];
      if(data["is_expert"]){
        this.user_category = 'expert'
      }
      if(data['is_staff']){
        this.user_category = 'staff'
      }
      window.localStorage.setItem('user_category', this.user_category)
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
.float-right {
  float: right;
}

/* For print paper setting. */
@media print {
  @page { margin-top: 20px; margin-bottom: 20px;}
  .v-main {
    padding: 0px !important;
  }
  .a4 {
    height: 29.7cm !important;
    width: 21cm !important;
    margin: auto;
  }
  .page-divide {
    page-break-after: always;
  }
  .no-print {
    display: none;
  }
  html {
    -webkit-print-color-adjust:exact;
  }
}
.signature-dialog {
  left: 0;
  position: absolute;
  width: 90vw !important;
  min-width: 280px !important;
  max-width: 400px !important;
}
.signature-pad {
  width: 100% !important;
  min-width: 280px;
  max-width: 400px;
  height: 45vw !important;
  min-height: 140px;
  max-height: 200px;
}
.root_tag {
   min-width:360px;
}
/* Progress circular Style*/
.v-progress-circular {
    display: block;
    width: 100px;
    margin: 0 auto;
}
/* Notion Style */
.notion-page-offset{
  margin-top: 0px;
}
.notion-title {
  text-align: center;
}
.notion-page img {
   padding:1px;
   border:1px solid #021a40;
}
.ql-container {
   font-size: 16px !important;
}
</style>