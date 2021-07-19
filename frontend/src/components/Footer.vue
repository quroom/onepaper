<template>
  <v-footer absolute app width="auto" style="overflow:auto">
    <v-row color="lighten-1" justify="center" no-gutters style="overflow:auto">
      <template v-for="link in links">
        <v-btn
          v-if="link.route != undefined"
          :key="link.title"
          :to="link.route"
          text
          rounded
          class="my-2"
          exact
        >
          {{ $t(link.title) }}
        </v-btn>
        <v-btn
          v-else
          :key="link.title"
          text
          rounded
          class="my-2 ml-6"
          exact
          :href="`mailto:${link.email}`"
        >
          {{ $t(link.title) }}:{{ link.email }}
        </v-btn>
      </template>
      <v-col class="text-center" cols="12">
        {{ $t("footer_info") }}
        <br />
        Copyright © ONEPAPER. All Rights Reserved.
      </v-col>
    </v-row>
  </v-footer>
</template>

<script>
export default {
  name: "Footer",
  data: () => ({
    links: [
      // 회사소개, 공지사항, 이용안내, 고객센터, 고객센터 만들기전까지 contact_us
      { title: "service_intro", route: { name: "service-intro" } },
      // #FIXME It doesn't work correcly So I stop to support until it works well.
      // { title: "how_to_use", route: { name: "manuals" } },
      { title: "notice", route: { name: "notices" } },
      { title: "contact_us", email: "quroom@naver.com" }
    ]
  })
};
</script>

<style></style>
