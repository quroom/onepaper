<template>
  <NotionRenderer :blockMap="blockMap" :mapPageUrl=mapPageUrl :pageLinkOptions="pageLinkOptions" fullPage />
</template>

<script>
import { NotionRenderer, getPageBlocks } from "vue-notion";

export default {
  name: "ManualDetail",
  props: {
    id: {
      required: true,
    }
  },
  components: { NotionRenderer },
  watch: {
    //Update page from samepage, just with different pageid.
    '$route.path': async function(){
      console.log(this.$route.params.id);
      this.blockMap = await getPageBlocks(this.$route.params.id)
    }
  },
  data(){
    return { 
      pageLinkOptions: { component: 'router-link', href: 'to' },
      blockMap: null 
    }
  },
  methods:{
    mapPageUrl(pageId = "") {
      pageId = pageId.replace(/-/g, "");
      return `/manuals/${pageId}`;
    }
  },
  async created() {
    this.blockMap = await getPageBlocks(this.id);
  },
};
</script>

<style scoped>
@import "../../node_modules/vue-notion/src/styles.css"; /* optional Notion-like styles */
</style>