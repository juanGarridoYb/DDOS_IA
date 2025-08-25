<template>
  <div id="app">
    <nav>
      <router-link to="/">Dashboard</router-link> |
      <router-link to="/traffic-analysis">Análisis de Tráfico</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
nav {
  padding: 1rem;
  background: #f4f4f4;
  margin-bottom: 1rem;
}
nav a {
  margin-right: 1rem;
  text-decoration: none;
}
</style>
