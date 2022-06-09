<template>
  <v-app-bar app width="100%">
    <v-dialog
      v-model="dialog"
      max-width="400px"
      @click:outside="
        messages = [];
        success = false;
      "
    >
      <v-card>
        <v-card-title>
          {{ `${$t("add_quick_trade_user")} ${$t("link")}` }}
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
          <v-btn color="primary" @click.stop="copyText()">
            {{ $t("copy") }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-app-bar-nav-icon
      id="v-menu"
      @click="
        drawer = true;
        showTour(false);
      "
    >
    </v-app-bar-nav-icon>
    <v-navigation-drawer v-model="drawer" absolute temporary app @input="drawerInput">
      <v-row justify="center">
        <v-col class="menu-cursor text-body-2 pa-2" cols="auto">{{ $t("menu") }}</v-col>
        <v-btn class="close-btn" text icon @click="drawer = false">
          <v-icon class="close-icon">
            close
          </v-icon>
        </v-btn>
      </v-row>
      <v-divider></v-divider>
      <v-list dense>
        <router-link v-for="item in items" :to="item.route" :key="item.title + `-nav`">
          <template v-if="isShown(item)">
            <v-list-item link>
              <v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>{{
                  `${$t(item.title)}${item.title2 ? "(" + $t(item.title2) + ")" : ""}`
                }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </template>
        </router-link>
        <v-divider></v-divider>
        <v-list-item key="link" @click="dialog = true">
          <v-list-item-icon>
            <v-icon> link </v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ $t("add_quick_trader_link") }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item @click="switchLoc()">
          <v-list-item-icon>
            <span v-if="this.$i18n.locale === 'ko'">
              EN
            </span>
            <span v-else>
              한국
            </span>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ $t("language_change") }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider></v-divider>
      </v-list>
      <div class="pa-2 pt-4">
        <v-btn block dark color="error" href="/accounts/logout/">
          {{ $t("logout") }}
          <v-icon>exit_to_app</v-icon>
        </v-btn>
      </div>
    </v-navigation-drawer>
    <v-spacer></v-spacer>
    <template v-if="!is_minimum_width">
      <template v-for="item in items">
        <v-btn
          :id="`v-${item.route.name}`"
          color="primary"
          v-if="isShown(item) && !item.appbar_only"
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
    <v-spacer></v-spacer>
    <v-btn
      v-if="this.$store.state.user_category === 'user'"
      id="v-help"
      color="grey darken-2"
      text
      rounded
      @click.prevent="showTour(true)"
    >
      <v-icon> help </v-icon>
    </v-btn>
  </v-app-bar>
</template>
<script>
import { apiService } from "@/common/api_service";
import { applyValidation } from "@/common/common_api";

export default {
  name: "NavbarItem",
  computed: {
    is_minimum_width() {
      return this.$vuetify.breakpoint.width < this.$store.state.minimum_width;
    }
  },
  data() {
    return {
      email: null,
      drawer: false,
      items: [
        {
          title: "listing",
          icon: "description",
          route: { name: "listings" }
        },
        {
          title: "paper",
          icon: "description",
          route: { name: "papers" }
        },
        {
          title: "profile",
          icon: "account_box",
          route: { name: "profiles" }
        },
        {
          title: "ask_move_in",
          title2: "ask",
          icon: "description",
          appbar_only: true,
          route: { name: "asklistings" }
        },
        {
          title: "mandate_paper",
          icon: "description",
          route: { name: "mandates" },
          user_category: "expert",
          //FIXME: Should be removed.
          expert_only: true,
          appbar_only: true
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
  created() {
    this.email = this.$store.state.user.email;
    this.link = `${window.location.protocol}//${window.location.host}/profiles/${this.email}`;
    this.user_category = this.$store.state.user_category;
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
      this.messages = `${this.$i18n.t("link_is_copied")}<br>${this.$i18n.t("send_your_link")}`;
    },
    isShown(item) {
      return (
        !item.user_category ||
        this.user_category == "staff" ||
        item.user_category == this.user_category
      );
    },
    drawerInput(toggle) {
      if (toggle == false) {
        this.showTour();
      }
    },
    showTour(flag) {
      if (
        ["papers", "paper-detail", "paper-editor", "profile-editor"].indexOf(this.$route.name) <=
        -1
      ) {
        if (flag === true) {
          alert(this.$t("unspport_function"));
          return 0;
        } else {
          return 0;
        }
      }
      if (flag) {
        this.$store.commit("SET_USER_SETTING", { is_tour_on: true });
        let endpoint = "/api/user-setting/";
        let method = "PUT";
        let data = {
          is_tour_on: true
        };
        apiService(endpoint, method, data).then((data) => {
          if (data.id == undefined) {
            applyValidation(data);
          }
        });
      }
      const tour_name = this.$route.name;
      if (flag) {
        if (this.$tours[tour_name].currentStep == -1) {
          this.$tours[tour_name].currentStep =
            this.$store.state.tour_index === -1 ? 0 : this.$store.state.tour_index;
        }
      } else if (flag === false) {
        this.$store.commit("SET_TOUR_INDEX", this.$tours[tour_name].currentStep);
        this.$tours[tour_name].currentStep = -1;
      } else {
        if (
          this.$store.state.user_setting.is_tour_on &&
          this.$tours[tour_name].currentStep == -1
        ) {
          this.$tours[tour_name].currentStep = this.$store.state.tour_index;
        }
      }
    }
  }
};
</script>

<style scoped>
.close-btn {
  cursor: pointer !important;
  position: absolute;
  width: 36px !important;
  height: 36px !important;
  top: 0px;
  right: 0px;
}
.menu-cursor {
  cursor: default;
}
</style>
