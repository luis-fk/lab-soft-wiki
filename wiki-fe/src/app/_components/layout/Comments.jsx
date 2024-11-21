'use client';
import React, { useEffect, useState } from 'react';
import ErrorMessage from "@/components/auth/ErrorMessage";
import SuccessMessage from "@/components/auth/SuccessMessage";
import '@/styles/wiki/article.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faThumbsUp } from '@fortawesome/free-solid-svg-icons';
import Link from 'next/link';

export default function Comments({ params }) {
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const characterLimit = 1000;

  useEffect(() => {
    const fetchComments = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/commentary/list/${params.articleId}/`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });
        
        const data = await response.json();
        if (!response.ok) {
          setErrorMessage(data.error);
          return;
        }
        
        const commentsWithLikes = data.map((comment) => ({
          ...comment,
          liked: false,
        }));

        commentsWithLikes.sort((a, b) => {
          if (b.likes !== a.likes) {
              return b.likes - a.likes;
          }
          return new Date(b.created_at) - new Date(a.created_at);
      });

        setComments(commentsWithLikes);
      } catch (err) {
        return;
      }
    };

    fetchComments();
  }, []);

  const handleCommentSubmit = async () => {
    if (!newComment.trim()) {
      setErrorMessage('O comentário não pode estar vazio.');
      return;
    }

    if (newComment.length > 1000) {
      setErrorMessage('O comentário deve ter no maximo 1000 caracteres.');
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:8000/commentary/create/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: newComment, user_id: params.userId, article_id: params.articleId }),
      });

      const data = await response.json();

      if (!response.ok) {
        setErrorMessage(data.error);
        return;
      }

      setComments([data, ...comments]); 
      setNewComment(''); 
      setSuccessMessage('Comentário enviado com sucesso!');
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err) {
      setErrorMessage('Um erro ocorreu ao tentar enviar o comentário.');
    }
  };

  const handleLike = async (commentId, currentLikes, isLiked) => {
    const updatedComments = comments.map((comment) =>
      comment.id === commentId
        ? { ...comment, liked: !comment.liked, likes: comment.liked ? comment.likes - 1 : comment.likes + 1 }
        : comment
    );

    setComments(updatedComments);

    const newLikes = isLiked ? currentLikes - 1 : currentLikes + 1;

    try {
      await fetch(`http://127.0.0.1:8000/commentary/update/${commentId}/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ likes: newLikes })
      });
    } catch (err) {
      setErrorMessage('Um erro ocorreu2 ao tentar enviar o like.');
    }
  };

  return (
    <div>
      <hr style={{ border: 'none', borderTop: '1px solid #333', width: '95%', margin: '20px auto' }} />

      <h1 style={{ paddingBottom: '0px' }}>Comentários</h1>

      <div style={{ display: 'flex', justifyContent: 'flex-start', paddingLeft: '20px' }}>
        <ErrorMessage message={errorMessage} />
        <SuccessMessage message={successMessage} />
      </div>

      {params.userId ? (
        <div className="comment-input-section" style={{ padding: '20px' }}>
        <textarea
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          placeholder="Escreva seu comentário..."
          rows="3"
          style={{ width: '100%', padding: '10px', fontSize: '16px' }}
          maxLength={characterLimit}
        />
        <div style={{ textAlign: 'left', fontSize: '14px', color: newComment.length >= characterLimit - 100 ? 'red' : 'gray' }}>
          {newComment.length} / {characterLimit} caracteres
        </div>
        <button onClick={handleCommentSubmit} style={{ marginTop: '10px', padding: '10px 20px' }}>
          Enviar Comentário
        </button>
      </div>
      ) : <p>Para comentar é necessario <Link href="/login">entrar na sua conta</Link>.</p>}
      
      {comments.length > 0 ? (
        comments.map((comment) => (
          <div key={comment.id} className="comment">
            <h3 style={{ paddingBottom: '0px' }}>{comment.user_name}</h3>
            <p style={{ paddingLeft: '20px' }}>{comment.text}</p>
            <div style={{ paddingLeft: '10px', display: 'flex', alignItems: 'center' }}>
              <FontAwesomeIcon
                icon={faThumbsUp}
                style={{ marginRight: '5px', color: comment.liked ? 'blue' : 'gray', cursor: 'pointer', marginBottom: '5px' }}
                onClick={() => handleLike(comment.id, comment.likes, comment.liked)}
              />
              <span>{comment.likes}</span>
            </div>
            <span style={{ paddingLeft: '10px' }}>
              {new Date(comment.created_at).toLocaleDateString('pt-BR', {
                day: 'numeric',
                month: 'long',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
              })}</span>
            <hr style={{ border: 'none', borderTop: '1px solid #333', width: '95%', margin: '20px auto' }} />
          </div>
        ))
      ) : <></>}
    </div>
  );
}
