<template>
  <v-tour :name="name" :steps="steps" :options="options" :callbacks="callbacks">
    <template slot-scope="tour">
      <transition name="fade">
        <v-step
          v-if="tour.steps[tour.currentStep]"
          :step="tour.steps[tour.currentStep]"
          :key="tour.currentStep"
          :previous-step="tour.previousStep"
          :next-step="tour.nextStep"
          :stop="tour.stop"
          :skip="stopTour"
          :is-first="tour.isFirst"
          :is-last="tour.isLast"
          :labels="tour.labels"
          :enabled-buttons="options.enabledButtons"
          :highlight="options.highlight"
          :stop-on-fail="options.stopOnTargetNotFound"
          :debug="options.debug"
          @targetNotFound="$emit('targetNotFound', $event)"
        >
          <template>
            <div slot="actions">
              <div class="v-step__buttons">
                <button
                  @click.prevent="stopTour"
                  v-if="tour.isFirst"
                  class="v-step__button v-step__button-skip"
                >
                  {{ $t("skip_tour") }}
                </button>
                <button
                  @click.prevent="tour.previousStep"
                  v-if="!tour.isFirst && !isStepButtonDisabled('buttonPrevious')"
                  class="v-step__button v-step__button-previous"
                >
                  {{ $t("back") }}
                </button>
                <button
                  @click.prevent="tour.nextStep"
                  v-if="!tour.isLast && !isStepButtonDisabled('buttonNext')"
                  class="v-step__button v-step__button-next"
                >
                  {{ $t("next") }}
                </button>
                <button
                  @click.prevent="tour.finish"
                  v-if="tour.isLast"
                  class="v-step__button v-step__button-stop"
                >
                  {{ $t("done_tour") }}
                </button>
              </div>
            </div>
          </template>
        </v-step>
      </transition>
    </template>
  </v-tour>
</template>
<script>
import { apiService } from "@/common/api_service";
import { applyValidation } from "@/common/common_api";
export default {
  name: "CustomTour",
  props: {
    name: {
      type: String
    },
    steps: {
      type: Array
    },
    options: {
      type: Object,
      default: () => {
        return {
          highlight: false,
          labels: {
            buttonSkip: "Skip tour",
            buttonPrevious: "Previous",
            buttonNext: "Next",
            buttonStop: "Finish"
          },
          enabledButtons: {
            buttonSkip: true,
            buttonPrevious: true,
            buttonNext: true,
            buttonStop: true
          },
          startTimeout: 0,
          stopOnTargetNotFound: true,
          useKeyboardNavigation: true,
          enabledNavigationKeys: {
            escape: true,
            arrowRight: true,
            arrowLeft: true
          },
          debug: false
        };
      }
    },
    callbacks: {
      type: Object,
      default: () => {
        return {
          onStart: () => {},
          onPreviousStep: (currentStep) => {}, // eslint-disable-line no-unused-vars
          onNextStep: (currentStep) => {}, // eslint-disable-line no-unused-vars
          onStop: () => {},
          onSkip: () => {},
          onFinish: () => {}
        };
      }
    }
  },
  computed: {
    step() {
      const tour = this.$tours[this.name];
      return this.steps[tour.currentStep];
    }
  },
  methods: {
    stopTour() {
      let endpoint = "/api/user-setting/";
      let method = "PUT";
      const tour = this.$tours[this.name];
      if (tour.currentStep == 0) {
        tour.stop();
        this.$store.commit("SET_USER_SETTING", {
          is_tour_on: false
        });

        //Update setting, to server, to remember after visiting.
        let user_setting = this.$store.state.user_setting;
        apiService(endpoint, method, { is_tour_on: user_setting.is_tour_on }).then((data) => {
          if (data.id == undefined) {
            applyValidation(data);
          }
        });
      }
    },
    isStepButtonDisabled(name) {
      return Object.prototype.hasOwnProperty.call(this.step, "disabledButtons")
        ? this.step.disabledButtons[name]
        : false;
    }
  }
};
</script>
