import { useEffect, useState, useRef } from "react";
import MessageBubble from "./MessageBubble";
import InputBar from "./InputBar";

function generateClientId() {
  return "client-" + Math.random().toString(36).slice(2);
}

const ROOM_ID = "entropy-lane-room"; // shared by both users

function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [clientId] = useState(generateClientId);
  const lastTsRef = useRef(0);

  const sendMessage = async (text) => {
    if (!text.trim()) return;

    setMessages((p) => [...p, { text, sender: "me" }]);

    await fetch("http://10.25.163.201:8000/send_message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        roomId: ROOM_ID,
        senderId: clientId,
        message: text,
      }),
    });
  };

  useEffect(() => {
    const poll = setInterval(async () => {
      const res = await fetch(
        `http://10.25.163.201:8000/receive_message?roomId=${ROOM_ID}&clientId=${clientId}&lastTs=${lastTsRef.current}`
      );

      const data = await res.json();

      if (data.messages.length) {
        data.messages.forEach((m) => {
          lastTsRef.current = Math.max(lastTsRef.current, m.ts);
          setMessages((p) => [...p, { text: m.text, sender: "other" }]);
        });
      }
    }, 1500);

    return () => clearInterval(poll);
  }, [clientId]);

  return (
    <div className="chat-window">
      <h3>EntropyLane Chat</h3>

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
