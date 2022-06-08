<template>
  <v-app app :style="`overflow-x:auto; min-width:${$store.state.minimum_width}px`">
    <NavbarItem id="v-navbar" class="no-print root_tag" />
    <v-main class="root_tag">
      <keep-alive
        v-if="!$route.meta.isPaperDestroied && !$store.state.is_paper_updated"
        include="PaperList"
      >
        <!-- sync data need to be fixed. This is temporary code for preventing and doing update correctly when paper is changed..-->
        <router-view />
      </keep-alive>
      <!-- FIXME: Can we make both isAskListingDestroied and isListingDestroied are working differently?
      It should be first here because when moving to listing-detail,
      isAskListingDestroied and isListingDestroied both are true  -->
      <keep-alive v-else-if="!$route.meta.isAskListingDestroied" include="AskListingList">
        <router-view />
      </keep-alive>
      <keep-alive v-else-if="!$route.meta.isListingDestroied" include="ListingList">
        <!-- sync data need to be fixed. This is temporary code for preventing and doing update correctly when paper is changed..-->
        <router-view />
      </keep-alive>
      <router-view v-else />
    </v-main>
    <Footer class="no-print root_tag" />
  </v-app>
</template>

<script>
import NavbarItem from "./components/NavbarItem";
import Footer from "./components/Footer";
export default {
  name: "App",
  components: {
    NavbarItem,
    Footer
  },
  computed: {
    is_staff() {
      return this.$store.state.user_category == "staff";
    }
  },
  watch: {
    $route(to) {
      if (this.$store.state.has_profile == false && this.is_staff == false) {
        if (to.name == "paper-editor" || to.name == "listing-editor") {
          alert(this.$i18n.t("no_profile_cant_use_service"));
          this.$router.push({ name: "profile-editor" });
        }
      }
    }
  }
};
</script>
<style>
html {
  overflow-x: auto;
}
/* Chrome, Safari, Edge, Opera */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
/* Firefox */
input[type="number"] {
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
.btn-right {
  position: absolute;
  right: 0px;
}

.signature-dialog {
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
/* Progress circular Style*/
.v-progress-circular {
  display: block;
  width: 100px;
  margin: 0 auto;
}
/* Notion Style */
.notion-page-offset {
  margin-top: 0px;
}
.notion-title {
  text-align: center;
}
.notion-page img {
  padding: 1px;
  border: 1px solid #021a40;
}
.ql-container {
  font-size: 16px !important;
}
.v-quill-editor .ql-container {
  height: 40vh !important;
}
.row {
  margin-left: -4px;
  margin-right: -4px;
}
.v-step {
  z-index: 90000000 !important;
}
.v-menu__content {
  z-index: 90000001 !important;
  pointer-events: all !important;
}
.tour-set {
  height: 60%;
}
/* In paper-detail , desc-realestate info highlighted border is hided by v-card
So I added this style. */
.v-tour__target--highlighted {
  padding-left: 4px;
  padding-right: 4px;
}
/* For print paper setting. */
@media print {
  @page {
    margin-top: 20px;
    margin-bottom: 20px;
  }
  .v-application {
    overflow: visible !important;
    padding: 0px !important;
  }
  .a4 {
    height: 29.7cm !important;
    width: 21cm !important;
    margin: auto;
  }
  .v-main {
    padding: 0px !important;
    margin: 0px !important;
  }
  .page-divide {
    page-break-after: always;
  }
  .no-print {
    display: none;
  }
  html {
    -webkit-print-color-adjust: exact;
    font-size: 12px;
  }
  .ql-container {
    font-size: 12px !important;
  }
}
.row {
  margin-top: 0px;
  margin-bottom: 0px;
}
</style>
