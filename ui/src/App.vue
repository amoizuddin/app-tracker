<template>
  <v-app>
    <v-main>
      <v-app-bar density="comfortable">
        <v-btn variant="plain" size="x-large" :ripple="false" @click="home">
          Job App Tracker</v-btn
        >
        <v-btn variant="text" @click="addApp">Add</v-btn>
        <v-btn variant="text" @click="stats">Stats</v-btn>
        <template v-slot:append
          ><v-btn variant="plain">Sign In</v-btn>
        </template>
      </v-app-bar>
      <RouterView />
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { useRouter } from "vue-router";

export default {
  name: "App",
  setup() {
    const router = useRouter();
    const addApp = () => {
      console.log("add Application:");
      //redirect to edit page
      //window.location.href = `/add/}`;
      router.push(`/add`);
    };
    const home = () => {
      console.log("add Application:");
      //redirect to edit page
      //window.location.href = `/add/}`;
      router.push(`/`);
    };
    const stats = () => {
      router.push(`/stats`);
    };
    const signin = () => {
      router.push(`/signin`);
    };
    return {
      addApp,
      home,
      stats,
    };
  },
};

/*const addApplication = () => {
  console.log("AddApplication");
  window.location.href = `/add/`;
};*/
</script>

<style></style>
