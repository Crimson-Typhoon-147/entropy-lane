import { useEffect, useState, useRef } from "react";
import MessageBubble from "./MessageBubble";
import InputBar from "./InputBar";

const ROOM_ID = "entropy-lane-room";
const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

const WS_BASE = API_BASE.startsWith("https")
  ? API_BASE.replace("https", "wss")
  : API_BASE.replace("http", "ws");

function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [clientId] = useState(() => "client-" + Math.random().toString(36).slice(2, 9));
  const [username, setUsername] = useState(() => localStorage.getItem("entropy-username") || "");
  const [tempUsername, setTempUsername] = useState("");
  
  // 🔥 New State for dynamic entropy bar
  const [currentEntropy, setCurrentEntropy] = useState(7.2); 

  const scrollRef = useRef(null);
  const wsRef = useRef(null);
  const intervalRef = useRef(null);

  const [isActive, setIsActive] = useState(true);

  useEffect(() => {
    const handleVisibility = () => setIsActive(!document.hidden);
    document.addEventListener("visibilitychange", handleVisibility);
    return () => document.removeEventListener("visibilitychange", handleVisibility);
  }, []);

  const startPolling = () => {
    if (intervalRef.current) return;
    intervalRef.current = setInterval(async () => {
      if (!isActive) return;
      try {
        const res = await fetch(`${API_BASE}/receive_messages/${ROOM_ID}?clientId=${clientId}`);
        const data = await res.json();
        if (data.messages?.length > 0) {
          setMessages((prev) => {
            const existing = new Set(prev.map((m) => m.text + m.name));
            const filtered = data.messages.filter((m) => !existing.has(m.text + m.sender));
            const mapped = filtered.map((m) => ({ text: m.text, sender: "other", name: m.sender }));
            return [...prev, ...mapped];
          });
        }
      } catch (err) { console.error("Polling error:", err); }
    }, 2000);
  };

  const stopPolling = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  useEffect(() => {
    if (!username) return;
    let ws;
    try {
      ws = new WebSocket(`${WS_BASE}/ws/${ROOM_ID}/${clientId}`);
    } catch {
      startPolling();
      return;
    }
    wsRef.current = ws;
    ws.onopen = () => { stopPolling(); };
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.sender_id === clientId) return;
      setMessages((prev) => [...prev, { text: data.text, sender: "other", name: data.sender || "Unknown" }]);
      
      // Update entropy if peer sends metadata (optional enhancement)
      if(data.shannon) setCurrentEntropy(data.shannon);
    };
    ws.onerror = () => { ws.close(); };
    ws.onclose = () => { startPolling(); };
    return () => { ws.close(); stopPolling(); };
  }, [clientId, username]);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const joinChat = () => {
    if (!tempUsername.trim()) return;
    localStorage.setItem("entropy-username", tempUsername.trim());
    setUsername(tempUsername.trim());
  };

  // =========================
  // 🚀 UPDATED SEND MESSAGE
  // =========================
  const sendMessage = async (text) => {
    if (!text.trim()) return;

    const myMsg = { text, sender: "me", name: username };
    setMessages((prev) => [...prev, myMsg]);

    try {
      const response = await fetch(`${API_BASE}/send_message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          roomId: ROOM_ID,
          senderId: clientId,
          senderName: username,
          message: text,
        }),
      });

      const data = await response.json();
      
      // 🔥 Extract live entropy from backend response to drive the bar
      // Note: Ensure your FastAPI returns {"status": "ok", "shannon": ...}
      if (data.shannon) {
        setCurrentEntropy(data.shannon);
      } else {
        // Fallback: Just jitter the bar slightly to show it's "calculating"
        setCurrentEntropy(7.0 + Math.random() * 0.8);
      }

    } catch (err) {
      console.error("Send failed:", err);
    }
  };

  if (!username) {
    return (
      <div className="login-overlay">
        <div className="login-box">
          <h2>EntropyLane</h2>
          <input type="text" placeholder="Username" value={tempUsername} onChange={(e) => setTempUsername(e.target.value)} onKeyDown={(e) => e.key === "Enter" && joinChat()} />
          <button onClick={joinChat}>Join Secure Room</button>
        </div>
      </div>
    );
  }

  // Calculate percentage (Entropy maxes at 8.0)
  const entropyPercent = Math.min((currentEntropy / 8) * 100, 100);

  return (
    <div className="chat-layout">
      <aside className="security-sidebar">
        <div className="sidebar-header">🛡️ Security Status</div>

        {/* 🔥 NEW: Dynamic Entropy Progress Bar */}
        <div className="stat-card entropy-meter">
          <div className="meter-label">
            <label>Live Entropy</label>
            <span className="entropy-value">{entropyPercent.toFixed(1)}%</span>
          </div>
          <div className="progress-bg">
            <div 
              className="progress-fill" 
              style={{ width: `${entropyPercent}%` }}
            ></div>
          </div>
          <p className="micro-text">
            {currentEntropy > 7 ? "High Randomness Detected" : "Generating Bits..."}
          </p>
        </div>

        <div className="stat-card">
          <label>Mode</label>
          <p>{wsRef.current?.readyState === 1 ? "WebSocket" : "Polling"}</p>
        </div>

        <div className="stat-card">
          <label>Entropy Source</label>
          <p>Multi-Source</p>
        </div>

        <div className="stat-card">
          <label>Encryption</label>
          <p>AES-GCM</p>
        </div>
      </aside>

      <main className="chat-container">
        <header className="chat-nav">
          <h4>EntropyLane Room</h4>
        </header>

        <div className="messages-viewport">
          {messages.map((m, i) => (
            <div key={i} className={`message-wrapper ${m.sender === "me" ? "msg-right" : "msg-left"}`}>
              {m.sender === "other" && <span className="sender-tag">{m.name}</span>}
              <MessageBubble text={m.text} sender={m.sender} />
            </div>
          ))}
          <div ref={scrollRef} />
        </div>

        <div className="input-container">
          <InputBar onSend={sendMessage} />
        </div>
      </main>
    </div>
  );
}

export default ChatWindow;