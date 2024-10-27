import React from 'react'
import '@/styles/article.css'
import Comments from '@/components/layout/Comments'
import { getSession } from '@/lib/session'

export default async function Article({params}) {
  const session = await getSession();

  return (
      <div className='article-container'>
        <h1>{params?.title}</h1>
        <p>{params?.content}</p>

        <Comments params={{ articleId: params?.articleId, userId: session?.userId }} />
      </div>
  );
}
