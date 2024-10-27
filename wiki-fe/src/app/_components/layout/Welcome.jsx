import React from 'react'
import '@/styles/welcome.css'

export default async function Welcome({params}) {

  return (
      <div className='article-container'>
        <h1>{params?.title}</h1>
        <p>{params?.content}</p>
      </div>
  );
}
