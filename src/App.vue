<template>
  <div id="app">
    <NavBar />
    <router-view />
  </div>
</template>

<script lang="ts">
import NavBar from "./components/NavBar.vue";

export default {
  name: "App",
};
</script>

<style>
/*add global styles here*/
</style>
