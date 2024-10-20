'use client'
import React, { useEffect, useState } from 'react';
import '@/styles/profile/profile-info.css';
import '@/styles/profile/users.css';

export default function Users() {
  const [users, setUsers] = useState([]); 
  const [error, setError] = useState(null); 

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/user/list/`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });

        if (!response.ok) {
          setError(response.error);
          return;
        }

        const data = await response.json();
        setUsers(data); 
      } catch (err) {
        setError('Um erro ocorreu ao tentar carregar os usuarios. Por favor tente novamente.');
      } 
    };

    fetchUsers();
  }, []); 

  if (error) {
    return <div className='profile-container'>{error}</div>;
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toISOString().split('T')[0]; // Returns YYYY-MM-DD format
  };

  return (
    <div className='profile-container'>
      <h2>Usuários</h2>
      <table className="user-table">
        <thead>
          <tr>
            <th>Nome de usuário</th>
            <th>Email</th>
            <th>Cidade</th>
            <th>Role</th>
            <th>Data de inscrição</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.username}</td>
              <td>{user.email}</td>
              <td>{user.cidade ? user.cidade : 'Não informado'}</td>
              <td>{user.role.charAt(0).toUpperCase() + user.role.slice(1)}</td>
              <td>{formatDate(user.date_joined)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
