import React, { useEffect, useState } from 'react';

const Notification = () => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return;

    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const host = window.location.host; // inclut le port si présent
    const wsUrl = `${protocol}://${host}/ws/notifications/?token=${token}`;

    const ws = new WebSocket(wsUrl);

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setMessages(prev => [...prev, data.message]);
        setTimeout(() => setMessages(prev => prev.slice(1)), 5000);
      } catch (e) {
        console.log('Invalid WS message', e);
      }
    };
    ws.onclose = () => console.log('WS closed');
    ws.onerror = (e) => console.log('WS error', e);

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
