// App.jsx
import ChatWindow from "./components/ChatWindow";
// REMOVE: import SecurityPanel from "./components/SecurityPanel";
import "./App.css"; // CHANGE THIS from "./styles.css"

function App() {
  return (
    // Change className to match the root styles in App.css if needed, 
    // but the ID #root is already handled.
    <ChatWindow /> 
  );
}

export default App;