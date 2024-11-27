<template>
  <v-container>
    <v-card
      class="mx-auto"
      variant="elevated"
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
        height="80vh"
        :items-per-page="50"
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
            style="margin-right: 16px"
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
              @click="editApplication(item.id)"
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
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

interface Application {
  id: number;
  company_name: string;
  position: string;
  status: string;
  date_applied: string;
}

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

    const applications = ref<Application[]>([]);
    const router = useRouter();

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

    const editApplication = (id: number) => {
      console.log("Edit Application:", id);
      //redirect to edit page
      //window.location.href = `/edit/${id}`;
      router.push(`/edit/${id}`);
    };
    const deleteApplication = async (id: number) => {
      try {
        await axios.delete(`http://127.0.0.1:8000/applications/${id}`);
        fetchApplications();
      } catch (error) {
        console.error(`Failed to delete application with ID ${id}`, error);
      }
    };

    onMounted(fetchApplications);
    return {
      headers,
      applications,
      formatDate,
      //getRowClass,
      //search: "",
      getStatusClass,
      deleteApplication,
      editApplication,
    };
  },
});
</script>

<style></style>
