const LOCAL_API = "http://127.0.0.1:8000";

// Will be defined ONLY when Cloudflare tunnel is active
const TUNNEL_API = import.meta.env.VITE_TUNNEL_URL;

export const API_BASE =
  TUNNEL_API && TUNNEL_API.length > 0
    ? TUNNEL_API
    : LOCAL_API;
