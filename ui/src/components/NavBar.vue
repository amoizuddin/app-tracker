<template>
  <nav>
    <ul>
      <li><router-link to="/">Dashboard</router-link></li>
      <li><router-link to="/add">Add Application</router-link></li>
    </ul>
  </nav>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "NavBar",
});
</script>

<style>
nav ul {
  display: flex;
  list-style-type: none;
  padding: 0;
}

nav yl li {
  margin-right: 15px;
}
</style>
