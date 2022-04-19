<template>
  <v-container>
    <v-overlay v-if="isLoading">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </v-overlay>
    <template v-if="id && isAuthor">
      <v-chip-group>
        <DeleteAlert v-if="readonly" :id="id" url="/api/listings/" router_name="listings" />
        <v-spacer></v-spacer>
        <v-btn v-if="readonly" class="ma-1 auto" color="green" dark @click="readonly_flag = false">
          {{ $t("edit") }}
        </v-btn>
        <v-btn v-else class="ma-1 auto" dark @click="readonly_flag = true">
          {{ $t("read_mode") }}
        </v-btn>
      </v-chip-group>
    </template>
    <template v-if="!id">
      <v-row justify="center" no-gutters>
        <v-radio-group row v-model="is_asking">
          <v-radio :label="$t('ask')" :value="true" :readonly="readonly"></v-radio>
          <v-radio :label="$t('sale')" :value="false" :readonly="readonly"></v-radio>
        </v-radio-group>
      </v-row>
      <ValidationObserver v-if="is_asking" ref="asking_obs">
        <AskListing :obj="ask_listing_obj" :fields_names="fields_names"></AskListing>
      </ValidationObserver>
    </template>
    <ValidationObserver v-show="!is_asking || id" ref="obs">
      <v-row no-gutters>
        <v-col id="v-create-listing" cols="12">
          <ValidationProvider
            v-slot="{ errors }"
            ref="title"
            :name="`${$t('title')}`"
            :rules="`required|max:20`"
          >
            <v-text-field
              class="ma-auto"
              v-model="title"
              :readonly="readonly"
              :error-messages="errors"
              :label="`${$t('title')}`"
              :placeholder="readonly ? $t('no_result') : ''"
              type="String"
              style="max-width:400px"
            ></v-text-field>
          </ValidationProvider>
        </v-col>
      </v-row>
      <ValidationProvider
        ref="image"
        :name="$t('room_images')"
        :rules="`${image_required}|max_count:10`"
        v-slot="{ errors }"
      >
        <v-row align="center" justify="center" style="height:100%; ">
          <!-- #FIXME: unnecessary space line -->
          <v-col cols="12" style="max-width: 700px;">
            <v-switch
              class="ma-0"
              v-if="id"
              :readonly="isAuthor ? false : true"
              v-model="status"
              :label="status ? $t('vacancy') : $t('no_vacancy')"
              hide-details="auto"
              style="min-width:140px; width:140px"
              @click="isAuthor ? update_status() : ''"
            ></v-switch>
          </v-col>
          <v-carousel
            v-if="images_data.length"
            ref="carousel"
            height="400px"
            style="width:100vw; min-wdith:345px; max-width:700px; border:1px solid grey;"
          >
            <v-carousel-item v-for="(image, i) in images_data" :key="i">
              <v-img
                contain
                :src="image.image_src"
                style="max-width: 100%; height: 100%; max-height:350px; margin: auto;"
              >
                <v-row class="carousel-menu" v-if="!readonly">
                  <v-btn
                    v-if="images_data.length > 1"
                    @click="deleteImage(i)"
                    color="red darken-2"
                    dark
                    icon
                    width="auto"
                  >
                    <v-icon>remove_circle</v-icon>
                    <span>{{ $t("delete_image") }}</span>
                  </v-btn>
                  <v-spacer></v-spacer>
                  <v-btn
                    v-if="image.is_default !== true"
                    @click="setDefaultImageIndex(i)"
                    color="green"
                    dark
                    width="auto"
                  >
                    <v-icon>check</v-icon>
                    <span>{{ $t("default") }}</span>
                  </v-btn>
                  <v-btn v-else color="green" dark text width="auto">
                    <v-icon>check</v-icon>
                    <span>{{ $t("default") }}</span>
                  </v-btn>
                </v-row>
              </v-img>
            </v-carousel-item>
          </v-carousel>
        </v-row>
        <!-- #FIXME:Drag and Drop 구현 https://george-hadjigeorgiou97.medium.com/step-by-step-custom-drag-drop-upload-component-in-vuetify-vue-2-43c99794643d -->

        <v-file-input
          v-if="!readonly"
          :clearable="false"
          multiple
          :label="$t('room_images')"
          accept="image/*"
          @click.stop
          @change="changeImages"
          :error-messages="errors"
        >
          <template v-slot:selection="{ index }">
            <span v-if="index == 0">{{ images_data.length }} Files</span>
          </template>
        </v-file-input>
      </ValidationProvider>
      <v-row>
        <v-col cols="12" sm="8">
          <AddressSearch
            id="v-address"
            ref_name="address"
            :readonly="readonly"
            :label="readonly ? $t('address') : $t('address') + $t('search')"
            outlined
            :address.sync="address"
          ></AddressSearch>
        </v-col>
        <v-col cols="6" sm="2">
          <LazyTextField
            v-model="address.dong"
            :readonly="readonly"
            :label="`(${$t('optional')}) ${$t('dong')}`"
            outlined
            hide-details="auto"
          ></LazyTextField>
        </v-col>
        <span id="v-dong-ho"></span>
        <v-col cols="6" sm="2">
          <LazyTextField
            v-model="address.ho"
            :readonly="readonly"
            :label="`(${$t('optional')}) ${$t('ho')}`"
            outlined
            hide-details="auto"
          ></LazyTextField>
        </v-col>
      </v-row>
      <v-row>
        <v-col v-if="readonly ? online_visit : true" class="_checkbox" cols="2" sm="auto">
          <v-checkbox
            v-model="online_visit"
            :readonly="readonly"
            :label="$t('online_visit')"
          ></v-checkbox>
        </v-col>
        <v-col v-if="readonly ? short_lease : true" class="_checkbox" cols="2" sm="auto">
          <v-checkbox
            v-model="short_lease"
            :readonly="readonly"
            :label="$t('short_lease')"
          ></v-checkbox>
        </v-col>
        <v-col cols="4" sm="auto">
          <ValidationProvider
            ref="item_category"
            :name="$t('item_category')"
            v-slot="{ errors }"
            rules="required"
          >
            <v-select
              id="v-item-category"
              v-model="item_category"
              :readonly="readonly"
              :error-messages="errors"
              :items="$getConstList('ITEM_CATEGORY_LIST')"
              item-text="text"
              item-value="value"
              :label="$t('item_category')"
              style="max-width:150px"
            >
              <template v-slot:selection="{ item }">{{ $t(item.text) }}</template>
              <template v-slot:item="{ item }">{{ $t(item.text) }}</template>
            </v-select>
          </ValidationProvider>
        </v-col>
        <v-col cols="4" sm="auto">
          <ValidationProvider
            ref="trade_category"
            :name="$t('trade_category')"
            v-slot="{ errors }"
            rules="required"
          >
            <v-select
              id="v-trade-category"
              v-model="trade_category"
              :readonly="readonly"
              :error-messages="errors"
              :items="$getConstList('TRADE_CATEGORY_LIST')"
              item-text="text"
              item-value="value"
              :label="$t('trade_category')"
              style="max-width:150px"
            >
              <template v-slot:selection="{ item }">{{ $t(item.text) }}</template>
              <template v-slot:item="{ item }">{{ $t(item.text) }}</template>
            </v-select>
          </ValidationProvider>
        </v-col>
        <template v-if="trade_category == $getConstByName('TRADE_CATEGORY', 'rent')">
          <v-col
            v-for="(contract_field, index) in fields_names.contract_fields"
            cols="auto"
            :key="`index` + index"
          >
            <ValidationProvider
              v-slot="{ errors }"
              :ref="contract_field.name"
              :name="$t(contract_field.name)"
              :rules="`required|max_value:${contract_field.max_value}`"
            >
              <LazyTextField
                v-model="$data['' + contract_field.name]"
                :readonly="readonly"
                :error-messages="errors"
                :label="$t(contract_field.name)"
                :suffix="$t('manwon')"
                :type="contract_field.type"
                required
                style="width:150px;"
              ></LazyTextField>
            </ValidationProvider>
          </v-col>
        </template>
        <template v-else>
          <template v-for="(contract_field, index) in fields_names.contract_fields">
            <v-col
              v-if="contract_field.name != 'monthly_fee'"
              cols="6"
              md="3"
              :key="`index` + index"
            >
              <ValidationProvider
                v-slot="{ errors }"
                :ref="contract_field.name"
                :name="$t(contract_field.name)"
                :rules="`required|max_value:${contract_field.max_value}`"
              >
                <LazyTextField
                  v-model="$data['' + contract_field.name]"
                  :readonly="readonly"
                  :error-messages="errors"
                  :label="$t(contract_field.name)"
                  :suffix="$t('manwon')"
                  :type="contract_field.type"
                  required
                ></LazyTextField>
              </ValidationProvider>
            </v-col>
          </template>
        </template>
      </v-row>
      <LazyTextArea
        class="mt-4"
        v-model="content"
        :label="`(${$t('optional')}) ${$t('detail_info')}`"
        :placeholder="readonly ? $t('no_result') : $t('detail_info_placeholder')"
        outlined
        rows="4"
        auto-grow
        :readonly="readonly"
      ></LazyTextArea>
      <v-divider class="my-2"></v-divider>
      <v-card v-if="readonly">
        <v-card-title class="grey darken-1">
          <span v-if="author_profile.expert_profile" class="text-h6 white--text"
            >{{ `${$t("realestate_agency")}` }}
          </span>
          <span v-else class="text-h6 white--text">{{ `${$t("author")}` }} </span>
        </v-card-title>
        <v-list>
          <v-list-item>
            <v-list-item-action>
              {{ $t("mobile_number") }}
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>{{ author_profile.mobile_number }}</v-list-item-title>
              <v-list-item-subtitle
                v-if="
                  author_profile.certification
                    ? author_profile.certification.is_certificated
                    : false
                "
                class="c"
              >
                {{
                  $t("certified_detail", { updated_at: author_profile.certification.updated_at })
                }}</v-list-item-subtitle
              >
              <v-list-item-subtitle v-else class="uncertified-mobile">{{
                $t("uncertified_detail")
              }}</v-list-item-subtitle>
            </v-list-item-content>

            <v-list-item-action>
              <a
                v-if="UA.indexOf('android') > -1"
                :href="
                  `sms://${author_profile.mobile_number}?&body=${$t('insterested_in', {
                    link: current_url
                  })}`
                "
              >
                <v-icon>sms</v-icon>
              </a>
              <!-- #FIXME:Comment out because test is not done yet. -->
              <!-- <a
                v-else-if="UA.indexOf('iphone') > -1 || UA.indexOf('ipad') > -1"
                :href="
                  `sms://${author_profile.mobile_number}&body=${$t('insterested_in', {
                    link: current_url
                  })}`
                "
              >
                <v-icon>sms</v-icon>
              </a> -->
            </v-list-item-action>
          </v-list-item>
          <v-divider inset></v-divider>
          <template v-if="author_profile.expert_profile">
            <v-list-item>
              <v-list-item-action>
                {{ $t("registration_number") }}
              </v-list-item-action>

              <v-list-item-content>
                <v-list-item-title>{{
                  author_profile.expert_profile.registration_number
                }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>

            <v-divider inset></v-divider>
            <v-list-item>
              <v-list-item-action>{{ $t("owner") }} </v-list-item-action>

              <v-list-item-content>
                <v-list-item-title>{{ author_profile.user.name }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>

            <v-divider inset></v-divider>

            <v-list-item>
              <v-list-item-action>{{ $t("shop_name") }} </v-list-item-action>

              <v-list-item-content>
                <v-list-item-title>{{
                  author_profile.expert_profile.shop_name
                }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>

            <v-divider inset></v-divider>

            <v-list-item>
              <v-list-item-action>{{ $t("address") }} </v-list-item-action>

              <v-list-item-content>
                <v-list-item-title>{{ full_newaddress }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </template>
        </v-list>
      </v-card>
    </ValidationObserver>
    <v-col v-if="!id || !readonly" cols="12" class="text-right">
      <v-btn id="v-submit" class="primary" @click="submit()">{{ $t("submit") }}</v-btn>
    </v-col>
  </v-container>
</template>

<script>
import { apiService, apiService_formData } from "@/common/api_service";
import { applyValidation } from "@/common/common_api";
import Constants from "@/plugins/Constants";
import AskListing from "@/components/AskListing";
import DeleteAlert from "@/components/DeleteAlert";
import resizeImage from "@/plugins/image_resize";

export default {
  name: "ListingEditor",
  props: {
    default_is_asking: {
      type: [Boolean],
      required: false
    }
  },
  components: {
    AskListing,
    DeleteAlert
  },
  computed: {
    current_url: function() {
      if (window) {
        return window.location.href;
      }
      return "";
    },
    full_newaddress: function() {
      const address = this.author_profile.address;
      var fullNewAddress = address.new_address;
      var dongExist = false;
      if (address.dong) {
        fullNewAddress += `, ${address.dong}${this.$i18n.t("dong")}`;
        dongExist = true;
      }
      if (address.ho) {
        if (dongExist) {
          fullNewAddress += ` ${address.ho}${
            this.author_profile.expert_profile.is_shown_ho ? this.$i18n.t("ho") : ""
          }`;
        } else {
          fullNewAddress += `, ${address.ho}${
            this.author_profile.expert_profile.is_shown_ho ? this.$i18n.t("ho") : ""
          }`;
        }
      }
      return fullNewAddress;
    },
    fields_names() {
      return {
        contract_fields: [
          {
            name: "security_deposit",
            type: "Number",
            max_value: Constants.MAX_SECURITY_DEPOSIT
          },
          {
            name: "monthly_fee",
            type: "Number",
            max_value: Constants.MAX_MONTHLY_FEE
          },
          {
            name: "maintenance_fee",
            type: "Number",
            max_value: Constants.MAX_MAINTENANCE_FEE
          }
        ]
      };
    },
    image_required() {
      const image_links_length = this.image_links.filter((item) => item.is_deleted == false)
        .length;
      const images_length = this.images.length;
      const total_images_length = image_links_length + images_length;

      if (total_images_length < 1) {
        return "required";
      }
      return "";
    },
    isAuthor() {
      if (this.author_profile.user) {
        return this.author_profile.user.email === this.$store.state.user.email;
      }
      return false;
    },
    readonly() {
      return this.id != null ? this.readonly_flag : false;
    },
    images_data() {
      var _images = [];
      for (const image_link of this.image_links) {
        if (image_link.is_deleted !== true) {
          _images.push({
            obj: image_link,
            image: null,
            id: image_link.id,
            image_src: image_link.image,
            delete: image_link.is_deleted ? true : false,
            is_default: image_link.is_default
          });
        }
      }
      for (const image_file of this.local_images) {
        _images.push({
          obj: image_file.image,
          image: image_file.image,
          image_src: image_file.image_src,
          delete: false,
          is_default: image_file.is_default ? true : false
        });
      }
      const default_list = _images.filter((item) => item.is_default === true);
      if (default_list.length === 0 && _images.length !== 0) {
        _images[0].is_default = true;
      }

      return _images;
    },
    UA() {
      return navigator.userAgent.toLowerCase();
    }
  },
  watch: {
    images(vals) {
      this.local_images = vals.reduce(
        (acc, item) => [
          ...acc,
          {
            image: item,
            is_default: item.is_default ? item.is_default : false,
            image_src: window.URL.createObjectURL(item)
          }
        ],
        []
      );
      const default_image_data = this.images_data.find((item) => item.is_default === true);
      if (default_image_data === undefined) {
        this.local_images[0].is_default = true;
      }
    }
  },
  data() {
    return {
      id: undefined,
      isLoading: false,
      is_listing_updated: false,
      readonly_flag: true,
      title: "",
      author_profile: {
        mobile_number: "",
        certification: {
          is_certificated: false,
          updated_at: ""
        }
      },
      address: {
        old_address: null,
        dong: "",
        ho: ""
      },
      down_payment: null,
      security_deposit: null,
      maintenance_fee: 0,
      monthly_fee: null,
      content: "",
      item_category: 1,
      trade_category: 1,
      online_visit: false,
      short_lease: false,
      status: 0,
      images: [],
      resizedImgs: [],
      image_links: [],
      delete_images: [],
      local_images: [],
      is_asking: false,
      ask_listing_obj: {
        title: "",
        item_category: 1,
        trade_category: 1,
        location: "",
        security_deposit: null,
        monthly_fee: null,
        maintenance_fee: 0,
        online_visit: false,
        term_of_lease: 12,
        content: "",
        visit_date: null,
        moving_date: null
      }
    };
  },
  methods: {
    changeImages(files) {
      const that = this;

      this.$refs.image.validate(files.concat(this.images_data)).then(function(result) {
        if (result.valid === true) {
          const current_images_index = that.images_data.length;
          that.images.push.apply(that.images, files);
          if (current_images_index > 0) {
            that.$refs.carousel.internalValue = current_images_index;
          }
        }
      });
    },
    deleteImage(index) {
      const image_data = this.images_data[index];

      if (image_data.image === null) {
        const deleted_image = this.image_links.find((item) => item === image_data.obj);
        if (deleted_image) {
          deleted_image.is_deleted = true;
        }
      } else {
        this.images = this.images.filter((item) => item !== image_data.obj);
      }
    },
    setDefaultImageIndex(index) {
      const image_data = this.images_data[index];

      this.image_links.forEach((item) => {
        if (item === image_data.obj) {
          item.is_default = true;
        } else {
          item.is_default = false;
        }
      });
      this.local_images.forEach((item) => {
        if (item.image === image_data.obj) {
          item.is_default = true;
        } else {
          item.is_default = false;
        }
      });
    },
    update_status() {
      let endpoint = `/api/listings/${this.id}/status/`;
      let method = "PUT";
      apiService(endpoint, method, { status: this.status }).then((data) => {
        if (data.status != undefined) {
          this.status = data.status;
          this.$store.commit("SET_IS_LISTING_UPDATED", true);
        } else {
          applyValidation(data);
        }
        this.isLoading = false;
      });
    },
    async submit() {
      const that = this;
      if (this.is_asking === true) {
        this.$refs.asking_obs.validate().then(async function(v) {
          if (v === true) {
            let endpoint = "/api/asklistings/";
            let method = "POST";
            if (that.id !== undefined) {
              endpoint += `${that.id}/`;
              method = "PUT";
            }

            apiService(endpoint, method, that.ask_listing_obj).then(function(data) {
              if (data.id != undefined) {
                alert(that.$i18n.t("request_success"));
                that.$router.push({
                  name: "asklistings"
                });
              } else {
                applyValidation(data, that);
              }
            });
            that.isLoading = false;
          }
        });
      } else {
        this.$refs.obs.validate().then(async function(v) {
          if (v === true) {
            that.resizedImgs = [];
            that.isLoading = true;
            const formData = new FormData();
            let endpoint = "/api/listings/";
            let method = "POST";
            if (that.id !== undefined) {
              endpoint += `${that.id}/`;
              method = "PUT";
            }
            formData.append("listingaddress.old_address", that.address["old_address"]);
            formData.append("listingaddress.old_address_eng", that.address["old_address_eng"]);
            formData.append("listingaddress.new_address", that.address["new_address"]);
            formData.append("listingaddress.bjdongName", that.address["bjdongName"]);
            formData.append("listingaddress.bjdongName_eng", that.address["bjdongName_eng"]);
            formData.append("listingaddress.sigunguCd", that.address["sigunguCd"]);
            formData.append("listingaddress.bjdongCd", that.address["bjdongCd"]);
            formData.append("listingaddress.bun", that.address["bun"]);
            formData.append("listingaddress.ji", that.address["ji"]);
            formData.append("listingaddress.dong", that.address["dong"]);
            formData.append("listingaddress.ho", that.address["ho"]);
            formData.append("title", that.title);
            if (that.down_payment != null) {
              formData.append("down_payment", that.down_payment);
            }
            if (that.security_deposit != null) {
              formData.append("security_deposit", that.security_deposit);
            }
            if (that.maintenance_fee != null) {
              formData.append("maintenance_fee", that.maintenance_fee);
            }
            if (that.monthly_fee != null) {
              formData.append("monthly_fee", that.monthly_fee);
            }
            formData.append("content", that.content);
            formData.append("item_category", that.item_category);
            formData.append("trade_category", that.trade_category);
            formData.append("online_visit", that.online_visit);
            formData.append("short_lease", that.short_lease);

            var idx = 0;

            if (that.id !== undefined) {
              for (const uploaded_img of that.image_links) {
                const matched_img = that.images_data.find((item) => item.obj == uploaded_img);
                if (!matched_img) {
                  idx += 1;
                  formData.append(`images[${idx}]id`, uploaded_img.id);
                  formData.append(`images[${idx}]image`, "");
                  formData.append(`images[${idx}]is_deleted`, uploaded_img.is_deleted);
                }
              }
            }
            for (const img of that.images_data) {
              if (img.id !== undefined && img.is_default === true) {
                idx += 1;
                formData.append(`images[${idx}]id`, img.id);
                formData.append(`images[${idx}]image`, "");
                formData.append(`images[${idx}]is_default`, img.is_default);
              }
              const file = img.image;
              if (file != null) {
                idx += 1;
                const resizedImage = await resizeImage({ file: file, maxSize: 1000 });
                formData.append(`images[${idx}]image`, resizedImage, file.name);
                formData.append(`images[${idx}]is_default`, img.is_default);
              }
            }
            apiService_formData(endpoint, method, formData).then(function(data) {
              if (data.id != undefined) {
                alert(that.$i18n.t("request_success"));
                that.$store.commit("SET_IS_LISTING_UPDATED", true);
                that.$router.push({
                  name: "listings"
                });
              } else {
                applyValidation(data, that);
              }
            });
            that.isLoading = false;
          }
        });
      }
    }
  },
  async beforeRouteEnter(to, from, next) {
    if (to.params.default_is_asking === true) {
      return next((vm) => {
        vm.is_asking = to.params.default_is_asking;
      });
    }
    if (to.params.id !== undefined) {
      let endpoint = `/api/listings/${to.params.id}/`;
      let data = await apiService(endpoint);
      if (data.id != undefined) {
        return next((vm) => {
          vm.id = data.id;
          vm.address = data.listingaddress;
          vm.author_profile = data.author_profile;
          vm.content = data.content;
          vm.item_category = data.item_category;
          vm.title = data.title;
          vm.trade_category = data.trade_category;
          vm.online_visit = data.online_visit;
          vm.short_lease = data.short_lease;
          vm.down_payment = data.down_payment;
          vm.security_deposit = data.security_deposit;
          vm.maintenance_fee = data.maintenance_fee;
          vm.monthly_fee = data.monthly_fee;
          vm.image_links = data.images;
          vm.status = data.status;
          vm.$store.commit("SET_IS_LISTING_UPDATED", false);
        });
      } else {
        applyValidation(data);
      }
    } else {
      return next();
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 1185px;
}
._checkbox {
  min-width: 115px;
  padding: 0;
  padding-left: 4px;
  padding-top: 12px;
}
.v-carousel__controls__item {
  margin: 0 3px;
}
.carousel-menu {
  background-color: rgba(19, 76, 142, 0.2);
}
.uncertified-mobile {
  color: rgba(255, 0, 0, 0.6) !important;
}
</style>
