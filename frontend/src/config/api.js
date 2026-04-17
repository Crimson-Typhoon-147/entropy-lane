import axios from 'axios';

const LOCAL_API = "http://127.0.0.1:8000";

// Will be defined ONLY when Cloudflare tunnel is active
const TUNNEL_API = import.meta.env.VITE_TUNNEL_URL;

export const API_BASE =
  TUNNEL_API && TUNNEL_API.length > 0
    ? TUNNEL_API
    : LOCAL_API;

const api = axios.create({
    baseURL: API_BASE,
});

// --- ENTROPY PROTOCOL FUNCTIONS ---

/** Phase 1: Request a locked entropy commitment from the server */
export const getCommitment = () => api.post('/commit');

/** Phase 2: Reveal entropy and fetch the Digital Signature + ZKP */
export const revealEntropy = (commitId) => api.get(`/reveal/${commitId}`);

/** Fetch the server's Public Key for client-side signature verification */
export const getSystemPublicKey = () => api.get('/system/public_key');

// --- MESSAGING FUNCTIONS ---

/** * Send an encrypted message. 
 * If commitId is provided, the backend generates ZKP/Signature proofs.
 */
export const sendMessage = (roomId, senderId, message, commitId = null) => 
    api.post('/send_message', {
        roomId,
        senderId,
        message,
        commit_id: commitId
    });

/** Fetch messages for a specific room */
export const receiveMessages = (roomId, clientId, lastTs = 0) => 
    api.get(`/receive_messages/${roomId}`, {
        params: { clientId, lastTs }
    });

export default api;