<template>
  <v-container>
    <v-app-bar :elevation="0">
      <template v-slot:prepend> </template>

      <v-app-bar-title>Job App Tracker</v-app-bar-title>
      <template v-slot:append>
        <v-btn>Add</v-btn>
      </template>
    </v-app-bar>
    <v-card
      title="Job Applications"
      class="mx-auto"
      variant="outline"
      max-width="75%"
      max-height="75%"
      elevation="10"
      flat
    >
      <v-data-table
        :headers="headers"
        :items="applications"
        item-value="id"
        class="elevation-1"
        density="compact"
        fixed-header
      >
        <template v-slot:[`item.date_applied`]="{ item }">
          {{ formatDate(item.date_applied) }}
        </template>
        <template v-slot:[`item.status`]="{ item }">
          <span :class="getStatusClass(item.status)">
            {{ item.status }}
            <v-icon v-if="item.status.toLowerCase() === 'ghosted'" class="mr-2"
              >mdi-ghost</v-icon
            >
          </span>
        </template>
        <template v-slot:[`item.actions`]="{ item }">
          <v-speed-dial
            location="left center"
            transition="fade-transition"
            width="10%"
          >
            <template v-slot:activator="{ props: activatorProps }">
              <v-fab
                v-bind="activatorProps"
                size="small"
                icon="mdi-dots-horizontal"
                variant="flat"
                density="compact"
              ></v-fab>
            </template>

            <v-btn
              key="1"
              icon="mdi-pencil"
              size="small"
              variant="flat"
              density="compact"
              @click="editAppliaction(item.id)"
            ></v-btn>
            <v-btn
              key="2"
              size="small"
              icon="mdi-delete"
              variant="flat"
              density="compact"
              @click="deleteApplication(item.id)"
            ></v-btn>
          </v-speed-dial>
          <!--
          <v-btn
            prepend-icon="mdi-pencil"
            variant="tonal"
            size="x-small"
            @click="editApplication(item.id)"
          >
            edit
          </v-btn>
          <v-btn
            prepend-icon="mdi-delete"
            variant="tonal"
            size="x-small"
            @click="deleteApplication(item.id)"
          >
            delete
          </v-btn>
          -->
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import axios from "axios";

export default defineComponent({
  name: "DashboardPage",
  setup() {
    const headers = ref([
      { key: "company_name", title: "Company Name" },
      { key: "position", title: "Position" },
      { key: "status", title: "Status" },
      { key: "date_applied", title: "Date Applied" },
      { key: "actions", value: "actions", sortable: false },
    ]);

    const applications = ref([]);

    const fetchApplications = async () => {
      try {
        //DB_FLAG: DATABASE CALL
        //TODO: replace this with some variable or something
        const response = await axios.get("http://127.0.0.1:8000/applications/");
        applications.value = response.data;
        console.log("headers:", headers);
      } catch (error) {
        console.error("Failed to fetch applications:", error);
      }
    };
    const formatDate = (dateString: string): string => {
      if (!dateString) return "";
      const date = new Date(dateString);
      return new Intl.DateTimeFormat("en-US", { dateStyle: "medium" }).format(
        date
      );
    };
    /*
    const getRowClass = (item: any): string => {
      console.log("getRowClass called");
      switch (item.status.toLowerCase()) {
        case "interviewing":
          return "row-yellow";
        case "rejected":
          return "row-red";
        case "ghosted":
          return "row-grey";
        case "offer":
          return "row-green";
        default:
          return "";
      }
    };
    */
    const getStatusClass = (status: string) => {
      switch (status.toLowerCase()) {
        case "interviewing":
          return "text-yellow-darken-3";
        case "rejected":
          return "text-red-darken-3";
        case "ghosted":
          return "text-grey-darken-3";
        case "offer":
          return "text-green-darken-3";
        default:
          return "";
      }
    };

    /*
    const editApplication = (id: number) => {
      console.log("Edit Application:", id);
      //redirect to edit page
      window.location.href = `/edit/${id}`;
    };
    const deleteApplication = async (id: number) => {
      try {
        await axios.delete(`http://127.0.0.1:8000/applications/${id}`);
        fetchApplications();
      } catch (error) {
        console.error(`Failed to delete application with ID ${id}`, error);
      }
    }; */

    onMounted(fetchApplications);
    return {
      headers,
      applications,
      formatDate,
      //getRowClass,
      //search: "",
      getStatusClass,
      //deleteApplication,
      // editApplication,
    };
  },
});
</script>

<style>
.row-yellow {
  color: #fdd835 !important; /* Yellow */
}

.row-green {
  color: #4caf50; /* Green */
}

.row-red {
  color: #f44336; /* Red */
}

.row-grey {
  color: #9e9e9e; /* Grey */
}
</style>
