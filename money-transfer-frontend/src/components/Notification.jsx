import React, { useEffect, useState } from 'react';

const Notification = () => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/notifications/');
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages(prev => [...prev, data.message]);
      setTimeout(() => {
        setMessages(prev => prev.slice(1));
      }, 5000);
    };
    return () => ws.close();
  }, []);

  return (
    <div className="fixed top-4 right-4 space-y-2 z-50">
      {messages.map((msg, idx) => (
        <div key={idx} className="bg-green-500 text-white p-2 rounded shadow-md">
          {msg}
        </div>
      ))}
    </div>
  );
};

export default Notification;
