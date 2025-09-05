// src/pages/RegisterPage.jsx
import React, { useState } from "react";
import { register } from "../services/api"; // on l’ajoutera dans api.js
import { useNavigate } from "react-router-dom";

function RegisterPage() {
  const [formData, setFormData] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await register(formData);
      navigate("/login"); // après inscription, redirige vers login
    } catch (err) {
      setError("Erreur lors de l'inscription");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <form
        onSubmit={handleSubmit}
        className="bg-white shadow-md rounded-lg p-6 w-80"
      >
        <h2 className="text-xl font-bold mb-4">Créer un compte</h2>
        {error && <p className="text-red-500">{error}</p>}

                <input
          type="text"
          name="username"
          placeholder="Nom d'utilisateur"
          onChange={handleChange}
          className="w-full p-2 border rounded mb-4"
          required
          autoComplete="username"
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          onChange={handleChange}
          className="w-full p-2 border rounded mb-4"
          required
          autoComplete="email"
        />
        <input
          type="password"
          name="password"
          placeholder="Mot de passe"
          onChange={handleChange}
          className="w-full p-2 border rounded mb-4"
          required
          autoComplete="new-password"
        />


        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
        >
          S'inscrire
        </button>
      </form>
    </div>
  );
}

export default RegisterPage;
