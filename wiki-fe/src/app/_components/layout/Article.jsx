import React from 'react'
import '@/styles/wiki/article.css'
import Comments from '@/components/layout/Comments'
import { getSession } from '@/lib/session'

export default async function Article({ params }) {
  const session = await getSession();

  try {
    await fetch(`http://127.0.0.1:8000/article/update/${params.articleId}/`, {
    method: 'PUT',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ views: params.articleViews + 1 }),
  });   
  } catch {}

  return (
      <div className='article-container'>
        <h1>{params?.title}</h1>
        <p>{params?.content}</p>

        {params.isValidArticle ? <Comments params={{ articleId: params?.articleId, userId: session?.userId}}></Comments> : null}
      </div>
  );
}
