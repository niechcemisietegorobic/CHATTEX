export const API_URL = import.meta.env.VITE_CHATTEX_API_URL;
export const SOCKET_URL = import.meta.env.VITE_CHATTEX_WEBSOCKET_API_URL;

export function tokenHeader() {
  const t = localStorage.getItem('token');
  return {'Authorization': 'Bearer ' + t, 'Content-Type': 'application/json'};
}
