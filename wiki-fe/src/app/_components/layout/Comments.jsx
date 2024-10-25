'use client';
import React, { useEffect, useState } from 'react';
import ErrorMessage from "@/components/auth/ErrorMessage";
import '@/styles/article.css';

export default function Comments() {
  const [comments, setComments] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    const fetchComments = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/comentary/list/`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });

        if (!response.ok) {
          setErrorMessage('Um erro ocorreu ao tentar carregar os comentários.');
        }

        const data = await response.json();
        setComments(data);
      } catch (err) {
        setErrorMessage('Um erro ocorreu ao tentar carregar os comentários.');
      }
    };

    fetchComments();
  }, []);

  return (
    <div>
      <h1>Comentários</h1>
      <div style={{ display: 'flex', justifyContent: 'flex-start', paddingLeft: '20px' }}>
        <ErrorMessage message={errorMessage} />
      </div>

      {comments.length > 0 ? (
        comments.map((comment) => (
          <div key={comment.id} className="comment">
            <h3>Fulano Teste:</h3>
            <p style={{ paddingLeft: '20px' }}>Parabéns</p>
            <span className="comment-date" style={{ paddingLeft: '10px' }}>{new Date().toLocaleDateString('pt-BR', {
              day: 'numeric',
              month: 'long',
              year: 'numeric'
            })}</span>
            <hr style={{ border: 'none', borderTop: '1px solid #333', width: '95%', margin: '20px auto' }} />
          </div>
        ))
      ) : <></>}
    </div>
  );
}
