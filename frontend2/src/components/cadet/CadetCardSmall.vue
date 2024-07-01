    <template>
      <!--v-card
        class="mx-auto rounded-xl"
        max-width="344"
        :hover="!selected"
        :elevation="selected ? 5 : false"
      -->
      <v-card
        class="mx-auto rounded-xl pb-3"
        max-width="152"

      >

        <v-card-title class="d-flex justify-content-between">
            <!--div class="mr-1" :style="{ whiteSpace: 'pre-wrap', textOverflow: 'ellipsis' }"-->
          <div class="mr-1 mt-1" :style="{textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap', maxWidth: '100%', lineHeight: '1.2em'}">
            {{cadetData['name'] + ' ' + cadetData['surname']}}
          </div>
          <div v-if="cadetData['priority']">
            <v-badge color="grey-darken-1" inline :content="cadetData['priority']+'-й'"></v-badge>
          </div>
        </v-card-title>

        <v-card-subtitle>
          <div class="text-h8">
            {{"@sobakayasobaka"}}
          </div>
          <div>{{cadetData['group']['name'] + ' ' +  'взвод'}}</div>
          {{ cadetData['pm_cell_id']+' ячейка'}}
        </v-card-subtitle>
      </v-card>
    </template>

  <script>
  //import editRoleDialog from "@/components/EditRoleDialog";
  export default {
    name: "CadetCardSmall",
    //components:{editRoleDialog}
    props:{
      cadetData:{
        type: Object,
        required: true
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