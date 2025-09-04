import React, { useState, useEffect } from 'react';
import { createTransaction, downloadReceipt, convertCurrency } from '../services/api';

const TransactionForm = () => {
  const [receiverId, setReceiverId] = useState('');
  const [amount, setAmount] = useState('');
  const [proof, setProof] = useState(null);
  const [preview, setPreview] = useState(null);
  const [currencySender, setCurrencySender] = useState('XAF');
  const [currencyReceiver, setCurrencyReceiver] = useState('RWF');
  const [amountReceiver, setAmountReceiver] = useState(null);
  const [lastTransactionId, setLastTransactionId] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setProof(file);
    setPreview(URL.createObjectURL(file));
  };

  // --- Conversion en temps réel ---
  useEffect(() => {
    const fetchConversion = async () => {
      if (!amount || Number(amount) <= 0) {
        setAmountReceiver(null);
        return;
      }
      try {
        const data = await convertCurrency(currencySender, currencyReceiver, Number(amount));
        setAmountReceiver(data.converted_amount); // Assurez-vous que le backend renvoie `converted_amount`
      } catch (err) {
        console.error('Erreur conversion :', err);
        setAmountReceiver(null);
      }
    };

    fetchConversion();
  }, [amount, currencySender, currencyReceiver]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLastTransactionId(null); // reset avant nouvelle transaction

    if (Number(amount) <= 0) {
      alert('Le montant doit être supérieur à 0');
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append('receiver', receiverId);
    formData.append('amount_sender', amount);
    formData.append('currency_sender', currencySender);
    formData.append('currency_receiver', currencyReceiver);
    if (proof) formData.append('proof', proof);

    try {
      const transaction = await createTransaction(formData);
      alert('Transaction créée !');
      setReceiverId('');
      setAmount('');
      setProof(null);
      setPreview(null);
      setLastTransactionId(transaction.id);
    } catch (err) {
      console.error(err);
      alert('Erreur lors de la création de la transaction');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReceipt = async () => {
    if (!lastTransactionId) return;
    try {
      await downloadReceipt(lastTransactionId);
    } catch (err) {
      console.error(err);
      alert('Erreur lors du téléchargement du reçu');
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
          min="1"
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

        {/* Affichage du montant converti */}
        {amountReceiver !== null && (
          <div className="text-gray-700 font-semibold">
            Montant estimé pour le receiver: {amountReceiver} {currencyReceiver}
          </div>
        )}

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
          className={`w-full py-2 rounded text-white transition ${
            loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
          }`}
          disabled={loading}
        >
          {loading ? 'Envoi en cours...' : 'Send'}
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
