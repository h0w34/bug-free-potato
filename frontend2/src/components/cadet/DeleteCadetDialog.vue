<template>
  <v-dialog
    v-model="deleteCadetDialog"
    max-width="650"
    min-wdth="500"
    max-height="auto"
    v-click-outside="closeDialog"
  >

    <v-card max-height="700px" class="rounded-xl my-4" color="grey-lighten-5"
      :disabled="saving"
      :loading="saving"
    >
      <template v-slot:loader="{ isActive }">
        <v-progress-linear
          :active="isActive "
          color="deep-purple"
          height="4"
          indeterminate
        ></v-progress-linear>
      </template>

      <v-card-title class="d-flex justify-space-between align-center mt-1">
          <div class="text-h7 font-weight-regular text-medium-emphasis p-0 ml-2 d-flex align-center">
            <v-icon class="mr-2" size="small" :style="{ opacity: 0.8}">mdi-trash-can</v-icon>
            <div>Удалить курсанта</div>
          </div>
<!--            <div class="unselectable ml-2 text-h5 font-weight-medium text-medium-emphasis"  >
            Добавить курсанта
          </div>-->
        <v-btn icon="mdi-close" variant="text" @click="closeDialog"></v-btn>

      </v-card-title>
      <v-divider class="my-0"/>

      <v-skeleton-loader
        v-if="loading"
        type="text@3"
      />
      <div v-else class="font-weight-regular text-light-emphasis text-center mb-2">
        <div v-if="deletingSuccess">
          <v-container fluid class="p-5 pb-4">
              Курсант успешно удалён.
          </v-container>
        </div>
        <div v-else-if="error" >
          <v-container fluid class="p-5 pb-4">
              Ой! ＞︿＜<br>
              Возникла ошибка при удалении д/л.<br>
              Перепроверьте данные или попробуйте позже.
          </v-container>
        </div>
        <div v-else-if="cadetStatistics?.future_duties.length > 0">
          <v-container fluid class="p-5 mb-2">
              У этого курсанта есть запланированные сутки. <br/>
              Замените его/её на других и попробуйте ещё раз.
          </v-container>
        </div>
        <div v-else>
          <v-container fluid class="p-5 pb-4">
              Вы уверены, что хотите безвозвратно<br/>
          удалить этого курсанта? Его статистика, пользователь <br/>
            и достижения также будут удалены.
          </v-container>
        </div>

      </div>

      <v-divider class="my-0 mt-2"/>

      <v-card-actions v-if="cadetStatistics && cadetStatistics.future_duties.length === 0" class="m-1">

        <div class="d-flex justify-content-end mr-2">
          <v-btn
            variant="outlined"
            color="grey-darken-3"
            density="comfortable"
            @click="closeDialog"
          >
            {{(error || deletingSuccess)? 'Понятно' : 'Отмена'}}
          </v-btn>
          <v-btn
            v-if="!(error || deletingSuccess)"
            @click="sendDeleteRequest"
            variant="outlined"
            color="red"
            density="comfortable"
          >
            Удалить
          </v-btn>
        </div>
      </v-card-actions>
    </v-card>

  </v-dialog>
</template>

<script>


import {mapState, mapActions} from "vuex";
/*import CadetCard from "@/components/cadet/CadetCard";*/
import ResourcesService from "@/services/resources-data.service";
/*
import cadetCard from "@/components/cadet/CadetCard";
*/

export default {
  name: 'DeleteCadetDialog',
  /*components: {CadetCard},*/
  props: {
    cadetData: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      loading: true,
      saving: false,
      cadetStatistics: null,
      error: false,
      deletingSuccess: false,
    }
  },

/*  async beforeMount() {
    this.loading = true;
    if(!this.cadetStatistics) {
      await ResourcesService.getCadetStatistics()
    }
    this.loading = false;
  },*/

  computed: {
    ...mapState('layoutStore', ['deleteCadetDialog']),
    ...mapState('authStore', ['user']),
  },
  methods: {
    ...mapActions('layoutStore', ['closeDeleteCadetDialog']),

    async fetchCadetStatistics() {
      this.loading=true;
      if (!this.cadetStatistics && this.cadetData) {
        // Fetch cadet statistics only if cadetData prop is provided
        try{
          this.cadetStatistics = await ResourcesService.getCadetStatistics(this.cadetData.id, {
            future_duties: true,
            future_reserves: false,
            stats: false,
          });
        } catch (error){
          this.error=true;
        } finally {
          this.loading=false;
        }
      }
    },
    async sendDeleteRequest(){
      this.saving = true;
      const loadingStartTime = performance.now();
      try {
        await ResourcesService.deleteCadet(this.cadetData.id);
        await new Promise(resolve => setTimeout(resolve, Math.max(500 - (performance.now() - loadingStartTime), 0)));
        this.deletingSuccess=true;
      }
      catch {
        await new Promise(resolve => setTimeout(resolve, Math.max(500 - (performance.now() - loadingStartTime), 0)));
        this.error=true;
      }
      finally {
        this.saving=false;
      }
    },

    closeDialog(){
      this.$emit('close')
      this.resetDialogSate();
    },

    resetDialogSate(){
      this.cadetStatistics=null;
      this.loading=true;
      this.error=false;
      this.saving=false;
      this.deletingSuccess=false;
    }
  },
  watch: {
    deleteCadetDialog(open) {
      if (open) {
        this.fetchCadetStatistics();
      }
    }
  }
}
</script>