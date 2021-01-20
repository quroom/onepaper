<template>
  <v-app-bar app width="100%">
    <v-dialog v-model="dialog" max-width="400px" @click:outside="messages = []; success = false;">
      <v-card>
        <v-card-title>
          {{ `${ $t("add_quick_trade_user")} ${$t('link')}` }}
        </v-card-title>
        <v-card-text class="text-body-1 text--primary">
          <LazyTextField
            v-model="link"
            :label="$t('link')"
            ref="link"
            :success="success"
            :success-messages="messages"
            readonly
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
            <template v-if="isShown(item)">
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
              <v-icon> link </v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title
                >{{ $t("add_quick_trader_link") }}</v-list-item-title>
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
        <v-btn
          v-if="isShown(item)"
          class="my-2"
          text
          rounded
          :to="item.route"
          :key="item.title"
          exact
        >
          {{ $t(item.title) }}
        </v-btn>
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
      <span class="font-weight-bold">[{{ username }}]</span>
      <v-icon>exit_to_app</v-icon>
    </v-btn>
  </v-app-bar>
</template>
<script>
export default {
  name: "NavbarItem",
  data() {
    return {
      username: null,
      drawer: false,
      items: [
        {
          title: "paper",
          icon: "description",
          route: { name: "home" },
        },
        {
          title: "profile",
          icon: "account_box",
          route: { name: "profiles" },
        },
        {
          title: "mandate_paper",
          icon: "description",
          route: { name: "mandates" },
          user_category: "expert",
          expert_only: true,
        },
        {
          title: "approve",
          icon: "how_to_reg",
          route: { name: "approve-expert" },
          user_category: "staff",
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
    const name = window.localStorage.getItem("name")
    this.username = window.localStorage.getItem("username")
    this.link = window.location.protocol + "//" + window.location.host + "/" + "profiles" + "/" + this.username + "/" + name;
    this.user_category = window.localStorage.getItem("user_category")
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
    },
    isShown(item){
      return !item.user_category || this.user_category=='staff' || item.user_category == this.user_category;
    }
  }
};
</script>

<style scoped>
</style>
