<template>
  <div class="dashboard">
    <h1>Firewall AI - Dashboard</h1>

    <button @click="fetchData">🔄 Actualizar</button>

    <table v-if="predictions.length > 0">
      <thead>
        <tr>
          <th>Flow ID</th>
          <th>Tipo</th>
          <th>Confianza</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in predictions" :key="p.flow_id">
          <td>{{ p.flow_id }}</td>
          <td>{{ p.type }}</td>
          <td>{{ (p.confidence * 100).toFixed(2) }} %</td>
        </tr>
      </tbody>
    </table>

    <p v-else>No hay predicciones todavía</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "DashboardView",
  data() {
    return {
      predictions: []
    };
  },
  methods: {
    async fetchData() {
      try {
        const res = await axios.post("http://localhost:5000/api/traffic", [
          { feature1: 0.1, feature2: 0.2, feature3: 0.3 }, 
          { feature1: 0.5, feature2: 0.6, feature3: 0.7 }
        ]);
        this.predictions = res.data.predictions;
      } catch (err) {
        console.error("[ERROR] No se pudo obtener datos:", err);
      }
    }
  }
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
  font-family: Arial, sans-serif;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th,
td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: center;
}

th {
  background: #f0f0f0;
}
</style>
