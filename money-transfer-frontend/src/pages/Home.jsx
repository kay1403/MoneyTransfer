import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-blue-200 to-white p-6">
      <h1 className="text-4xl font-bold mb-4 text-center text-blue-800">
        Welcome to MoneyTransfer App
      </h1>
      <p className="text-center mb-6 text-gray-700">
        Envoyez et recevez de l'argent facilement et en toute sécurité.
      </p>
      <div className="flex space-x-4">
        <Link
          to="/login"
          className="px-6 py-2 bg-blue-600 text-white rounded shadow hover:bg-blue-700 transition"
        >
          Login
        </Link>
        <Link
          to="/register"
          className="px-6 py-2 bg-green-600 text-white rounded shadow hover:bg-green-700 transition"
        >
          Register
        </Link>
      </div>
    </div>
  );
};

export default Home;
