import axios from "axios";

const axiosInstance = axios.create({
  // TODO:   baseURL: import.meta.env.VITE_API_ENDPOINT,
  baseURL: "http://localhost:5123",
});

export default axiosInstance;
