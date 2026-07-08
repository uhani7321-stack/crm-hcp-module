import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

export const extractFromChat = async (message) => {
  const response = await axios.post(`${API_URL}/ai/extract`, { message });
  return response.data;
};

export const logInteraction = async (data) => {
  const response = await axios.post(`${API_URL}/interactions`, data);
  return response.data;
};
