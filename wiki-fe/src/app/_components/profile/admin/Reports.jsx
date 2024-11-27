'use client';
import React, { useEffect, useState } from 'react';
import ErrorMessage from '@/components/auth/ErrorMessage';

export default function Reports() {
  const [reports, setReports] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/denuncia/list/`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });

        const data = await response.json();

        if (!response.ok) {
          setErrorMessage(data.error || 'Falha ao pegar as denúncias');
          return;
        }

        setReports(data);
      } catch (err) {
        setErrorMessage('Um erro ocorreu ao tentar pegar as denúncias.');
      }
    };

    fetchReports();
  }, []);

  return (
    <div style={{ padding: '20px', width: '50%', paddingTop: '0px', opacity: 0.8 }}>
      <h1>Denúncia de casos de dengue</h1>
      {errorMessage && (
        <ErrorMessage message={errorMessage} />
      )}
      {reports.length > 0 ? (
        <ul style={{ listStyleType: 'none', padding: 0 }}>
          {reports.map((report) => (
            <li
              key={report.id}
              style={{
                border: '1px solid #ddd',
                padding: '10px',
                marginBottom: '10px',
                borderRadius: '5px',
                backgroundColor: '#f9f9f9',
              }}
            >
              <p>
                <strong>Usuário:</strong> <br />
                <ul>
                  <li><strong>Nome:</strong> {report.user.name}</li>
                  <li><strong>Email:</strong> {report.user.email}</li>
                </ul>
              </p>
              <p>
                <strong>Endereço:</strong> <br />
                <ul>
                  <li>{report.endereco.rua} {report.endereco.numero === -1 ? '' : report.endereco.numero}, {report.endereco.bairro}, {report.endereco.cidade}, {report.endereco.estado}</li>
                </ul>
              </p>
              <p>
                <strong>Denúncia:</strong> {report.text}
              </p>
            </li>
          ))}
        </ul>
      ) : (
        <p>Nenhuma denúncia encontrada.</p>
      )}
    </div>
  );
}
