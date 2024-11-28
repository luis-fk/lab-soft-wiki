"use client";
import "@/styles/info/contact-form.css";
import ErrorMessage from '@/components/auth/ErrorMessage';
import SuccessMessage from '@/components/auth/SuccessMessage';
import React, { useState, useEffect, useRef  } from 'react';
import { getSession } from '@/lib/session';
import Link from "next/link";

export default function Report() {
    const [errorMessage, setErrorMessage] = useState(null);
    const [successMessage, setSuccessMessage] = useState(null);
    const [session, setSession] = useState(null);
    const formRef = useRef(null);

    useEffect(() => {
        const fetchSession = async () => {
            const sessionData = await getSession();
            setSession(sessionData);
        };

        fetchSession();
    }, []);

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

            const reportData = {
                state: formData.get('state'),
                city: formData.get('city'),
                district: formData.get('district'),
                street: formData.get('street'),
                number: formData.get('number'),
                text: formData.get('content'),
            };

            if (!reportData.number) {
              reportData.number = -1;  
            }

            const response = await fetch(`http://127.0.0.1:8000/denuncia/create/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: session.userId, ...reportData}),
            });
            
            const data = await response.json();
        
            if (!response.ok) {
                setErrorMessage(data.error);
                return;
            }
          
            setSuccessMessage('Denúncia enviada com sucesso!');
            setTimeout(() => setSuccessMessage(''), 3000);
            formRef.current.reset();
        } catch (error) {
            setErrorMessage("Ocorreu um erro ao enviar a denúncia, por favor tente novamente mais tarde!");
        }
    };

    return (
        <div className="contact-container">
            <h2>Faça uma denúncia sobre um caso de dengue na sua região</h2>
            <form onSubmit={handleSubmit} ref={formRef}>
                <div>
                    <label htmlFor="state">Estado</label>
                    <input type="text" name="state" placeholder="Estado" required />
                </div>

                <div>
                    <label htmlFor="city">Cidade</label>
                    <input type="text" name="city" placeholder="Cidade" required />
                </div>

                <div>
                    <label htmlFor="district">Bairro</label>
                    <input type="text" name="district" placeholder="Bairro" required />
                </div>

                <div>
                    <label htmlFor="street">Rua</label>
                    <input type="text" name="street" placeholder="Rua" />
                </div>

                <div>
                    <label htmlFor="street">Número</label>
                    <input type="number" name="number" placeholder="Número" />
                </div>

                <div>
                    <label htmlFor="content">Informações extras</label>
                    <textarea name="content" placeholder="Deixe sua mensagem aqui..." rows="5" required></textarea>
                </div>

                {session?.userId ? <div className="submitButton-container">
                    <button type="submit">Enviar Denúncia</button>
                </div> : <p>Para fazer uma denúncia é necessario <Link href="/login">entrar na sua conta</Link>.</p>}

                {errorMessage && <ErrorMessage message={errorMessage} />}
                {successMessage && <SuccessMessage message={successMessage} />}
            </form>
        </div>
    );
}
