import React from 'react'
import '@/styles/content.css'
import { decrypt } from '@/app/_lib/session'
import { cookies } from 'next/headers'

export default async function Content({params}) {
  return (
    <div className='content-container'>
      <h1>{params?.title}</h1>
      <p>{params?.content}</p>
    </div>
  );
}
