<template>
  <v-container>
    <v-card
      title="Add App"
      class="mx-auto"
      variant="flat"
      max-width="75%"
      max-height="75vh"
      elevation="10"
      flat
    >
      <v-form ref="form" v-model="valid" @submit.prevent="Add">
        <v-text-field
          :rules="companyRules"
          :counter="30"
          v-model="app.company_name"
          max-width="90%"
          class="mx-auto mb-4"
          label="Company"
          placeholder="Ex: Google"
          type="input"
          variant="outlined"
          required
        ></v-text-field>

        <v-text-field
          label="Position"
          class="mx-auto mb-4"
          placeholder="Ex: Software Engineer"
          v-model="app.position"
          type="input"
          max-width="90%"
          variant="outlined"
          :rules="positionRules"
          :counter="30"
          required
        ></v-text-field>

        <!--Drop down-->
        <v-select
          label="Status"
          class="mx-auto mb-4"
          variant="outlined"
          v-model="app.status"
          :items="statusOptions"
          max-width="90%"
          :rules="[(v) => !!v || 'Item is required']"
          required
        ></v-select>

        <!--Calendar-->
        <v-text-field
          label="Date Applied"
          class="mx-auto mb-4"
          placeholder="YYYY-MM-DD"
          v-model="app.date_applied"
          type="input"
          max-width="90%"
          variant="outlined"
          :rules="dateRules"
          :counter="10"
          required
        ></v-text-field>
        <v-btn location="right" @click="cancelAdd()" variant="text"
          >Cancel</v-btn
        >
        <v-btn
          location="right"
          color="primary"
          type="submit"
          variant="text"
          :disabled="!valid"
          @click="Add()"
          >Done</v-btn
        >
      </v-form>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { VForm } from "vuetify/lib/components/index.mjs";
import axios from "axios";

export default defineComponent({
  name: "AddApplicationPage",
  setup() {
    const router = useRouter();
    const form = ref<VForm | null>(null);
    const valid = ref(false);
    const today = new Date().toISOString().split("T")[0];
    const statusOptions = [
      "Applied",
      "Rejected",
      "Interviewing",
      "Offer",
      "Ghosted",
    ];

    const app = ref({
      id: 0,
      company_name: "",
      position: "",
      status: "",
      date_applied: today,
    });

    watch(
      () => valid.value,
      (newVal, oldVal) => {
        console.log(`valid changed from ${oldVal} to ${newVal}`);
      }
    );
    const companyRules = [
      (v: string) => !!v || "Company name is required",
      (v: string) =>
        v.length <= 30 || "Company name must be less than 30 characters",
    ];
    const positionRules = [
      (v: string) => !!v || "position is required",
      (v: string) =>
        v.length <= 30 || "Position must be less than 30 characters",
    ];
    const dateRules = [
      (v: string) => !!v || "Date is required",
      (v: string) =>
        /^\d{4}-\d{2}-\d{2}$/.test(v) || "Date must be in YYYY-MM-DD format",
      (v: string) => {
        const date = new Date(v);
        return (
          !isNaN(date.getTime()) || "Invalid date, please provide a valid date"
        );
      },
    ];

    const Add = async () => {
      console.log("Button clicked, valid status:", valid.value);
      if (!form.value) {
        console.error("form reference is missing");
        return;
      }

      // Force validation
      const isValid = await form.value.validate();
      if (!isValid) {
        console.log("Form is not valid");
        return;
      }

      try {
        await axios.post(`http://127.0.0.1:8000/applications/`, app.value);
        console.log("Application updated successfully");
        router.push("/");
      } catch (error) {
        console.error("Failed to update application:", error);
      }
    };

    const cancelAdd = () => {
      router.push("/");
    };
    return {
      //schema,
      form,
      valid,
      app,
      router,
      statusOptions,
      Add,
      cancelAdd,
      companyRules,
      positionRules,
      dateRules,
    };
  },
});
</script>
