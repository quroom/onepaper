<template>
  <v-container min-width="250">
    <NotionRenderer
      :blockMap="blockMap"
      :mapPageUrl="mapPageUrl"
      :pageLinkOptions="pageLinkOptions"
      fullPage
    />
  </v-container>
</template>

<script>
//Vue-Notion Manual : https://github.com/janniks/vue-notion/tree/main/docs#notion-api
import { NotionRenderer, getPageBlocks } from "vue-notion";

export default {
  components: { NotionRenderer },
  data() {
    return {
      pageLinkOptions: { component: "router-link", href: "to" },
      blockMap: null
    };
  },
  methods: {
    mapPageUrl(pageId = "") {
      pageId = pageId.replace(/-/g, "");
      return `/manuals/${pageId}`;
    }
  },
  async created() {
    // get Notion blocks from the API via a Notion pageId
    this.blockMap = await getPageBlocks("ae3044376388491794b73ace424b27f3");
  }
};
</script>

<style scoped>
@import "../../node_modules/vue-notion/src/styles.css"; /* optional Notion-like styles */
</style>
