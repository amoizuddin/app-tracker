<template>
  <v-container>
    <v-container>
      <v-progress-circular
        v-if="isLoading"
        indeterminate
        color="primary"
      ></v-progress-circular>
    </v-container>
    <v-card
      title="Edit application"
      class="mx-auto mt-2 mb-2"
      variant="flat"
      max-width="75%"
      max-height="75%"
      elevation="10"
      flat
    >
      <v-form ref="form" v-model="valid" @submit.prevent="saveEdit">
        <v-text-field
          :rules="companyRules"
          :counter="30"
          v-model="app.company_name"
          max-width="90%"
          class="mx-auto mt-2 mb-2"
          label="Company"
          placeholder="Ex: Google"
          type="input"
          variant="outlined"
          required
        ></v-text-field>

        <v-text-field
          label="Position"
          class="mx-auto mt-2 mb-2"
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
          class="mx-auto mt-2 mb-2"
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
          class="mx-auto mt-2 mb-2"
          placeholder="YYYY-MM-DD"
          v-model="app.date_applied"
          type="input"
          max-width="90%"
          variant="outlined"
          :rules="dateRules"
          :counter="10"
          required
        ></v-text-field>
        <v-btn location="right" @click="cancelEdit()" variant="text"
          >Cancel</v-btn
        >
        <v-btn
          location="right"
          color="primary"
          type="submit"
          variant="text"
          :disabled="!valid"
          @click="saveEdit()"
          >Done</v-btn
        >
      </v-form>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { VForm } from "vuetify/lib/components/index.mjs";
//import { Form, Field } from "vee-validate";
//import * as yup from "yup";
import axios from "axios";

export default defineComponent({
  name: "EditApplicationPage",
  //components: { Form, Field },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const isLoading = ref(true);
    const form = ref<VForm | null>(null);
    const valid = ref(false);
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
      date_applied: "",
    });
    /*
    const schema = yup.object({
      company_name: yup
        .string()
        .required("company name is required")
        .max(30, "company name must be less than 30 characters"),
      positon: yup
        .string()
        .required("position is required")
        .max(30, "position mus tbe less than 30 characters"),
      status: yup.string().required("status is required"),
      date_applied: yup
        .string()
        .required("date applied is required")
        .matches(/^\d{4}-\d{2}-\d{2}$/, "date must be in YYYY-MM-DD format")
        .test(
          "is-valid-date",
          "invalid date, please provide a valid date",
          (value) => {
            const date = new Date(value);
            return !isNaN(date.getTime());
          }
        ),
    });
    */

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

    const fetchAppDetails = async () => {
      try {
        const { id } = route.params;
        const response = await axios.get(
          `http://127.0.0.1:8000/applications/${id}`
        );
        const appData = response.data;
        app.value = {
          ...appData,
          date_applied: new Date(appData.date_applied)
            .toISOString()
            .split("T")[0],
        };
        isLoading.value = false;
      } catch (error) {
        console.error("failed to fetch application details:", error);
        isLoading.value = false;
      }
    };

    const saveEdit = async () => {
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
        await axios.put(
          `http://127.0.0.1:8000/applications/${app.value.id}`,
          app.value
        );
        console.log("Application updated successfully");
        router.push("/");
      } catch (error) {
        console.error("Failed to update application:", error);
      }
    };

    const cancelEdit = () => {
      router.push("/");
    };

    onMounted(fetchAppDetails);
    return {
      //schema,
      form,
      valid,
      app,
      isLoading,
      router,
      statusOptions,
      saveEdit,
      cancelEdit,
      companyRules,
      positionRules,
      dateRules,
    };
  },
});
</script>
