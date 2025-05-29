import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/', // replace with your Django URL
  withCredentials: true, // for cookies/csrf if needed
});

export default api;
