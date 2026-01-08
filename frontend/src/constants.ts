export const API_URL = "http://localhost:5000";

export function tokenHeader() {
  const t = localStorage.getItem('token');
  return {'Authorization': 'Bearer ' + t, 'Content-Type': 'application/json'};
}