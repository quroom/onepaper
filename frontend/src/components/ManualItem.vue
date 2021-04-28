<template>
  <NotionRenderer
    :blockMap="blockMap"
    :mapPageUrl="mapPageUrl"
    :pageLinkOptions="pageLinkOptions"
    fullPage
  />
</template>

<script>
import { NotionRenderer, getPageBlocks } from "vue-notion";

export default {
  name: "ManualItem",
  props: {
    id: {
      required: true
    }
  },
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
    this.blockMap = await getPageBlocks(this.id);
  }
};
</script>

<style scoped>
@import "../../node_modules/vue-notion/src/styles.css"; /* optional Notion-like styles */
</style>
