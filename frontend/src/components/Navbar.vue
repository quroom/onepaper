<template>
  <v-app-bar app>
    <v-dialog v-model="dialog" max-width="400px">
      <v-card>
        <v-card-title>
          {{ $t("add_allowed_user") }}
        </v-card-title>
        <v-card-text class="text-body-1 text--primary">
          <v-text-field
            v-model="link"
            :label="$t('link')"
            ref="link"
            :success="success"
            :success-messages="messages"
          >
            <template v-slot:message="{ message, key }">
              <div v-html="message" :key="key"></div>
            </template>
          </v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click.prevent="copyText()">
            {{ $t("copy") }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-app-bar-nav-icon @click="drawer = true"> </v-app-bar-nav-icon>
    <v-navigation-drawer v-model="drawer" absolute temporary app>
      <v-list nav dense>
        <v-list-item-group active-class="deep-purple--text text--accent-4">
          <router-link
            v-for="item in items"
            :v-if="!item.staff_only || item.staff_only == is_staff"
            :to="item.route"
            :key="item.title + `-nav`"
          >
            <v-list-item>
              <v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-icon>

              <v-list-item-content>
                <v-list-item-title>{{ $t(item.title) }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </router-link>
          <v-divider></v-divider>
          <v-list-item
            key="link"
            @click="
              messages = [];
              success = false;
              dialog = true;
            "
          >
            <v-list-item-icon>
              <v-icon> arrow_right_alt </v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title
                >{{ $t("profile") }} {{ $t("allow") }}
                {{ $t("link") }}</v-list-item-title
              >
            </v-list-item-content>
          </v-list-item>
          <v-list-item @click="switchLoc()">
            <v-list-item-icon>
              <flag v-if="this.$i18n.locale === 'ko'" iso="kr" />
              <flag v-else iso="us" />
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title
                >{{ $t("language") }} {{ $t("change") }}</v-list-item-title
              >
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
    <template v-if="$vuetify.breakpoint.width > 500">
      <router-link :to="{ name: 'home' }">
        <v-toolbar-title class="text-uppercase grey--text">
          OnePaper
        </v-toolbar-title>
      </router-link>
      <router-link :to="{ name: 'home' }">
        <v-icon>home</v-icon>
      </router-link>
      <v-spacer></v-spacer>
      <template v-for="item in items">
        <router-link
          v-if="!item.staff_only || item.staff_only == is_staff"
          class="ma-4"
          :to="item.route"
          :key="item.title"
        >
          {{ $t(item.title) }}
        </router-link>
      </template>
      <v-spacer></v-spacer>
    </template>
    <v-spacer v-else></v-spacer>
    <v-btn text color="grey" href="/accounts/logout/">
      <span>{{ $t("logout") }}</span>
      <v-icon>exit_to_app</v-icon>
    </v-btn>
  </v-app-bar>
</template>
<script>
export default {
  name: "Navbar",
  props: {
    is_staff: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      requestUser: null,
      drawer: false,
      items: [
        {
          title: "paper",
          icon: "description",
          route: { name: "home" },
          staff_only: false
        },
        {
          title: "profile",
          icon: "account_box",
          route: { name: "profiles" },
          staff_only: false
        },
        {
          title: "mandate_paper",
          icon: "account_box",
          route: { name: "mandates" },
          staff_only: false
        },
        {
          title: "approve",
          icon: "how_to_reg",
          route: { name: "approve-expert" },
          staff_only: true
        }
      ],
      link: null,
      dialog: false,
      success: false,
      messages: ""
    };
  },
  created() {
    this.requestUser = window.localStorage.getItem("username");
    const name = window.localStorage.getItem("name");
    this.link = window.location.protocol + "//" + window.location.host + "/" + "profiles" + "/" + this.requestUser + "/" + name;
  },
  methods: {
    switchLoc() {
      this.$i18n.locale = this.$i18n.locale === "en" ? "ko" : "en";
    },
    copyText() {
      let link = this.$refs.link.$el.querySelector("input");
      link.select();
      document.execCommand("copy");
      this.success = true;
      this.messages = this.$i18n.t("link_is_copied") + "" + "<br>" +"" + this.$i18n.t("send_your_link");
    }
  }
};
</script>

<style>
a:hover {
  text-decoration: none;
}
</style>
