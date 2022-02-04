<template>
  <v-col cols="12" sm="6" md="4" lg="3">
    <v-card class="outlined tile">
      <v-carousel height="250px">
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
              <img :src="image.image" style="height: 100%; max-height:250px; margin: auto;" />
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
        <v-card-title class="card-title pt-2 pb-0 px-4 text-truncate text-center">
          {{ listing.title }}
        </v-card-title>
        <v-card-text class="pr-0 pb-0">
          <div>
            {{
              listing.listingaddress.old_address ? listing.listingaddress.old_address : $t("none")
            }}
          </div>
          <span>
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
            <!-- <span class="answer_count">
            {{`${$t('answer')}(${listing.answer_count})`}}
          </span> -->
          </span>
        </v-card-text>
        <v-card-actions class="pt-0">
          <v-chip v-if="listing.online_visit === true" class="ml-1 mt-1" color="primary">{{
            $t("online_visit")
          }}</v-chip>
          <v-chip v-if="listing.short_lease === true" class="ml-1 mt-1" color="orange" dark>{{
            $t("short_lease")
          }}</v-chip>
          <v-spacer></v-spacer>
          <v-btn text color="black accent-4">
            {{ `${$t("detail")} ${$t("view")}` }}
          </v-btn>
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
