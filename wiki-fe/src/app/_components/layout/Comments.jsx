'use client';
import React, { useEffect, useState } from 'react';
import ErrorMessage from "@/components/auth/ErrorMessage";
import '@/styles/article.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faThumbsUp } from '@fortawesome/free-solid-svg-icons';

export default function Comments({ params }) {
  const [comments, setComments] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');

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
        }

        const commentsWithLikes = data.map((comment) => ({
          ...comment,
          liked: false,
        }));

        setComments(commentsWithLikes);
      } catch (err) {
        setErrorMessage('Um erro ocorreu ao tentar carregar os comentários.');
      }
    };

    fetchComments();
  }, []);

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
      setErrorMessage('Um erro ocorreu ao tentar enviar o like.');
    }
  };

  return (
    <div>
      <hr style={{ border: 'none', borderTop: '1px solid #333', width: '95%', margin: '20px auto' }} />

      <h1 style={{ paddingBottom: '0px' }}>Comentários</h1>
      <div style={{ display: 'flex', justifyContent: 'flex-start', paddingLeft: '20px' }}>
        <ErrorMessage message={errorMessage} />
      </div>

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
