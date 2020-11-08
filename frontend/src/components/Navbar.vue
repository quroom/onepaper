<template>
  <v-app-bar app>

    <v-app-bar-nav-icon @click="drawer = true">
    </v-app-bar-nav-icon>
    <v-navigation-drawer
      v-model="drawer"
      absolute
      temporary
      app
    >
      <v-list dense>
         <v-list-item-group
            v-model="group"
            active-class="deep-purple--text text--accent-4"
          >
        <v-list-item
          v-for="item in items"
          :key="item.title"
          :to="item.route"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
         </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
    <template v-if="$vuetify.breakpoint.width > 500">
      <router-link :to="{ name: 'Home' }">
        <v-toolbar-title class="text-uppercase grey--text">
          OnePaper
        </v-toolbar-title>
      </router-link>
      <router-link :to="{ name: 'Home' }">
        <v-icon>home</v-icon>
      </router-link>
      <v-spacer></v-spacer>
      <router-link class="ma-4" :to="{ name: 'profiles' }">
        {{ $t("profile") }}
      </router-link>
      <router-link class="ma-4" :to="{ name: 'Home' }">
        {{ $t("contract") }}
      </router-link>
      <v-spacer></v-spacer>
    </template>
    <v-spacer v-else></v-spacer>
    <v-btn text color="grey" href="/accounts/logout/">
      <span>{{ $t("logout") }}</span>
      <v-icon>exit_to_app</v-icon>
    </v-btn>
    <span @click="switchLoc()">
      <flag v-if="this.$i18n.locale==='ko'" iso="us"/>
      <flag v-else iso="kr" />
    </span>
  </v-app-bar>
</template>
<script>
import i18n from "@/plugins/i18n";

export default {
  name: "Navbar",
  data() {
    return {
      requestUser: null,
      drawer : false,
      items: [
        { title: `${i18n.t("paper")}`, icon: 'description', route: "/"},
        { title: `${i18n.t("profile")}`, icon: 'account_box' , route: "profiles"},
      ],
      group : null,
    }
  },
  created() {
    this.requestUser = window.localStorage.getItem("username");
  },
  methods: {
    switchLoc() {
      console.log("click")
      this.$i18n.locale = this.$i18n.locale === "en" ? "ko" : "en";
    }
  }
};
</script>

<style>
a:hover {
  text-decoration: none;
}

/* .fixed-bar {
  /* position: sticky; */
  /* position: -webkit-sticky; for Safari */
  /* top: 0px; */
  /* bottom: 0;
  height: 10vh !important;
  overflow-y: auto;
  z-index: 2;
} */
</style>
