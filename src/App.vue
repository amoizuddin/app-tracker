<template>
  <v-app>
    <v-main>
      <!--
      <v-container>
       
         <v-btn color="primary">Hello, Vuetify!</v-btn>
        <v-icon icon="mdi-home" />
        <router-link to="/">Home</router-link>
        <router-link to="/add">Add Application</router-link>
        -->
      <RouterView />
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { RouterView } from "vue-router";

export default {
  name: "App",
};
</script>

<style></style>
