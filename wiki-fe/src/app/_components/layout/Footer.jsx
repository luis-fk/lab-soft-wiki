import React from 'react'
import '@/styles/layout/footer.css'
import Link from 'next/link'

export default function Footer() {
  return (
    <div className="footer-content">
        <p>&copy; 2024 WikiDengue. Todos os direitos reservados.</p>
        <p><Link href="/">Inicio</Link> | <Link href="/contato">Contato</Link> | <Link href="/">Sobre</Link> | <Link href="/terms">Políticas de Privacidade</Link></p>
    </div>
  )
}
