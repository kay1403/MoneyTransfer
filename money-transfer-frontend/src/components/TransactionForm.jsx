import React, { useState } from 'react';
import { createTransaction, downloadReceipt } from '../services/api';

const TransactionForm = () => {
  const [receiverId, setReceiverId] = useState('');
  const [amount, setAmount] = useState('');
  const [proof, setProof] = useState(null);
  const [preview, setPreview] = useState(null);
  const [currencySender, setCurrencySender] = useState('XAF');
  const [currencyReceiver, setCurrencyReceiver] = useState('RWF');
  const [lastTransactionId, setLastTransactionId] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setProof(file);
    setPreview(URL.createObjectURL(file));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('receiver', receiverId);
    formData.append('amount_sender', amount);
    formData.append('currency_sender', currencySender);
    formData.append('currency_receiver', currencyReceiver);
    if (proof) formData.append('proof', proof);

    try {
      const transaction = await createTransaction(formData);
      alert('Transaction created!');
      setReceiverId('');
      setAmount('');
      setProof(null);
      setPreview(null);
      setLastTransactionId(transaction.id); // sauvegarde ID pour le PDF
    } catch (err) {
      console.error(err);
      alert('Error creating transaction');
    }
  };

  const handleDownloadReceipt = async () => {
    if (!lastTransactionId) return;
    try {
      await downloadReceipt(lastTransactionId);
    } catch (err) {
      console.error(err);
      alert('Error downloading receipt');
    }
  };

  return (
    <div className="bg-white p-6 rounded shadow-md w-full max-w-md mx-auto">
      <h2 className="text-xl font-bold mb-4">Send Money</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          placeholder="Receiver ID"
          value={receiverId}
          onChange={e => setReceiverId(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />
        <input
          placeholder="Amount"
          value={amount}
          onChange={e => setAmount(e.target.value)}
          type="number"
          className="w-full p-2 border rounded"
          required
        />
        <div className="flex space-x-2">
          <input
            placeholder="Sender Currency"
            value={currencySender}
            onChange={e => setCurrencySender(e.target.value)}
            className="w-1/2 p-2 border rounded"
          />
          <input
            placeholder="Receiver Currency"
            value={currencyReceiver}
            onChange={e => setCurrencyReceiver(e.target.value)}
            className="w-1/2 p-2 border rounded"
          />
        </div>
        <input type="file" onChange={handleFileChange} className="w-full" />
        {preview && (
          <img
            src={preview}
            alt="proof preview"
            className="mt-2 w-32 h-32 object-cover rounded"
          />
        )}
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
        >
          Send
        </button>
      </form>

      {lastTransactionId && (
        <button
          onClick={handleDownloadReceipt}
          className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700 transition mt-4"
        >
          Télécharger le reçu PDF
        </button>
      )}
    </div>
  );
};

export default TransactionForm;
