import { useState } from "react";

function MessageBubble({ text, sender, meta }) {
  const [showDetails, setShowDetails] = useState(false);

  return (
    <div className={`message ${sender}`}>
      <p>{text}</p>

      {meta && (
        <>
          <button
            className="details-btn"
            onClick={() => setShowDetails(!showDetails)}
          >
            🔍 View Encryption Details
          </button>

          {showDetails && (
            <div className="encryption-details">
              <p><b>Algorithm:</b> {meta.algorithm}</p>
              <p><b>Entropy Source:</b> {meta.entropy_source}</p>
              <p><b>Entropy Block #:</b> {meta.entropy_index}</p>
              <p><b>Nonce:</b> {meta.nonce}</p>
              <p><b>Ciphertext:</b> {meta.ciphertext}</p>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default MessageBubble;
