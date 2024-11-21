"use client";
import "@/styles/info/contact-form.css";
import ErrorMessage from '@/components/auth/ErrorMessage';
import SuccessMessage from '@/components/auth/SuccessMessage';
import React, { useState, useEffect, useRef  } from 'react';
import { getSession } from '@/lib/session';
import Link from "next/link";

export default function ContactForm() {
    const [errorMessage, setErrorMessage] = useState(null);
    const [successMessage, setSuccessMessage] = useState(null);
    const [session, setSession] = useState(null);
    const formRef = useRef(null);

    useEffect(() => {
        async function fetchSession() {
            const sessionData = await getSession();
            setSession(sessionData);
        }

        fetchSession();
    }, [])

    useEffect(() => {
        const timeout = setTimeout(() => {
            if (errorMessage) setErrorMessage(null);
            if (successMessage) setSuccessMessage(null);
        }, 5000);

        return () => clearTimeout(timeout);
    }, [errorMessage, successMessage]);

    const handleSubmit = async (event) => {
        event.preventDefault();
        
        try {
            const formData = new FormData(event.target);

            const data = {
                subject: formData.get('subject'),
                email: formData.get('email'),
                content: formData.get('content')
            };

            const response = await fetch('/api/email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const message = await response.json();
            if (message.message.includes("Ocorreu algum erro")) {
                setErrorMessage("Ocorreu um erro ao enviar o email, por favor tente novamente mais tarde!");
                return;
            }
            
            setSuccessMessage(message.message);
            formRef.current.reset();
        } catch (error) {
            setErrorMessage("Ocorreu um erro ao enviar o email, por favor tente novamente mais tarde!");
        }
    };

    return (
        <div className="contact-container">
            <form onSubmit={handleSubmit} ref={formRef}>
                <div>
                    <label htmlFor="subject">Assunto</label>
                    <input type="text" name="subject" placeholder="Assunto" required />
                </div>

                <div>
                    <label htmlFor="email">Seu email:</label>
                    <input type="email" name="email" placeholder="Email" required />
                </div>

                <div>
                    <label htmlFor="content">Conteúdo</label>
                    <textarea name="content" placeholder="Deixe sua mensagem aqui..." rows="5" required></textarea>
                </div>

                {
                    (session?.userId && session) 
                    ? (
                        <div className="submitButton-container">
                            <button type="submit">Enviar Email</button>
                        </div>
                    ) 
                    : <p>Para entrar em contato é necessario <Link href="/login">entrar na sua conta</Link>.</p>
                }

                {errorMessage && <ErrorMessage message={errorMessage} />}
                {successMessage && <SuccessMessage message={successMessage} />}
            </form>
        </div>
    );
}
