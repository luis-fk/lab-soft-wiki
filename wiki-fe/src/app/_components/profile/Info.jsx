import React from 'react'
import '@/styles/profile/profile-info.css'
import { getSession } from '@/lib/session'

export default async function Info() {
  const session = await getSession();

  // const response = await fetch(`http://127.0.0.1:8000/user/list/id=${session.userId}`, {
  //   method: 'GET',
  //   headers: { 'Content-Type': 'application/json' },
  // });
  
  return (
    <div className='profile-container'>
    </div>
  )
}
