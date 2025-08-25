import axios from "axios";

const API_URL = "http://localhost:5000/api";

export const getTraffic = async () => {
  try {
    const res = await axios.get(`${API_URL}/traffic`);
    return res.data;
  } catch (err) {
    console.error("Error al obtener tráfico:", err);
    return null;
  }
};
