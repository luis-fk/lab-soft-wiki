'use client'
import React, { useEffect, useState } from 'react';
import '@/styles/profile/profile-info.css';
import { getSession } from '@/lib/session';

export default function Info() {
  const [user, setUser] = useState(null); 
  const [error, setError] = useState(null); 

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
        console.log(data);
      } catch (error) {
        setError('Ocorreu um erro ao carregar as informações do usuário.');
      } 
    };

    fetchUser();
  }, []); 


  if (error) {
    return <div className='profile-container'>{error}</div>; 
  }

  if (!user) {
    return <div className='profile-container'>Carregando informações do usuário...</div>; 
  }

  return (
    <div className='profile-container'>
        <div>
          <h2>Informações do Usuário</h2>
          <p><strong>Nome:</strong> {user.name}</p>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Cidade:</strong> {user.city ? user.city : 'Não informado'}</p>
<<<<<<< HEAD
<<<<<<< HEAD
          <p><strong>Permissão:</strong> {user.role.charAt(0).toUpperCase() + user.role.slice(1)}</p>
=======
          <p><strong>Permissão:</strong> {user.role}</p>
>>>>>>> e98d37f (integration changes)
=======
          <p><strong>Permissão:</strong> {user.role.charAt(0).toUpperCase() + user.role.slice(1)}</p>
>>>>>>> aff970a (integration final changes)
          <p><strong>Data de inscrição:</strong> {new Date(user.date_joined).toLocaleDateString()}</p>
        </div>
    </div>
  );
}
