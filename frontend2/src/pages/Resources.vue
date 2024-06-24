<template>
<div
>
  <v-toolbar
      class="px-5 d-flex justify-content-center"
      color="white"
      border="1"
  >
    <v-breadcrumbs
        :items="breadcrumbItems"

        class="mb-0 d-flex justify-content-center text-center align-center" >
      <template v-slot:divider>
        <v-icon icon="mdi-chevron-right"></v-icon>
      </template>
    </v-breadcrumbs>
  </v-toolbar>



</div>
  <v-row class="justify-content-start">
    <v-col cols="auto" class="m-4 d-flex justify-content-center">
      <v-treeview
        v-model="tree"
        :items="treeItems"
        :opened="initiallyOpen"
        item-key="name"
        activatable
        open-on-click
      >
        <template v-slot:prepend="{ item, open }">
          <v-icon v-if="!item.file">
            {{ open ? 'mdi-folder-open' : 'mdi-folder' }}
          </v-icon>
          <v-icon v-else>
            {{ files[item.file] }}
          </v-icon>
        </template>
      </v-treeview>
    </v-col>
    <v-divider
      vertical
    />
  </v-row>
</template>

<script>
import { mapState, mapActions, /*mapGetters*/ } from 'vuex';
import { useRoute, useRouter } from 'vue-router';

export default {
  name: "ResourcesPage",
  setup() {
    const route = useRoute();
    const router = useRouter();

    return {
      route,
      router,
    };
  },

  data: () => ({
      items: [
        {
          title: 'Коптевская ул. 63',
          disabled: false,
          href: '#',
        },
        {
          title: 'ФПСОИБ',
          disabled: false,
          href: '#',
        },
        {
          title: '3 Курс',
          disabled: false,
          href: '#',
        },
        {
          title: '913 взвод',
          disabled: false,
          href: '#',
        }
      ],
      initiallyOpen: ['public'],
      files: {
        html: 'mdi-language-html5',
        js: 'mdi-nodejs',
        json: 'mdi-code-json',
        md: 'mdi-language-markdown',
        pdf: 'mdi-file-pdf-box',
        png: 'mdi-file-image',
        txt: 'mdi-file-document-outline',
        xls: 'mdi-file-excel',
      },
      tree: [],
      breadcrumbItems: [],
      treeItems: [],
      items2: [
        {
          title: '.git',
        },
        {
          title: 'node_modules',
        },
        {
          title: 'public',
          children: [
            {
              title: 'static',
              children: [{
                title: 'logo.png',
                file: 'png',
              }],
            },
            {
              title: 'favicon.ico',
              file: 'png',
            },
            {
              title: 'index.html',
              file: 'html',
            },
          ],
        },
        {
          title: '.gitignore',
          file: 'txt',
        },
        {
          title: 'babel.config.js',
          file: 'js',
        },
        {
          title: 'package.json',
          file: 'json',
        },
        {
          title: 'README.md',
          file: 'md',
        },
        {
          title: 'vue.config.js',
          file: 'js',
        },
        {
          title: 'yarn.lock',
          file: 'txt',
        },
      ],
    }),
  computed: {
    ...mapState('ResourcesStore', ['resourcesList']),
    /*...mapGetters('ResourcesStore', ['breadcrumbItems', 'treeItems']),*/

        selectedLocationId() {
      if (this.resourcesList) {
        const locationId = this.route.query.locationId
          ? parseInt(this.route.query.locationId)
          : this.resourcesList.locations[0].id;
        return locationId;
      }
      return null;
    },
    selectedFacultyId() {
      if (this.resourcesList && this.selectedLocationId) {
        const location = this.resourcesList.locations.find((l) => l.id === this.selectedLocationId);
        const facultyId = this.route.query.facultyId
          ? parseInt(this.route.query.facultyId)
          : location.faculties[0].id;
        return facultyId;
      }
      return null;
    },
    selectedCourseId() {
      if (this.resourcesList && this.selectedFacultyId) {
        const faculty = this.resourcesList.locations
          .flatMap((l) => l.faculties)
          .find((f) => f.id === this.selectedFacultyId);
        const courseId = this.route.query.courseId
          ? parseInt(this.route.query.courseId)
          : faculty.courses[0].id;
        return courseId;
      }
      return null;
    },
    selectedGroupId() {
      if (this.resourcesList && this.selectedCourseId) {
        const course = this.resourcesList.locations
          .flatMap((l) => l.faculties)
          .flatMap((f) => f.courses)
          .find((c) => c.id === this.selectedCourseId);

        if (course && course.groups.length > 0) {
          const groupId = this.route.query.groupId
            ? parseInt(this.route.query.groupId)
            : course.groups[0].id;
          return groupId;
        }
      }
      return null;
    },

    /*breadcrumbItems() {
      return this.$store.getters['ResourcesStore/breadcrumbItems'](
        this.selectedLocationId,
        this.selectedFacultyId,
        this.selectedCourseId,
        this.selectedGroupId
      );
    },
    treeItems() {
      return this.$store.getters['ResourcesStore/treeItems'](this.selectedLocationId);
    },*/

  },

  async created() {
    console.log('Created the resources Page!')
    await this.fetchResourcesList();
  },

  watch: {
    resourcesList() {
      this.updateBreadcrumbItems();
      this.updateTreeItems();
    },
  },

  methods:{
    ...mapActions('ResourcesStore', ['fetchResourcesList']),
    updateBreadcrumbItems() {
      this.breadcrumbItems = this.$store.getters['ResourcesStore/breadcrumbItems'](
        this.selectedLocationId,
        this.selectedFacultyId,
        this.selectedCourseId,
        this.selectedGroupId
      );
    },
    updateTreeItems() {
      this.treeItems = this.$store.getters['ResourcesStore/treeItems'](this.selectedLocationId);
    },
    updateUrl(locationId, facultyId, courseId, groupId) {
      this.router.replace({
        query: {
          locationId,
          facultyId,
          courseId,
          groupId,
        },
      });
    },
  }
}
</script>

<style scoped>
.v-toolbar {
  border-width: 1px;
  border-style: solid;
  border-color: #d7d7d7;
}
</style>