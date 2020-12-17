<template>
  <v-app-bar app width="100%">
    <v-dialog v-model="dialog" max-width="400px" @click:outside="messages = []; success = false;">
      <v-card>
        <v-card-title>
          {{ $t("add_trade_user") }}
        </v-card-title>
        <v-card-text class="text-body-1 text--primary">
          <LazyTextField
            v-model="link"
            :label="$t('link')"
            ref="link"
            :success="success"
            :success-messages="messages"
          >
            <template v-slot:message="{ message, key }">
              <div v-html="message" :key="key"></div>
            </template>
          </LazyTextField>
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
            :to="item.route"
            :key="item.title + `-nav`"
          >
            <template v-if="!item.staff_only || item.staff_only == is_staff">
              <v-list-item>
                <v-list-item-icon>
                  <v-icon>{{ item.icon }}</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>{{ $t(item.title) }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </template>
          </router-link>
          <v-divider></v-divider>
          <v-list-item
            key="link"
            @click="dialog = true;"
          >
            <v-list-item-icon>
              <v-icon> arrow_right_alt </v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title
                >{{ $t("add_trader_link") }}</v-list-item-title>
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
          <v-divider></v-divider>
          <v-list-item
            :to="{ name: 'user-editor'}"
          >
            <v-list-item-icon>
              <v-icon>account_box</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>
                {{$t("edit_registor_info")}}
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
    <template v-if="this.$root.$el.clientWidth > 500">
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
    </template>
    <template v-else>
      <router-link
        class="ma-4"
        :to="{ name: 'home' }"
      >
        {{ $t("paper") }}
      </router-link>
    </template>
    <v-spacer></v-spacer>
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
          icon: "description",
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
  mounted() {
    this.$root.$on('link_dialog', data => {
        this.dialog = data;
    });
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

<style scoped>
</style>
