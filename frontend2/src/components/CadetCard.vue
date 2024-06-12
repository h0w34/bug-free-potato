    <template>
      <!--v-card
        class="mx-auto rounded-xl"
        max-width="344"
        :hover="!selected"
        :elevation="selected ? 5 : false"
      -->
      <v-card
        class="mx-auto rounded-xl"
        max-width="344"
        hover
      >

        <v-card-title class="d-flex justify-content-between">
            <div class="mr-1" :style="{ whiteSpace: 'pre-wrap', textOverflow: 'ellipsis' }">{{cadetData['name'] + ' ' + cadetData['surname']}}</div>
            <div v-if="cadetData['priority']">
            <v-badge color="grey-darken-1" inline :content="cadetData['priority']+'-й'"></v-badge>
          </div>
        </v-card-title>

        <v-card-subtitle>
          <div class="text-h8">
            {{"@sobakayasobaka"}}
          </div>
          {{cadetData['group'] + ' ' +  'взвод' + ' | ячейка: ' + cadetData['pm_cell_id']}}
        </v-card-subtitle>

        <v-divider class="mx-2 mb-2"/>
          <template v-slot:actions>
           <v-spacer />
            <!--v-btn selected-class="bg-primary"
                @click="toggleCard"
                class="text-none"
                color="medium-emphasis"
                min-width="92"
                variant="outlined"
                rounded
             -->
            <v-btn
                @click="toggleCard"
                class="text-none mb-1"
                color="medium-emphasis"
                min-width="92"
                variant="outlined"
                rounded
             >
               Выбрать
             </v-btn>
           <v-spacer />
          </template>
      </v-card>
    </template>

  <script>
  //import editRoleDialog from "@/components/EditRoleDialog";
  export default {
    name: "CadetCard",
    //components:{editRoleDialog}
    props:{
      cadetData:{
        type: Array
      }
    },
    data(){
      return {
        selected: false
      }
    },
    methods:{
      toggleCard(){
        this.$emit('select', this.cadetData)
        /*if(this.selected === false) this.$emit('select', this.cadetData)
        this.selected = !this.selected*/
      }
    }
  }
  </script>

  <style scoped>
    .selected {
      border: 2px solid #4CAF50;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
    }
  </style>