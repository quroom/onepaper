<template>
  <nav>    
      <v-app-bar text>
        <router-link :to="{ name: 'home' }">
        </router-link>
      </v-app-bar>
  </nav>
</template>
<script>
export default {
  name: "NavbarComponent",
}
</script>