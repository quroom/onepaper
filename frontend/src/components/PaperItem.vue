<template>
  <v-col class="pa-1" cols="12" sm="6" lg="4" xl="3">
    <v-card class="outlined tile" :to="{ name: 'paper-detail', params: { id: paper.id } }">
      <template v-if="paper.status !== null">
        <v-chip class="ma-2 mr-0">
          {{ paper.id }}
        </v-chip>
        <v-chip v-if="paper.is_hidden" class="ma-2 mr-0" ark label>
          <v-icon left>
            visibility_off
          </v-icon>
        </v-chip>
        <v-chip
          class="ma-2 mr-0"
          :color="
            paper.status == $getConstByName('status_category', 'progress')
              ? 'success'
              : paper.status == $getConstByName('status_category', 'done')
              ? 'primary'
              : paper.status == $getConstByName('status_category', 'draft')
              ? ''
              : paper.status == $getConstByName('status_category', 'denied')
              ? 'error'
              : 'deep-purple'
          "
          dark
          label
        >
          <v-icon left>
            label
          </v-icon>
          {{ $getConstI18("status_category", paper.status) }}
        </v-chip>
        <div class="text-body-2 ma-2 mr-1" style="float:right">{{ paper.updated_at }}</div>
      </template>
      <v-card-title class="card-title pt-2 pb-0 px-4 text-truncate text-center">
        {{ paper.title }}
      </v-card-title>
      <v-card-text v-if="paper.address">
        <div>
          <span>{{ paper.address.old_address }}</span>
          <span v-if="paper.address.detail">, {{ paper.address.detail }}</span>
        </div>
        <div>
          {{ `${$t("term_of_lease")}: ${paper.from_date} ~ ${paper.to_date}` }}
        </div>
        <span>
          <template v-if="paper.trade_category == $getConstByName('trade_category', 'rent')">
            <div>
              {{
                `${$t("security_deposit")}: 
                  ${paper.security_deposit}${$t("won")}`
              }}
            </div>
            <div>
              {{ `${$t("monthly_fee")}: ${paper.monthly_fee}${$t("won")}` }}
            </div>
            <span>{{ `${$t("maintenance_fee")}: ${paper.maintenance_fee}${$t("won")}` }}</span>
          </template>
          <template
            v-else-if="paper.trade_category == $getConstByName('trade_category', 'depositloan')"
          >
            <div>
              {{ `${$t("security_deposit")}: ${paper.security_deposit}${$t("won")}` }}
            </div>
            <span>{{ `${$t("maintenance_fee")}: ${paper.maintenance_fee}${$t("won")}` }}</span>
          </template>
          <!-- #FIXME to be updated -->
          <template
            v-else-if="paper.trade_category == $getConstByName('trade_category', 'purchase')"
          >
          </template>
          <template
            v-else-if="paper.trade_category == $getConstByName('trade_category', 'exchange')"
          >
          </template>
          <!-- <span class="answer_count">
            {{`${$t('answer')}(${paper.answer_count})`}}
          </span> -->
        </span>
      </v-card-text>
    </v-card>
  </v-col>
</template>

<script>
export default {
  name: "PaperItem",
  props: {
    paper: {
      type: Object,
      required: true
    }
  },
  methods: {
    clear() {
      this.$refs["signaturePad"].clearSignature();
    },
    open() {
      this.$nextTick(() => {
        this.$refs["signaturePad"].resizeCanvas();
      });
    },
    newtab(image) {
      let newTab = window.open();
      newTab.document.body.innerHTML = "<img src=" + image + ' width="500px" height="500px">';
    }
  },
  created() {
    this.requestUser = this.$store.state.user.email;
  }
};
</script>

<style scoped>
.answer_count {
  position: absolute;
  right: 10px;
}
.author-name {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.card-title {
  display: block;
  font-size: 1rem;
}
</style>
