import React, { useState, useRef, useEffect, useLayoutEffect } from "react";
import ReactMarkdown from "react-markdown";
import "./App.scss";

function App() {
  const [question, setQuestion] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);
  const containerRef = useRef(null);
  const [userId, setUserId] = useState("");
  const [chatId, setChatId] = useState("");
  const [isSending, setIsSending] = useState(false);

  useEffect(() => {
    let storedId = localStorage.getItem("user_id");
    if (!storedId) {
      storedId = crypto.randomUUID();
      localStorage.setItem("user_id", storedId);
    }
    setUserId(storedId);

    const fetchChatId = async () => {
      try {
        const res = await fetch("http://localhost:8000/new-chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_id: storedId }),
        });

        if (!res.ok) {
          throw new Error(`Erreur HTTP ${res.status}`);
        }

        const data = await res.json();
        setChatId(data.chat_id);
      } catch (err) {
        console.error("Erreur lors de la récupération du chatId", err);
        setMessages(prev => [
          ...prev,
          { role: "bot", content: "❌ Erreur lors de l'initialisation du chat." }
        ]);
      }
    };

    fetchChatId();
  }, []);

  const handleAsk = async () => {
    if (!question.trim() || isSending || !chatId) return;

    setIsSending(true);
    setMessages(prev => [...prev, { role: "user", content: question }]);
    setImageUrl("");

    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question,
          chat_id: chatId,
          user_id: userId,
        }),
      });

      if (!res.ok) {
        throw new Error(`Erreur HTTP ${res.status}`);
      }

      const data = await res.json();
      console.log("[DEBUG] /ask response", data);

      setMessages(prev => [
        ...prev,
        { role: "bot", content: data.answer || "🤖 Réponse vide." },
      ]);

      setImageUrl(data.image_url || "");
      setQuestion("");
    } catch (err) {
      console.error("Erreur lors de l'appel à /ask", err);
      setMessages(prev => [
        ...prev,
        {
          role: "bot",
          content:
            "❌ Une erreur est survenue lors de la récupération de la réponse. Veuillez réessayer.",
        },
      ]);
    } finally {
      setIsSending(false);
    }
  };

  const scrollToBottom = () => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  };

  useLayoutEffect(() => {
    scrollToBottom();
  }, [messages, imageUrl]);

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleAsk();
    }
  };

  return (
    <div style={{ display: "flex", height: "100%", width: "100%", overflow: "hidden", boxSizing: "border-box" }}>
      {imageUrl && (
        <div style={{
          flex: 1,
          background: "#f5f5f5",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          transition: "all 0.3s",
          overflow: "hidden",
        }}>
          <img
            src={`http://localhost:8000${imageUrl}`}
            alt="Présentation"
            style={{
              maxWidth: "90%",
              maxHeight: "90%",
              borderRadius: 12,
              boxShadow: "0 2px 12px #aaa",
            }}
            onLoad={scrollToBottom}
          />
        </div>
      )}

      <div style={{ display: "flex", flexDirection: "column", height: "100%", width: "100%", overflow: "hidden" }}>
        <div style={{ padding: "32px 48px 16px 48px", flexShrink: 0 }}>
          <h1 style={{ marginTop: 0 }}>Stream Digital Twin</h1>
        </div>

        <div
          ref={containerRef}
          style={{
            flex: 1,
            minHeight: 0,
            overflowY: "auto",
            padding: "0 48px",
            display: "flex",
            flexDirection: "column",
          }}
        >
          {messages.map((msg, idx) => (
            <div
              key={idx}
              style={{
                alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
                background: msg.role === "user" ? "#e3f2fd" : "#f0f0f0",
                color: "#222",
                borderRadius: 16,
                padding: "10px 20px",
                marginBottom: 12,
                maxWidth: "80%",
                fontSize: 18,
                whiteSpace: msg.role === "user" ? "pre-line" : undefined,
              }}
            >
              {msg.role === "bot" ? (
                <ReactMarkdown>{msg.content}</ReactMarkdown>
              ) : (
                msg.content
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <div
          style={{
            display: "flex",
            alignItems: "center",
            padding: "16px 48px",
            borderTop: "1px solid #eee",
            background: "#fff",
            flexShrink: 0,
          }}
        >
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Posez votre question..."
            disabled={isSending}
            style={{
              flex: 1,
              padding: 12,
              fontSize: 18,
              borderRadius: 8,
              border: "1px solid #ccc",
              marginRight: 12,
              boxSizing: "border-box",
              background: isSending ? "#f9f9f9" : "white",
            }}
          />
          <button
            onClick={handleAsk}
            disabled={isSending}
            style={{
              padding: "10px 18px",
              fontSize: 18,
              borderRadius: 8,
              background: isSending ? "#90caf9" : "#1976d2",
              color: "#fff",
              border: "none",
              cursor: isSending ? "not-allowed" : "pointer",
            }}
          >
            ➤
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
