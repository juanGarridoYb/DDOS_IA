<template>
  <div>
    <h1>Análisis de Tráfico</h1>
    <button @click="fetchTraffic">Cargar tráfico</button>

    <table v-if="traffic.length > 0">
      <thead>
        <tr>
          <th>Flow ID</th>
          <th>Tipo</th>
          <th>Confianza</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in traffic" :key="item.flow_id">
          <td>{{ item.flow_id }}</td>
          <td>{{ item.type }}</td>
          <td>{{ (item.confidence * 100).toFixed(2) }}%</td>
        </tr>
      </tbody>
    </table>

    <p v-if="traffic.length === 0">No hay datos todavía.</p>
  </div>
</template>

<script>
export default {
  name: 'TrafficAnalysis',
  data() {
    return {
      traffic: []
    }
  },
  methods: {
    async fetchTraffic() {
      const response = await fetch("http://localhost:5000/api/traffic", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify([
          { dummy: "flow1" },
          { dummy: "flow2" },
          { dummy: "flow3" }
        ])
      });

      const data = await response.json();
      this.traffic = data.predictions;
    }
  }
}
</script>
