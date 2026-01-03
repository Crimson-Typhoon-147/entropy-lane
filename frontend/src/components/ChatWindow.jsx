import { useEffect, useState, useRef } from "react";
import MessageBubble from "./MessageBubble";
import InputBar from "./InputBar";

// -------------------------------
// Utils
// -------------------------------
function generateClientId() {
  return "client-" + Math.random().toString(36).slice(2);
}

// Shared room
const ROOM_ID = "entropy-lane-room";

// Backend base URL
const API_BASE = import.meta.env.VITE_API_BASE;

function ChatWindow() {
  // -------------------------------
  // STATE & REFS (ALWAYS RUN)
  // -------------------------------
  const [messages, setMessages] = useState([]);
  const [clientId] = useState(generateClientId);
  const [username, setUsername] = useState("");
  const [tempUsername, setTempUsername] = useState("");
  const lastTsRef = useRef(0);

  // -------------------------------
  // Load username once
  // -------------------------------
  useEffect(() => {
    const saved = localStorage.getItem("entropy-username");
    if (saved) setUsername(saved);
  }, []);

  // -------------------------------
  // RECEIVE MESSAGE (POLLING)
  // -------------------------------
  useEffect(() => {
    if (!username) return;

    const poll = setInterval(async () => {
      try {
        const res = await fetch(
          `${API_BASE}/receive_message?roomId=${ROOM_ID}&clientId=${clientId}&lastTs=${lastTsRef.current}`
        );

        if (!res.ok) return;

        const data = await res.json();

        if (data.messages && data.messages.length) {
          setMessages((prev) => {
            const updated = [...prev];

            data.messages.forEach((m) => {
              lastTsRef.current = Math.max(lastTsRef.current, m.ts);
              updated.push({
                text: m.text,
                sender: "other",
                name: m.senderName,
                meta: m.meta || null,
              });
            });

            return updated;
          });
        }
      } catch (err) {
        console.error("Polling failed:", err);
      }
    }, 1500);

    return () => clearInterval(poll);
  }, [clientId, username]);

  // -------------------------------
  // JOIN HANDLER (USED BY ENTER + BUTTON)
  // -------------------------------
  const joinChat = () => {
    const value = tempUsername.trim();
    if (!value) return;
    localStorage.setItem("entropy-username", value);
    setUsername(value);
  };

  // -------------------------------
  // SEND MESSAGE
  // -------------------------------
  const sendMessage = async (text) => {
    if (!text.trim() || !username) return;

    setMessages((prev) => [
      ...prev,
      { text, sender: "me", name: username },
    ]);

    try {
      await fetch(`${API_BASE}/send_message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          roomId: ROOM_ID,
          senderId: clientId,
          senderName: username,
          message: text,
        }),
      });
    } catch (err) {
      console.error("Send failed:", err);
    }
  };

  // ======================================================
  // RENDER
  // ======================================================
  return (
    <div className="chat-window">
      <div className="chat-header">
        <h3>EntropyLane</h3>
        <span className="secure-badge">🔒 Secure Session</span>
      </div>

      <div className="chat-messages">
        {!username ? (
          <>
            <p style={{ color: "#ccc" }}>
              Enter your name to join the chat
            </p>

            <input
              type="text"
              placeholder="Your name"
              value={tempUsername}
              autoFocus
              onChange={(e) => setTempUsername(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  joinChat();
                }
              }}
              style={{
                padding: "10px",
                borderRadius: "6px",
                border: "1px solid #444",
                background: "#020617",
                color: "#e5e7eb",
                width: "100%",
                maxWidth: "300px",
                marginBottom: "12px",
              }}
            />

            <button
              onClick={joinChat}
              style={{
                padding: "10px 16px",
                borderRadius: "6px",
                border: "none",
                background: "#16a34a",
                color: "#052e16",
                fontWeight: "600",
                cursor: "pointer",
                maxWidth: "140px",
              }}
            >
              Join Chat
            </button>
          </>
        ) : (
          messages.map((m, i) => (
            <MessageBubble
              key={i}
              text={m.text}
              sender={m.sender}
              name={m.name}
              meta={m.meta}
            />
          ))
        )}
      </div>

      {username && <InputBar onSend={sendMessage} />}
    </div>
  );
}

export default ChatWindow;
