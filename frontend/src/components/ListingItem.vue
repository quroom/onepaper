<template>
  <!-- FIXME: Need to be optimization for layout -->
  <v-col class="pa-1" cols="12" sm="6" md="4" lg="3">
    <v-card class="outlined tile">
      <v-carousel height="200px">
        <v-chip class="item-category">{{
          $getConstI18("ITEM_CATEGORY", listing.item_category)
        }}</v-chip>
        <v-chip class="mobile-number" :color="is_certificated ? '' : 'red lighten-2'">
          <div class="text-right">
            {{
              `${
                listing.author_profile.mobile_number
                  ? listing.author_profile.mobile_number
                  : $t("none")
              }`
            }}
          </div>
        </v-chip>
        <v-carousel-item
          class="text-center"
          v-for="(image, i) in listing.images"
          :key="i"
          @click.stop
        >
          <v-row no-gutters align="center" justify="center">
            <router-link
              :to="{
                name: 'listing-detail',
                params: { id: listing.id }
              }"
            >
              <img :src="image.image" style="height: 100%; max-height:200px; margin: auto;" />
            </router-link>
          </v-row>
        </v-carousel-item>
      </v-carousel>
      <router-link
        :to="{
          name: 'listing-detail',
          params: { id: listing.id }
        }"
        style="text-decoration: none; color: inherit;"
      >
        <v-card-title class="card-title pt-1 pb-0 px-4 text-truncate text-center">
          {{ listing.title }}
        </v-card-title>
        <v-card-text class="pr-0 pb-0">
          <div>
            {{
              listing.listingaddress.old_address ? listing.listingaddress.old_address : $t("none")
            }}
          </div>
          <span>
            <template v-if="!is_sharehouse">
              <template v-if="listing.trade_category == $getConstByName('trade_category', 'rent')">
                <div>
                  {{
                    `${$t("security_deposit_short")}${listing.security_deposit}${$t("man")}
                      ${$t("monthly_fee_short")}${listing.monthly_fee}${$t("man")} /
                      ${$t("maintenance_fee")}${listing.maintenance_fee}${$t("man")}`
                  }}
                </div>
              </template>
              <template
                v-else-if="
                  listing.trade_category == $getConstByName('trade_category', 'depositloan')
                "
              >
                <div>
                  {{
                    `${$t("security_deposit")}${listing.security_deposit}${$t("man")} /
                      ${$t("maintenance_fee")}${listing.maintenance_fee}${$t("man")}`
                  }}
                </div>
              </template>
              <template
                v-else-if="listing.trade_category == $getConstByName('trade_category', 'purchase')"
              >
              </template>
              <template
                v-else-if="listing.trade_category == $getConstByName('trade_category', 'exchange')"
              >
              </template>
            </template>
            <div class="pr-4 text-right">
              {{
                this.listing.listingvisits_count > 0
                  ? `${$t("ask_move_in")}(${this.listing.listingvisits_count})`
                  : ""
              }}
              {{ this.listing.listingvisits_count > 0 && this.avaliable_count > 0 ? " / " : "" }}
              <span class="red--text">
                {{ this.avaliable_count > 0 ? `${$t("vacancy")}(${this.avaliable_count})` : "" }}
              </span>
            </div>
            <!-- <span class="answer_count">
            {{`${$t('answer')}(${listing.answer_count})`}}
          </span> -->
          </span>
        </v-card-text>
        <v-card-actions class="pt-0 pb-1">
          <v-chip v-if="listing.online_visit === true" class="ml-1 mt-1" color="primary">{{
            $t("online_visit")
          }}</v-chip>
          <v-chip v-if="listing.minimum_period < 12" class="ml-1 mt-1" color="orange" dark>{{
            `${listing.minimum_period}${$t("months")}`
          }}</v-chip>
          <v-spacer></v-spacer>
          <v-btn v-if="avaliable_count > 0" text color="black accent-4">
            {{ `${$t("detail")} ${$t("view")}` }}
          </v-btn>
          <v-chip v-else class="ml-1 mt-1" color="red lighten-1" dark>{{
            $t("no_vacancy")
          }}</v-chip>
        </v-card-actions>
      </router-link>
    </v-card>
  </v-col>
</template>

<script>
export default {
  name: "ListingItem",
  props: {
    listing: {
      type: Object,
      required: true
    }
  },
  computed: {
    is_certificated: function() {
      if (this.listing.author_profile.certification) {
        return this.listing.author_profile.certification.is_certificated;
      }
      return false;
    },
    is_sharehouse: function() {
      return this.listing.item_category == this.$getConstByName("ITEM_CATEGORY", "sharehouse");
    },
    avaliable_count: function() {
      if (this.is_sharehouse) {
        const count = this.listing.listingitems.filter((listingitem) => {
          if (new Date(listingitem.available_date) <= new Date()) {
            return true;
          } else {
            return false;
          }
        }).length;
        return count;
      } else {
        return new Date(this.listing.available_date) <= new Date() ? 1 : 0;
      }
    }
  },
  methods: {}
};
</script>

<style scoped>
.card-title {
  display: block;
  font-size: 1rem;
  font-weight: 500;
}
.item-category {
  position: absolute;
  top: 8px;
  left: 8px;
  opacity: 0.85;
  z-index: 1;
}
.mobile-number {
  position: absolute;
  top: 8px;
  right: 8px;
  opacity: 0.85;
  z-index: 1;
}
</style>
