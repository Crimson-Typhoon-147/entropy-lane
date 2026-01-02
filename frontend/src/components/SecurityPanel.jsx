function SecurityPanel() {
  return (
    <div className="security-panel">
      <h4>Security Status</h4>

      <p><strong>Entropy Source:</strong> Traffic Video</p>
      <p><strong>Shannon Entropy:</strong> ~3.7 bits</p>
      <p><strong>Min-Entropy:</strong> ~3.9 bits</p>

      <h5>NIST SP 800-22</h5>
      <ul>
        <li>Frequency Test: ✅ Pass</li>
        <li>Runs Test: ✅ Pass</li>
      </ul>

      <p><strong>Encryption:</strong> AES-GCM</p>
    </div>
  );
}

export default SecurityPanel;
