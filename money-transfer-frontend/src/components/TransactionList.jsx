import React, { useEffect, useState } from 'react';
import api from '../services/api';

const TransactionList = () => {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    const fetchTransactions = async () => {
      const res = await api.get('transactions/');
      setTransactions(res.data);
    };
    fetchTransactions();
  }, []);

  const getStatusColor = (status) => {
    switch(status) {
      case 'PENDING': return 'bg-yellow-300';
      case 'CONFIRMED': return 'bg-green-300';
      case 'FAILED': return 'bg-red-300';
      default: return 'bg-gray-300';
    }
  };

  return (
    <div className="p-4 bg-white rounded shadow-md">
      <h3 className="text-lg font-bold mb-2">My Transactions</h3>
      <ul className="space-y-2">
        {transactions.map(tx => (
          <li key={tx.id} className="flex justify-between items-center p-2 border rounded">
            <span>{tx.sender.username} → {tx.receiver.username}</span>
            <span>{tx.amount_receiver} {tx.currency_receiver}</span>
            <span className={`px-2 py-1 rounded ${getStatusColor(tx.status)}`}>{tx.status}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TransactionList;
