import React, { useState } from 'react';
import { createTransaction } from '../services/api';

const TransactionForm = () => {
  const [receiverId, setReceiverId] = useState('');
  const [amount, setAmount] = useState('');
  const [proof, setProof] = useState(null);
  const [preview, setPreview] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setProof(file);
    setPreview(URL.createObjectURL(file));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (amount <= 0) {
      alert('Le montant doit être supérieur à 0');
      return;
    }

    const formData = new FormData();
    formData.append('receiver', receiverId);
    formData.append('amount_sender', amount);
    formData.append('currency_sender', 'XAF');
    formData.append('currency_receiver', 'RWF');
    if (proof) formData.append('proof', proof);

    try {
      await createTransaction(formData);
      alert('Transaction créée !');
      setReceiverId('');
      setAmount('');
      setProof(null);
      setPreview(null);
    } catch (err) {
      console.log(err);
      alert('Erreur lors de la transaction');
    }
  };

  return (
    <div className="bg-white p-6 rounded shadow-md w-full max-w-md mx-auto">
      <h2 className="text-xl font-bold mb-4">Envoyer de l'argent</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          placeholder="ID du destinataire"
          value={receiverId}
          onChange={e => setReceiverId(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />
        <input
          placeholder="Montant"
          value={amount}
          onChange={e => setAmount(e.target.value)}
          type="number"
          className="w-full p-2 border rounded"
          required
        />
        <input
          type="file"
          onChange={handleFileChange}
          className="w-full"
        />
        {preview && <img src={preview} alt="proof preview" className="mt-2 w-32 h-32 object-cover rounded"/>}
        <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition">
          Envoyer
        </button>
      </form>
    </div>
  );
};

export default TransactionForm;
