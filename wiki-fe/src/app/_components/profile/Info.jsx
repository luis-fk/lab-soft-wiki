'use client'
import React, { useEffect, useState } from 'react';
import '@/styles/profile/profile-info.css';
import { getSession } from '@/lib/session';
import SuccessMessage from '@/components/auth/SuccessMessage'

export default function Info() {
  const [user, setUser] = useState(null); 
  const [error, setError] = useState(null); 
  const [name, setName] = useState('');
  const [city, setCity] = useState('');
  const [success, setSuccess] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const session = await getSession(); 
        const response = await fetch(`http://127.0.0.1:8000/user/list/${session.userId}/`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });
        
        if (!response.ok) {
          setError(response.error);
          return;
        }

        const data = await response.json();
        setUser(data);
        setName(data.name);
      } catch (error) {
        setError('Ocorreu um erro ao carregar as informações do usuário.');
      } 
    };

    fetchUser();
  }, []); 

  const handleSubmit = async () => {
    try {
      const session = await getSession(); 
      const response = await fetch(`http://127.0.0.1:8000/user/update/${session.userId}/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, city }),
      });

      if (!response.ok) {
        setError('Erro ao atualizar a informação.');
        return;
      }

      setSuccess('Informação atualizada com sucesso!');
    } catch (error) {
      setError('Ocorreu um erro ao atualizar o nome.');
    }
  };

  if (error) {
    return <div className='profile-container'>{error}</div>; 
  }

  if (!user) {
    return <div className='profile-container'>Carregando informações do usuário...</div>; 
  }

  return (
    <div className='profile-container'>
        <div>
          <h2>Informações da Conta</h2>

          <div className="data-container">
            <p><strong>Nome: </strong></p>
            <input type="text" value={name} onChange={(e) => setName(e.target.value)} className="data-input" />
          </div>

          <div className="data-container">
            <p><strong>Email: </strong> {user.email}</p>
          </div>
  
          <div className="data-container">
            <p><strong>Cidade:</strong></p>
            <input type="text" value={city} onChange={(e) => setCity(e.target.value)} className="data-input" />
          </div>

          <div className="data-container">
            <p><strong>Permissão:</strong> {user.role.charAt(0).toUpperCase() + user.role.slice(1)}</p>
          </div>

          <div className="data-container">
            <p><strong>Data de inscrição:</strong> {new Date(user.date_joined).toLocaleDateString()}</p>
          </div>

          <button onClick={handleSubmit} className="update-button">Atualizar</button>
          <SuccessMessage message={success} />
        </div>
    </div>
  );
}
