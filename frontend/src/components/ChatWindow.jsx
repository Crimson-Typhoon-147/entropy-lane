import { useState } from "react";
import MessageBubble from "./MessageBubble";
import InputBar from "./InputBar";

function ChatWindow() {
  const [messages, setMessages] = useState([]);

  const sendMessage = async (text) => {
    if (!text.trim()) return;

    // 1️⃣ Add user message
    setMessages((prev) => [...prev, { text, sender: "me" }]);

    try {
      // 2️⃣ Call backend
      const response = await fetch("http://127.0.0.1:8000/send_message", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: text }),
      });

      if (!response.ok) {
        throw new Error("Backend error");
      }

      // 3️⃣ Parse response safely
      const data = await response.json();

      // 4️⃣ Add backend reply
      setMessages((prev) => [
        ...prev,
        {
          text: data.reply,
          sender: "other",
          meta: {
            ciphertext: data.ciphertext,
            nonce: data.nonce,
            entropy_index: data.entropy_index,
            algorithm: data.algorithm,
            entropy_source: data.entropy_source,
          },
        },
      ]);
    } catch (error) {
      // 5️⃣ Error fallback (no data reference here!)
      setMessages((prev) => [
        ...prev,
        {
          text: "⚠️ Error communicating with backend",
          sender: "other",
        },
      ]);
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h3>EntropyLane</h3>
        <span className="secure-badge">🔒 Secure Session</span>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <p className="empty-chat">No messages yet</p>
        )}

        {messages.map((msg, index) => (
          <MessageBubble
            key={index}
            text={msg.text}
            sender={msg.sender}
            meta={msg.meta}
          />
        ))}
      </div>

      <InputBar onSend={sendMessage} />
    </div>
  );
}

export default ChatWindow;
