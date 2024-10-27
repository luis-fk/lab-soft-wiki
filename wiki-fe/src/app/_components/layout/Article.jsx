import React from 'react'
import '@/styles/article.css'
import Comments from '@/components/layout/Comments'

export default async function Article({params}) {
  return (
      <div className='article-container'>
        <h1>{params?.title}</h1>
        <p>{params?.content}</p>

        <Comments params={{ articleId: params?.articleId }} />
      </div>
  );
}
