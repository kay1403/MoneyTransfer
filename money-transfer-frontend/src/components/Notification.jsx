import React, { useEffect, useState } from 'react';

const Notification = () => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    // WebSocket sécurisé pour production
    const ws = new WebSocket('wss://moneyTransfer.onrender.com/ws/notifications/');

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // Ajouter le message
      setMessages(prev => [...prev, data.message]);
      // Supprimer le message après 5 secondes
      setTimeout(() => {
        setMessages(prev => prev.slice(1));
      }, 5000);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
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
