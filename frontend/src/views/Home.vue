<template>
  <div class="home">
    <v-container class="my-5">
      <v-row>
        <v-dialog v-model="warning_dialog">
          <v-row no-gutters>
            <v-col class="text-center" cols="12">
              <v-card v-model="error">
                <div class="text-h6 red--text ">
                  {{ error }}
                </div>
              </v-card>
            </v-col>
          </v-row>
        </v-dialog>
        <v-dialog v-model="dialog" height="400px" max-width="400px" eager>
            <v-card>
              <VueSignaturePad
                class="signature_pad"
                width="100%"
                height="400px"
                ref="signaturePad"
                :options= "{
                  minWidth: 3,
                  maxWidth: 3,
                  penColor: 'red',
                }"
              />
              <v-card-actions>
                <v-btn color="blue darken-1" text @click="dialog = false">{{$t('close')}}</v-btn>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="clear('seller')"
                >{{$t('clear')}}</v-btn>
                <v-spacer></v-spacer>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="save('seller')"
                >{{$t('save')}}</v-btn>
              </v-card-actions>
            </v-card>
        </v-dialog>
        <v-col
          cols="12"
          md="6"
          lg="4"
          xl="3"
          v-for="paper in papers"
          :key="paper.id"
        >
          <v-card
            class="outlined tile"
            :to="{ name: 'paper', params: { id: paper.id } }"
          >
            <div class="text-body-2" style="float:right">
              {{ $t("last") }}{{ $t("updated_at") }} : {{ paper.updated_at}}
            </div>
            <v-card-title class="ma-1">
              {{ paper.room_name }}
              {{ $getConstI18("trade_type", paper.trade_type) }}
            </v-card-title>
            <v-card-subtitle style="float:right">
              {{ $t("author") }}: <span class="author-name"> {{ paper.author }} </span>
            </v-card-subtitle>
            <v-card-text>
              <div>
                {{ paper.address }}
              </div>
              <span>
                {{ $getConstI18("realestate_type", paper.realestate_type) }}
              </span>
              <span v-if="paper.trade_type == $getConstByVal('trade_type', 'rent')">
                보{{ paper.security_deposit }}/월 {{paper.monthly_fee}}
              </span>
              <span v-else-if="paper.trade_type == $getConstByVal('trade_type', 'depositloan')">
              </span>
              <span v-else-if="paper.trade_type == $getConstByVal('trade_type', 'trade')">
              </span>
              <span v-else-if="paper.trade_type == $getConstByVal('trade_type', 'exchange')">
              </span>
            </v-card-text>
            <v-card-actions>
              <v-btn
              style="z-index:2;"
              @click.prevent="open(paper)"
              v-if="!isLoading && !IsSigned(paper.paper_contractors)"
              color="red"
              dark
              top
              right
              >
                <v-icon>create</v-icon>
                {{$t("signature")}}
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
      <router-link :to="{ name: 'paper-editor' }">
        <v-btn color="grey" dark absolute fab mid right>
          <v-icon>add</v-icon>
        </v-btn>
      </router-link>
    </v-container>
  </div>
</template>

<script>
import { apiService, apiService_formData } from "@/common/api.service";
import i18n from "@/plugins/i18n";

export default {
  name: "Home",
  data() {
    return {
      papers: [],
      dialog: false,
      warning_dialog:  false,
      error: null,
      requestUser: null,
      isLoading: true,
      current_paper: null,
    };
  },
  computed: {
    
  },
  methods: {
    IsSigned(contractors) {
      const self = this;
      for(var i=0; i<contractors.length; i++){
        var contractor = contractors[i]        
        if(contractor.profile.user.username==self.requestUser){
          return !(contractor.signature == null);
        }
      }
      console.log("what?")
    },
    getCurrentContractor() {
      const self = this;
      const contractors = self.current_paper.paper_contractors
      for(var i=0; i<contractors.length; i++){
        var contractor = contractors[i]        
        if(contractor.profile.user.username==self.requestUser){
          return contractor
        }
      }
    },
    getPapers() {
      let endpoint = "api/papers/";
      this.isLoading = true;
      apiService(endpoint).then(data => {
        this.papers.push(...data.results);
        this.isLoading = false;
      });
    },    
    clear() {
      this.$refs['signaturePad'].clearSignature();
    },
    save() {
      const { isEmpty, data } = this.$refs['signaturePad'].saveSignature();   
      if(isEmpty) {
        this.warning_dialog = true;
        this.error = i18n.t("signature_empty_warning");
      }

      let self = this;
      let endpoint = `/api/papers/${this.current_paper.id}/signature/`;

      try {
        fetch(data).then(
          res => {
          return res.blob()
        }).then(
          myblob =>{
            const formData  = new FormData();
            formData.append('image', myblob, "signature_" + self.getCurrentContractor().id + ".png");
            formData.append('contractor', self.getCurrentContractor().id);
    
            apiService_formData(endpoint, 'POST', formData).then(data => {
              if (data.id) {
                window.location.reload()
              } else {
                this.warning_dialog = true;
                self.error= data;
              }
            });
          }
        )
      } catch (err) {
        console.log(err);
      }
    },
    open(paper) {
      this.current_paper = paper;
      this.dialog = true;
      this.$nextTick(() => {
        this.$refs["signaturePad"].resizeCanvas();
      });
    },
    newtab(image) {
      var newTab = window.open();
      newTab.document.body.innerHTML = '<img src=' + image + ' width="500px" height="500px">';
    } 
  },
  created() {
    this.getPapers();
    this.requestUser = window.localStorage.getItem("username");
  }
};
</script>
<style>
  .author-name {
    font-weight:bold !important;
    color : #DC3545
  }
</style>