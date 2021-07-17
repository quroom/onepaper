<template>
  <v-col class="pa-1" cols="12" sm="6" lg="4" xl="3">
    <v-card class="outlined tile" :to="{ name: 'paper-detail', params: { id: paper.id } }">
      <v-chip class="ma-2 mr-0">
        {{ paper.id }}
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
      <div class="text-body-2 mt-2 mr-1" style="float:right; max-width: 220px;">
        {{ paper.updated_at }}
        <div v-if="paper.author">
          <div :class="{ 'author-name': true, 'primary--text': paper.is_contractor }">
            <span> {{ paper.author }} </span>
          </div>
        </div>
      </div>
      <v-card-title class="card-title pt-2 pb-0 px-4 text-truncate text-center">
        {{ paper.title }}
      </v-card-title>
      <v-card-text v-if="paper.address">
        <div>
          {{ paper.address.old_address }}
          <span v-if="!!paper.address.dong"> {{ paper.address.dong }}{{ $t("dong") }}</span>
          <span v-if="!!paper.address.ho"> {{ paper.address.ho }}{{ $t("ho") }}</span>
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
