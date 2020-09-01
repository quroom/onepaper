<template>
  <div class="container my-5">
    <h1>test</h1>
  </div>
</template>

<script>
import i18n from "@/plugins/i18n";

export default {
  name: "PaperEditor",
  data() {
    return {
      land_type: null,
      lot_area: null,
      building_structure: null,
      building_type: null,
      building_area: null,
      title: null,
      trade_type: null,
      address: null,
      room_name: null,
      realesate_type: null,
      down_payment: null,
      security_deposit: null,
      monthly_fee: null,
      from_date: null,
      to_date: null,
      expert_id: null,
      seller_id: null,
      buyer_id: null,
      special_agreement: null,
    }
  },
  created() {
    document.title = i18n.t("created_paper_title")
  }
}
</script>
<style>

</style>