import React from 'react'
import '@/styles/layout/body.css'
import Link from 'next/link'
import { getSession } from '@/lib/session'

export default async function Body({ children }) {
  const session = await getSession();
  
  return (
    <>
        <div className="body-container">
            <div className="sidebar">
                <h2>Navegação</h2>

                <Link href="/">Início</Link>
                <Link href="/perfil">Informações da conta</Link>

                {session.role === 'admin' &&
                <>
                    <Link href="/admin/users">Usuários</Link>
                </>
                }
                {(session.role === 'admin' || session.role === 'staff') &&
                <>
                    <Link href="/denuncias">Denúncias</Link>
                </>
                }
            </div>

            {children}
        </div>
    </>
  )
}