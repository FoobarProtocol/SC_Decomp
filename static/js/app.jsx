import React, { useState } from 'react';
import ReactDOM from 'react-dom';

const App = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newMessage = {
      text: input,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };

    setMessages([...messages, newMessage]);
    setInput('');

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();
      setMessages(msgs => [...msgs, {
        text: data.response,
        sender: 'assistant',
        timestamp: new Date().toISOString(),
      }]);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Sapper IDE</h1>
      </header>
      
      <main className="chat-container">
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              <div className="message-content">{msg.text}</div>
              <div className="message-timestamp">
                {new Date(msg.timestamp).toLocaleTimeString()}
              </div>
            </div>
          ))}
        </div>
        
        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="message-input"
          />
          <button type="submit" className="send-button">
            Send
          </button>
        </form>
      </main>
    </div>
  );
};

ReactDOM.render(<App />, document.getElementById('root'));
