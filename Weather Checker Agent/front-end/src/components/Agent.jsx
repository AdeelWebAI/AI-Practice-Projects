import { useState } from "react";

export default function Agent() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    // User ka message add karo
    const userMsg = { role: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    // Filhaal dummy agent response (future me FastAPI se fetch karenge)
    setTimeout(() => {
      const botMsg = { role: "assistant", text: "🤖 Agent ka dummy reply!" };
      setMessages((prev) => [...prev, botMsg]);
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="flex flex-col items-center justify-center mt-6 w-full max-w-2xl">
      {/* Chat Window */}
      <div className="bg-white shadow-xl rounded-2xl w-full h-[400px] p-4 overflow-y-auto">
        {messages.length === 0 && (
          <p className="text-gray-400 text-center mt-10">
            Start chatting with your AI Agent 🤖
          </p>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`my-2 flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`px-4 py-2 rounded-2xl max-w-[70%] text-sm ${
                msg.role === "user"
                  ? "bg-blue-500 text-white rounded-br-none"
                  : "bg-gray-200 text-gray-900 rounded-bl-none"
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start my-2">
            <div className="px-4 py-2 bg-gray-200 rounded-2xl text-gray-700 animate-pulse">
              Thinking...
            </div>
          </div>
        )}
      </div>

      {/* Input Box */}
      <div className="flex w-full mt-3 gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Type your question..."
          className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-500 text-white font-semibold rounded-xl shadow-md hover:from-blue-600 hover:to-purple-600 transition duration-300 disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}
