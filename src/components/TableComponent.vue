<template>
  <table>
    <thead>
      <tr>
        <th>Company</th>
        <th>Position</th>
        <th>Status</th>
        <th>Date Applied</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="application in applications" :key="application.id">
        <td>{{ application.company_name }}</td>
        <td>{{ application.position }}</td>
        <td>{{ application.status }}</td>
        <td>{{ application.date_applied }}</td>
        <td>
          <button @click="$emit('edit', application.id)">Edit</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script lang="ts">
import { defineComponent, DefineComponent, PropType } from "vue";
export default defineComponent({
  name: "TableComponent",
  props: {
    applications: {
      type: Array as PropType<
        Array<{
          id: number;
          company_name: string;
          position: string;
          status: string;
          date_applied: string;
        }>
      >,
      required: true,
    },
  },
});
</script>

<style>
table {
  width: 75%;
  margin: 0 auto;
  border-collapse: collapse;
}

th,
td {
  padding: 10px;
  border: 1px solid #ddd;
}

th {
  background-color: #f4f4f4;
}
</style>
