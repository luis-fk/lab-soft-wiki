'use client'
import React, { useEffect, useState } from 'react';
import '@/styles/profile/profile-info.css';
import { getSession } from '@/lib/session';
import SuccessMessage from '@/components/auth/SuccessMessage'
import ErrorMessage from '@/components/auth/ErrorMessage'


export default function Info() {
  const [user, setUser] = useState(null); 
  const [error, setError] = useState(null); 
  const [name, setName] = useState('');
  const [city, setCity] = useState('');
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [success, setSuccess] = useState(null);
  const [changePasswordSucces, setChangePasswordSuccess] = useState('');
  const [passwordError, setPasswordError] = useState('');

  const roleTranslations = {
    'admin': 'Administrador',
    'user': 'Usuário',
    'staff': 'Pesquisador'
  };

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const session = await getSession(); 
        const response = await fetch(`http://127.0.0.1:8000/user/detail/${session.userId}/`, {
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
        setCity(data.city);
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
      setError('Ocorreu um erro ao atualizar a informação.');
    }
  };

  const handleChangePassword = async () => {
    if (newPassword !== confirmPassword) {
      setPasswordError('As senhas devem ser iguais.');
      return;
    }

    try {
      const session = await getSession(); 
      const response = await fetch(`http://127.0.0.1:8000/user/update_password/${session.userId}/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          password: currentPassword, 
          new_password: newPassword 
        }),
      });

      if (!response.ok) {
        setPasswordError('Erro ao atualizar a senha.');
        return;
      }

      setChangePasswordSuccess('Senha atualizada com sucesso!');
    } catch (error) {
      setPasswordError('Ocorreu um erro ao atualizar a senha, tente novamente mais tarde.');
    }
  }

  if (!user) {
    return <div className='profile-container'>Carregando informações do usuário...</div>; 
  }

  return (
    <div className='profile-container'>
        <div className='account-information-container'>
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
            <p><strong>Permissão:</strong> {roleTranslations[user.role]}</p>
          </div>

          <div className="data-container">
            <p><strong>Data de inscrição:</strong> {new Date(user.date_joined).toLocaleDateString()}</p>
          </div>

          <button onClick={handleSubmit} className="update-button">Atualizar</button>

          <SuccessMessage message={success} />
          <ErrorMessage message={error} />
        </div>

        <div>
          <h2>Alterar senha</h2>

          <div className="data-container">
            <p><strong>Senha atual:</strong></p>
            <input type="password" value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} 
                   className="data-input" required/>
          </div>

          <div className="data-container">
            <p><strong>Nova senha:</strong></p>
            <input type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} 
                   className="data-input" required/>
          </div>

          <div className="data-container">
            <p><strong>Confirme a nova senha:</strong></p>
            <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} 
                   className="data-input" required/>
          </div>

          <button onClick={handleChangePassword} className="update-button">Atualizar senha</button>

          <ErrorMessage message={passwordError} />
          <SuccessMessage message={changePasswordSucces} />
        </div>
    </div>
  );
}
