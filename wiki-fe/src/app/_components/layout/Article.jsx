import React from 'react'
import '@/styles/article.css'

export default async function Article({params}) {
  return (
    <div className='article-container'>
      <h1>{params?.title}</h1>
      <p>{params?.content}</p>
    </div>
  );
}
