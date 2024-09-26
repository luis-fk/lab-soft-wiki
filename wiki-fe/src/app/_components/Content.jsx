import React from 'react'
import '@/styles/content.css'

export default function Content({params}) {

  return (
    <div className='content-container'>
      <h1>{params?.title}</h1>
      <p>{params?.content}</p>
    </div>
  )
}
