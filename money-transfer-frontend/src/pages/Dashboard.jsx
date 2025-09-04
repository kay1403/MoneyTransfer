import React, { useEffect } from 'react';
import TransactionForm from '../components/TransactionForm';
import TransactionList from '../components/TransactionList';
import Notification from '../components/Notification';
import { isAuthenticated } from '../services/auth';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated()) {
      navigate('/'); // Redirige vers login si pas connecté
    }
  }, [navigate]);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <Notification />
      <h1 className="text-2xl font-bold mb-4 text-center">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <TransactionForm />
        <TransactionList />
      </div>
    </div>
  );
};

export default Dashboard;
