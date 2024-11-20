<template>
  <div>
    <h1>Dashboard</h1>
    <TableComponent :applications="applications" @edit="editApplication" />
  </div>
</template>

<script lang="ts">
import TableComponent from "@/components/TableComponent.vue";
import { defineComponent, ref, onMounted } from "vue";
import axios from "axios";

export default defineComponent({
  name: "DashboardPage",
  components: {
    TableComponent,
  },
  setup() {
    const applications = ref<
      Array<{
        id: number;
        company_name: string;
        position: string;
        status: string;
        date_applied: string;
      }>
    >([]);
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
    const editApplication = (id: number) => {
      console.log("Edit Application:", id);
      //redirect to edit page
      window.location.href = `/edit/${id}`;
    };
    onMounted(fetchApplications);
    return {
      applications,
      editApplication,
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
