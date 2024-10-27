'use client'
import React, { useEffect, useState } from 'react';
import '@/styles/profile/users.css';
import SuccessMessage from '@/components/auth/SuccessMessage'
import ErrorMessage from '@/components/auth/ErrorMessage'

export default function Users() {
  const [users, setUsers] = useState([]); 
  const [originalUsers, setOriginalUsers] = useState([]);
  const [error, setError] = useState(''); 
  const [success, setSuccess] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearchActive, setIsSearchActive] = useState(false);

  const roleTranslations = {
    'admin': 'Administrador',
    'user': 'Usuário',
    'staff': 'Pesquisador'
  };

  const roles = ['admin', 'user', 'staff'];
  
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/user/list/`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });

        const data = await response.json();

        if (!response.ok) {
          setError(data.error);
          return;
        }

        setUsers(data); 
        setOriginalUsers(data);
      } catch {
        setError('Um erro ocorreu ao tentar carregar os usuarios. Por favor tente novamente.');
      } 
    };

    fetchUsers();
  }, []); 

  const handleRoleChange = async (userId, newRole) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/user/update/${userId}/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role: newRole })
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error);
        return;
      }

      setUsers(prevUsers => 
        prevUsers.map(user => 
          user.id === userId ? { ...user, role: newRole } : user
        )
      );

      setSuccess('Permissão do usuário atualizada com sucesso!');
    } catch {
      setError('Um erro ocorreu ao tentar atualizar a permissão do usuário.');

    }
  };

  const handleSearch = async () => {
    if (isSearchActive) {
      setUsers(originalUsers); 
      setSearchQuery('');
      setIsSearchActive(false);
      setError('');
      return;
    }

    if (!searchQuery) {
      setError('Por favor, insira um email para busca.');
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:8000/user/list/${1}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });

      if (!response.ok) {
        setError('Usuário não encontrado.');
        setUsers([]); // Clear users if not found
        return;
      }

      const data = await response.json();
      setUsers([data]); // Set only the searched user
      setError('');
      setIsSearchActive(true);
    } catch {
      setError('Um erro ocorreu ao tentar buscar o usuário. Por favor tente novamente.');
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toISOString().split('T')[0];
  };

  return (
    <>
      <div className='users-container'>
        <h2>Usuários</h2>

        <div>
          <input type="text" placeholder="Buscar por email" value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)} className="search-input"
          />

          <button onClick={handleSearch} className="search-button">
            {isSearchActive ? 'Limpar' : 'Buscar'}
          </button>
        </div>

        <SuccessMessage message={success} />
        <ErrorMessage message={error} />

        <table className="user-table">
          <thead>
            <tr>
              <th>Nome</th>
              <th>Email</th>
              <th>Cidade</th>
              <th>Role</th>
              <th>Data de inscrição</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id}>
                <td>{user.name}</td>
                <td>{user.email}</td>
                <td>{user.city ? user.city : 'Não informado'}</td>
                <td>
                  <select value={user.role} onChange={(e) => handleRoleChange(user.id, e.target.value)}>
                    <option value={user.role}>{roleTranslations[user.role]}</option>
                    {roles.filter(role => role !== user.role).map((role) => (
                      <option key={role} value={role}>{roleTranslations[role]}</option>
                    ))}
                  </select>
                </td>
                <td>{formatDate(user.date_joined)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
    
  );
}
