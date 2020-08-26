<template>
    <v-app>
        <NavbarComponent />
        <router-view />
    </v-app>
</template>

<script>
import NavbarComponent from "./components/Navbar.vue";

export default {
    name: "App",
    components: {
        NavbarComponent
    },

    data: () => ({
        //
    })
};
</script>
