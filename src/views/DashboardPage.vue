<template>
  <v-container>
    <v-card class="mx-auto" max-width="800">
      <v-data-table
        :headers="headers"
        :items="applications"
        item-value="id"
        class="elevation-1"
        dense
      >
        <template v-slot:[`item.actions`]="{ item }">
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
      { text: "Company Name", value: "company_name" },
      { text: "Position", value: "position" },
      { text: "Status", value: "status" },
      { text: "Date Applied", value: "date_applied" },
      { text: "Actions", value: "actions", sortable: false },
    ]);

    const applications = ref([]);

    const fetchApplications = async () => {
      try {
        //DB_FLAG: DATABASE CALL
        //TODO: replace this with some variable or something
        const response = await axios.get("http://127.0.0.1:8000/applications/");
        applications.value = response.data;
      } catch (error) {
        console.error("Failed to fetch applications:", error);
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
      //deleteApplication,
      // editApplication,
    };
  },
});
</script>

<style>
h1 {
  text-align: center;
  margin-bottom: 10px;
}
</style>
