export const API_URL = import.meta.env.VITE_CHATTEX_API_URL;
export const SOCKET_URL = import.meta.env.VITE_CHATTEX_WEBSOCKET_API_URL;
export const IS_DEV = (import.meta.env.VITE_CHATTEX_DEV) == "true";
export const BUILD_NUMBER = (IS_DEV ? import.meta.env.VITE_CHATTEX_BUILD_NUMBER : 1);

export function tokenHeader() {
  const t = localStorage.getItem('token');
  return { 'Authorization': 'Bearer ' + t, 'Content-Type': 'application/json' };
}
