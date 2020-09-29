<template>
  <nav>
    <v-app-bar>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
      <router-link :to="{ name: 'Home' }">
        <v-toolbar-title class="text-uppercase grey--text">
          OnePaper
        </v-toolbar-title>
      </router-link>
      <router-link :to="{ name: 'Home' }">
        <v-icon>home</v-icon>
      </router-link>
      <v-spacer></v-spacer>
      <router-link :to="{ name: 'profiles' }">
        {{ $t("profile") }}
      </router-link>
      <v-spacer></v-spacer>
      <v-btn text color="grey" href="/accounts/logout/">
        <span>{{ $t("logout") }}</span>
        <v-icon>exit_to_app</v-icon>
      </v-btn>
      <v-btn @click="switchLoc()">
        {{ this.$i18n.locale === "en" ? "한글" : "English" }}
      </v-btn>
    </v-app-bar>
  </nav>
</template>
<script>
export default {
  name: "NavbarComponent",
  methods: {
    switchLoc() {
      this.$i18n.locale = this.$i18n.locale === "en" ? "ko" : "en";
    }
  }
};
</script>

<style>
a:hover {
  text-decoration: none;
}
</style>
