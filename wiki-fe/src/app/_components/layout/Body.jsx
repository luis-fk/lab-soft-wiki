import React from 'react'
import '@/styles/layout/body.css'
import Link from 'next/link'

export default function Body({ children }) {
  return (
    <>
        <div className="body-container">
            <div className="sidebar">
                <h2>Navegação</h2>

                <Link href="/">Início</Link>
                <Link href="/wiki/dengue">A Dengue</Link>
            </div>

            {children}
        </div>
    </>
  )
}