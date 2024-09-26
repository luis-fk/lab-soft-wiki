import React from 'react'
import '@/styles/footer.css'

export default function Footer() {
  return (
    <div className="footer-content">
        <p>&copy; 2024 WikiDengue. Todos os direitos reservados.</p>
        <p><a href="{% url 'encyclopedia:random' %}">Contato</a> | <a href="{% url 'encyclopedia:random' %}">Sobre</a> | <a href="{% url 'encyclopedia:random' %}">Políticas de Privacidade</a></p>
    </div>
  )
}
