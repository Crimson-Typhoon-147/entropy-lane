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

// Backend base URL (LOCAL / CLOUDFLARE / PROD)
const API_BASE = import.meta.env.VITE_API_BASE;

function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [clientId] = useState(generateClientId);
  const lastTsRef = useRef(0);

  // -------------------------------
  // SEND MESSAGE
  // -------------------------------
  const sendMessage = async (text) => {
    if (!text.trim()) return;

    // Optimistic UI
    setMessages((prev) => [...prev, { text, sender: "me" }]);

    try {
      await fetch(`${API_BASE}/send_message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          roomId: ROOM_ID,
          senderId: clientId,
          message: text,
        }),
      });
    } catch (err) {
      console.error("Send failed:", err);
    }
  };

  // -------------------------------
  // RECEIVE MESSAGE (POLLING)
  // -------------------------------
  useEffect(() => {
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
              updated.push({ text: m.text, sender: "other" });
            });

            return updated;
          });
        }
      } catch (err) {
        console.error("Polling failed:", err);
      }
    }, 1500);

    return () => clearInterval(poll);
  }, [clientId]);

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h3>EntropyLane</h3>
        <span className="secure-badge">🔒 Secure Session</span>
      </div>

      <div className="chat-messages">
        {messages.map((m, i) => (
          <MessageBubble key={i} text={m.text} sender={m.sender} />
        ))}
      </div>

      <InputBar onSend={sendMessage} />
    </div>
  );
}

export default ChatWindow;
