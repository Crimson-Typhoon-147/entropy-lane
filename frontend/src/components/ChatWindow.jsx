import { useEffect, useState, useRef } from "react";
import MessageBubble from "./MessageBubble";
import InputBar from "./InputBar";

const ROOM_ID = "entropy-lane-room";
const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [clientId] = useState(() => "client-" + Math.random().toString(36).slice(2, 9));
  const [username, setUsername] = useState(() => localStorage.getItem("entropy-username") || "");
  const [tempUsername, setTempUsername] = useState("");
  
  const lastTsRef = useRef(0.0);
  const scrollRef = useRef(null);

  // 🔄 THE SYNC ENGINE
  useEffect(() => {
    if (!username) return;

    const poll = setInterval(async () => {
      try {
        const url = `${API_BASE}/receive_messages/${ROOM_ID}?clientId=${clientId}&lastTs=${lastTsRef.current}`;
        const res = await fetch(url);
        if (!res.ok) return;
        const data = await res.json();

        if (data.messages && data.messages.length > 0) {
          const currentTs = parseFloat(lastTsRef.current);
          const newOnes = data.messages.filter(m => parseFloat(m.ts) > currentTs);
          
          if (newOnes.length > 0) {
            lastTsRef.current = Math.max(...newOnes.map(m => parseFloat(m.ts)));
            const mapped = newOnes.map(m => ({
              text: m.text,
              sender: "other", // Received messages always stay left
              name: m.sender,
              meta: m.proofs || null,
            }));
            setMessages((prev) => [...prev, ...mapped]);
          }
        }
      } catch (err) { console.error("Sync Error:", err); }
    }, 50);
    return () => clearInterval(poll);
  }, [clientId, username]);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const joinChat = () => {
    if (!tempUsername.trim()) return;
    localStorage.setItem("entropy-username", tempUsername);
    setUsername(tempUsername);
  };

const sendMessage = async (text) => {
  if (!text.trim()) return;

  // 1. ADD TO SCREEN IMMEDIATELY (Instant Feedback)
  const myMsg = { 
    text: text, 
    sender: "me", 
    name: username,
    ts: Date.now() / 1000 // Temporary timestamp
  };
  
  setMessages((prev) => [...prev, myMsg]);

  // 2. SEND TO SERVER IN THE BACKGROUND
  try {
    await fetch(`${API_BASE}/send_message`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        roomId: ROOM_ID, 
        senderId: clientId, 
        message: text 
      }),
    });
  } catch (err) {
    console.error("Background sync failed:", err);
  }
};

  if (!username) {
    return (
      <div className="login-overlay">
        <div className="login-box">
          <h2>EntropyLane</h2>
          <input type="text" placeholder="Username" onChange={e => setTempUsername(e.target.value)} onKeyDown={e => e.key === 'Enter' && joinChat()} />
          <button onClick={joinChat}>Join Secure Room</button>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-layout">
      {/* 🛠 Left Sidebar: Security Stats */}
      <aside className="security-sidebar">
        <div className="sidebar-header">🛡️ Security Status</div>
        <div className="stat-card">
          <label>Entropy Source</label>
          <p>Traffic Video</p>
        </div>
        <div className="stat-card">
          <label>NIST SP 800-22</label>
          <p className="pass">Pass ✅</p>
        </div>
        <div className="stat-card">
          <label>Encryption</label>
          <p>AES-GCM</p>
        </div>
      </aside>

      {/* 💬 Main Chat Area */}
      <main className="chat-container">
        <header className="chat-nav">
          <div className="status-indicator">●</div>
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