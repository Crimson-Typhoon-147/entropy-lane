import ChatWindow from "./components/ChatWindow";
import SecurityPanel from "./components/SecurityPanel";
import "./styles.css";

function App() {
  return (
    <div className="app-container">
      <ChatWindow />
      <SecurityPanel />
    </div>
  );
}

export default App;
